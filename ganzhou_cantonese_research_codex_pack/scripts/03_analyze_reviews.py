from pathlib import Path
import json
import pandas as pd
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/reviews_raw.csv"
LEXICON = ROOT / "config/keyword_lexicon.json"
OUT_DIR = ROOT / "data/processed"
TABLE_DIR = ROOT / "outputs/tables"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)

def load_lexicon():
    with LEXICON.open("r", encoding="utf-8") as f:
        return json.load(f)

def find_keywords(text, keywords):
    text = str(text)
    return [k for k in keywords if k in text]

def classify_sentiment(text, pos_words, neg_words):
    pos = find_keywords(text, pos_words)
    neg = find_keywords(text, neg_words)
    if len(pos) > len(neg):
        return "正向"
    if len(neg) > len(pos):
        return "负向"
    if pos and neg:
        return "混合"
    return "中性/待人工确认"

def main():
    if not RAW.exists():
        raise FileNotFoundError(f"缺少原始数据：{RAW}")

    df = pd.read_csv(RAW)
    if df.empty:
        print("reviews_raw.csv 目前没有数据，仅保留表头。请先录入评论样本。")
        return

    lex = load_lexicon()
    pos_words = lex["positive"]
    neg_words = lex["negative"]
    scene_words = lex["scene"]
    culture_words = lex["cantonese_culture"]

    df["positive_keywords"] = df["review_text"].apply(lambda x: "、".join(find_keywords(x, pos_words)))
    df["negative_keywords"] = df["review_text"].apply(lambda x: "、".join(find_keywords(x, neg_words)))
    df["scene_keywords"] = df["review_text"].apply(lambda x: "、".join(find_keywords(x, scene_words)))
    df["cantonese_culture_keywords"] = df["review_text"].apply(lambda x: "、".join(find_keywords(x, culture_words)))
    df["sentiment"] = df["review_text"].apply(lambda x: classify_sentiment(x, pos_words, neg_words))

    classified_path = OUT_DIR / "reviews_classified.csv"
    df.to_csv(classified_path, index=False, encoding="utf-8-sig")

    all_pos = Counter()
    all_neg = Counter()
    all_scene = Counter()
    all_culture = Counter()

    for text in df["review_text"].fillna("").astype(str):
        all_pos.update(find_keywords(text, pos_words))
        all_neg.update(find_keywords(text, neg_words))
        all_scene.update(find_keywords(text, scene_words))
        all_culture.update(find_keywords(text, culture_words))

    def counter_to_df(counter, name):
        return pd.DataFrame(counter.most_common(30), columns=["keyword", "count"]).assign(type=name)

    keyword_summary = pd.concat([
        counter_to_df(all_pos, "正向"),
        counter_to_df(all_neg, "负向"),
        counter_to_df(all_scene, "场景"),
        counter_to_df(all_culture, "粤菜文化")
    ], ignore_index=True)

    keyword_path = TABLE_DIR / "review_keyword_summary.csv"
    keyword_summary.to_csv(keyword_path, index=False, encoding="utf-8-sig")

    sentiment_summary = df.groupby("sentiment").size().reset_index(name="count")
    sentiment_path = TABLE_DIR / "review_sentiment_summary.csv"
    sentiment_summary.to_csv(sentiment_path, index=False, encoding="utf-8-sig")

    print(f"已输出：{classified_path}")
    print(f"已输出：{keyword_path}")
    print(f"已输出：{sentiment_path}")

if __name__ == "__main__":
    main()
