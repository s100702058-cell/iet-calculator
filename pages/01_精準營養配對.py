import streamlit as st
import pandas as pd

st.set_page_config(page_title="精準營養配對模組-CNOS終極版", page_icon="📊", layout="wide")

st.title("📊 臨床生化導航、重症透析與台灣在地團膳整合配對平台")
st.write("本模組已全面導入 NCP 生化評估矩陣、未透析 CKD 照護、HD/CAPD 雙流運算與台灣季節時蔬成本管制點！")

st.markdown("---")

# ==================== 疾病、重症與生化指標核心資料庫 ====================
DISEASE_DB = {
    "一般健康成人 (General Adult)": {
        "kcal_min": 25, "kcal_max": 30, "pro_min": 0.8, "pro_max": 1.0, "notes": "維持一般平衡。監測指標：Albumin, FPG, TG, TC。",
        "lab_notes": "📌 常規生化指標：維持基礎代謝與微量元素平衡即可。"
    },
    "慢性腎臟病-未透析 (CKD)": {
        "kcal_min": 30, "kcal_max": 35, "pro_min": 0.6, "pro_max": 0.8, "notes": "嚴格限蛋！蛋白質限制在 0.6-0.8 g/kg 以延緩腎衰竭。熱量需給足。監測指標：BUN, Cr, eGFR, K, P。",
        "lab_notes": "🚨 關鍵生化指標：密切監測血清鉀與磷！若 eGFR 降至中重度，蔬菜必須切後充分汆燙 3-5 分鐘以阻斷高血鉀心臟風險。"
    },
    "糖尿病腎病變 (Diabetic Nephropathy, DN)": {
        "kcal_min": 25, "kcal_max": 30, "pro_min": 0.8, "pro_max": 0.8, "notes": "控糖限蛋極致！蛋白質定錨 0.8 g/kg 延緩腎絲球硬化。醣類必須精準均分。監測指標：HbA1c, FPG, UACR, eGFR。",
        "lab_notes": "🚨 關鍵生化指標：注意 UACR 微量白蛋白尿！若開始出現漏水警訊，需嚴格限制高飽和脂肪肉品與精製糖，防範血管內皮二次高壓受損。"
    },
    "慢性腎臟病-血液透析階段 (HD)": {
        "kcal_min": 30, "kcal_max": 35, "pro_min": 1.2, "pro_max": 1.4, "notes": "高補償優質蛋白！透析流失大量胺基酸，蛋白質大幅拉高至 1.2-1.4 g/kg。監測指標：iPTH, K, P, Ca, Albumin, Hb。",
        "lab_notes": "🚨 關鍵生化指標：嚴控兩次透析間水份（體重增加<5%）。血磷過高易引發血管鈣化與骨病變，餐中需確實搭配磷結合劑。"
    },
    "慢性腎臟病-腹膜透析階段 (CAPD)": {
        "kcal_min": 30, "kcal_max": 35, "pro_min": 1.2, "pro_max": 1.5, "notes": "持續性白蛋白流失補償！需求拉高至 1.2-1.5 g/kg。⚠️已自動扣除腹膜吸收之葡萄糖熱量 (約200 kcal/日)。監測指標：Albumin, TG, TC, K, P。",
        "lab_notes": "🚨 關鍵生化指標：腹膜每日流失 5-15g 蛋白質，極易誘發嚴重 PEM（蛋白質能量營養不良），且常伴隨高脂血症，需搭配高纖維飲食。"
    },
    "ICU 重症加護-急性期 (Critical Care-Acute)": {
        "kcal_min": 20, "kcal_max": 25, "pro_min": 1.2, "pro_max": 1.5, "notes": "急性代謝應激型！高蛋白對抗肌肉分解。熱量初期限制在 20-25 kcal/kg，嚴防再餵食症候群！監測指標：CRP, Prealbumin, Glucose, Lactate。",
        "lab_notes": "🚨 關鍵生化指標：CRP 飆高且 Albumin 急跌屬負性急性期反應，絕非單純缺營養。血磷若暴跌 (<2.0 mg/dL) 預示 Refeeding Risk，需立刻暫緩熱量追擊！"
    },
    "ERAS 術後加速康復程 (ERAS Protocol)": {
        "kcal_min": 25, "kcal_max": 30, "pro_min": 1.2, "pro_max": 1.5, "notes": "減少生理應激。若為腸胃道手術，初期配合低渣或無渣飲食。監測指標：Pre-op Albumin, Post-op CRP, Glucose, Fluid Balance。",
        "lab_notes": "🚨 關鍵生化指標：術前白蛋白若 <3.0 g/dL 預示傷口癒合不良。初期菜單必須強制鎖定『無乳品/無渣』，避免酪蛋白凝乳在腸道下段留下包袱。"
    },
    "高血脂症 (Hyperlipidemia)": {
        "kcal_min": 25, "kcal_max": 30, "pro_min": 0.8, "pro_max": 1.2, "notes": "脂質調配型。降低飽和脂肪，膳食纖維干預目標拉高至 50g 以上以加速膽酸排泄。監測指標：LDL-C, TG, TC, HDL-C。",
        "lab_notes": "🚨 關鍵生化指標：以調降 LDL-C 為核心干預靶點。總脂肪不是越低越好，重點是脂肪種類（單元不飽和 MUFA 與 omega-3 優先）。"
    }
}

