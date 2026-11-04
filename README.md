# AI-native PM

面向产品经理的 AI 协作方法包：需求共写、原型共创，以及按需使用的决策访谈、HTML报告与证据核查。

**当前版本：0.6.0-rc.1+diagram.1，公开预发布。** 脚本与内容检查不代表宿主安装或真实业务使用通过。

- [从一个需求开始](plugins/ai-native-pm/GETTING_STARTED.md)
- [安装、六个技能和使用说明](plugins/ai-native-pm/README.md)
- [协作流程架构](plugins/ai-native-pm/WORKFLOW.md)
- [版本记录](plugins/ai-native-pm/CHANGELOG.md)
- [下载预发布包](https://github.com/shihao-zhang/ai-native-pm/releases)

本次仅更新架构图，原样采用0.6.0-rc.4图示；技能内容仍为首次公开版本。

![协作流程](plugins/ai-native-pm/architecture.svg)

## 获取与使用

下载Release中的完整plugin ZIP，或单个skill ZIP。需要Git版本时：

```sh
git clone https://github.com/shihao-zhang/ai-native-pm.git
cd ai-native-pm
git checkout v0.6.0-rc.1+diagram.1
```

仓库包含本地marketplace示例；克隆不等于已安装。按包内安装说明由使用者选择安装方式，并核实宿主实际加载。也可以直接让agent读取所选skill的SKILL.md与相对参考文件。

PRD生成器需要uv及Python 3.10+；HTML报告的检查与预览工具需要Node.js。具体命令和局限见各skill内说明。设计系统、业务工程、账号和项目上下文由使用者提供，本包不附带私有DS或自动连接服务。

## 维护与反馈

这是从统一维护源生成的公开分发仓。公开Issue/PR可以提建议或修正；维护者将认可的改动回流维护源后重新生成，不在多个安装副本中分别维护。反馈只提供获准公开的最小示例。

公开打包过程见[发布说明](PUBLISHING.md)。许可为[MIT](LICENSE)，上游署名见[NOTICE](NOTICE.md)。
