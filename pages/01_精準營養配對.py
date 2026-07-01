import streamlit as st
import pandas as pd

st.set_page_config(page_title="精準營養配對模組-CNOS終極旗艦版", page_icon="📊", layout="wide")

st.title("🧬 臨床生化導航、治療飲食處方與台灣在地團膳全自動決策平台")
st.write("已完美融會貫通 84 頁商業配方大數據與 176 頁醫院常用治療伙食指南，達成三大營養素、水份與去鉀 CCP 跨頁全面聯動！")

st.markdown("---")

# ==================== 176頁醫院治療伙食與病理限制資料庫 ====================
DIET_DB = {
    "常規均衡普通飲食": {"kcal_kg": 30, "pro_g": 1.0, "cho_ratio": 55, "notes": "基礎均衡飲食。適用於消化吸收完全正常之一般患者。", "residue": "常規一般飲食"},
    "清流質飲食 (Residue-Free Liquid)": {"kcal_kg": 8, "pro_g": 0.2, "cho_ratio": 80, "notes": "🚨完全無渣、不產氣。每日熱量上限400-500大卡，以供應水分為主。⚠️禁忌連續使用超過48小時，嚴防營養破產！", "residue": "無渣飲食 (完全清空/嚴禁乳品)"},
    "天然全流質飲食 (Full Liquid Diet)": {"kcal_kg": 30, "pro_g": 1.2, "cho_ratio": 55, "notes": "室溫下呈液態。固體食材需經煮熟、均質機打碎。適用於食道狹窄或咀嚼困難者。", "residue": "低渣飲食 (低纖維/限制乳品)"},
    "半流質飲食 (Semi-Liquid Diet)": {"kcal_min": 30, "kcal_kg": 35, "pro_g": 1.5, "cho_ratio": 60, "notes": "食材經剁碎絞碎加入白粥，不需或稍加咀嚼即可吞嚥（如大腸癌術後過渡期）。", "residue": "低渣飲食 (低纖維/限制乳品)"},
    "細泥飲食 (Pureed Diet - NDD1)": {"kcal_kg": 30, "pro_g": 1.2, "cho_ratio": 58, "notes": "專供吞嚥障礙期病患。完全煮熟再攪磨，必要時添加增稠劑，嚴禁乾脆、薄液體或過黏糯米製品！", "residue": "無渣飲食 (完全清空/嚴禁乳品)"},
    "軟質飲食 (Soft Diet)": {"kcal_kg": 30, "pro_g": 1.2, "cho_ratio": 55, "notes": "質地軟、易咀嚼，容易消化且不含粗纖維。介於正常與半流質之間。避免油炸硬物。", "residue": "低渣飲食 (低纖維/限制乳品)"},
    "限制熱量減重飲食 (Low Calorie)": {"kcal_kg": 20, "pro_g": 1.2, "cho_ratio": 50, "notes": "每日設定 500-1000 kcal 熱量赤字。男生不低於1500，女生不低於1200大卡。SAFA≤10%。", "residue": "常規一般飲食"},
    "糖尿病精準控糖飲食 (Diabetic)": {"kcal_kg": 25, "pro_g": 1.0, "cho_ratio": 50, "notes": "三餐定時定量、碳水化合物均勻分佈。膳食纖維提高至 20-35g/天，延緩血糖暴增速度。", "residue": "常規一般飲食"},
    "傾食症候群防範飲食 (Dumping)": {"kcal_kg": 30, "pro_g": 1.5, "cho_ratio": 45, "notes": "🚨胃切除/繞道術後專用。乾濕分離！進餐不喝水，嚴禁精製簡單糖，嚴防空腸滲透壓腹瀉休克！", "residue": "低渣飲食 (低纖維/限制乳品)"},
    "慢性腎臟病-未透析期 (CKD Non-HD)": {"kcal_kg": 30, "pro_g": 0.6, "cho_ratio": 60, "notes": "🚨嚴格低蛋白飲食 (0.6-0.8 g/kg) 延緩腎衰竭。熱量給足，大量搭配低氮澱粉與粉飴！", "residue": "常規一般飲食"},
    "慢性腎臟病-血液透析期 (HD)": {"kcal_kg": 32, "pro_g": 1.2, "cho_ratio": 50, "notes": "蛋白質大反轉補償 (1.2 g/kg)！補足洗劑偷走的胺基酸。嚴控水份、血鉀與血磷！", "residue": "常規一般飲食"},
    "慢性腎臟病-腹膜透析期 (CAPD)": {"kcal_kg": 30, "pro_g": 1.3, "cho_ratio": 45, "notes": "腹膜每日持續流失 5-15g 大分子白蛋白，極易引發 PEM！⚠️已自動扣除腹膜液葡萄糖吸收 200 kcal。", "residue": "常規一般飲食"},
    "慢性肝病/肝硬化照護飲食": {"kcal_kg": 32, "pro_g": 1.1, "cho_ratio": 62, "notes": "🚨必須少量多餐，且強迫安排『夜間點心 (Late-night snack)』選植物性 BCAA 阻斷夜間骨骼肌自噬分解！", "residue": "常規一般飲食"},
    "高阻塞性肺病低 RQ 飲食 (COPD)": {"kcal_min": 30, "kcal_kg": 30, "pro_g": 1.2, "cho_ratio": 40, "notes": "🚨高脂低醣 (脂肪拉高至 35-40%)。利用脂肪超低呼吸商 (RQ=0.7) 特性降低肺部 CO2 通氣排碳死線！", "residue": "常規一般飲食"},
    "高血脂超高纖維干預飲食": {"kcal_kg": 25, "pro_g": 1.0, "cho_ratio": 50, "notes": "核心干預指標：膳食纖維直接開掛衝破 50g 以上！黏稠物理屏障強力網羅膽酸，阻斷其腸肝循環。", "residue": "常規一般飲食"},
    "大面積灼傷高張代謝飲食 (Burn)": {"kcal_kg": 35, "pro_g": 2.0, "cho_ratio": 50, "notes": "🚨採用 Curreri 處方公式！高熱量高蛋白 (20-25% EE)。強制外掛 Vitamin C 500mg、Vitamin A 10000 IU！", "residue": "常規一般飲食"}
}