# ==================== 台灣在地四季時蔬與成本資料庫 ====================
VEG_TAIWAN_DB = {
    "春夏季盛產時蔬 (低成本/高優質)": [
        {"name": "台灣空心菜", "potassium": "高鉀 (需汆燙)", "cost_pkg": "低 (約 30-40 元/kg)", "ccp": "🚨 CCP 備料點：必須先切、充分汆燙 3 分鐘、去汁液方可烹調，阻斷高血鉀風暴。"},
        {"name": "在地澎湖絲瓜", "potassium": "中/低鉀 (去皮)", "cost_pkg": "低 (約 35-45 元/kg)", "ccp": "適合低渣/無渣過渡期飲食，去皮去籽質地極軟，腸道零負擔。"},
        {"name": "有機綠蘆筍", "potassium": "高鉀 (限鉀慎用)", "cost_pkg": "高 (約 120-150 元/kg)", "ccp": "重症限鉀與限經費個案需嚴格控管份量，切勿盲目大量排入菜單。"},
        {"name": "台灣中清苦瓜", "potassium": "中鉀", "cost_pkg": "中 (約 50-60 元/kg)", "ccp": "低渣飲食者禁用。常規糖尿病個案首選，含苦瓜素具臨床助攻效益。"}
    ],
    "秋冬季盛產時蔬 (低成本/高優質)": [
        {"name": "高山初秋高麗菜", "potassium": "低/中鉀", "cost_pkg": "極低 (約 20-30 元/kg)", "ccp": "團膳成本控制神物！質地爽脆，低渣飲食者需徹底煮至熟爛方可使用。"},
        {"name": "在地優質白蘿蔔", "potassium": "低鉀 (透析首選)", "cost_pkg": "低 (約 25-35 元/kg)", "ccp": "鉀離子極低，HD/CAPD 與糖尿病腎病變病患的最佳餐盤安全墊底食材。"},
        {"name": "國產精選青花菜", "potassium": "高鉀高磷", "cost_pkg": "中 (約 60-80 元/kg)", "ccp": "🚨 CCP 關鍵管制：含高膳食纖維，改善高血脂（目標50g）首選，但腎病與透析者必須切小朵強力汆燙去鉀！"},
        {"name": "埔里鮮嫩香菇", "potassium": "極高鉀高磷 (危險)", "cost_pkg": "高 (約 140-180 元/kg)", "ccp": "❌ 嚴重腎病、透析與痛風急性期禁忌！富含普林與高磷，團膳配膳需嚴格剔除。"}
    ]
}

# ==================== Sidebar: NCP 臨床評估與輸入 ====================
st.sidebar.header("📋 第一步：NCP 臨床情境定錨")
weight = st.sidebar.number_input("個案體重 (kg):", min_value=30.0, max_value=200.0, value=60.0, step=0.5)

