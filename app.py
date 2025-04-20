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
site_order = [
    "全部位", "食道", "胃", "結腸", "直腸Ｓ状結腸移行部",
    "肝及び肝内胆管", "胆のう及び他の胆道", "膵", "気管、気管支及び肺",
    "乳房（女性のみ）", "子宮", "卵巣", "前立腺", "膀胱の悪性新生物",
    "悪性リンパ腫", "白　血　病", "大腸"
]
sites = [s for s in site_order if s in df["部位"].unique()]
prefs = df["都道府県"].unique()
genders = df["性別"].unique()

# UI
st.title("Cancer Site-specific Age-adjusted Mortality Rate (Under 75)")

site = st.sidebar.selectbox("Select cancer site", sites, index=sites.index("全部位"))
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
ax.legend(loc="upper right")
if data_line_pref.empty and pref != "全国":
    st.warning(f"No data available for {site} ({gender}) in {pref}")
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

import json
import plotly.express as px

# 地図描画（都道府県別ヒートマップ）
st.subheader(f"{year} - Prefecture ASR Map: {site} ({gender})")

# 都道府県コードを追加（JISコード）
pref_code_map = {
    "北海道": "01", "青森県": "02", "岩手県": "03", "宮城県": "04", "秋田県": "05",
    "山形県": "06", "福島県": "07", "茨城県": "08", "栃木県": "09", "群馬県": "10",
    "埼玉県": "11", "千葉県": "12", "東京都": "13", "神奈川県": "14", "新潟県": "15",
    "富山県": "16", "石川県": "17", "福井県": "18", "山梨県": "19", "長野県": "20",
    "岐阜県": "21", "静岡県": "22", "愛知県": "23", "三重県": "24", "滋賀県": "25",
    "京都府": "26", "大阪府": "27", "兵庫県": "28", "奈良県": "29", "和歌山県": "30",
    "鳥取県": "31", "島根県": "32", "岡山県": "33", "広島県": "34", "山口県": "35",
    "徳島県": "36", "香川県": "37", "愛媛県": "38", "高知県": "39", "福岡県": "40",
    "佐賀県": "41", "長崎県": "42", "熊本県": "43", "大分県": "44", "宮崎県": "45",
    "鹿児島県": "46", "沖縄県": "47"
}
data_bar["コード"] = data_bar["都道府県"].map(pref_code_map)

# GeoJSONの読み込み（中身確認用）
st.subheader("GeoJSON debug info (first feature)")
try:
    with open("japan_prefectures.geojson", "r", encoding="utf-8") as f:
        geojson = json.load(f)
    if geojson and "features" in geojson and len(geojson["features"]) > 0:
        st.write(geojson["features"][0]["properties"])
except Exception as e:
    st.warning("Could not read GeoJSON file.")
try:
    with open("japan_prefectures.geojson", "r", encoding="utf-8") as f:
        geojson = json.load(f)

    fig3 = px.choropleth_mapbox(
        data_bar,
        geojson=geojson,
        locations="コード",
        color=str(year),
        color_continuous_scale="OrRd",
        range_color=(data_bar[str(year)].min(), data_bar[str(year)].max()),
        featureidkey="properties.code",
        labels={str(year): "ASR"},
        
    )
    fig3.update_layout(mapbox_style="carto-positron", mapbox_zoom=4.5, mapbox_center={"lat": 36.5, "lon": 138.0})
    fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig3)
except Exception as e:
    st.info("Map data not available in this environment.")

# 出典
st.caption("Source: National Cancer Center Japan, Cancer Information Service (https://ganjoho.jp/reg_stat/statistics/data/dl/index.html)")
