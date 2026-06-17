# 请 Codex 执行的任务

你将接手一个名为 `ganzhou_cantonese_research_codex_pack` 的研究项目。请先阅读 `README.md` 和 `AGENTS.md`，然后完成以下工作。

## 项目背景

我正在通过线上渠道调研赣州市区粤式餐饮市场，想判断赣州消费者对粤式饮食文化、广式早茶、茶餐厅、烧腊、粤菜正餐的接受度，并进一步判断陶陶居、点都德这类品牌是否适合进入赣州市场。

## 你需要做什么

### 第一阶段：检查项目结构

请检查以下文件是否存在：

- `data/raw/restaurants_raw.csv`
- `data/raw/reviews_raw.csv`
- `data/raw/social_posts_raw.csv`
- `data/raw/brand_score_inputs.csv`
- `notes/search_keywords.md`
- `scripts/02_clean_restaurants.py`
- `scripts/03_analyze_reviews.py`
- `scripts/04_score_brand_fit.py`
- `scripts/05_generate_report_md.py`

如果缺失，请补齐。

### 第二阶段：等待或使用我手动录入的数据

数据来源以我人工线上采集为准，包括大众点评/美团、高德地图、小红书、抖音、本地公众号等公开可见信息。你不要尝试绕过平台限制，也不要自行伪造数据。

### 第三阶段：运行数据处理

请依次运行：

```bash
pip install -r requirements.txt
python scripts/02_clean_restaurants.py
python scripts/03_analyze_reviews.py
python scripts/04_score_brand_fit.py
python scripts/05_generate_report_md.py
```

若缺少数据，请输出清晰的待采集字段清单，而不是编造结论。

### 第四阶段：生成初步结论

请生成 `reports/ganzhou_cantonese_market_report_draft.md`，报告必须包含：

1. 调研样本说明。
2. 赣州市区现有粤菜供给结构。
3. 核心商圈分布。
4. 价格带分布。
5. 消费者正向评价关键词。
6. 消费者负向评价关键词。
7. 广式早茶文化接受度判断。
8. 陶陶居适配性判断。
9. 点都德适配性判断。
10. 粤菜入赣路径建议。
11. 小红书选题建议。

## 结论要求

结论必须标注证据来源，例如来自哪张表、多少条评论、多少家门店。样本不足时必须明确写出“当前样本不足，不足以支撑强结论”。

## 禁止事项

禁止编造门店、评分、人均、评论和消费者反馈。
禁止越权抓取、绕过登录、破解验证码、调用非授权接口。
禁止将“开业热度”直接等同于“长期复购”。
禁止只写品牌招商口号，必须落到价格、口味、场景、商圈、复购和文化接受度。