selected_disease = st.sidebar.selectbox("請選擇臨床情境/目標疾病:", list(DISEASE_DB.keys()))
disease_info = DISEASE_DB[selected_disease]

residue_type = st.sidebar.radio("腸道渣質限制:", ["常規一般飲食", "低渣飲食 (低纖維/限制乳品)", "無渣飲食 (腸道術後/完全清空/嚴禁乳品)"])

# 🚀 補回失蹤的生化指標輸入專區
st.sidebar.markdown("---")
st.sidebar.header("🩸 第二步：生化指標輸入 (Labs)")
lab_alb = st.sidebar.number_input("血清白蛋白 Albumin (g/dL):", min_value=1.0, max_value=6.0, value=3.5, step=0.1)
lab_k = st.sidebar.number_input("血清鉀 Potassium (mEq/L):", min_value=2.0, max_value=8.0, value=4.0, step=0.1)
lab_p = st.sidebar.number_input("血清磷 Phosphorus (mg/dL):", min_value=1.0, max_value=10.0, value=3.5, step=0.1)

if "糖尿病" in selected_disease or "Diabetic" in selected_disease:
    lab_hba1c = st.sidebar.number_input("糖化血色素 HbA1c (%):", min_value=4.0, max_value=15.0, value=6.5, step=0.1)
else:
    lab_hba1c = 6.0

st.sidebar.markdown("---")
st.sidebar.header("🌾 膳食纖維與台灣時蔬設定")
fiber_mode = st.sidebar.radio("膳食纖維每日目標:", ["常規成人基礎需求 (34g/日)", "有效改善高血脂高劑量干預 (50g+/日)"])
target_fiber = 34 if "34g" in fiber_mode else 50

taiwan_season = st.sidebar.selectbox("當前台灣採購季節:", list(VEG_TAIWAN_DB.keys()))

st.sidebar.markdown("---")
st.sidebar.header("⚙️ 第三步：外援商業營養品 (ONS) 扣除")
use_ons = st.sidebar.checkbox("搭配使用『口服補充/商業配方』")

ons_kcal, ons_p, ons_f, ons_c = 0.0, 0.0, 0.0, 0.0
if use_ons:
    ons_cans = st.sidebar.slider("每日使用罐數 (1罐預設250kcal, P:10g, F:8.5g, C:33.5g):", 1, 6, 2, step=1)
    ons_kcal = ons_cans * 250.0
    ons_p = ons_cans * 10.0
    ons_f = ons_cans * 8.5
    ons_c = ons_cans * 33.5

st.sidebar.markdown("---")
st.sidebar.header("⚖️ 第四步：自體淨需求計算")
kcal_kg = st.sidebar.slider("每日每公斤熱量 (kcal/kg):", 15, 45, int(disease_info["kcal_max"]), step=1)
pro_g_kg = st.sidebar.slider("每日每公斤蛋白質 (g/kg):", 0.5, 2.5, float(disease_info["pro_min"]), step=0.1)

raw_tdee = weight * kcal_kg
if "CAPD" in selected_disease:
    raw_tdee = max(0.0, raw_tdee - 200.0)

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
st.sidebar.header("🧬 第五步：代換表資料庫微調")

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

meat_type = st.sidebar.selectbox("肉類分級選擇:", ["中脂肉類 (P:7g, F:5g)", "低脂肉類 (P:7g, F:3g)", "高脂肉類 (P:7g, F:10g)", "不吃肉類/無肉品 (P:0g, F:0g)"])

if "中脂" in meat_type:
    meat_p, meat_f, is_meat_free = 7.0, 5.0, False
    meat_ref = "生重 35 克中脂肉類 (如豆腐 80 克、雞蛋 55 克)"
elif "低脂" in meat_type:
    meat_p, meat_f, is_meat_free = 7.0, 3.0, False
    meat_ref = "生重 35 克低脂肉類 (如一般魚類 35 克、無糖豆漿 190 毫升)"
elif "高脂" in meat_type:
    meat_p, meat_f, is_meat_free = 7.0, 10.0, False
    meat_ref = "生重 35 克高脂肉類 (如百頁豆腐 70 克)"
