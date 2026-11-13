"""Build release assets from the public plugin snapshot using the standard library."""

import argparse
import hashlib
import io
import json
import re
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = "plugins/ai-native-pm"
UPSTREAM_LICENSE = "licenses/mattpocock-skills-MIT.txt"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def hashes(files):
    return {name: digest(data) for name, data in sorted(files.items())}


def files_at(folder):
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError(f"Expected a real directory: {folder.name}")
    files = {}
    for path in sorted(folder.rglob("*")):
        name = path.relative_to(folder).as_posix()
        if path.is_symlink() or any(c in name for c in "\\:\n\r"):
            raise ValueError(f"Invalid package path: {name}")
        if path.is_file():
            files[name] = path.read_bytes()
        elif not path.is_dir():
            raise ValueError(f"Expected a regular file: {name}")
    return files


def skills_in(files):
    result = {}
    for name, data in files.items():
        if name.startswith("skills/"):
            _, skill, relative = name.split("/", 2)
            result.setdefault(skill, {})[relative] = data
    for name, skill in result.items():
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or "SKILL.md" not in skill:
            raise ValueError(f"Invalid skill inventory: {name}")
    return result


def make_zip(files, prefix):
    buffer = io.BytesIO()
    with ZipFile(buffer, "w", compression=ZIP_STORED) as archive:
        for name, data in sorted(files.items()):
            info = ZipInfo(f"{prefix}/{name}", (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return buffer.getvalue()


def package_files(plugin, root_license):
    manifest = json.loads(plugin["plugin.json"])
    source = json.loads(plugin["SOURCE.json"])
    version = manifest["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
        raise ValueError("Invalid release version")
    if source["version"] != version or manifest["name"] != "ai-native-pm":
        raise ValueError("Plugin/source identity mismatch")
    expected = {k: manifest[k] for k in ("name", "version", "description")}
    if json.loads(plugin[".codex-plugin/plugin.json"]) != expected | {"skills": "./skills/"}:
        raise ValueError("Codex manifest mismatch")
    skills = skills_in(plugin)
    if source["skills_files"] != {name: hashes(files) for name, files in skills.items()}:
        raise ValueError("Skill inventory differs from SOURCE.json")
    if source["plugin_files"] != hashes({k: v for k, v in plugin.items() if k != "SOURCE.json"}):
        raise ValueError("Plugin inventory differs from SOURCE.json")
    if not root_license or plugin["LICENSE"] != root_license:
        raise ValueError("Plugin MIT license differs from the root LICENSE")
    if not plugin["NOTICE.md"] or not plugin[UPSTREAM_LICENSE]:
        raise ValueError("Missing upstream attribution or license")

    output = {f"ai-native-pm-plugin-{version}.zip": make_zip(plugin, "ai-native-pm")}
    for name, files in skills.items():
        legal = {"LICENSE": root_license}
        if name == "sz-grilling":
            legal.update({key: plugin[key] for key in ("NOTICE.md", UPSTREAM_LICENSE)})
        for key in files.keys() & legal.keys():
            if files[key] != legal[key]:
                raise ValueError(f"Conflicting license or notice in {name}: {key}")
        output[f"{name}-skill-{version}.zip"] = make_zip(files | legal, name)

    sums = "".join(f"{digest(data)}  {name}\n" for name, data in sorted(output.items()))
    return output | {"SHA256SUMS": sums.encode("utf-8")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "downloads")
    parser.add_argument("--check", action="store_true", help="Require exact output bytes")
    args = parser.parse_args()
    try:
        if (ROOT / "plugins").is_symlink() or (ROOT / "LICENSE").is_symlink():
            raise ValueError("Public snapshot paths must not be symlinks")
        if args.output.is_symlink():
            raise ValueError("Output must not be a symlink")
        output = args.output.parent.resolve(strict=True) / args.output.name
        if any(output.is_relative_to(ROOT / name) for name in (PLUGIN, ".git")):
            raise ValueError("Choose an output outside the plugin and Git metadata")
        expected = package_files(files_at(ROOT / PLUGIN), (ROOT / "LICENSE").read_bytes())
        if args.check or output.exists():
            if files_at(output) != expected:
                raise ValueError("Download bytes differ. Use a new --output directory to rebuild.")
        else:
            output.mkdir()
            for name, data in expected.items():
                with (output / name).open("xb") as stream:
                    stream.write(data)
    except (KeyError, OSError, ValueError) as error:
        parser.exit(1, f"Packaging failed: {error}\n")
    print(f"Verified {len(expected) - 1} ZIPs and SHA256SUMS")


if __name__ == "__main__":
    main()
