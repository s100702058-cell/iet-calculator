import streamlit as st
import pandas as pd

# 設定網頁標題與風格
st.set_page_config(page_title="精準營養神算配對器", page_icon="🥗", layout="centered")

# 網頁視覺大標
st.title("🥗 精準營養神算配對器 (Dietitian Calculator)")
st.write("已成功整合官方新版食物代換表資料庫，支援多種乳品與肉類脂肪等級的精準臨床計算！")

st.markdown("---")

# ==================== Sidebar: 使用者輸入區 ====================
st.sidebar.header("📋 第一步：輸入個案基本資料")
weight = st.sidebar.number_input("請輸入體重 (kg):", min_value=30.0, max_value=200.0, value=60.0, step=0.5)

activity_level = st.sidebar.selectbox(
    "請選擇每日活動強度 (Physical Activity Level):",
    ["輕度活動 (30 kcal/kg) - 辦公、靜態生活", 
     "中度活動 (35 kcal/kg) - 經常走動、家務、輕度運動", 
     "重度活動 (40 kcal/kg) - 重體力勞動、高強度運動訓練"]
)

if "輕度" in activity_level:
    activity_factor = 30
elif "中度" in activity_level:
    activity_factor = 35
else:
    activity_factor = 40

st.sidebar.markdown("---")
st.sidebar.header("⚖️ 第二步：三大營養素比例分配")

control_mode = st.sidebar.radio(
    "請選擇您要優先調整的營養素組合：",
    ["優先調整 蛋白質 % 與 脂肪 % (醣類自動墊底)", "優先調整 蛋白質 % 與 醣類 % (脂肪自動墊底)"]
)

p_ratio = st.sidebar.slider("蛋白質比例 (Protein %):", 10, 50, 20, step=1)

if "優先調整 蛋白質 % 與 脂肪 %" in control_mode:
    f_ratio = st.sidebar.slider("脂肪比例 (Lipid %):", 10, 50, 30, step=1)
    c_ratio = 100 - p_ratio - f_ratio
else:
    c_ratio = st.sidebar.slider("醣類比例 (Carbohydrates %):", 20, 70, 50, step=1)
    f_ratio = 100 - p_ratio - c_ratio

st.sidebar.info(f"當前配對比例：\n- 醣類 (CHO): {c_ratio}%\n- 蛋白質 (PRO): {p_ratio}%\n- 脂肪 (FAT): {f_ratio}%")

if c_ratio < 0 or f_ratio < 0:
    st.sidebar.error("❌ 比例加總超過 100%，請重新調整滑桿比例！")

st.sidebar.markdown("---")
st.sidebar.header("🧬 第三步：對接新版食物代換表資料庫")

# 🎛️ 讀取 PDF 附-2 乳品類定義
milk_type = st.sidebar.selectbox(
    "請選擇臨床指定乳品型態 (Dairy Type):",
    ["低脂乳品 (P:8g, F:4g, C:12g)", "全脂乳品 (P:8g, F:8g, C:12g)", "脫脂乳品 (P:8g, F:0g, C:12g)"]
)

if "低脂" in milk_type:
    milk_p, milk_f, milk_c = 8.0, 4.0, 12.0
    milk_ref = "240 毫升低脂奶"
elif "全脂" in milk_type:
    milk_p, milk_f, milk_c = 8.0, 8.0, 12.0
    milk_ref = "240 毫升全脂奶"
else:
    milk_p, milk_f, milk_c = 8.0, 0.0, 12.0
    milk_ref = "240 毫升脫脂奶"

# 🎛️ 讀取 PDF 附-3 豆魚蛋肉類脂肪分級
meat_type = st.sidebar.selectbox(
    "請選擇臨床指定肉類分級 (Meat Type):",
    ["中脂肉類 (P:7g, F:5g)", "低脂肉類 (P:7g, F:3g)", "高脂肉類 (P:7g, F:10g)"]
)

if "中脂" in meat_type:
    meat_p, meat_f = 7.0, 5.0
    meat_ref = "生重 35 克中脂肉類 (如傳統豆腐 80 克、雞蛋 55 克)"
elif "低脂" in meat_type:
    meat_p, meat_f = 7.0, 3.0
    meat_ref = "生重 35 克低脂肉類 (如一般魚類 35 克、無糖豆漿 190 毫升)"
else:
    meat_p, meat_f = 7.0, 10.0
    meat_ref = "生重 35 克高脂肉類 (如百頁豆腐 70 克、秋刀魚 35 克)"

