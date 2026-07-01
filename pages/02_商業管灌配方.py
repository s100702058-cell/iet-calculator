import streamlit as st
import pandas as pd

st.set_page_config(page_title="商業管灌配方輔助決策系統", page_icon="🧪", layout="wide")

st.title("🧪 商業管灌配方輔助決策系統 (CNOS 專業核檢版)")
st.write("本模組完全對齊 84 頁『醫院常用營養配方介紹』官方臨床指引，導入亞培與益富完整成分矩陣與 RQ 代謝動力學！")

st.markdown("---")

# ==================== 84頁精確營養品大數據庫 (Verbatim Database) ====================
ABBOTT_POLYMERIC = {
    "管灌安素 (OSMOLITE)": {"kcal": 251, "pro": "14.0%", "fat": "29.3%", "cho": "56.7%", "dense": "1.0 kcal/mL", "fiber": "0g", "fos": "0g", "target": "一般常規均衡營養需求者", "notes": "最接近人體生理體液滲透壓 (300-500 mOsm/kg)，病患耐受度高。"},
    "愛美力 (OSMOLITE HN)": {"kcal": 250, "pro": "16.7%", "fat": "29.0%", "cho": "54.3%", "dense": "1.0 kcal/mL", "fiber": "0g", "fos": "0g", "target": "積極營養照護、需要較高蛋白質者", "notes": "HN 代表 High Nitrogen (高氮)，提供豐富必需胺基酸。"},
    "健力體 (JEVITY)": {"kcal": 251, "pro": "16.6%", "fat": "30.1%", "cho": "53.3%", "dense": "1.0 kcal/mL", "fiber": "3.33g", "fos": "0g", "target": "長期管灌、需要補充膳食纖維以維持腸道機能者", "notes": "添加天然黃豆纖維，能有效改善管灌常見之便秘或軟便。"},
    "愛美力涵纖": {"kcal": 301, "pro": "18.4%", "fat": "29.0%", "cho": "52.6%", "dense": "1.2 kcal/mL", "fiber": "5.5g", "fos": "2.5g", "target": "限水、高熱量且需高纖維雙重干預者", "notes": "高熱量濃縮配方。內含 2.5g FOS 果寡醣，建立優質腸道菌相受體。"},
    "健力體FOS粉狀配方": {"kcal": 264, "pro": "15.4%", "fat": "29.58%", "cho": "55.02%", "dense": "1.0 kcal/mL", "fiber": "4.4g", "fos": "1.8g", "target": "經濟型自製沖泡、需要果寡醣膳食纖維支持者", "notes": "粉狀劑型，方便臨床依個案水份調配溶解度。"}
}

DISEASE_SPECIFIC_DB = {
    "肺部疾病類 (Pulmonary - 益沛佳)": {
        "代表產品": "益沛佳 (Pulmocare)",
        "熱量分佈": "蛋白質 16.7% | 脂肪 55.1% | 碳水化合物 28.2%",
        "理化指標": "蛋白質 62.6g/L (鈉/鈣酪蛋白) | 脂肪 93.3g/L | 碳水化合物 105.7g/L",
        "脂肪組態": "55.8% 橄欖油 + 20% MCT (易利用中鏈) + 14% 玉米油 + 7% 高油酸紅花油",
        "臨床核心效益": "🚨 專供呼吸衰竭、COPD病患。利用脂肪超低呼吸商 (RQ=0.7) 物理特性，斷絕 CO2 廢物產出，臨床實證能顯著減少呼吸器依賴時間 (減低死亡率)！外加肉鹼協助脂肪代謝。"
    },
    "糖尿病類 (Diabetes - 葡勝納)": {
        "代表產品": "葡勝納系列 (SR菁選 / 原味不甜 / 嚴選 / 三重強護)",
        "熱量分佈": "嚴選配方：碳水 33.1% | 蛋白質 19.4% | 脂肪 47.5% (高單元不飽和 MUFA)",
        "理化指標": "荷蘭原裝進口，全系列皆具備官方認證之『低升糖指數 (低GI √)』安全標章",
        "脂肪組態": "富含單元不飽和脂肪酸 (MUFA)，能有效穩定血管內皮屏障，降低動脈硬化風險",
        "臨床核心效益": "🚨 專防住院病患因 Hyperglycemia 引發之滲透性利尿、傷口癒合延遲及肌肉流失。將 GL 控制在低範圍 (≤10)，確保餐後血糖曲線平穩。"
    },
    "腎臟病-未透析低蛋白類 (Pre-Dialysis)": {
        "代表產品": "亞培普寧勝 (New) / 益富易能充",
        "熱量分佈": "新版普寧勝：蛋白質 18% | 碳水 34% | 脂肪 48% (舊版為 Pro 14%)",
        "理化指標": "易能充：提供 200 kcal 點心補充，蛋白質僅 0.8g，且落實低鈉、低磷、低鉀控制",
        "脂肪組態": "植物性油粉、芥花油高熱量基底，富含膳食纖維 (菊糖 1.9g)",
        "臨床核心效益": "🚨 專用於 CKD Stage 1-5 未透析患者。嚴格執行限制蛋白質干預指標 (0.6-0.75 g/kg)，防止含氮廢物堆積引發尿毒症狀與腸胃道發炎嘔吐。"
    },
    "腎臟病-已透析高蛋白類 (Dialysis)": {
        "代表產品": "亞培腎補納 (New) / 益富元氣強",
        "熱量分佈": "新版腎補納：蛋白質 10% | 碳水 42% | 脂肪 48% (舊版蛋白質僅 6%)",
        "理化指標": "元氣強：蛋白質佔熱量高達 32.6% (分離黃豆蛋白優質正宮)，每包含 8g 優質蛋白",
        "脂肪組態": "高濃度芥花油與 MCT 聯手，高生物價，且維持極低電解質負荷",
        "臨床核心效益": "🚨 專用於 HD 血液透析與 CAPD 腹膜透析個案。補償透析機器無情偷走的 10-13g 胺基酸，強效拉高血清白蛋白，對抗高死亡相對風險！"
    }
}

