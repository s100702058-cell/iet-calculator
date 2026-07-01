import streamlit as st
import pandas as pd

st.set_page_config(page_title="精準營養配對模組-CNOS終極版", page_icon="📊", layout="wide")

st.title("📊 臨床生化導航、重症透析與台灣在地團膳整合配對平台")
st.write("本模組已全面打通『商業管灌配方』與『天然食物代換表』之數據主動脈！選擇配方罐數後，系統將自動扣除並重算六大類份數。")

st.markdown("---")

# ==================== 84頁精確醫院常用商業配方資料庫 ====================
FORMULA_DB = {
    "不搭配商業配方 / 純天然食物代換": {
        "kcal": 0, "pro": 0.0, "fat": 0.0, "cho": 0.0, "water": 0, "fiber": 0.0, "notes": "完全採用台灣在地天然六大類食物進行精準菜單代換設計。"
    },
    "【常規均衡】管灌安素 (Osmolite 1.0 kcal/mL)": {
        "kcal": 251, "pro": 8.8, "fat": 8.2, "cho": 35.6, "water": 200, "fiber": 0.0,
        "notes": "標準等滲透壓均衡配方，自由水比例高，適用於腸胃功能正常者。"
    },
    "【高氮修復】愛美力 (Osmolite HN 1.0 kcal/mL)": {
        "kcal": 250, "pro": 10.4, "fat": 8.1, "cho": 33.9, "water": 198, "fiber": 0.0,
        "notes": "高氮修復配方，適合手術後或需要積極組織修補之個案。"
    },
    "【常規高纖】健力體 (Jevity 1.0 kcal/mL)": {
        "kcal": 251, "pro": 10.4, "fat": 8.4, "cho": 33.4, "water": 198, "fiber": 3.33,
        "notes": "添加天然黃豆纖維，能有效維持腸道完整性並改善便秘。"
    },
    "【濃縮高纖】愛美力涵纖 (1.2 kcal/mL)": {
        "kcal": 301, "pro": 13.8, "fat": 9.7, "cho": 39.6, "water": 202, "fiber": 5.5,
        "notes": "高熱量濃縮配方。內含 FOS 果寡醣，限水個案首選。"
    },
    "【強效限水】雙卡HN (Two Cal HN 2.0 kcal/mL)": {
        "kcal": 478, "pro": 20.0, "fat": 22.8, "cho": 51.4, "water": 167, "fiber": 0.0,
        "notes": "極致超濃縮配方！自由水比例低，灌食期間需嚴密監測個案水份缺口。"
    },
    "【糖腎專用】葡勝納嚴選 (Glucerna 250mL)": {
        "kcal": 258, "pro": 12.5, "fat": 13.6, "cho": 21.4, "water": 212, "fiber": 5.3,
        "notes": "具備低GI安全標章。富含單元不飽和脂肪酸 (MUFA)，專防高血糖滲透性利尿風險。"
    },
    "【洗腎透析】新版腎補納 (Nepro 237mL)": {
        "kcal": 425, "pro": 10.6, "fat": 22.7, "cho": 46.4, "water": 170, "fiber": 3.7,
        "notes": "高蛋白、低電解質負荷。補償血液透析與腹膜透析流失之白蛋白。"
    },
    "【未洗腎期】新版普寧勝 (Suplena 237mL)": {
        "kcal": 425, "pro": 19.1, "fat": 22.7, "cho": 37.9, "water": 170, "fiber": 2.65,
        "notes": "限制蛋白質飲食控制專用，適用於延緩 CKD 惡化速度。"
    }
}