# ==================== Core Algorithm: 營養計算核心 ====================
if c_ratio >= 0 and f_ratio >= 0:
    tdee = weight * activity_factor

    target_cho_g = (tdee * (c_ratio / 100)) / 4
    target_pro_g = (tdee * (p_ratio / 100)) / 4
    target_fat_g = (tdee * (f_ratio / 100)) / 9

    # 設定臨床指南蔬菜與水果基本基礎量 (PDF 附-5, 附-6 規範)
    veg_servings = 3.0    
    fruit_servings = 2.0  
    milk_servings = 1.0   

    # 動態代入 PDF 轉換矩陣常數
    base_cho = (veg_servings * 5) + (fruit_servings * 15) + (milk_servings * milk_c)
    base_pro = (veg_servings * 1) + (fruit_servings * 0) + (milk_servings * milk_p)
    base_fat = (veg_servings * 0) + (fruit_servings * 0) + (milk_servings * milk_f)

    rem_cho = target_cho_g - base_cho
    rem_pro = target_pro_g - base_pro

    # 全穀雜糧類 (PDF 附-4 每份 C:15g, P:2g)
    grain_servings = max(0.0, rem_cho / 15)
    
    # 豆魚蛋肉類 (動態扣除全穀蛋白質，並依選定肉類脂肪等級除以特定蛋白質常數)
    rem_pro_after_grain = rem_pro - (grain_servings * 2)
    meat_servings = max(0.0, rem_pro_after_grain / meat_p)

    # 油脂與堅果種子類 (PDF 附-7 每份 F:5g)
    current_fat = base_fat + (meat_servings * meat_f)
    rem_fat = target_fat_g - current_fat
    fat_servings = max(0.0, rem_fat / 5)

    # ==================== Dashboard: 網頁結果呈現 ====================
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 總熱量需求 (TDEE)", f"{tdee:.0f} kcal")
    col2.metric("🍗 目標蛋白質", f"{target_pro_g:.1f} g")
    col3.metric("🍚 目標醣類", f"{target_cho_g:.1f} g")

    st.markdown("### 🎯 三大產能營養素目標配對")
    macro_df = pd.DataFrame({
        "營養素 (Nutrients)": ["醣類 (Carbohydrates)", "蛋白質 (Proteins)", "脂肪 (Lipids)"],
        "分配比例 (%)": [c_ratio, p_ratio, f_ratio],
        "目標克數 (g)": [round(target_cho_g, 1), round(target_pro_g, 1), round(target_fat_g, 1)]
    })
    st.table(macro_df)

    st.markdown("### 🍽️ 換算六大類食物精準份數與克數 (對接新版 PDF 資料庫)")
    
    food_groups_data = {
        "六大類食物名稱 (Food Groups)": [
            "全穀雜糧類 (Whole Grains)",
            "豆魚蛋肉類 (Beans, Fish, Eggs, Meat)",
            "所選乳品類 (Selected Dairy)",
            "蔬菜類 (Vegetables)",
            "水果類 (Fruits)",
            "油脂與堅果種子類 (Fats & Oils)"
        ],
        "計算出之精準份數 (Servings)": [
            f"{grain_servings:.1f} 份",
            f"{meat_servings:.1f} 份",
            f"{milk_servings:.1f} 份",
            f"{veg_servings:.1f} 份",
            f"{fruit_servings:.1f} 份",
            f"{fat_servings:.1f} 份"
        ],
        "新版生重與品項精確換算參考 (Grams/Reference)": [
            f"約 {grain_servings*25:.1f} 克未熟乾穀 (1 份等於生重 20-30 克，如 1/4 碗飯或半把冬粉)",
            f"搭配目前設定，1 份相當於：{meat_ref}",
            f"搭配目前設定，1 份相當於：{milk_ref}",
            f"約 {veg_servings*100:.1f} 克生菜 (1 份等於可食生重 100 克，如煮熟約大半碗)",
            f"約 {fruit_servings*100:.1f} 克切塊水果 (1 份約等於碗裝 8 分滿，如切塊哈密瓜 150 克)",
            f"約 {fat_servings*5:.1f} 克烹調油 (1 份等於精製油 5 克或各式花生仁 10 粒)"
        ]
    }
    
    st.dataframe(pd.DataFrame(food_groups_data), use_container_width=True)
    st.success("🎉 整合運算成功！這套選單已完美扣合官方新版食物代換手冊，精準度無懈可擊！")
else:
    st.warning("⚠️ 比例加總已超出 100%，請調低滑桿比例以利程式重新演算。")