# ==================== UI Sidebar 導航中樞 ====================
st.sidebar.header("📋 第一步：商業配方四大分類點將")
formula_category = st.sidebar.selectbox(
    "選擇臨床配方分型 (Commercial Classification):",
    ["聚合配方 (Polymeric Formula)", "單體/元素配方 (Monomeric/Elemental Formula)", "特殊疾病配方 (Disease-Specific Formula)", "單素配方 (Modular Formula)"]
)

st.sidebar.markdown("---")
st.sidebar.header("💡 國考/臨床名師口訣複習")
if "聚合" in formula_category:
    st.sidebar.success("💡 **正餐結婚梗**：三大營養素完整未水解，滲透壓最天然安全（300-500 mOsm/kg），專配腸胃道健全的正宮個案！")
elif "單體" in formula_category:
    st.sidebar.error("💡 **乾爹給現金梗**：100% 水解胜肽與游離胺基酸，滲透壓極高（500-600 mOsm/kg），灌太快會引發嚴重滲透性腹瀉！")
elif "特殊" in formula_category:
    st.sidebar.info("💡 **量身定制大愛梗**：針對肝、腎、肺、糖尿病等器官衰竭進行分子比例重組，價格昂貴但靶向精準！")
else:
    st.sidebar.warning("💡 **單一工具人梗**：純粉飴或純乳清蛋白粉，嚴禁單獨長期使用，否則引發巨量與微量營養素集體破產！")

# ==================== Main Panel UI 輸出畫面 ====================
if "聚合" in formula_category:
    st.subheader("👨‍⚕️ 聚合配方 (Polymeric Formula) —— 亞培大量製備系列矩陣核檢 (頁碼 5)")
    st.write("適用於腸胃道消化吸收功能完全正常之個案，大部分病患皆具備極佳耐受性：")
    
    # 轉化 84 頁成分對比表為美觀的 DataFrame
    poly_rows = []
    for p_name, p_data in ABBOTT_POLYMERIC.items():
        poly_rows.append({
            "產品品項名稱": p_name,
            "單份熱量 budget": f"{p_data['kcal']} Kcal",
            "蛋白質比 %": p_data["pro"],
            "脂肪比例 %": p_data["fat"],
            "碳水比例 %": p_data["cho"],
            "熱量濃度": p_data["dense"],
            "總膳食纖維": p_data["fiber"],
            "FOS 果寡醣": p_data["fos"],
            "臨床精準適用對象": p_data["target"]
        })
    st.dataframe(pd.DataFrame(poly_rows), use_container_width=True)
    
    st.info("💡 **名師強迫症查核筆記**：管灌安素與愛美力皆為零纖維配方；若發現病患出現短期腹瀉或長期便秘，應即刻跳轉介入含 3.33g 纖維之 **健力體 (JEVITY)** 進行腸道蠕動平衡調控。")

