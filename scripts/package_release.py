"""Package the checked-in public snapshot; no downloads or publication."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/ai-native-pm'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def package():
    manifest = json.loads((PLUGIN / 'plugin.json').read_text())
    source = json.loads((PLUGIN / 'SOURCE.json').read_text())
    version = manifest['version']
    assert version == source['version'], 'Manifest/source version mismatch'
    compatibility = json.loads((PLUGIN / '.codex-plugin/plugin.json').read_text())
    assert all(compatibility[k] == manifest[k] for k in ('name','version','description'))
    assert compatibility['skills'] == './skills/'
    for name, files in source['skills_files'].items():
        actual = {p.relative_to(PLUGIN/'skills'/name).as_posix(): digest(p.read_bytes())
                  for p in (PLUGIN/'skills'/name).rglob('*') if p.is_file()}
        assert actual == files, f'Skill content differs from recorded source: {name}'
    out = ROOT / 'dist'
    out.mkdir(exist_ok=True)
    def archive(name, entries):
        with zipfile.ZipFile(out/name, 'w', zipfile.ZIP_DEFLATED) as z:
            for path, data in sorted(entries):
                info = zipfile.ZipInfo(path, date_time=(2026,11,4,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                z.writestr(info, data)
    files = [(p.relative_to(PLUGIN).as_posix(), p.read_bytes())
             for p in PLUGIN.rglob('*') if p.is_file()]
    archive(f'ai-native-pm-plugin-{version}.zip', [('ai-native-pm/'+p,d) for p,d in files])
    names = [f'ai-native-pm-plugin-{version}.zip']
    for skill in sorted(source['skills_files']):
        entries = [(skill+'/'+p.removeprefix('skills/'+skill+'/'),d)
                   for p,d in files if p.startswith('skills/'+skill+'/')]
        entries += [(skill+'/LICENSE', (PLUGIN/'LICENSE').read_bytes())]
        if skill == 'sz-grilling':
            entries += [(skill+'/NOTICE.md', (PLUGIN/'NOTICE.md').read_bytes()),
                        (skill+'/licenses/mattpocock-skills-MIT.txt', (PLUGIN/'licenses/mattpocock-skills-MIT.txt').read_bytes())]
        name = f'{skill}-skill-{version}.zip'
        archive(name, entries)
        names.append(name)
    (out/'SHA256SUMS').write_text(''.join(f'{digest((out/n).read_bytes())}  {n}\n' for n in names))
    print(f'Packaged {len(names)} archives; recorded skill files match; checksums: {out / "SHA256SUMS"}')

if __name__ == '__main__':
    package()
