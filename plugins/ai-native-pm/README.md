# AI-native PM

版本：0.6.0-rc.1。构建性质：公开预发布。插件身份为`ai-native-pm`，按任务选用下列能力；插件只负责分发，不增加另一套流程、MCP、hook或业务授权。来源见[SOURCE.json](SOURCE.json)，版本变化见[CHANGELOG](CHANGELOG.md)。许可见[MIT LICENSE](LICENSE)，上游署名见[NOTICE](NOTICE.md)。

**第一次使用从[一个需求开始](GETTING_STARTED.md)**：选择项目、核已有材料，再决定复用还是新建chat。协作关系见[架构导航与图](WORKFLOW.md)；想把实战反馈变成方法时，按需读[经验内化指南](references/learning-loop.md)。安装后不会自动建项目或运行后台维护；可将指南交给当前agent执行已授权部分。

| 任务 | 入口 | 边界 |
|---|---|---|
| 与PM起草或修改需求文档 | [prd-cowrite](skills/prd-cowrite/SKILL.md) | 按需生成PRD HTML，不负责原型工程实现 |
| 与PM新建或实质迭代可交互原型 | [prototype-codesign](skills/prototype-codesign/SKILL.md) | 使用项目产品定义、DS及工程环境；独立验收或局部样式施工不重跑共创 |
| 单独检查改判影响 | [backscan](skills/backscan/SKILL.md) | 只核相关范围，不自动发订正消息 |
| 单独核报告或回执的证据 | [evidence-check](skills/evidence-check/SKILL.md) | 读取证据和给建议，不代替实际验收 |
| 明确希望逐题挑战方案与关键选择 | [sz-grilling](skills/sz-grilling/SKILL.md) | 可选决策访谈；普通“先对齐”不自动进入 |
| 制作或评审静态HTML报告／手册 | [editorial-report-html](skills/editorial-report-html/SKILL.md) | 独立阅读产物；PRD HTML及交互原型沿既有流程 |

先按本轮目标选能力，具体触发条件以各自SKILL.md为准；此表只作导航。可以在已有需求中按需进入决策访谈，结束后把已确认决定交回原任务。基于PRD另做汇报时保留定义来源与版本；扩展资料、发布和上传仍按相应授权执行。

## 安装：Codex本地项目