else:
    meat_p, meat_f, is_meat_free = 0.0, 0.0, True
    meat_ref = "當前已完全剔除肉類蛋白質與脂肪分配！"

meal_mode = st.sidebar.selectbox(
    "餐次分配模式:",
    ["常規三餐等分 (早33.3%, 午33.3%, 晚33.3%)", "常規四餐結構 (早30%, 午30%, 晚30%, 點心10%)", "重症/糖腎少量多餐 (六餐均分各16.6%)"]
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

# ==================== UI Output Dashboard ====================
st.subheader(f"🩺 當前臨床情境診斷：{selected_disease}")
st.info(f"💡 **臨床介入核心指引**：{disease_info['notes']}\n\n📢 **生化評估導航提示**：{disease_info['lab_notes']}")

# 🚀 補回自動化生化臨床警報看板
st.markdown("### 🚨 臨床生化即時警報系統 (Biochemical Alert System)")
alert_col1, alert_col2, alert_col3, alert_col4 = st.columns(4)

with alert_col1:
    if lab_alb < 3.0:
        st.error(f"🔴 白蛋白過低: {lab_alb} g/dL\n\n高度 PEM (蛋白質能量營養不良) 風險！重症發炎滲漏期，建議介入 ONS 商業配方。")
    elif lab_alb < 3.5:
        st.warning(f"🟠 白蛋白邊緣: {lab_alb} g/dL\n\n輕度營養不良風險，應監測每日優質蛋白攝取進度。")
    else:
        st.success(f"🟢 白蛋白正常: {lab_alb} g/dL")

with alert_col2:
    if lab_k > 5.1:
        st.error(f"🔴 血鉀超標: {lab_k} mEq/L\n\n高血鉀急性期！嚴防心臟毒性。下方已啟動去鉀 HACCP CCP 管制！")
    elif lab_k < 3.5:
        st.warning(f"🟠 血鉀偏低: {lab_k} mEq/L\n\n低血鉀警訊。需注意個案是否有腹瀉或利尿劑交互作用。")
    else:
        st.success(f"🟢 血鉀正常: {lab_k} mEq/L")

with alert_col3:
    if lab_p > 4.5:
        st.error(f"🔴 血磷超標: {lab_p} mg/dL\n\n高血磷警訊！易引發血管鈣化。配餐需嚴格剔除堅果類、內臟與加工品。")
    elif lab_p < 2.0:
        st.error(f"🔴 血磷急性暴跌: {lab_p} mg/dL\n\n極高再餵食症候群 (Refeeding Risk)！請立即限制熱量與醣類比例。")
    else:
        st.success(f"🟢 血磷正常: {lab_p} mg/dL")

with alert_col4:
    if "糖尿病" in selected_disease or "Diabetic" in selected_disease:
        if lab_hba1c > 7.0:
            st.error(f"🔴 血糖控制失控: {lab_hba1c}%\n\n微血管漏水警訊 UACR 易超標！請務必鎖定『少量多餐/六餐均分』。")
        else:
            st.success(f"🟢 血糖控制達標: {lab_hba1c}%")
    else:
        st.caption("📌 本情境未觸發糖功能專異性監測")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
if "CAPD" in selected_disease:
    col1.metric("📊 淨天然食物熱量需求", f"{tdee:.0f} kcal", "已扣除葡萄糖吸收量 200 kcal")
else:
    col1.metric("📊 淨天然食物熱量需求", f"{tdee:.0f} kcal")
col2.metric("🍚 淨醣類目標克數", f"{target_cho_g:.1f} g ({cho_ratio:.0f}%)")
col3.metric("🍗 淨蛋白質目標克數", f"{target_pro_g:.1f} g")
col4.metric("🌾 膳食纖維干舉目標", f"{target_fiber} g/日")

st.markdown("### 🍽️ 淨天然食物：六大類食物每日精準總份數")
grain_note = "禁止糙米，改用白米飯、冬粉或西谷米！" if "一般" not in residue_type else "一份等於生重20-30g，如1/4碗飯。若是CKD或糖腎限蛋白，多利用粉飴與冬粉！"
veg_note = "無渣飲食已將蔬菜降為0份。" if residue_type == "無渣飲食 (腸道術後/完全清空/嚴禁乳品)" else "一份生重100g。限鉀個案切記配合右側 HACCP 進行切後汆燙去鉀！"
fruit_note = "無渣飲食已將水果降為0份。" if residue_type == "無渣飲食 (腸道術後/完全清空/嚴禁乳品)" else "一份約100g。糖腎、CKD、HD、CAPD必須控管在2份內並避開高鉀高糖地雷。"
milk_note = "已強制關閉乳品類，消除酪蛋白凝乳殘渣包袱！" if milk_servings == 0 else f"1份等於240ml。當前選用：{milk_type}"

food_groups_data = {
    "六大類食物名稱": ["全穀雜糧類", "豆魚蛋肉類", "乳品類", "蔬菜類", "水果類", "油脂與堅果種子類"],
    "每日精準總份數": [f"{grain_servings:.1f} 份", f"{meat_servings:.1f} 份", f"{milk_servings:.1f} 份", f"{veg_servings:.1f} 份", f"{fruit_servings:.1f} 份", f"{fat_servings:.1f} 份"],
    "臨床生重與品項精確指引": [grain_note, f"搭配目前設定，1份相當於：{meat_ref}。低渣/無渣個案嚴禁油炸與帶筋老肉！", milk_note, veg_note, fruit_note, f"約 {fat_servings*5:.1f} 克烹調油。低渣/無渣飲食者嚴禁整粒堅果，避免顆粒摩擦腸壁！"]
}
st.dataframe(pd.DataFrame(food_groups_data), use_container_width=True)

# 餐次分配表格
st.markdown("### ⏰ 每餐次六大類食物份數全自動配對表")
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

# ==================== HACCP 台灣季節食材成本交互控制面板 ====================
st.markdown("---")
st.subheader(f"🏥 供膳供應管理：{taiwan_season} 食材庫與 HACCP 🚨CCP 管制點對齊")
st.write("針對目前勾選的採購季節，系統自動篩選出台灣在地易取得時蔬、成本分析與高危重症 HACCP 監測重點：")

season_veg_data = VEG_TAIWAN_DB[taiwan_season]
veg_rows = []
for veg in season_veg_data:
    ccp_text = veg["ccp"]
    # 🚀 補回血鉀 > 5.1 時的動態 CCP 暴力升級控制
    if lab_k > 5.1 and "需汆燙" in veg["potassium"]:
        ccp_text = f"🔴 核心緊急臨界點！個案當前血鉀高達 {lab_k}，本時蔬必須由廚工強迫延長汆燙至 5 分鐘，瀝汁必須 100% 倒掉，嚴防病床心臟停搏反應！"
        
    veg_rows.append({
        "台灣在地推薦時蔬": veg["name"],
        "鉀離子風險分級": veg["potassium"],
        "團膳採購成本分析": veg["cost_pkg"],
        "🚨 HACCP 關鍵管制點 (CCP) 臨床指導方針": ccp_text
    })
st.dataframe(pd.DataFrame(veg_rows), use_container_width=True)

# 🚀 補回自動化產出 PES 診斷報告
st.markdown("---")
st.subheader("📋 臨床自動化 NCP 營養診斷報告 (PES Statement)")
if lab_alb < 3.0:
    st.code(f"【營養診斷】蛋白質能量攝取不足 (Problem) r/t 臨床發炎應激與食慾不振 (Etiology) e/b 血清白蛋白急性低下至 {lab_alb} g/dL 與體重流失 (Signs/Symptoms)")
elif lab_k > 5.1:
    st.code(f"【營養診斷】電解質排泄與攝取過剩異常 (Problem) r/t 腎臟過濾廓清率下降與藥物交互作用 (Etiology) e/b 臨床血清鉀高達 {lab_k} mEq/L 之高血鉀表徵 (Signs/Symptoms)")
else:
    st.code("【營養診斷】目前生化常數未達急性臨界點，維持個體化精準預算膳食支持干預。")