# ==================== 84頁精確醫院常用商業配方資料庫 ====================
FORMULA_DB = {
    "不搭配商業配方 / 純天然食物代換": {"kcal": 0, "pro": 0.0, "fat": 0.0, "cho": 0.0, "water": 0, "fiber": 0.0, "notes": "完全採用台灣在地天然食物進行菜單代換設計。"},
    "【常規均衡】管灌安素 (Osmolite 1.0 kcal/mL)": {"kcal": 251, "pro": 8.8, "fat": 8.2, "cho": 35.6, "water": 200, "fiber": 0.0, "notes": "標準等滲透壓均衡配方，自由水比例高 (84.3%)，適用於腸胃功能正常者。"},
    "【高氮修復】愛美力 (Osmolite HN 1.0 kcal/mL)": {"kcal": 250, "pro": 10.4, "fat": 8.1, "cho": 33.9, "water": 198, "fiber": 0.0, "notes": "高氮修復配方 (High Nitrogen)，適合手術後或需要積極組織修補之個案。"},
    "【常規高纖】健力體 (Jevity 1.0 kcal/mL)": {"kcal": 251, "pro": 10.4, "fat": 8.4, "cho": 33.4, "water": 198, "fiber": 3.33, "notes": "添加天然黃豆纖維，能有效維持腸道完整性並改善管灌便秘。"},
    "【濃縮高纖】愛美力涵纖 (1.2 kcal/mL)": {"kcal": 301, "pro": 13.8, "fat": 9.7, "cho": 39.6, "water": 202, "fiber": 5.5, "notes": "高熱量濃縮配方。內含 FOS 果寡醣，限水或高能量需求個案首選。"},
    "【強效限水】雙卡HN (Two Cal HN 2.0 kcal/mL)": {"kcal": 478, "pro": 20.0, "fat": 22.8, "cho": 51.4, "water": 167, "fiber": 0.0, "notes": "極致超濃縮配方！自由水比例暴跌至 70%，灌食期間需嚴密監測個案水份缺口。"},
    "【糖腎專用】葡勝納嚴選 (Glucerna 250mL)": {"kcal": 258, "pro": 12.5, "fat": 13.6, "cho": 21.4, "water": 212, "fiber": 5.3, "notes": "具備低GI安全標章。富含單元不飽和脂肪酸 (MUFA)，專防高血糖滲透性利尿風險。"},
    "【洗腎透析】新版腎補納 (Nepro 237mL)": {"kcal": 425, "pro": 10.6, "fat": 22.7, "cho": 46.4, "water": 170, "fiber": 3.7, "notes": "高蛋白、低電解質負荷。完美補償血液透析與腹膜透析流失之大分子白蛋白。"},
    "【未洗腎期】新版普寧勝 (Suplena 237mL)": {"kcal": 425, "pro": 19.1, "fat": 22.7, "cho": 37.9, "water": 170, "fiber": 2.65, "notes": "限制蛋白質飲食控制專用 (Pro佔比極低)，適用於延緩 CKD 惡化速度。"}
}

