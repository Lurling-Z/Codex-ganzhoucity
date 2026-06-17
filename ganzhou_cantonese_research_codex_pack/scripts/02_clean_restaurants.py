from pathlib import Path
import pandas as pd
import re

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/restaurants_raw.csv"
OUT_DIR = ROOT / "data/processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "restaurants_clean.csv"
SUMMARY = ROOT / "outputs/tables/restaurant_summary.csv"
SUMMARY.parent.mkdir(parents=True, exist_ok=True)

def to_number(value):
    if pd.isna(value):
        return None
    text = str(value).strip()
    if not text:
        return None
    text = re.sub(r"[^\d.]", "", text)
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None

def price_band(price):
    if pd.isna(price):
        return "未知"
    if price < 50:
        return "30-50元以下/轻量消费"
    if price < 90:
        return "50-90元/日常聚餐"
    if price < 150:
        return "90-150元/品质聚餐"
    return "150元以上/高端或宴请"

def normalize_bool(value):
    if pd.isna(value):
        return "未知"
    text = str(value).strip().lower()
    if text in {"1", "yes", "y", "true", "是", "有", "适合"}:
        return "是"
    if text in {"0", "no", "n", "false", "否", "无", "不适合"}:
        return "否"
    return str(value).strip() or "未知"

def infer_type(category, dishes):
    text = f"{category or ''} {dishes or ''}"
    if any(k in text for k in ["早茶", "茶楼", "点心", "虾饺", "烧卖", "红米肠"]):
        return "广式早茶/点心"
    if any(k in text for k in ["茶餐厅", "港式"]):
        return "港式茶餐厅"
    if any(k in text for k in ["烧腊", "烧鹅", "叉烧", "豉油鸡"]):
        return "烧腊/粤式快餐"
    if any(k in text for k in ["顺德", "啫啫", "粤菜"]):
        return "粤菜正餐/顺德菜"
    if any(k in text for k in ["肠粉", "云吞", "煲仔饭"]):
        return "粤式小吃/简餐"
    return "其他/待人工确认"

def main():
    if not RAW.exists():
        raise FileNotFoundError(f"缺少原始数据：{RAW}")

    df = pd.read_csv(RAW)
    if df.empty:
        print("restaurants_raw.csv 目前没有数据，仅保留表头。请先录入门店样本。")
        return

    df.columns = [c.strip() for c in df.columns]
    for col in ["avg_price", "rating", "review_count", "favorite_count"]:
        if col in df.columns:
            df[col] = df[col].apply(to_number)

    for col in ["in_mall", "has_morning_tea", "has_private_room", "family_friendly", "business_friendly"]:
        if col in df.columns:
            df[col] = df[col].apply(normalize_bool)

    df["store_name_norm"] = df["store_name"].astype(str).str.strip()
    df = df.drop_duplicates(subset=["store_name_norm", "platform", "business_area"], keep="first")

    df["price_band"] = df["avg_price"].apply(price_band)
    df["cantonese_type"] = df.apply(
        lambda r: infer_type(r.get("category", ""), r.get("recommended_dishes", "")),
        axis=1
    )

    df.to_csv(OUT, index=False, encoding="utf-8-sig")

    summary = pd.DataFrame({
        "metric": [
            "门店样本数",
            "平台数量",
            "商圈数量",
            "平均人均消费",
            "平均评分",
            "平均评论数"
        ],
        "value": [
            len(df),
            df["platform"].nunique() if "platform" in df else None,
            df["business_area"].nunique() if "business_area" in df else None,
            round(df["avg_price"].mean(), 2) if "avg_price" in df else None,
            round(df["rating"].mean(), 2) if "rating" in df else None,
            round(df["review_count"].mean(), 2) if "review_count" in df else None
        ]
    })
    summary.to_csv(SUMMARY, index=False, encoding="utf-8-sig")

    print(f"已输出：{OUT}")
    print(f"已输出：{SUMMARY}")

if __name__ == "__main__":
    main()
