import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# データ読み込み
df = pd.read_csv("asr75.csv", encoding="utf-8")

# 年の列を抽出
year_columns = [col for col in df.columns if col.isdigit()]
years = list(map(int, year_columns))

# 都道府県英語変換マップ（簡易版）
pref_map = {
    "北海道": "Hokkaido", "青森県": "Aomori", "岩手県": "Iwate", "宮城県": "Miyagi", "秋田県": "Akita",
    "山形県": "Yamagata", "福島県": "Fukushima", "茨城県": "Ibaraki", "栃木県": "Tochigi", "群馬県": "Gunma",
    "埼玉県": "Saitama", "千葉県": "Chiba", "東京都": "Tokyo", "神奈川県": "Kanagawa", "新潟県": "Niigata",
    "富山県": "Toyama", "石川県": "Ishikawa", "福井県": "Fukui", "山梨県": "Yamanashi", "長野県": "Nagano",
    "岐阜県": "Gifu", "静岡県": "Shizuoka", "愛知県": "Aichi", "三重県": "Mie", "滋賀県": "Shiga",
    "京都府": "Kyoto", "大阪府": "Osaka", "兵庫県": "Hyogo", "奈良県": "Nara", "和歌山県": "Wakayama",
    "鳥取県": "Tottori", "島根県": "Shimane", "岡山県": "Okayama", "広島県": "Hiroshima", "山口県": "Yamaguchi",
    "徳島県": "Tokushima", "香川県": "Kagawa", "愛媛県": "Ehime", "高知県": "Kochi", "福岡県": "Fukuoka",
    "佐賀県": "Saga", "長崎県": "Nagasaki", "熊本県": "Kumamoto", "大分県": "Oita", "宮崎県": "Miyazaki",
    "鹿児島県": "Kagoshima", "沖縄県": "Okinawa", "全国": "Japan"
}

# 選択肢作成
sites = df["部位"].unique()
prefs = df["都道府県"].unique()
genders = df["性別"].unique()

# UI
st.title("Cancer Site-specific Age-adjusted Mortality Rate (Under 75)")

site = st.sidebar.selectbox("Select cancer site", sorted(sites), index=sorted(sites).index("全部位"))
gender = st.sidebar.selectbox("Select gender", genders)
pref = st.sidebar.selectbox("Select prefecture", prefs)
year = st.sidebar.selectbox("Select year for comparison", sorted(years))

# 表示用ラベル変換
pref_label = pref_map.get(pref, pref)

# フィルタリング（年次推移）
data_line = df[(df["部位"] == site) & (df["性別"] == gender)]
data_line_nation = data_line[data_line["都道府県"] == "全国"]
data_line_pref = data_line[data_line["都道府県"] == pref]

# 折れ線グラフ
st.subheader(f"{site} ({gender}) - Trend: {pref_label} vs National Average")
fig, ax = plt.subplots()
if not data_line_nation.empty:
    ax.plot(years, data_line_nation[year_columns].values.flatten(), label="Japan", color="#999999", linewidth=2)
if pref != "全国":
    if not data_line_pref.empty:
        ax.plot(years, data_line_pref[year_columns].values.flatten(), label=pref_label, color="#E69F00", linewidth=2)
ax.set_xlabel("Year")
ax.set_ylabel("ASR (per 100,000, under 75)")
ax.legend()
st.pyplot(fig)

# 特定年の都道府県比較
st.subheader(f"{year} - Prefecture Comparison: {site} ({gender})")
data_bar = df[(df["部位"] == site) & (df["性別"] == gender) & (df["都道府県"] != "全国")][["都道府県", str(year)]]
data_bar["英語県名"] = data_bar["都道府県"].map(pref_map)
data_bar_sorted = data_bar.sort_values(by=str(year), ascending=False)
fig2, ax2 = plt.subplots(figsize=(14, 6))
ax2.bar(data_bar_sorted["英語県名"], data_bar_sorted[str(year)], color="#0072B2")
ax2.set_xlabel("Prefecture")
ax2.set_ylabel("ASR (per 100,000, under 75)")
ax2.set_xticklabels(data_bar_sorted["英語県名"], rotation=60, ha='right', fontsize=10)
st.pyplot(fig2)

# 出典
st.caption("Source: National Cancer Center Japan, Cancer Information Service (https://ganjoho.jp/reg_stat/statistics/data/dl/index.html)")
