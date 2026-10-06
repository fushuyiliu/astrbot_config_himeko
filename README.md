# AstrBot Himeko 公开配置指南

[English](README.en.md) | 中文

这是为 [Himeko Companion 插件](https://github.com/fushuyiliu/astrbot_plugin_himeko) 准备的**公开、脱敏配置指南仓**。它帮助使用者完成 AstrBot 的通用准备、模型选择、插件安装顺序与隐私检查。

它不是生产配置备份，也不是一键部署包。仓库内没有、也不应当加入真实的主人 ID、模型密钥、平台令牌、服务器地址、聊天记录、数据库、日志、附件或备份。

## 与插件仓的关系

| 仓库 | 职责 | 不包含 |
| --- | --- | --- |
| 本仓 `astrbot_config_himeko` | 通用 AstrBot 配置步骤、公开模板、兼容性说明 | 真实运行配置与凭据 |
| [插件仓 `astrbot_plugin_himeko`](https://github.com/fushuyiliu/astrbot_plugin_himeko) | 可安装的姬子互动、主人记忆、提醒和附件插件 | 平台令牌、模型密钥、真实主人数据 |

两个仓库不使用 Git 子模块、自动同步、目录复制或共享运行目录。它们只通过安装说明与版本兼容性联动。

## 安装顺序

1. 按 [AstrBot 官方文档](https://docs.astrbot.app/) 安装 AstrBot，并通过 WebUI 启动它。
2. 在 AstrBot WebUI 配置你的消息平台与模型服务。模型选择、模型密钥和平台凭据都只保存在你自己的 AstrBot 环境中。
3. 阅读本仓的 [兼容性说明](COMPATIBILITY.md)，确认 AstrBot 版本满足插件要求。
4. 从插件仓安装 `astrbot_plugin_himeko`，再在插件 WebUI 设置中手动填写主人 ID 和所需功能开关。
5. 用虚构内容完成首次互动和删除测试，再使用真实私聊数据。

## 公开模板的使用方式

[`templates/astrbot_plugin_himeko.config.example.json`](templates/astrbot_plugin_himeko.config.example.json) 只展示插件配置字段及安全默认值。

- 优先通过 AstrBot WebUI 的插件配置页面填写；不要把填写后的配置文件提交回本仓。
- `owner_id` 必须保持为空，直到你在自己的 AstrBot 管理界面中填入精确发送者 ID。
- 所有敏感能力开关默认关闭。先验证普通互动，再按需逐项开启记忆、提醒和附件。
- 不要把模型密钥填到示例文件。模型由 AstrBot 的 AI 配置管理。

## 隐私检查清单

提交任何变更前确认：

- 没有 `cmd_config.json`、真实 `*_config.json`、`.env`、证书、私钥、令牌或密码。
- 没有 IP/域名、主人 ID、手机号、邮箱、聊天记录、附件、日志、SQLite 数据库或备份。
- 示例只含空字符串、虚构值或明确的占位符。
- 文档没有承诺未实际验证的手机端、云端或性能结果。

运行：

```powershell
python tools/audit_public_config_repo.py .
```

自动扫描只是辅助，发布前仍须人工逐文件复核。

## 已知边界

- 本仓不替代 AstrBot 官方文档，也不修改 AstrBot 本体。
- 本仓不自动安装插件、不启动服务、不上传配置，也不连接任何平台。
- 删除本仓文件不会删除你机器上的 AstrBot 配置、模型服务记录或消息平台数据；请分别按对应产品的文档处理。

## 贡献与安全

提交前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。安全问题遵循 [SECURITY.md](SECURITY.md)；不要在公开 issue 中提供秘密或私人聊天内容。

原创文本和模板采用 [MIT License](LICENSE)。与 AstrBot、插件仓的关系及依赖边界见 [NOTICE.md](NOTICE.md)。