# ==================== 疾病、重症與生化指標核心資料庫 ====================
DISEASE_DB = {
    "一般健康成人 (General Adult)": {
        "kcal_min": 25, "kcal_max": 30, "pro_min": 0.8, "pro_max": 1.0, "notes": "維持一般平衡。監測指標：Albumin, FPG, TG, TC。",
        "lab_notes": "📌 常規生化指標：維持基礎代謝與微量元素平衡即可。"
    },
    "慢性腎臟病-未透析 (CKD)": {
        "kcal_min": 30, "kcal_max": 35, "pro_min": 0.6, "pro_max": 0.8, "notes": "嚴格限蛋！蛋白質限制在 0.6-0.8 g/kg 以延緩腎衰竭。熱量需給足。監測指標：BUN, Cr, eGFR, K, P。",
        "lab_notes": "🚨 關鍵生化指標：密切監測血清鉀與磷！蔬菜必須切後充分汆燙 3-5 分鐘以阻斷高血鉀心臟風險。"
    },
    "糖尿病腎病變 (Diabetic Nephropathy, DN)": {
        "kcal_min": 25, "kcal_max": 30, "pro_min": 0.8, "pro_max": 0.8, "notes": "控糖限蛋極致！蛋白質定錨 0.8 g/kg 延緩腎絲球硬化。醣類必須精準均分。監測指標：HbA1c, FPG, UACR, eGFR。",
        "lab_notes": "🚨 關鍵生化指標：注意 UACR 微量白蛋白尿！防範血管內皮二次高壓受損。"
    },
    "慢性腎臟病-血液透析階段 (HD)": {
        "kcal_min": 30, "kcal_max": 35, "pro_min": 1.2, "pro_max": 1.4, "notes": "高補償優質蛋白！透析流失大量胺基酸，蛋白質大幅拉高至 1.2-1.4 g/kg。監測指標：iPTH, K, P, Ca, Albumin, Hb。",
        "lab_notes": "🚨 關鍵生化指標：嚴控兩次透析間水份（體重增加<5%）。"
    },
    "慢性腎臟病-腹膜透析階段 (CAPD)": {
        "kcal_min": 30, "kcal_max": 35, "pro_min": 1.2, "pro_max": 1.5, "notes": "持續性白蛋白流失補償！需求拉高至 1.2-1.5 g/kg。⚠️已自動扣除腹膜吸收之葡萄糖熱量 (約200 kcal/日)。監測指標：Albumin, TG, TC, K, P。",
        "lab_notes": "🚨 關鍵生化指標：腹膜每日流失 5-15g 蛋白質，極易湧發 PEM 風險。"
    }
}

VEG_TAIWAN_DB = {
    "春夏季盛產時蔬 (低成本/高優質)": [
        {"name": "台灣空心菜", "potassium": "高鉀 (需汆燙)", "cost_pkg": "低 (約 30-40 元/kg)", "ccp": "🚨 CCP 備料點：必須先切、充分汆燙 3 分鐘、去汁液方可烹調，阻斷高血鉀風暴。"},
        {"name": "在地澎湖絲瓜", "potassium": "中/低鉀 (去皮)", "cost_pkg": "低 (約 35-45 元/kg)", "ccp": "適合低渣/無渣過渡期飲食，去皮去籽質地極軟，腸道零負擔。"}
    ],
    "秋冬季盛產時蔬 (低成本/高優質)": [
        {"name": "高山初秋高麗菜", "potassium": "低/中鉀", "cost_pkg": "極低 (約 20-30 元/kg)", "ccp": "團膳成本控制神物！質地爽脆，低渣飲食者需徹底煮至熟爛方可使用。"},
        {"name": "在地優質白蘿蔔", "potassium": "低鉀 (透析首選)", "cost_pkg": "低 (約 25-35 元/kg)", "ccp": "鉀離子極低，HD/CAPD 與糖尿病腎病變病患的最佳餐盤安全墊底食材。"}
    ]
}

# ==================== Sidebar: NCP 臨床評估與連動輸入 ====================
st.sidebar.header("📋 第一步：NCP 個案基礎定錨")
weight = st.sidebar.number_input("個案體重 (kg):", min_value=30.0, max_value=200.0, value=60.0, step=0.5)

selected_disease = st.sidebar.selectbox("請選擇臨床情境/目標疾病:", list(DISEASE_DB.keys()))
disease_info = DISEASE_DB[selected_disease]

residue_type = st.sidebar.radio("腸道渣質限制:", ["常規一般飲食", "低渣飲食 (低纖維/限制乳品)", "無渣飲食 (腸道術後/完全清空/嚴禁乳品)"])

# 🚀 核心大改版：直接在左側置入『商業配方格式化連動中樞』
st.sidebar.markdown("---")
st.sidebar.header("🧪 第二步：商業管灌配方添加 (連動核心)")
selected_formula = st.sidebar.selectbox("請指定調配的商業配方品項:", list(FORMULA_DB.keys()))
formula_info = FORMULA_DB[selected_formula]

cans = st.sidebar.slider("每日固定灌食罐數/份數:", min_value=0, max_value=10, value=2, step=1)

# 計算配方帶入的各項營養素常數
en_kcal = cans * formula_info["kcal"]
en_pro = cans * formula_info["pro"]
en_fat = cans * formula_info["fat"]
en_cho = cans * formula_info["cho"]
en_water = cans * formula_info["water"]

if cans > 0:
    st.sidebar.success(f"💾 商業配方已鎖定扣除額：\n- 熱量：-{en_kcal:.0f} kcal\n- PRO：-{en_pro:.1f} g\n- 水分：-{en_water:.0f} mL")

st.sidebar.markdown("---")
st.sidebar.header("🩸 第三步：生化指標輸入 (Labs)")
lab_alb = st.sidebar.number_input("血清白蛋白 Albumin (g/dL):", min_value=1.0, max_value=6.0, value=3.5, step=0.1)
lab_k = st.sidebar.number_input("血清鉀 Potassium (mEq/L):", min_value=2.0, max_value=8.0, value=4.0, step=0.1)
lab_p = st.sidebar.number_input("血清磷 Phosphorus (mg/dL):", min_value=1.0, max_value=10.0, value=3.5, step=0.1)

