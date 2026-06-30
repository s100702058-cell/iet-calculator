import streamlit as st
import pandas as pd

# 設定網頁標題與風格
st.set_page_config(page_title="精準營養神算配對器", page_icon="🥗", layout="centered")

# 網頁視覺大標
st.title("🥗 精準營養神算配對器 (Dietitian Calculator)")
st.write("透過臨床營養學食物交換表演算法，將體重與熱量精準配對至六大類食物克數！")

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

# 解析活動熱量係數
if "輕度" in activity_level:
    activity_factor = 30
elif "中度" in activity_level:
    activity_factor = 35
else:
    activity_factor = 40

st.sidebar.markdown("---")
st.sidebar.header("⚖️ 第二步：三大營養素比例分配")
p_ratio = st.sidebar.slider("蛋白質比例 (Protein %):", 10, 35, 20, step=1)
f_ratio = st.sidebar.slider("脂肪比例 (Lipid %):", 15, 40, 30, step=1)
c_ratio = 100 - p_ratio - f_ratio

st.sidebar.info(f"當前配對比例：\n- 醣類 (CHO): {c_ratio}%\n- 蛋白質 (PRO): {p_ratio}%\n- 脂肪 (FAT): {f_ratio}%")

if c_ratio < 0:
    st.sidebar.error("❌ 比例加總超過 100%，請重新調整蛋白質與脂肪比例！")

# ==================== Core Algorithm: 營養計算核心 ====================
# 1. 計算 TDEE
tdee = weight * activity_factor

# 2. 計算三大營養素目標克數 (Target Grams)
target_cho_g = (tdee * (c_ratio / 100)) / 4
target_pro_g = (tdee * (p_ratio / 100)) / 4
target_fat_g = (tdee * (f_ratio / 100)) / 9

# 3. 食物交換表自動媒合演算法
veg_servings = 3.0    # 蔬菜類基本 3 份
fruit_servings = 2.0  # 水果類基本 2 份
milk_servings = 1.0   # 乳品類(低脂)基本 1 份

base_cho = (veg_servings * 5) + (fruit_servings * 15) + (milk_servings * 12)
base_pro = (veg_servings * 1) + (fruit_servings * 0) + (milk_servings * 8)
base_fat = (veg_servings * 0) + (fruit_servings * 0) + (milk_servings * 4)

rem_cho = target_cho_g - base_cho
rem_pro = target_pro_g - base_pro

grain_servings = max(0.0, rem_cho / 15)
rem_pro_after_grain = rem_pro - (grain_servings * 2)
meat_servings = max(0.0, rem_pro_after_grain / 7)

current_fat = base_fat + (meat_servings * 5)
rem_fat = target_fat_g - current_fat
fat_servings = max(0.0, rem_fat / 5)

# ==================== Dashboard: 網頁結果呈現 ====================
if c_ratio >= 0:
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

    st.markdown("### 🍽️ 換算六大類食物精準份數與克數")
    st.write("根據台灣衛福部每日飲食指南之每份生重估算：")
    
    food_groups_data = {
        "六大類食物名稱 (Food Groups)": [
            "全穀雜糧類 (Whole Grains)",
            "豆魚蛋肉類 (Beans, Fish, Eggs, Meat)",
            "低脂乳品類 (Low-fat Dairy)",
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
        "常見生重換算參考 (Grams/Reference)": [
            f"約 {grain_servings*25:.1f} 克的未熟乾穀 (依生重20-30g換算，約1/4碗飯)",
            f"約 {meat_servings*35:.1f} 克生肉 (一份約等於生重30-35g/一台兩)",
            f"約 {milk_servings*240:.1f} 毫升液態奶 (一份約等於240ml)",
            f"約 {veg_servings*100:.1f} 克生菜 (一份約等於可食生重100g)",
            f"約 {fruit_servings*100:.1f} 克切塊水果 (一份約等於碗裝8分滿/約100g)",
            f"約 {fat_servings*5:.1f} 克烹調油 (一份約等於精製油5g/一茶匙)"
        ]
    }
    
    st.dataframe(pd.DataFrame(food_groups_data), use_container_width=True)
    st.success("🎉 運算成功！這套選單就像完美的情人，精準滿足你身體的每一分預算！")
else:
    st.warning("⚠️ 請修正左側邊欄的三大營養素百分比，使其加總等於 100% 以啟動神算大師。")
