from pathlib import Path
import csv
import itertools

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/tables/ai_search_queries.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

city_terms = ["赣州", "赣州市区", "章贡区", "赣州万象城", "赣州九方", "赣州君尚", "赣州步步高新天地", "赣州万达"]
category_terms = ["粤菜", "广式早茶", "早茶", "港式茶餐厅", "茶餐厅", "烧腊", "烧鹅", "叉烧", "肠粉", "虾饺", "点心", "茶楼", "顺德菜", "啫啫煲", "煲仔饭"]
platform_terms = ["大众点评", "美团", "小红书", "抖音", "高德地图", "百度地图", "携程", "TripAdvisor", "公众号"]
intent_terms = ["推荐", "探店", "评价", "人均", "排队", "适合家庭", "周末", "新店"]

queries = []

for city, cat in itertools.product(city_terms, category_terms):
    queries.append([f"{city} {cat}", "城市+品类"])

for city, cat, platform in itertools.product(city_terms[:4], category_terms[:8], platform_terms):
    queries.append([f"{city} {cat} {platform}", "城市+品类+平台"])

for city, cat, intent in itertools.product(city_terms[:4], category_terms[:8], intent_terms):
    queries.append([f"{city} {cat} {intent}", "城市+品类+意图"])

brand_queries = [
    "陶陶居 赣州",
    "点都德 赣州",
    "赣州 需要陶陶居吗",
    "赣州 需要点都德吗",
    "赣州 广州酒家",
    "赣州 蔡澜点心",
    "赣州 炳胜 粤菜",
]

for q in brand_queries:
    queries.append([q, "品牌意向/对标"])

# 去重
seen = set()
deduped = []
for q, t in queries:
    if q not in seen:
        seen.add(q)
        deduped.append([q, t])

with OUT.open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["query", "query_type"])
    writer.writerows(deduped)

print(f"已生成 {len(deduped)} 条 AI 检索关键词：{OUT}")