st.sidebar.markdown("---")
st.sidebar.header("⚖ Cub 需求設定與淨計算")
kcal_kg = st.sidebar.slider("每日每公斤熱量需求 (kcal/kg):", 15, 45, int(disease_info["kcal_max"]), step=1)
pro_g_kg = st.sidebar.slider("每日每公斤蛋白質需求 (g/kg):", 0.5, 2.5, float(disease_info["pro_min"]), step=0.1)
target_water_total = st.sidebar.number_input("每日總液體液體水需求 (mL):", min_value=500, max_value=5000, value=2000, step=50)

# 計算原始需求
raw_tdee = weight * kcal_kg
if "CAPD" in selected_disease:
    raw_tdee = max(0.0, raw_tdee - 200.0) # 扣除腹膜吸收糖熱量
raw_pro_g = weight * pro_g_kg

# 核心全自動扣除：算清賸餘要交給『天然食物代換表』的預算淨額
tdee = max(0.0, raw_tdee - en_kcal)
target_pro_g = max(0.0, raw_pro_g - en_pro)
gap_water = max(0.0, target_water_total - en_water)

pro_kcal = target_pro_g * 4
pro_ratio_total = (pro_kcal / tdee) * 100 if tdee > 0 else 0
max_cho_ratio = max(15.0, 100 - pro_ratio_total - 10)
cho_ratio = st.sidebar.slider("微調 賫餘天然食物 醣類比例 (%):", 15, int(max_cho_ratio), 50, step=1)
fat_ratio = 100 - pro_ratio_total - cho_ratio

target_cho_g = ((tdee * (cho_ratio / 100)) / 4) if tdee > 0 else 0
target_fat_g = ((tdee * (fat_ratio / 100)) / 9) if tdee > 0 else 0

st.sidebar.markdown("---")
st.sidebar.header("🌾 台灣時蔬採購季節")
taiwan_season = st.sidebar.selectbox("當前台灣採購季節:", list(VEG_TAIWAN_DB.keys()))

# ==================== Core Matching Algorithm ====================
if residue_type == "無渣飲食 (腸道術後/完全清空/嚴禁乳品)":
    milk_p, milk_f, milk_c, milk_servings = 0.0, 0.0, 0.0, 0.0
    veg_servings, fruit_servings = 0.0, 0.0
else:
    milk_p, milk_f, milk_c, milk_servings = 8.0, 4.0, 12.0, 1.0 # 預設低脂
    veg_servings, fruit_servings = 3.0, 2.0

# 扣除基本蔬果奶後的剩餘量
base_cho = (veg_servings * 5) + (fruit_servings * 15) + (milk_servings * milk_c)
base_pro = (veg_servings * 1) + (fruit_servings * 0) + (milk_servings * milk_p)
base_fat = (veg_servings * 0) + (fruit_servings * 0) + (milk_servings * milk_f)

rem_cho = target_cho_g - base_cho
rem_pro = target_pro_g - base_pro

grain_servings = max(0.0, rem_cho / 15)
rem_pro_after_grain = rem_pro - (grain_servings * 2)

meat_type = st.sidebar.selectbox("天然肉類分級選擇:", ["中脂肉類 (P:7g, F:5g)", "低脂肉類 (P:7g, F:3g)", "不吃肉類/無肉品"])
meat_p, meat_f = (7.0, 5.0) if "中脂" in meat_type else ((7.0, 3.0) if "低脂" in meat_type else (0.0, 0.0))

if meat_p > 0:
    meat_servings = max(0.0, rem_pro_after_grain / meat_p)
else:
    meat_servings = 0.0

current_fat = base_fat + (meat_servings * meat_f)
rem_fat = target_fat_g - current_fat
fat_servings = max(0.0, rem_fat / 5)

# ==================== UI Output Dashboard ====================
st.subheader(f"🩺 臨床診斷：{selected_disease} (當前選用：{selected_formula} $\\times$ {cans} 罐)")
st.info(f"💡 **臨床介入核心指引**：{disease_info['notes']}\n\n📢 **生化評估導航提示**：{disease_info['lab_notes']}")

# 🚨 臨床生化即時警報看板
st.markdown("### 🚨 臨床生化即時警報系統 (Biochemical Alert System)")
alert_col1, alert_col2, alert_col3 = st.columns(3)

with alert_col1:
    if lab_alb < 3.0:
        st.error(f"🔴 白蛋白過低: {lab_alb} g/dL\n\n高度 PEM 風險！現有商業配方注入量 {en_pro:.1f}g，仍建議拉高優質蛋白配比。")
    else:
        st.success(f"🟢 白蛋白正常: {lab_alb} g/dL")

