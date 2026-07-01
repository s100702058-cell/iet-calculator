import streamlit as st
import pandas as pd

st.set_page_config(page_title="精準營養配對模組", page_icon="📊", layout="wide")

st.title("📊 精準營養神算配對模組 (門診/重症/ERAS)")
st.write("本模組專門處理個案之精確三大產能營養素分配、渣質限制、ONS 扣除與餐次全自動矩陣配對。")

st.markdown("---")

# 疾病別矩陣定義
DISEASE_DB = {
    "一般健康成人 (General Adult)": {"kcal_min": 25, "kcal_max": 30, "pro_min": 0.8, "pro_max": 1.0, "notes": "維持一般均衡飲食，定錨基本微量元素平衡。"},
    "ICU 重症加護-急性期 (Critical Care-Acute)": {"kcal_min": 20, "kcal_max": 25, "pro_min": 1.2, "pro_max": 1.5, "notes": "高發炎高消耗！給予高蛋白對抗肌肉分解。初期熱量切記不可給太高（20-25 kcal/kg），嚴防致命的『再餵食症候群 (Refeeding Syndrome)』！"},
    "ICU 重症加護-恢復期 (Critical Care-Recovery)": {"kcal_min": 25, "kcal_max": 35, "pro_min": 1.5, "pro_max": 2.0, "notes": "進入組織重建期。熱量與蛋白質全面拉高，全力修復瘦體組織。"},
    "ERAS 術後加速康復程 (ERAS Protocol)": {"kcal_min": 25, "kcal_max": 30, "pro_min": 1.2, "pro_max": 1.5, "notes": "強調術後早期進食、減少生理應激。若為腸胃道手術，初期必須嚴格配合低渣或無渣飲食，減少腸道工作量。"},
    "第二型糖尿病 (Diabetes Mellitus)": {"kcal_min": 25, "kcal_max": 30, "pro_min": 1.0, "pro_max": 1.2, "notes": "控制總醣量、均勻分配三餐、增加膳食纖維。控制水果份量與時機，禁止含糖飲料。"},
    "慢性腎臟病-未透析 (CKD)": {"kcal_min": 30, "kcal_max": 35, "pro_min": 0.6, "pro_max": 0.8, "notes": "限制蛋白質、鈉、鉀、磷。採低氮澱粉（冬粉、西谷米）、蔬菜切後必須汆燙以避出鉀離子。"},
    "高血脂症 (Hyperlipidemia)": {"kcal_min": 25, "kcal_max": 30, "pro_min": 0.8, "pro_max": 1.2, "notes": "降低飽和脂肪與反式脂肪，多選單元不飽和脂肪（橄欖油），膳食纖維干預目標建議拉高至 50g 以上以加速膽酸排泄。"}
}

# ==================== Sidebar: 使用者輸入區 ====================
st.sidebar.header("📋 NCP 臨床情境定錨")
weight = st.sidebar.number_input("個案體重 (kg):", min_value=30.0, max_value=200.0, value=60.0, step=0.5)

selected_disease = st.sidebar.selectbox("選擇臨床目標疾病:", list(DISEASE_DB.keys()))
disease_info = DISEASE_DB[selected_disease]

residue_type = st.sidebar.radio("腸道渣質限制:", ["常規一般飲食", "低渣飲食 (低纖維/限制乳品)", "無渣飲食 (腸道術後/完全清空/嚴禁乳品)"])

st.sidebar.markdown("---")
st.sidebar.header("🌾 膳食纖維臨床干預")
fiber_mode = st.sidebar.radio("膳食纖維每日目標:", ["常規成人基礎需求 (34g/日)", "有效改善高血脂高劑量干預 (50g+/日)"])
target_fiber = 34 if "34g" in fiber_mode else 50

st.sidebar.markdown("---")
st.sidebar.header("⚙️ 外援商業營養品 (ONS) 扣除")
use_ons = st.sidebar.checkbox("搭配使用『口服補充/商業配方』")

ons_kcal, ons_p, ons_f, ons_c = 0.0, 0.0, 0.0, 0.0
if use_ons:
    ons_cans = st.sidebar.slider("每日使用罐數 (1罐預設250kcal, P:10g, F:8.5g, C:33.5g):", 1, 6, 2, step=1)
    ons_kcal = ons_cans * 250.0
    ons_p = ons_cans * 10.0
    ons_f = ons_cans * 8.5
    ons_c = ons_cans * 33.5

st.sidebar.markdown("---")
st.sidebar.header("⚖️ 自體淨需求計算")
kcal_kg = st.sidebar.slider("每日每公斤熱量 (kcal/kg):", 15, 45, int(disease_info["kcal_max"]), step=1)
pro_g_kg = st.sidebar.slider("每日每公斤蛋白質 (g/kg):", 0.5, 2.5, float(disease_info["pro_min"]), step=0.1)