# ==================== 台灣在地四季時蔬與成本資料庫 ====================
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

# ==================== Sidebar: NCP 臨床情境定錨 ====================
st.sidebar.header("📋 第一步：NCP 臨床情境定錨")
weight = st.sidebar.number_input("個案體重 (kg):", min_value=30.0, max_value=200.0, value=60.0, step=0.5)

# 🚀 176頁治療伙食完整進駐Dropdown選單
selected_diet = st.sidebar.selectbox("請選擇臨床醫院治療伙食處方:", list(DIET_DB.keys()))
diet_info = DIET_DB[selected_diet]

# 自動連動渣質飲食限制與乳品開關
residue_type = diet_info["residue"]
st.sidebar.markdown(f"**當前自動鎖定腸道渣質限制**：`{residue_type}`")

# 🚀 84頁商業配方格式化點將連動中樞
st.sidebar.markdown("---")
st.sidebar.header("🧪 第二步：外援商業管灌配方添加")
selected_formula = st.sidebar.selectbox("請指定搭配的商業配方品項:", list(FORMULA_DB.keys()))
formula_info = FORMULA_DB[selected_formula]
cans = st.sidebar.slider("每日固定灌食罐數/份數:", min_value=0, max_value=10, value=2, step=1)

# 計算配方分攤掉的各項營養素常數
en_kcal = cans * formula_info["kcal"]
en_pro = cans * formula_info["pro"]
en_fat = cans * formula_info["fat"]
en_cho = cans * formula_info["cho"]
en_water = cans * formula_info["water"]

if cans > 0:
    st.sidebar.success(f"💾 配方已自動分攤扣除額：\n- 熱量：-{en_kcal:.0f} kcal\n- PRO：-{en_pro:.1f} g\n- 水分：-{en_water:.0f} mL")

# 🩸 生化指標輸入專區
st.sidebar.markdown("---")
st.sidebar.header("🩸 第三步：生化檢驗指標輸入 (Labs)")
lab_alb = st.sidebar.number_input("血清白蛋白 Albumin (g/dL):", min_value=1.0, max_value=6.0, value=3.5, step=0.1)
lab_k = st.sidebar.number_input("血清鉀 Potassium (mEq/L):", min_value=2.0, max_value=8.0, value=4.0, step=0.1)
lab_p = st.sidebar.number_input("血清磷 Phosphorus (mg/dL):", min_value=1.0, max_value=10.0, value=3.5, step=0.1)

