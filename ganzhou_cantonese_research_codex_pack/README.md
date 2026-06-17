# 赣州市区粤式餐饮线上调研 Codex 执行包

## 项目目标

本项目用于线上调研赣州市区粤式餐饮市场，判断赣州消费者对粤式饮食文化、广式早茶、粤菜正餐、烧腊、茶餐厅等品类的接受度，并进一步评估陶陶居、点都德进入赣州市场的适配性。

本项目不是自动爬取平台数据的工具包。大众点评、小红书、抖音、美团、高德等平台的数据，建议通过人工搜索、人工记录、公开页面可见内容整理、截图后人工录入等合规方式采集。Codex 的任务是帮助清洗、分类、分析和生成报告。

## 推荐执行流程

1. 阅读 `AGENTS.md`，确认 Codex 的工作边界。
2. 打开 `CODEX_TASK.md`，将其中任务直接交给 Codex。
3. 按 `notes/search_keywords.md` 进行线上搜索。
4. 将采集到的信息填入 `data/raw/*.csv`。
5. 运行脚本：

```bash
pip install -r requirements.txt
python scripts/02_clean_restaurants.py
python scripts/03_analyze_reviews.py
python scripts/04_score_brand_fit.py
python scripts/05_generate_report_md.py
```

6. 查看输出：
   - `data/processed/`
   - `outputs/tables/`
   - `reports/ganzhou_cantonese_market_report_draft.md`

## 核心判断问题

- 赣州目前粤式餐饮供给是否稀缺？
- 本地消费者接受的是粤式口味，还是广式茶楼文化？
- 粤菜在赣州更适合正餐、早茶、烧腊快餐、茶餐厅，还是家庭聚餐？
- 陶陶居和点都德分别适配赣州哪类商圈和消费场景？
- 若引进更多粤菜，应该先引进完整茶楼品牌，还是先引入轻量粤式小馆/烧腊/早茶点心？


## AI 信息检索增强版

如果你希望最大化利用 AI 的公开信息检索能力，请优先阅读：

- `AI_RETRIEVAL_GUIDE.md`
- `data/raw/ai_seed_leads.csv`
- `scripts/01_prepare_ai_search_queries.py`

建议先运行：

```bash
python scripts/01_prepare_ai_search_queries.py
```

这会生成 `outputs/tables/ai_search_queries.csv`，用于批量指导 ChatGPT、Codex、搜索引擎或浏览器搜索插件进行公开信息检索。

注意：AI 检索出来的是“线索池”，不是最终事实。门店是否仍在营业、人均是否准确、评论是否真实，需要二次核验。