以下是供使用者执行的安装说明，本候选尚未完成宿主安装验收。核心目录解包与脚本测试通过，不等于插件已被宿主发现。宿主支持情况以[官方插件说明](https://developers.openai.com/plugins/build/plugins)及本机实际结果为准。

1. 解压插件ZIP，确认只有一个`ai-native-pm/`顶层目录，里面含`plugin.json`、本说明、开始指南、架构导航、版本记录和`skills/`下的六个skill目录。将整个目录放到目标项目的`plugins/ai-native-pm/`；已有安装先保存旧版本，勿直接混合覆盖。
2. 把下面条目加入目标项目的`.agents/plugins/marketplace.json`。已有该文件时，保留其市场名称、其他配置和插件条目，只合并`plugins`中的本插件记录；没有该文件时可使用完整示例。`source.path`相对项目根，不是相对marketplace.json所在目录。
3. 在支持本地marketplace的宿主中刷新或重启，找到对应市场中的`ai-native-pm`并安装/启用。未显示时按官方说明检查本地目录、项目识别与市场注册，不把文件复制成功当安装成功。安装或启用会改变宿主配置，由使用者确认执行。
4. 新开对话，按任务选择来自`ai-native-pm`的技能，确认能读取对应包内参考；PRD工具可运行下方示例。UI及命名空间可能因宿主而异；优先从技能列表选择，明确核对来源。

```json
{
  "name": "ai-native-pm-local",
  "interface": {"displayName": "AI-native PM"},
  "plugins": [
    {
      "name": "ai-native-pm",
      "source": {"source": "local", "path": "./plugins/ai-native-pm"},
      "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
      "category": "Productivity"
    }
  ]
}
```

若只拿独立skill包，将所选skill整个目录放进目标项目支持的技能位置；Codex项目可用`.agents/skills/<技能名>/`。不要同时加载独立skill与plugin里的同名skill。其他客户端的插件格式尚未验证；支持技能文件或手动读取的agent可从完整核心的SKILL.md开始，不据此宣称插件自动接入。

## 开始共写

可以说：“用prd-cowrite与我共写这个需求。先核已有事实和授权，给本轮需要对齐的骨架、图与关键结论。缺少信息时标明缺口，不补造业务事实。”已有PRD就说明此次变化与已确认的边界，按需修改，不必从头跑流程。

SKILL.md是工作入口，其他材料按任务加载。业务文档放在自己的项目中，安装包作为只读资源；无命令执行能力时仍可共写Markdown，HTML生成明确标待执行。

原型任务可说：“用prototype-codesign推进本轮原型共创，沿用已确认方案与现有页面，先核当前阶段、写区和DS，只做本次增量。”它不要求重写PRD，不自带公司组件库或业务工程；项目输入缺失时按其[项目接入说明](skills/prototype-codesign/references/project-context.md)定向补齐。状态流与说明页约定从各自维护源生成随包镜像，不在安装副本手改。

首次使用自己的DS，可说：“先从项目已有资料找到DS；缺入口时跟我确认，用我已授权的仓库访问方式获取推荐消费包，固定版本并验证接入，把来源与使用方法记在本项目。”具体setup、无包时的构建选择、更新和可选维护专线都在上述接入说明中。它不依赖插件作者的本地session；账户登录由使用者完成，包内不含凭据，安装插件不等于已连接Codeup或已下载公司DS。

## 运行一个示例

以下为PRD构建示例；原型共创入口本身不依赖该生成器。运行示例需要已安装的uv与Python 3.10+，脚本仅使用标准库。先切到可写的业务或临时目录，再把下面`<plugin>`换成插件实际绝对路径；不要把输出写进安装包。

```sh
uv run --no-project --offline python "<plugin>/skills/prd-cowrite/scripts/build_prd_html.py" "<plugin>/skills/prd-cowrite/assets/example.md" example.fragment.html --standalone example.html --check-chairs
uv run --no-project --offline python "<plugin>/skills/prd-cowrite/scripts/svg_lint.py" example.html
```

打开example.html，检查图、折叠与待拍跳转。生成和有限图形体检通过仍需实际看屏；输入格式、退出码和工具边界见[构建说明](skills/prd-cowrite/references/build.md)。

## 更新、旧名迁移与回退

每次把新版完整解压到另一目录，先跑示例及本次变更相关场景，确认后切换安装来源或替换整个目录；保留旧版本原件。需要回退时恢复旧目录及原来的市场条目/启用配置，再在新对话核对来源。不要只换SKILL.md，也不要在安装副本中长期维护项目规则。

`0.3.0-rc.1`候选的插件曾叫`prd-cowrite`，从`0.3.0-rc.2`起改为`ai-native-pm`；内部skill名称和内容保持不变。旧候选未在本项目安装。若其他机器安装过旧名插件，先按宿主方式停用旧身份，再安装新身份，确认新版本正常后移除旧条目；不能假设更名会被识别为原身份的自动升级。独立skill的使用者无需因插件改名而改技能名。

## 反馈与维护

反馈具体任务、卡住的位置、预期与实际差异，隐去敏感信息即可，不要求上传完整会话。方法统一维护，项目资料留在使用者项目；共享详细方法在构建时装入各独立skill，不在多处手写。安装目录不手改，具体维护循环见元方法。真实业务使用、宿主安装和脚本回归分别记录，不互相代替。

本版将rename-term独立入口退为术语参考，backscan/evidence-check精简为可选核查；升级前保存现用版本，确认插件加载后再由使用者决定是否移出旧同名skill和旧rename-term入口。当前工程未执行此迁移。团队DS消费包、宿主加载与真实业务使用尚待验证；本版本不代表插件长期终态已定稿。

sz-grilling与editorial-report-html复用各自维护源，经确认版本导入为带指纹的只读快照后装配；本包不另维护其规则副本。它们的更新须回对应源头，重新导入、核变更并发布新候选；普通构建不追随正在变化的全局安装目录。来源版本及文件摘要见SOURCE.json。若本机已有同名独立skill，安装试验时明确选用来源，未经确认不自动删除或覆盖旧入口。
