import streamlit as st
import pandas as pd

st.set_page_config(page_title="商業管灌配方輔助決策系統", page_icon="🧪", layout="wide")

st.title("🧪 商業管灌配方動態決策與水分營養連動系統")
st.write("本模組完全對齊 84 頁官方臨床指引。輸入個案基礎目標後，選擇任何一款商業配方與罐數，系統將全自動動態扣除並計算剩餘缺口！")

st.markdown("---")

# ==================== 84頁精確營養品大數據庫 (內建臨床精密規格) ====================
FORMULA_DB = {
    "【常規均衡】管灌安素 (Osmolite 1.0 kcal/mL)": {
        "kcal": 251, "pro": 8.8, "fat": 8.2, "cho": 35.6, "water": 200, "fiber": 0.0,
        "notes": "標準等滲透壓均衡配方，自由水比例高 (84.3%)，適用於腸胃功能正常者。"
    },
    "【高氮修復】愛美力 (Osmolite HN 1.0 kcal/mL)": {
        "kcal": 250, "pro": 10.4, "fat": 8.1, "cho": 33.9, "water": 198, "fiber": 0.0,
        "notes": "高氮修復配方，適合手術後或需要積極組織修補之個案。"
    },
    "【常規高纖】健力體 (Jevity 1.0 kcal/mL)": {
        "kcal": 251, "pro": 10.4, "fat": 8.4, "cho": 33.4, "water": 198, "fiber": 3.33,
        "notes": "添加天然黃豆纖維，能有效維持腸道完整性並改善便秘或軟便。"
    },
    "【濃縮高纖】愛美力涵纖 (1.2 kcal/mL)": {
        "kcal": 301, "pro": 13.8, "fat": 9.7, "cho": 39.6, "water": 202, "fiber": 5.5,
        "notes": "高熱量濃縮配方。內含 FOS 果寡醣，限水個案首選。"
    },
    "【強效限水】雙卡HN (Two Cal HN 2.0 kcal/mL)": {
        "kcal": 478, "pro": 20.0, "fat": 22.8, "cho": 51.4, "water": 167, "fiber": 0.0,
        "notes": "極致超濃縮配方！自由水比例暴跌至 70%，灌食期間需嚴密監測個案水份缺口。"
    },
    "【糖腎專用】葡勝納嚴選 (Glucerna 250mL)": {
        "kcal": 258, "pro": 12.5, "fat": 13.6, "cho": 21.4, "water": 212, "fiber": 5.3,
        "notes": "具備低GI安全標章。富含單元不飽和脂肪酸 (MUFA)，專防高血糖滲透性利尿風險。"
    },
    "【洗腎透析】新版腎補納 (Nepro 237mL)": {
        "kcal": 425, "pro": 10.6, "fat": 22.7, "cho": 46.4, "water": 170, "fiber": 3.7,
        "notes": "高蛋白、低電解質負荷。完美補償血液透析與腹膜透析流失之大分子白蛋白。"
    },
    "【未洗腎期】新版普寧勝 (Suplena 237mL)": {
        "kcal": 425, "pro": 19.1, "fat": 22.7, "cho": 37.9, "water": 170, "fiber": 2.65,
        "notes": "限制蛋白質飲食控制專用 (Pro佔比極低)，適用於延緩 CKD 惡化速度。"
    },
    "【術前碳水】益富益能康 (Clear CHO 300mL)": {
        "kcal": 200, "pro": 0.0, "fat": 0.0, "cho": 50.0, "water": 264, "fiber": 0.0,
        "notes": "ERAS 術後加速康復指引專用。術前 2 小時清流質碳水補充，降低術後胰島素抗性。"
    }
}

# ==================== Layout Layout ====================
left_col, right_col = st.columns([1, 2])

# ==================== Left Column: 臨床設定與目標定錨 ====================
with left_col:
    st.header("📋 第一步：設定個案每日營養總目標")
    target_kcal = st.number_input("每日總熱量目標 (kcal):", min_value=500, max_value=4000, value=1800, step=50)
    target_pro = st.number_input("每日蛋白質目標 (g):", min_value=10, max_value=200, value=65, step=5)
    target_cho = st.number_input("每日碳水化合物目標 (g):", min_value=50, max_value=500, value=225, step=5)
    target_water = st.number_input("每日液體總水分目標 (mL):", min_value=500, max_value=5000, value=2000, step=50)
    
    st.markdown("---")
    st.header("🧪 第二步：選擇外援商業配方與灌食罐數")
    selected_formula = st.selectbox("請選擇欲調配的商業配方品項:", list(FORMULA_DB.keys()))
    formula_info = FORMULA_DB[selected_formula]
    
    cans = st.slider("每日預計灌食罐數/份數:", min_value=0, max_value=10, value=3, step=1)

