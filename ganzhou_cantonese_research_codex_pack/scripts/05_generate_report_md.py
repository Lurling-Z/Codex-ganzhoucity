from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
REPORT = REPORT_DIR / "ganzhou_cantonese_market_report_draft.md"

def read_csv(path):
    p = ROOT / path
    if not p.exists():
        return None
    try:
        return pd.read_csv(p)
    except Exception:
        return None

def md_table(df, max_rows=20):
    if df is None or df.empty:
        return "暂无数据。"
    return df.head(max_rows).to_markdown(index=False)

def main():
    restaurants = read_csv("data/processed/restaurants_clean.csv")
    restaurant_summary = read_csv("outputs/tables/restaurant_summary.csv")
    review_keywords = read_csv("outputs/tables/review_keyword_summary.csv")
    sentiment_summary = read_csv("outputs/tables/review_sentiment_summary.csv")
    brand_score = read_csv("outputs/tables/brand_fit_score.csv")
    social_posts = read_csv("data/raw/social_posts_raw.csv")

    store_count = 0 if restaurants is None else len(restaurants)
    review_count = 0
    reviews_classified = read_csv("data/processed/reviews_classified.csv")
    if reviews_classified is not None:
        review_count = len(reviews_classified)

    sample_warning = ""
    if store_count < 10 or review_count < 50:
        sample_warning = (
            "\\n> 样本提示：当前样本量偏小。若门店样本少于 10 家或评论样本少于 50 条，"
            "报告结论只能作为初步判断，不宜作为强招商判断。\\n"
        )

    report = f"""
# 赣州市区粤式餐饮市场线上调研报告（初稿）

## 1. 调研目的

本报告用于判断赣州市区消费者对粤式餐饮、广式早茶、粤式点心、烧腊、茶餐厅和粤菜正餐的接受度，并进一步评估陶陶居、点都德等广式茶楼品牌进入赣州市场的适配性。

## 2. 样本说明

- 门店样本数量：{store_count}
- 评论样本数量：{review_count}
- 社媒笔记样本数量：{0 if social_posts is None else len(social_posts)}

{sample_warning}

### 门店样本概览

{md_table(restaurant_summary)}

## 3. 赣州粤式餐饮供给结构

以下为已清洗门店样本中的品类、商圈、人均和平台信息。请结合人工观察进一步修正。

{md_table(restaurants[["store_name","platform","cantonese_type","business_area","avg_price","price_band","rating","review_count"]] if restaurants is not None and not restaurants.empty else None)}

## 4. 用户口碑分析

### 情绪分布

{md_table(sentiment_summary)}

### 高频关键词

{md_table(review_keywords)}

## 5. 价格接受度初步判断

请重点观察：
- 50 元以下：是否主要是烧腊饭、肠粉、茶餐厅简餐。
- 50-90 元：是否能形成日常聚餐与早茶消费。
- 90-150 元：是否有家庭聚餐、商务小聚、品质中餐需求。
- 150 元以上：是否仅为少量宴请需求。

如消费者对 80 元以上粤菜明显敏感，点都德/陶陶居进入需要降低决策门槛，例如早市套餐、工作日点心、家庭套餐、烧腊饭/牛河等更高频产品。

## 6. 广式早茶文化接受度判断

请根据评论和社媒内容判断：
- 消费者是否主动搜索“早茶/茶楼/点心”。
- 是否理解早茶不只是早餐，而是周末家庭、朋友小聚、茶楼社交场景。
- 是否接受茶位费、多人分食点心、排队等位、上午至下午的全天茶市。
- 是否认为粤菜“清淡舒服”，还是“不够辣、不下饭”。

## 7. 陶陶居入赣适配性

陶陶居更适合承担“老字号粤菜、城市首店、家庭聚餐、商务宴请、广府文化表达”的角色。判断重点：

- 赣州是否存在人均 100-150 元品质中餐消费基础。
- 核心商业体是否需要提升餐饮调性。
- 消费者是否对“广州老字号/正宗粤菜”有认知。
- 现有粤菜市场是否缺少标杆品牌。

风险在于面积、供应链、客单、服务标准和稳定复购。如果赣州消费者只愿意开业尝鲜，而不愿意长期复购，陶陶居直接大店进入风险较高。

## 8. 点都德入赣适配性

点都德更适合承担“广式早茶、点心爆品、全天茶市、年轻化打卡、排队话题”的角色。判断重点：

- 消费者是否熟悉虾饺、烧卖、红米肠、凤爪、叉烧包等点心。
- 是否愿意把早茶作为周末家庭消费方式。
- 是否能接受 70-120 元价格带。
- 商场是否有足够客流、等位空间和年轻客群传播能力。

风险在于赣州早茶习惯未必成熟。如果消费者认为点心“吃不饱、价格高、偏清淡”，点都德可能出现开业热闹、后期回落。

## 9. 品牌适配评分

{md_table(brand_score)}

## 10. 粤菜入赣路径建议

初步建议不要只盯陶陶居、点都德这类完整茶楼大店。更现实的路径是分三层：

1. 轻量粤式快餐/烧腊：验证日常复购。
2. 广式早茶点心店：验证周末家庭和年轻人打卡。
3. 粤菜正餐/茶楼品牌：验证城市首店和品质聚餐。

只有当“口味接受度”和“场景接受度”同时成立时，陶陶居、点都德才具备强讨论价值。

## 11. 小红书商业观察选题

- 赣州，缺一家真正的广式茶楼吗？
- 陶陶居和点都德，谁更适合先来赣州？
- 为什么赣州需要更多粤菜，但不一定马上需要大茶楼？
- 赣州人能接受广式早茶吗？
- 从虾饺到烧鹅，赣州粤菜市场还差什么？

## 12. 风险与不足

- 线上评论存在样本偏差，不能完全代表全体消费者。
- 小红书/抖音更容易放大打卡和尝鲜，不等于复购。
- 大众点评/美团评分受门店运营、团购、活动影响。
- 若样本不足，建议补充线下观察或消费者小样本访谈。
"""
    REPORT.write_text(report.strip() + "\n", encoding="utf-8")
    print(f"已输出：{REPORT}")

if __name__ == "__main__":
    main()