# 計算自體淨缺口
raw_tdee = weight * kcal_kg
raw_pro_g = weight * pro_g_kg
tdee = max(0.0, raw_tdee - ons_kcal)
target_pro_g = max(0.0, raw_pro_g - ons_p)
pro_kcal = target_pro_g * 4

if pro_kcal >= tdee and tdee > 0:
    st.sidebar.error("❌ 錯誤：蛋白質熱量超出剩餘總熱量預算！")
else:
    pro_ratio_total = (pro_kcal / tdee) * 100 if tdee > 0 else 0
    max_cho_ratio = max(15.0, 100 - pro_ratio_total - 10)
    min_cho_ratio = 15.0
    default_cho_ratio = 50.0 if min_cho_ratio <= 50.0 <= max_cho_ratio else min_cho_ratio
    
    cho_ratio = st.sidebar.slider("微調 醣類比例 (占剩餘總熱量 %):", int(min_cho_ratio), int(max_cho_ratio), int(default_cho_ratio), step=1)
    fat_ratio = 100 - pro_ratio_total - cho_ratio
    target_cho_g = ((tdee * (cho_ratio / 100)) / 4) if tdee > 0 else 0
    target_fat_g = ((tdee * (fat_ratio / 100)) / 9) if tdee > 0 else 0

st.sidebar.markdown("---")
st.sidebar.header("🧬 代換表資料庫微調")

# 🔒 無渣限制：乳品強制解鎖「無乳品」選項
if residue_type == "無渣飲食 (腸道術後/完全清空/嚴禁乳品)":
    milk_type = st.sidebar.selectbox("乳品分型 (無渣已強制鎖定):", ["不喝乳品/無乳品 (P:0g, F:0g, C:0g)"])
else:
    milk_type = st.sidebar.selectbox("乳品分型:", ["低脂乳品 (P:8g, F:4g, C:12g)", "全脂乳品 (P:8g, F:8g, C:12g)", "脫脂乳品 (P:8g, F:0g, C:12g)", "不喝乳品/無乳品 (P:0g, F:0g, C:0g)"])

if "低脂" in milk_type:
    milk_p, milk_f, milk_c, milk_servings = 8.0, 4.0, 12.0, 1.0
elif "全脂" in milk_type:
    milk_p, milk_f, milk_c, milk_servings = 8.0, 8.0, 12.0, 1.0
elif "脫脂" in milk_type:
    milk_p, milk_f, milk_c, milk_servings = 8.0, 0.0, 12.0, 1.0
else:
    milk_p, milk_f, milk_c, milk_servings = 0.0, 0.0, 0.0, 0.0

# 🔒 臨床急性解鎖：肉類分型新增「無肉品」選項
meat_type = st.sidebar.selectbox("肉類分級選擇:", ["中脂肉類 (P:7g, F:5g)", "低脂肉類 (P:7g, F:3g)", "高脂肉類 (P:7g, F:10g)", "不吃肉類/無肉品 (P:0g, F:0g)"])

if "中脂" in meat_type:
    meat_p, meat_f, is_meat_free = 7.0, 5.0, False
    meat_ref = "生重 35 克中脂肉類 (如豆腐 80 克、雞蛋 55 克)"
elif "低脂" in meat_type:
    meat_p, meat_f, is_meat_free = 7.0, 3.0, False
    meat_ref = "生重 35 克低脂肉類 (如一般魚類 35 克)"
elif "高脂" in meat_type:
    meat_p, meat_f, is_meat_free = 7.0, 10.0, False
    meat_ref = "生重 35 克高脂肉類 (如百頁豆腐 70 克)"
else:
    meat_p, meat_f, is_meat_free = 0.0, 0.0, True
    meat_ref = "當前已完全剔除肉類蛋白質與脂肪分配！"

meal_mode = st.sidebar.selectbox(
    "餐次分配模式:",
    ["常規三餐等分 (早33.3%, 午33.3%, 晚33.3%)", "常規四餐結構 (早30%, 午30%, 晚30%, 點心10%)", "重症少量多餐 (六餐均分各16.6%)"]
)

if "常規三餐" in meal_mode:
    meals = {"早餐": 0.333, "午餐": 0.333, "晚餐": 0.334}
elif "常規四餐" in meal_mode:
    meals = {"早餐": 0.30, "午餐": 0.30, "晚餐": 0.30, "點心": 0.10}
else:
    meals = {"第一餐": 0.166, "第二餐": 0.166, "第三餐": 0.166, "第四餐": 0.166, "第五餐": 0.166, "第六餐": 0.17}

