from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/brand_score_inputs.csv"
OUT_DIR = ROOT / "outputs/tables"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "brand_fit_score.csv"

WEIGHTS = {
    "price_fit": 0.18,
    "taste_fit": 0.16,
    "scene_fit": 0.20,
    "business_area_fit": 0.16,
    "communication_fit": 0.14,
    "culture_fit": 0.12,
    "supply_chain_difficulty": -0.04
}

def to_score(value):
    try:
        v = float(value)
    except Exception:
        return None
    if v < 0:
        return 0
    if v > 10:
        return 10
    return v

def main():
    if not RAW.exists():
        raise FileNotFoundError(f"缺少原始数据：{RAW}")

    df = pd.read_csv(RAW)
    if df.empty:
        # 输出默认评分模板，不生成结论
        default = pd.DataFrame([
            {"brand": "陶陶居", "note": "请基于调研数据填写 0-10 分"},
            {"brand": "点都德", "note": "请基于调研数据填写 0-10 分"}
        ])
        default.to_csv(OUT, index=False, encoding="utf-8-sig")
        print("brand_score_inputs.csv 目前没有数据。已输出默认品牌评分提示。")
        return

    for col in WEIGHTS:
        if col in df.columns:
            df[col] = df[col].apply(to_score)
        else:
            df[col] = None

    def weighted_score(row):
        total = 0
        available_weight = 0
        for col, w in WEIGHTS.items():
            if pd.notna(row[col]):
                total += row[col] * w
                available_weight += abs(w)
        if available_weight == 0:
            return None
        return round(total, 2)

    df["weighted_score"] = df.apply(weighted_score, axis=1)

    def verdict(score):
        if pd.isna(score):
            return "数据不足"
        if score >= 7.5:
            return "适配度较高，可进入重点招商讨论"
        if score >= 6:
            return "有机会，但需验证价格/场景/复购"
        if score >= 4.5:
            return "谨慎观察，适合先做轻量测试"
        return "当前适配度偏低，不建议直接大店进入"

    df["verdict"] = df["weighted_score"].apply(verdict)
    df.to_csv(OUT, index=False, encoding="utf-8-sig")
    print(f"已输出：{OUT}")

if __name__ == "__main__":
    main()
