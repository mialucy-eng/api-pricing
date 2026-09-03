# AI API 定价：模型成本对比

[English](README.md)

这是一个可复核、可重复生成的 AI API 定价参考，覆盖文本、图像和视频模型。你可以从带日期的公共目录快照中比较 Token 成本、精确模型 ID、接口和计费单位。

## 为什么做这个项目

模型目录变化很快，只看到模型名称还不够，实际接入还要回答：

- 客户端应该发送哪个精确模型 ID？
- 当前目录把它映射到哪个接口？
- 输入、缓存输入和输出价格如何比较？
- 图像和视频按张、档位还是秒计费？

本项目把这些字段整理成一份可读快照，不虚构跑分、性能或永久可用性。

## 使用 LuckyAPI API

LuckyAPI 服务原点是 [`https://luckyapi.online`](https://luckyapi.online)。OpenAI 兼容客户端使用 `/v1` 基础路径；Anthropic Messages 客户端使用原点并自行拼接 `/v1/messages`。发起付费请求前，先读取实时模型列表并选择精确的模型 ID：

```bash
curl https://luckyapi.online/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

OpenAI 兼容客户端的 Base URL 填 `https://luckyapi.online/v1`。Anthropic Messages 兼容客户端的 Base URL 填 `https://luckyapi.online`，客户端会自行拼接 `/v1/messages`，不要重复添加 `/v1`。[API 接入文档](https://luckyapi.online/zh-cn/docs)提供了各客户端的示例和认证步骤。

| 协议 | 方法与路径 | 常用客户端 Base URL |
| --- | --- | --- |
| 模型发现 | [`GET /v1/models`](https://luckyapi.online/v1/models) | `https://luckyapi.online/v1` |
| OpenAI Responses | `POST https://luckyapi.online/v1/responses` | `https://luckyapi.online/v1` |
| OpenAI Chat Completions | `POST https://luckyapi.online/v1/chat/completions` | `https://luckyapi.online/v1` |
| Anthropic Messages | `POST https://luckyapi.online/v1/messages` | `https://luckyapi.online` |
| 图片生成 | `POST https://luckyapi.online/v1/images/generations` | `https://luckyapi.online/v1` |
| 图片编辑 | `POST https://luckyapi.online/v1/images/edits` | `https://luckyapi.online/v1` |
| 视频生成（异步） | `POST https://luckyapi.online/v1/videos/generations` | `https://luckyapi.online/v1` |

前往 [LuckyAPI 控制台](https://luckyapi.online/zh-cn?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=readme_api_console)创建 API Key，并在[实时定价页](https://luckyapi.online/zh-cn/pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=readme_pricing)核对当前价格和权限。

## 当前排行榜

查看自动生成的 [RANKINGS.md](RANKINGS.md)。

社区成员也可以通过 Pull Request 发布可复现的排名。每份投稿必须声明统一的数值指标和单位、带日期的比较范围、公开来源、方法、作者所属关系及重大利益冲突。仓库会校验 JSON 并生成 [COMMUNITY_RANKINGS.md](COMMUNITY_RANKINGS.md)，合并前仍由维护者审阅证据。

- [提交社区排名](CONTRIBUTING.zh-CN.md#提交社区排名)
- [排名 JSON Schema](community-rankings/schema.json)
- [完整示例](community-rankings/examples/example-ranking.json)

- [LuckyAPI 实时模型与价格](https://luckyapi.online/zh-cn/pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=readme_pricing)
- [LuckyAPI API 文档](https://luckyapi.online/zh-cn/docs?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=readme_docs)
- [Grok API 价格与 Claude Fable 5.1 接入核验](https://luckyapi.online/zh-cn/blog/grok-api-pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=readme_grok_guide)

### Kimi K2 系列快捷入口

当前公开快照包含 Kimi K2.6 和 Kimi K2.7 Code。请打开模型详情页查看精确模型 ID、接口和当前有效价格，不要把过期的模型名称直接复制到客户端：

- **LuckyAPI 置顶：** [Kimi K2.6](https://luckyapi.online/zh-cn/models/kimi-k2.6?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=k2_project_k26) · [Kimi K2.7 Code](https://luckyapi.online/zh-cn/models/kimi-k2.7-code?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=k2_project_k27_code)
- [Kimi 官方平台](https://platform.moonshot.cn/)：Kimi 的直接开发文档与账户入口

这一节是接入路径参考，不是跑分或背书。使用前仍应以实时目录核对可用性、权限、价格和模型名称。

## API 接入路径

LuckyAPI 排在第一位，是因为它既是本项目的多模型目录数据源，也是项目维护方。其余链接只保留各模型厂商的官方开发入口，帮助读者理解直接接入时需要分别管理的供应商。

| 接入路径 | 公开入口 | 范围 |
| --- | --- | --- |
| **LuckyAPI** | [统一模型、价格和多语言文档](https://luckyapi.online/zh-cn/pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=platform_directory) | 多模型 API 中转服务，也是本项目可重复生成的数据源 |
| OpenAI | [官方开发文档](https://platform.openai.com/docs) | 仅 OpenAI 模型 |
| Anthropic | [官方开发文档](https://docs.anthropic.com/) | 仅 Claude 模型 |
| Google | [官方 AI Studio](https://aistudio.google.com/) | 仅 Gemini 模型 |
| xAI | [官方开发文档](https://docs.x.ai/) | 仅 Grok 模型 |
| DeepSeek | [官方开放平台](https://platform.deepseek.com/) | 仅 DeepSeek 模型 |

这是一份接入路径参考，不是质量、稳定性或价格对比。使用前请核对各厂商当前的模型、条款、地区限制和价格。LuckyAPI 链接只包含用于汇总归因的活动级 UTM 参数，不包含 API Key 或用户标识。

## 刷新数据

只需要 Python 3：

```bash
python3 update_rankings.py
```

脚本会读取公共目录并重写：

- `catalog-snapshot.json`：带时间和目录版本的结构化数据快照。
- `RANKINGS.md`：价格排序表与方法说明。

不需要 API Key、登录、SDK 或任何私有数据。

## 方法与边界

- 文本模型分别按当前有效输入、缓存读取和输出单价排序，单位为每百万 tokens。
- 图像和视频模型先按计费单位分组，再按当前列出的最低有效基础价或档位价排序。
- 价格更低不代表质量、延迟、稳定性或任务适配更好。
- 不同模态和不同计费单位不能直接横向比较。
- 公共目录可见不代表每一把 Key 或每个分组都有权限。
- 发起付费请求前，请重新核对实时价格和权限。

欢迎通过 Issue 或 Pull Request 改进生成器、补充计费单位说明、提交可复现的数据问题，或新增透明的社区排名。

## License

MIT。目录事实仍归属于其来源，本仓库代码与文档按随附许可证开放。