# ==================== Core Matching Algorithm ====================
veg_servings = 0.0 if residue_type == "無渣飲食 (腸道術後/完全清空/嚴禁乳品)" else 3.0
fruit_servings = 0.0 if residue_type == "無渣飲食 (腸道術後/完全清空/嚴禁乳品)" else 2.0

base_cho = (veg_servings * 5) + (fruit_servings * 15) + (milk_servings * milk_c)
base_pro = (veg_servings * 1) + (fruit_servings * 0) + (milk_servings * milk_p)
base_fat = (veg_servings * 0) + (fruit_servings * 0) + (milk_servings * milk_f)

rem_cho = target_cho_g - base_cho
rem_pro = target_pro_g - base_pro

grain_servings = max(0.0, rem_cho / 15)
rem_pro_after_grain = rem_pro - (grain_servings * 2)

if is_meat_free:
    meat_servings = 0.0
else:
    meat_servings = max(0.0, rem_pro_after_grain / meat_p)

current_fat = base_fat + (meat_servings * meat_f)
rem_fat = target_fat_g - current_fat
fat_servings = max(0.0, rem_fat / 5)

# ==================== UI Output ====================
st.subheader(f"🩺 當前臨床情境：{selected_disease}")
st.info(f"💡 **介入指引**：{disease_info['notes']}\n\n⚠️ **當前渣質限制**：{residue_type}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 總熱量需求 (含外援)", f"{raw_tdee:.0f} kcal")
col2.metric("🍚 淨天然食物熱量需求", f"{tdee:.0f} kcal")
col3.metric("🍗 淨蛋白質目標", f"{target_pro_g:.1f} g")
col4.metric("🌾 膳食纖維干預目標", f"{target_fiber} g/日")

st.markdown("### 🍽️ 淨天然食物：六大類食物每日精準總份數")
grain_note = "禁止糙米雜糧，請全面改用白米飯、白吐司、冬粉或西谷米！" if "一般" not in residue_type else "一份等於生重20-30g，如1/4碗飯。"
veg_note = "無渣飲食已將蔬菜降為0份。" if residue_type == "無渣飲食 (腸道術後/完全清空/嚴禁乳品)" else "一份等於生重100g。限鉀個案切記要先切再充分汆燙！"
fruit_note = "無渣飲食已將水果降為0份。" if residue_type == "無渣飲食 (腸道術後/完全清空/嚴禁乳品)" else "一份約100g。"
milk_note = "已強制關閉乳品類，避免酪蛋白凝乳造成腸道殘渣！" if milk_servings == 0 else f"1份等於240ml。當前選用：{milk_type}"

food_groups_data = {
    "六大類食物名稱": ["全穀雜糧類", "豆魚蛋肉類", "乳品類", "蔬菜類", "水果類", "油脂與堅果種子類"],
    "每日精準總份數": [f"{grain_servings:.1f} 份", f"{meat_servings:.1f} 份", f"{milk_servings:.1f} 份", f"{veg_servings:.1f} 份", f"{fruit_servings:.1f} 份", f"{fat_servings:.1f} 份"],
    "臨床生重與品項精確指引": [grain_note, f"搭配目前設定，1份相當於：{meat_ref}。低渣/無渣個案嚴禁油炸與帶筋老肉！", milk_note, veg_note, fruit_note, f"約 {fat_servings*5:.1f} 克烹調油。低渣/無渣飲食者嚴禁食用整粒堅果，避免顆粒摩擦腸壁！"]
}
st.dataframe(pd.DataFrame(food_groups_data), use_container_width=True)

st.markdown("### ⏰ 每餐次六大類食物份數自動配對表")
meal_rows = []
for m_name, m_pct in meals.items():
    meal_rows.append({
        "餐次 (Meal Time)": f"{m_name} ({m_pct*100:.1f}%)",
        "全穀雜糧類": f"{grain_servings * m_pct:.1f} 份",
        "豆魚蛋肉類": f"{meat_servings * m_pct:.1f} 份",
        "乳品類": f"{milk_servings * m_pct:.1f} 份" if milk_servings > 0 else "0.0 份",
        "蔬菜類": f"{veg_servings * m_pct:.1f} 份" if veg_servings > 0 else "0.0 份",
        "水果類": f"{fruit_servings * m_pct:.1f} 份" if fruit_servings > 0 else "0.0 份",
        "油脂堅果類": f"{fat_servings * m_pct:.1f} 份"
    })
st.dataframe(pd.DataFrame(meal_rows), use_container_width=True)
st.success("🎉 運算成功！這套選單已完美適配臨床餐次與重症渣質限制！")
