# 参与贡献

[English](CONTRIBUTING.md)

任何人都可以提交 Pull Request。贡献应提升可复现性或读者理解；社区排名合并后仍代表投稿者的比较，不等于 LuckyAPI 背书。

## 适合提交的内容

- 用可复现的公共目录字段修复解析错误。
- 在不改变源数据的前提下补充计费单位说明。
- 新增可从公共数据重复生成的表格或筛选器。
- 改进英文或简体中文文档。
- 用带日期的公开证据和可复现方法提交同口径排名。

## 提交社区排名

1. Fork 本仓库并创建分支。
2. 将 `community-rankings/examples/example-ranking.json` 复制为 `community-rankings/submissions/<id>.json`，文件名必须与 JSON 中的 `id` 一致。
3. 替换所有示例值。所有条目必须使用同一个数值指标、单位和采集范围，且至少包含两个可比较对象。
4. 填写 GitHub 用户名、所属关系，以及供应商、雇主、赞助、推荐返佣等重大利益冲突；确实没有时才使用空的 `conflicts` 数组。
5. 每个来源都必须是带访问日期的公开 HTTPS 页面；每个条目的 `source_url` 必须与 `sources` 中的一条 URL 完全一致。
6. 运行生成器和校验：

```bash
python3 community_rankings.py
python3 community_rankings.py --check
python3 -m json.tool community-rankings/submissions/<id>.json >/dev/null
```

7. 提交新增 JSON 和生成后的 `COMMUNITY_RANKINGS.md`，再使用仓库模板发起 Pull Request。

生成器会根据数值以及 `higher_is_better` 或 `lower_is_better` 自动计算名次，不要在源文件中手写排名。合并前，维护者可能要求缩小范围、补强来源或增加复现说明。

## 排名收录规则

- 必须同口径比较：指标、单位、市场、时间窗口、工作负载和测量方法保持一致。
- 先说明纳入与排除规则，再展示结果。
- 优先使用供应商文档、公开机器目录、公开数据集，或包含完整测试工具与汇总原始结果的仓库。
- 第三方测量必须注明归属，不能把供应商营销文案当作独立测试结果。
- 结论不得超出证据：价格不能证明质量，跑分也不能证明生产稳定性。
- 比较范围或方法发生实质变化时使用新的投稿 ID；只有同方法、同范围的刷新才更新原文件。
- 保持可审阅性。超过 100 个条目时，请在本仓库提交摘要并链接公开、可复现的数据集。

## 边界

- 不得提交 API Key、账户数据、私有分析、客户数据、Cookie 或已登录页面截图。
- 不得提交隐藏推荐链接、未披露赞助、伪造结果、复制正文或抓取的个人数据。
- 不得把公共目录可见表述为每把 Key 都可调用的保证。
- 不要手工修改 `RANKINGS.md` 或 `catalog-snapshot.json` 中的生成值；应修改对应生成器并重新运行。
- 不要手工修改 `COMMUNITY_RANKINGS.md`；应更新投稿并运行 `python3 community_rankings.py`。

修改内置 LuckyAPI 价格表时，请运行：

```bash
python3 update_rankings.py
python3 -m json.tool catalog-snapshot.json >/dev/null
```