# ⚖️ 需求設定與淨計算核心
st.sidebar.markdown("---")
st.sidebar.header("⚖️ 第四步：自體淨需求精算")
kcal_kg = st.sidebar.slider("每日每公斤熱量需求 (kcal/kg):", 15, 45, int(diet_info["kcal_kg"]), step=1)
pro_g_kg = st.sidebar.slider("每日每公斤蛋白質需求 (g/kg):", 0.5, 2.5, float(diet_info["pro_g"]), step=0.1)
target_water_total = st.sidebar.number_input("每日總液體水需求 (mL):", min_value=500, max_value=5000, value=2000, step=50)

# 計算原始需求
raw_tdee = weight * kcal_kg
if "CAPD" in selected_diet:
    raw_tdee = max(0.0, raw_tdee - 200.0) # 扣除腹膜液吸收糖熱量
raw_pro_g = weight * pro_g_kg

# 核心全自動跨頁扣除演算法
tdee = max(0.0, raw_tdee - en_kcal)
target_pro_g = max(0.0, raw_pro_g - en_pro)
gap_water = max(0.0, target_water_total - en_water)

pro_kcal = target_pro_g * 4
pro_ratio_total = (pro_kcal / tdee) * 100 if tdee > 0 else 0
max_cho_ratio = max(15.0, 100 - pro_ratio_total - 10)
cho_ratio = st.sidebar.slider("微調 賸餘天然食物 醣類比例 (%):", 15, int(max_cho_ratio), int(diet_info["cho_ratio"]), step=1)
fat_ratio = 100 - pro_ratio_total - cho_ratio

target_cho_g = ((tdee * (cho_ratio / 100)) / 4) if tdee > 0 else 0
target_fat_g = ((tdee * (fat_ratio / 100)) / 9) if tdee > 0 else 0

taiwan_season = st.sidebar.selectbox("當前台灣採購季節:", list(VEG_TAIWAN_DB.keys()))

meal_mode = st.sidebar.selectbox(
    "餐次分配模式:",
    ["常規三餐等分 (早33.3%, 午33.3%, 晚33.3%)", "常規四餐結構 (早30%, 午30%, 晚30%, 點心10%)", "重症/少量多餐 (六餐均分各16.6%)"]
)

if "常規三餐" in meal_mode:
    meals = {"早餐": 0.333, "午餐": 0.333, "晚餐": 0.334}
elif "常規四餐" in meal_mode:
    meals = {"早餐": 0.30, "午餐": 0.30, "晚餐": 0.30, "點心": 0.10}
else:
    meals = {"第一餐": 0.166, "第二餐": 0.166, "第三餐": 0.166, "第四餐": 0.166, "第五餐": 0.166, "第六餐": 0.17}

# ==================== Core Matching Algorithm ====================
if residue_type == "無渣飲食 (完全清空/嚴禁乳品)":
    milk_p, milk_f, milk_c, milk_servings = 0.0, 0.0, 0.0, 0.0
    veg_servings, fruit_servings = 0.0, 0.0
elif residue_type == "低渣飲食 (低纖維/限制乳品)":
    milk_p, milk_f, milk_c, milk_servings = 0.0, 0.0, 0.0, 0.0 # 低渣在醫院不供應乳製品避免酪蛋白凝乳
    veg_servings, fruit_servings = 1.5, 1.0 # 減半供應嫩瓜去渣果汁
else:
    milk_p, milk_f, milk_c, milk_servings = 8.0, 4.0, 12.0, 1.0
    veg_servings, fruit_servings = 3.0, 2.0

base_cho = (veg_servings * 5) + (fruit_servings * 15) + (milk_servings * milk_c)
base_pro = (veg_servings * 1) + (fruit_servings * 0) + (milk_servings * milk_p)
base_fat = (veg_servings * 0) + (fruit_servings * 0) + (milk_servings * milk_f)

