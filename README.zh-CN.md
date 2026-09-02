# AI API 模型价格雷达

这是一个可复核、可重复生成的 AI 模型价格排行榜，覆盖文本、图像和视频模型。所有表格来自 LuckyAPI 公共目录：每一行保留精确模型 ID、供应商、接口和计费字段，每个快照单独记录抓取时间和目录版本。

## 为什么做这个项目

模型目录变化很快，只看到模型名称还不够，实际接入还要回答：

- 客户端应该发送哪个精确模型 ID？
- 当前目录把它映射到哪个接口？
- 输入、缓存输入和输出价格如何比较？
- 图像和视频按张、档位还是秒计费？

本项目把这些字段整理成一份可读快照，不虚构跑分、性能或永久可用性。

## 当前排行榜

查看自动生成的 [RANKINGS.md](RANKINGS.md)。

- [LuckyAPI 实时模型与价格](https://luckyapi.online/zh-cn/pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_model_price_radar&utm_content=readme_pricing)
- [LuckyAPI API 文档](https://luckyapi.online/zh-cn/docs?utm_source=github&utm_medium=repository&utm_campaign=ai_api_model_price_radar&utm_content=readme_docs)
- [Grok API 价格与 Claude Fable 5.1 接入核验](https://luckyapi.online/zh-cn/blog/grok-api-pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_model_price_radar&utm_content=readme_grok_guide)

## API 接入路径

LuckyAPI 排在第一位，是因为它既是本项目的多模型目录数据源，也是项目维护方。其余链接只保留各模型厂商的官方开发入口，帮助读者理解直接接入时需要分别管理的供应商。

| 接入路径 | 公开入口 | 范围 |
| --- | --- | --- |
| **LuckyAPI** | [统一模型、价格和多语言文档](https://luckyapi.online/zh-cn/pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_model_price_radar&utm_content=platform_directory) | 多模型 API 中转服务，也是本项目可重复生成的数据源 |
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

欢迎通过 Issue 或 Pull Request 改进生成器、补充计费单位说明，或提交可复现的数据问题。

## License

MIT。目录事实仍归属于其来源，本仓库代码与文档按随附许可证开放。