elif "單體" in formula_category:
    st.subheader("🧪 單體/元素配方 (Monomeric/Elemental Formula) —— 應激黏膜修復矩陣 (頁碼 24-29)")
    st.write("適用於加護病房 (ICU)、短腸症、急性胰臟炎或發炎性腸道疾病等腸胃道功能嚴重受損之重症個案：")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.error("🔥 亞培創快復 (AlitraQ) -- Immunomodulation")
        st.markdown("""
        * **熱量分佈常數**：309 大卡/包，含 **15.8 克優質蛋白質 (100% 水解乳清胜肽，小分子好吸收)**。
        * **核心免疫戰力**：特別加強富含 **左旋麩醯胺酸 (Glutamine) 與精胺酸 (Arginine)**。
        * **臨床實證生化數據**：強效刺激受傷期腸道黏膜上皮細胞增生！**空腸增生率提升 20%、迴腸增生率大舉拉高 27%**！
        * **核心適配症**：嚴重燒燙傷、敗血症、腸胃道大手術後黏膜急性壞死萎縮。
        """)
    with col_b:
        st.error("🔥 益富免益增 (Immu-NU) -- 元素調節配方")
        st.markdown("""
        * **三大營養素優化**：脂肪含量極低，100% 符合重症低脂低渣元素飲食需求。
        * **蛋白質受體**：完全由高消化吸收率之乳清蛋白與游離胺基酸組成，降低腸道水份高滲拉力。
        * **臨床適配症**：腸胃極度不適引發之慣性重症腹瀉、低蛋白血症個案。
        """)
        
    st.warning("⚠️ **高滲透壓致命警訊 (CCP 管制)**：單體元素配方因溶質粒子數暴增，滲透壓高達 **500~600 mOsm/kg**！臨床灌食速度必須由低速 (20-30 mL/hr) 緩慢步進追加，否則會強力將組織水分抽入腸腔，引發嚴重的滲透性腹瀉 (Osmotic Diarrhea)！")

elif "特殊" in formula_category:
    st.subheader("🧬 特殊疾病配方 (Disease-Specific Formula) —— 各大器官靶向重組矩陣 (頁碼 10-22)")
    st.write("依據特定器官衰竭或高應激代謝障礙個案之病理機制，進行完美比例精準切換：")
    
    selected_spec = st.selectbox("請點選欲查閱的靶向器官專用配方:", list(DISEASE_SPECIFIC_DB.keys()))
    spec_data = DISEASE_SPECIFIC_DB[selected_spec]
    
    st.success(f"🎯 正在調閱：{spec_data['代表產品']} 臨床病理控制指南")
    
    detail_rows = [
        {"臨床核心評估維度": "三大營養素分配比例", "84頁官方指引精確數據": spec_data["熱量分佈"]},
        {"臨床核心評估維度": "理化常數與成分來源", "84頁官方指引精確數據": spec_data["理化指標"]},
        {"臨床核心評估維度": "脂肪酸與微量組態", "84頁官方指引精確數據": spec_data["脂肪組態"]},
        {"臨床核心評估維度": "🏥 臨床病理機制與為什麼說明", "84頁官方指引精確數據": spec_data["臨床核心效益"]}
    ]
    st.table(pd.DataFrame(detail_rows))

else:
    st.subheader("🛠️ 單素配方 (Modular Formula) —— 營養缺口填補工具人 (頁碼 29, 32, 66)")
    st.write("僅提供單一特定營養素，完全缺乏維生素與礦物質，嚴禁單獨作為常規單一營養來源：")
    
    col_x, col_y = st.columns(2)
    with col_x:
        st.warning("⚡ 亞培基速得 (Abound) / 益富優質蛋白質粉")
        st.markdown("""
        * **核心成分定錨**：100% 頂級乳清蛋白與白胺酸關鍵代謝物 **HMB (Metabolite of Leucine)**。
        * **四大細胞修復靶點**：
          1. 阻斷泛素調節路徑，**降低肌肉蛋白分解 (↓breakdown)**。
          2. 刺激 mTOR 訊號，**增加體內蛋白質組織合成 (↑protein synthesis)**。
          3. 顯著提高氮保留率，達成臨床正氮平衡目標。
          4. 強效刺激膠原蛋白沉積，加速三期重度壓瘡與重大創傷傷口復原。
        """)
    with col_y:
        st.warning("⚡ 益富糖貽 (純麥芽糊精能量粉)")
        st.markdown("""
        * **核心成分定錨**：不含蔗糖、不含乳糖，高溶解度之純複合性碳水化合物。
        * **臨床核心效益**：滲透壓極低，促進極快之胃排空速度。專為 CKD 未透析、肝臟器官衰竭或嚴重限水個案在不拉高蛋白質負荷的前提下，**瘋狂追加熱量預算**。
        """)

st.markdown("---")
st.caption("🚨 出題者思維例外防呆提示：本平台嚴格依循 DRIs 科學證據建構。泛酸 (Pantothenic acid) 與生物素 (Biotin) 因數據不足無法確立 EAR，故以 AI 呈現；在商業配方配膳時，若個案長期完全使用缺乏此類 AI 微量元素之單素配方，將觸發嚴重的巨量代謝崩潰與皮膚黏膜全面潰爛。")