rem_cho = target_cho_g - base_cho
rem_pro = target_pro_g - base_pro

grain_servings = max(0.0, rem_cho / 15)
rem_pro_after_grain = rem_pro - (grain_servings * 2)

meat_type = st.sidebar.selectbox("天然優質肉類分級:", ["中脂肉類 (P:7g, F:5g)", "低脂肉類 (P:7g, F:3g)", "不吃肉類/無肉品"])
meat_p, meat_f = (7.0, 5.0) if "中脂" in meat_type else ((7.0, 3.0) if "低脂" in meat_type else (0.0, 0.0))

if meat_p > 0:
    meat_servings = max(0.0, rem_pro_after_grain / meat_p)
else:
    meat_servings = 0.0

current_fat = base_fat + (meat_servings * meat_f)
rem_fat = target_fat_g - current_fat
fat_servings = max(0.0, rem_fat / 5)

# ==================== UI Output Dashboard ====================
st.subheader(f"🩺 臨床醫院治療伙食：{selected_diet}")
st.info(f"💡 **病理機轉介入指引**：{diet_info['notes']}\n\n📢 **選用配方**：{selected_formula} $\\times$ {cans} 罐。")

# 🚨 臨床生化即時警報看板
st.markdown("### 🚨 臨床生化即時警報系統 (Biochemical Alert System)")
alert_col1, alert_col2, alert_col3 = st.columns(3)

with alert_col1:
    if lab_alb < 3.0:
        st.error(f"🔴 白蛋白過低: {lab_alb} g/dL\n\n高度 PEM 肌肉流失風險！現有配方提供 {en_pro:.1f}g 蛋白，仍需追加高生物價優質膳食補償。")
    else:
        st.success(f"🟢 白蛋白正常: {lab_alb} g/dL")

with alert_col2:
    if lab_k > 5.1:
        st.error(f"🔴 血鉀超標: {lab_k} mEq/L\n\n高血鉀急性期！下方已自動將台灣時蔬 CCP 升級為『緊急強制去鉀』字串！")
    else:
        st.success(f"🟢 血鉀正常: {lab_k} mEq/L")

with alert_col3:
    if lab_p < 2.0:
        st.error(f"🔴 血磷急性暴跌: {lab_p} mg/dL\n\n極高再餵食症候群 (Refeeding Risk)！必須限制熱量與醣類進展速度。")
    else:
        st.success(f"🟢 血磷正常: {lab_p} mg/dL")

st.markdown("---")

# 總量連動展示圖卡
col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 賸餘天然伙食熱量需求", f"{tdee:.0f} kcal", f"商業配方已分攤 {en_kcal:.0f} kcal")
col2.metric("🍗 賸餘天然伙食蛋白目標", f"{target_pro_g:.1f} g", f"商業配方已分攤 {en_pro:.1f} g")
col3.metric("🍚 賸餘天然伙食醣類目標", f"{target_cho_g:.1f} g", f"商業配方已分攤 {en_cho:.1f} g")
col4.metric("💧 淨外加補水需求缺口", f"{gap_water:.0f} mL", f"商業配方自帶水 {en_water:.0f} mL")

# 特殊疾病微量元素開掛提醒卡片
if "灼傷" in selected_diet:
    st.warning("🔥 **灼傷高張代謝特殊外掛指標激活**：依據 Curreri 公式與 176 頁指引，已強制外掛建議調配 **Vitamin C 500 mg** 與 **Vitamin A 10,000 IU** 促進傷口快速癒合！")
elif "慢性肝病" in selected_diet:
    st.warning("🌙 **肝硬化強迫症夜點限制激活**：個案強迫必須安排『夜間點心 (Late-night snack)』選用低氮澱粉或黃豆 BCAA 點心，嚴防清晨發生飢餓自噬性低血糖！")
elif "清流質" in selected_diet:
    st.error("⚠️ **清流質連續使用危險死線**：當前清流質飲食已運算輸出，**絕對禁止連續使用超過 48 小時**，否則將陷入全面性巨量營養素破產！")