with alert_col2:
    if lab_k > 5.1:
        st.error(f"🔴 血鉀超標: {lab_k} mEq/L\n\n高血鉀急性期！下方已自動將台灣時蔬 CCP 升級為緊急強制去鉀字串！")
    else:
        st.success(f"🟢 血鉀正常: {lab_k} mEq/L")

with alert_col3:
    if lab_p < 2.0:
        st.error(f"🔴 血磷急性暴跌: {lab_p} mg/dL\n\n極高再餵食症候群 (Refeeding Risk)！左側商業配方罐數請先採取滋養灌食 (Trophic feeding) 策略。")
    else:
        st.success(f"🟢 血磷正常: {lab_p} mg/dL")

st.markdown("---")

# 總量連動展示圖卡
col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 賸餘天然食物熱量需求", f"{tdee:.0f} kcal", f"配方已分攤 {en_kcal:.0f} kcal")
col2.metric("🍗 賸餘天然食物蛋白目標", f"{target_pro_g:.1f} g", f"配方已分攤 {en_pro:.1f} g")
col3.metric("🍚 賸餘天然食物醣類目標", f"{target_cho_g:.1f} g", f"配方已分攤 {en_cho:.1f} g")
col4.metric("💧 淨外加補水需求缺口", f"{gap_water:.0f} mL", f"配方自帶水 {en_water:.0f} mL")

st.markdown("### 🍽️ 淨天然食物：六大類食物每日精準總份數 (已扣除商業配方)")
food_groups_data = {
    "六大類食物名稱": ["全穀雜糧類", "豆魚蛋肉類", "乳品類", "蔬菜類", "水果類", "油脂與堅果種子類"],
    "每日精準總份數": [f"{grain_servings:.1f} 份", f"{meat_servings:.1f} 份", f"{milk_servings:.1f} 份", f"{veg_servings:.1f} 份", f"{fruit_servings:.1f} 份", f"{fat_servings:.1f} 份"],
    "臨床生重與品項精確指引": [
        "禁止糙米，改用白米飯、冬粉或西谷米！若是CKD或糖腎限蛋白，多利用粉飴與冬粉！",
        f"搭配目前設定，1份相當於 35 克生肉。若商業配方已佔滿蛋白配額，此處份數會自動歸零，嚴防超標！",
        "無渣飲食已強制關閉。常規使用 1 份低脂乳 (240ml) 補足基本維生素與鈣質受體。",
        "一份生重 100g。限鉀個案切記配合右側 HACCP 進行切後充分汆燙 3-5 分鐘去鉀！",
        "一份約 100g。糖腎、CKD、HD、CAPD 必須控管在 2 份內並避開高鉀地雷。",
        f"約 {fat_servings*5:.1f} 克烹調油。低渣/無渣飲食者嚴禁整粒堅果，避免顆粒摩擦腸壁！"
    ]
}
st.dataframe(pd.DataFrame(food_groups_data), use_container_width=True)

# ==================== HACCP 台灣季節食材成本動態交互面板 ====================
st.markdown("---")
st.subheader(f"🏥 供膳供應管理：{taiwan_season} 在地時蔬與 HACCP 🚨CCP 管制點動態連動")
season_veg_data = VEG_TAIWAN_DB[taiwan_season]
veg_rows = []
for veg in season_veg_data:
    ccp_text = veg["ccp"]
    if lab_k > 5.1 and "需汆燙" in veg["potassium"]:
        ccp_text = f"🔴 核心緊急臨界點！個案當前血鉀高達 {lab_k}，本時蔬必須由廚工強迫延長汆燙至 5 分鐘，瀝汁必須 100% 倒掉，嚴防病床心臟停搏反應！"
        
    veg_rows.append({
        "台灣在地推薦時蔬": veg["name"],
        "鉀離子風險分級": veg["potassium"],
        "團膳採購成本分析": veg["cost_pkg"],
        "🚨 HACCP 關鍵管制點 (CCP) 臨床指導方針": ccp_text
    })
st.dataframe(pd.DataFrame(veg_rows), use_container_width=True)

# 🚀 全自動化產出結合商業配方扣除後的 NCP 營養處方
st.markdown("---")
st.subheader("📋 結合 ONS 扣除法之全自動臨床營養處方 (Nutrition Prescription)")
pres_text = f"【臨床處方】每日給予該個案常規天然食物共 {tdee:.0f} 大卡（內含蛋白質 {target_pro_g:.1f}g）；並經由管灌管道每日固定分次注入 {selected_formula} 共 {cans} 罐（占熱量 {en_kcal:.0f} kcal），餐與餐之間需外加強迫追加沖洗純水共 {gap_water:.0f} 毫升，以維體液與電解質平衡。"
st.code(pres_text, language="text")