# ==================== Core 連動交叉運算核心 ====================
# 計算配方帶入的總量
provided_kcal = cans * formula_info["kcal"]
provided_pro = cans * formula_info["pro"]
provided_cho = cans * formula_info["cho"]
provided_fat = cans * formula_info["fat"]
provided_water = cans * formula_info["water"]
provided_fiber = cans * formula_info["fiber"]

# 計算自體天然食物剩餘缺口 (Gap)
gap_kcal = max(0.0, target_kcal - provided_kcal)
gap_pro = max(0.0, target_pro - provided_pro)
gap_cho = max(0.0, target_cho - provided_cho)
gap_water = max(0.0, target_water - provided_water)

# ==================== Right Column: 視覺化儀表板與即時連動報告 ====================
with right_col:
    st.header("📊 臨床全自動解耦與連動數據看板 (Linked Dashboard)")
    st.info(f"🧬 **當前選用品項病理指引**：{formula_info['notes']}\n\n⚠️ 一旦調整左側『灌食罐數』，下方所有指標、賸餘食物配額與 NCP 診斷將瞬間重組！")
    
    # 頂層四大核心指標即時對位
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("🔥 剩餘熱量缺口", f"{gap_kcal:.0f} kcal", f"配方已提供 {provided_kcal} kcal", delta_color="inverse")
    metric_col2.metric("🍗 剩餘蛋白缺口", f"{gap_pro:.1f} g", f"配方已提供 {provided_pro:.1f} g", delta_color="inverse")
    metric_col3.metric("🍚 剩餘醣類缺口", f"{gap_cho:.1f} g", f"配方已提供 {provided_cho:.1f} g", delta_color="inverse")
    metric_col4.metric("💧 淨額外補水缺口", f"{gap_water:.0f} mL", f"配方自帶水 {provided_water} mL", delta_color="inverse")
    
    st.markdown("### 🔍 巨量營養素與水份動態對比平衡表")
    
    comparison_data = {
        "核心營養常數項目": ["總熱量 (Energy, kcal)", "蛋白質 (Protein, g)", "碳水化合物 (CHO, g)", "自由液體水 (Free Water, mL)", "總膳食纖維 (Fiber, g)"],
        "個案設定總目標": [f"{target_kcal} kcal", f"{target_pro} g", f"{target_cho} g", f"{target_water} mL", "依疾病調整"],
        "💾 當前商業配方提供量": [f"{provided_kcal} kcal", f"{provided_pro:.1f} g", f"{provided_cho:.1f} g", f"{provided_water} mL", f"{provided_fiber:.1f} g"],
        "🎯 賸餘需由天然食物/點心補足量": [f"{gap_kcal:.0f} kcal", f"{gap_pro:.1f} g", f"{gap_cho:.1f} g", f"{gap_water:.0f} mL", "由時蔬代換補足"]
    }
    st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)
    
    # 動態臨床危險阻斷防禦機制 (HACCP / Clinical Alerts)
    st.markdown("### 🚨 雙向動態臨床生理警報機制")
    
    alert_triggered = False
    if "雙卡HN" in selected_formula and cans >= 4:
        st.error(f"🔴 **高安全風險警報：極度限水高溶質負荷！**\n\n個案目前由雙卡HN灌食達 {cans} 罐，配方自帶自由水僅有 {provided_water} mL。病患每日尚有高達 {gap_water} mL 的龐大純水缺口！若未於點職端或管灌間歇期強迫灌注純水，個案將在 24 小時內陷入嚴重的高滲透壓脫水與高鈉血症！")
        alert_triggered = True
        
    if gap_pro == 0.0 and gap_kcal > 0:
        st.warning(f"🟠 **臨床配比失衡警告：熱量不足但蛋白質已破表！**\n\n當前選用之配方使得蛋白質預算已 100% 用罄，但熱量仍有 {gap_kcal:.0f} kcal 的龐大黑洞。此時絕對不可再盲目追加肉類或常規配方，剩餘熱量必須由『純單素配方（如益富糖貽）』進行無氮熱量阻擊，避免引發高 BUN 尿毒代謝危機！")
        alert_triggered = True
        
    if not alert_triggered:
        st.success("🟢 **生理常數運算平衡**：當前商業配方之水分與巨量營養素分佈未觸發極端病理臨界點，剩餘缺口可安全由精準代換表天然食物進行閉環補償。")

    # 全自動產出結合商業配方扣除後的 NCP 營養處方 (Nutrition Prescription)
    st.markdown("---")
    st.subheader("📋 結合 ONS 扣除法之全自動臨床營養處方 (Nutrition Prescription)")
    pres_text = f"【臨床處方】每日給予該個案常規均衡天然膳食共 {gap_kcal:.0f} 大卡，內含蛋白質 {gap_pro:.1f} 公克、醣類 {gap_cho:.1f} 公克；並經由管灌管道每日固定分次注入 {selected_formula} 共 {cans} 罐（占總熱量 {provided_kcal} kcal），餐與餐之間需額外強迫追加沖洗純水共 {gap_water:.0f} 毫升，以維體液與電解質平衡。"
    st.code(pres_text, language="text")