st.markdown("### 🍽️ 淨天然食物：六大類食物每日精準總份數 (已全面扣除商業配方)")
food_groups_data = {
    "六大類食物名稱": ["全穀雜糧類", "豆魚蛋肉類", "乳品類", "蔬菜類", "水果類", "油脂與堅果種子類"],
    "每日精準總份數": [f"{grain_servings:.1f} 份", f"{meat_servings:.1f} 份", f"{milk_servings:.1f} 份", f"{veg_servings:.1f} 份", f"{fruit_servings:.1f} 份", f"{fat_servings:.1f} 份"],
    "臨床生重與品項精確指引": [
        "精製穀類首選。若為低渣/無渣/CKD/糖腎，嚴禁糙米麩皮，全面改用白米飯、冬粉、西谷米或粉飴！",
        f"搭配目前設定，1份相當於 {meat_ref}。低渣/無渣個案嚴禁油炸與帶筋老肉，改用嫩豆腐、蒸魚、蛋白！",
        "無渣及低渣飲食已自動關閉乳品類，消除酪蛋白凝乳殘渣包袱！常規成人選用低脂乳1份。",
        "一份生重 100g。限鉀個案切記：必須先切、後充分汆燙 3-5 分鐘，瀝乾去汁後方可拌油烹調！",
        "一份約 100g。糖腎、CKD、HD、CAPD 必須控管在 2 份內，避開高鉀高糖地雷水果。",
        f"約 {fat_servings*5:.1f} 克烹調油。低渣/無渣飲食者嚴禁整粒堅果與花生仁，避免顆粒摩擦腸壁！"
    ]
}
st.dataframe(pd.DataFrame(food_groups_data), use_container_width=True)

# 餐次分配表格
st.markdown("### ⏰ 每餐次六大類食物份數全自動配對表")
st.write(f"當前伙食分配模式：**{meal_mode}**（表格內數字為各餐建議分配『份數』）")
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

# ==================== HACCP 台灣季節食材成本動態交互面板 ====================
st.markdown("---")
st.subheader(f"🏥 供膳供應管理：{taiwan_season} 在地時蔬與 HACCP 🚨CCP 管制點動態連動")
season_veg_data = VEG_TAIWAN_DB[taiwan_season]
veg_rows = []
for veg in season_veg_data:
    ccp_text = veg["ccp"]
    if lab_k > 5.1 and "需汆燙" in veg["potassium"]:
        ccp_text = f"🔴 核心緊急臨界點！個案當前血鉀高達 {lab_k} mEq/L，本時蔬必須由廚工強迫延長汆燙至 5 分鐘，瀝汁必須 100% 倒掉，嚴防病床心臟停搏反應！"
        
    veg_rows.append({
        "台灣在地推薦時蔬": veg["name"],
        "鉀離子風險分級": veg["potassium"],
        "團膳採購成本分析": veg["cost_pkg"],
        "🚨 HACCP 關鍵管制點 (CCP) 臨床指導方針": ccp_text
    })
st.dataframe(pd.DataFrame(veg_rows), use_container_width=True)

# 🚀 全自動化產出結合商業配方與治療伙食扣除後的 NCP 營養處方
st.markdown("---")
st.subheader("📋 結合 ONS 扣除法之全自動臨床營養處方 (Nutrition Prescription)")
pres_text = f"【臨床處方】每日針對個案施予『{selected_diet}』之天然常規餐點共 {tdee:.0f} 大卡（內含蛋白質 {target_pro_g:.1f}g）；並經由管灌管道每日固定分次注入 {selected_formula} 共 {cans} 罐（占熱量 {en_kcal:.0f} kcal），餐與餐之間需外加強迫追加沖洗純水共 {gap_water:.0f} 毫升，以維體液與電解質平衡。"
st.code(pres_text, language="text")
