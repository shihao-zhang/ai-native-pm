# 公开分发

本仓保存一个可分发的插件目录 `plugins/ai-native-pm/`。`downloads/` 包含完整插件、六个独立技能 ZIP 和 `SHA256SUMS`。历史公开版本由原 Git 标签和 Release 保留。

[来源记录](plugins/ai-native-pm/SOURCE.json) 标识公开派生候选、上游版本、固定输入摘要及公开文件哈希。固定输入含未提交的维护源内容，因此只能从所记录的固定分发输入复现快照。公开仓的脚本使用现有公开文件重新打包。方法变更须回到维护源，重新生成并核对内容。

## 校验或重建下载包

需要 uv 与 Python 3.10+，全程使用标准库。

```sh
uv run --no-project --offline python scripts/package_release.py --check
uv run --no-project --offline python scripts/package_release.py --output ./rebuilt-downloads
```

默认输出路径是 `downloads/`。已有目录时脚本只核对其内容，重建时可另选一个新目录。ZIP 使用固定顺序、时间戳、权限和无压缩存储，重复生成可逐字节比对。插件和独立包保留 [MIT 许可](LICENSE)，相关包附带 [sz-grilling 上游署名及许可](plugins/ai-native-pm/NOTICE.md)。

发布前核对版本、变更范围、脚本示例和包内文件。发布后从 Release 重新下载全部附件并逐个核对 SHA-256。宿主安装、自动触发、真实业务使用、实际设计系统接入及 HTML 界面验收分别记录。
