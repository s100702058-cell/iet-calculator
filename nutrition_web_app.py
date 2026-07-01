import streamlit as st

st.set_page_config(page_title="Clinical Nutrition OS", page_icon="🧬", layout="wide")

st.title("🏥 Clinical Nutrition Operating System (CNOS)")
st.subheader("未來頂尖營養師的專屬臨床決策支援平台")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 🚀 系統核心模組說明
    本平台依據**營養照護流程 (NCP)**、**衛福部最新食物代換表**與**臨床重症指南**設計，全面採用解耦模組化架構開發：
    
    * **🎨 頁面 01：精準營養配對 (含餐次與重症低渣)**
      - 支援常規門診、ICU 重症急性期與 ERAS 外科手術照護。
      - 導入 **ONS (口服營養補充)** 淨熱量自動扣除演算法。
      - 解鎖 **「無肉品」** 與 **「無乳品」** 之極端無渣、急性胰臟炎腸道休息設定。
      - 內建 **50g 超高纖維** 臨床脂質干預指標。
    * **🧪 頁面 02：商業管灌配方輔助決策系統**
      - 完整收錄「聚合、單體、特殊疾病、單素」四大型男配方。
      - 內建高滲透壓腹瀉警訊與肺病低醣高脂（低 RQ）生化機轉提示。
    * **🏥 頁面 03：團膳供應管理與 HACCP 🚨CCP 核檢**
      - 完美對齊採購、驗收冷鏈、備料解凍至「100-150g 留樣 48 小時」之完整供膳安全鏈。
    """)
    st.success("💡 請點擊左側邊欄的選單，切換進入特定臨床照護模組進行運算！")

with col2:
    st.info("""
    ### 🩺 
    國考遇到菜單設計與重症處方題，先找**「服務對象」**，再確立**「營養需求」**，最後才回推**「食物代換與配膳」**。這套多頁面系統的設計邏輯，正是完全依循此核心臨床思維建構而成！
    """)
    
    st.markdown("### 📊 臨床生理常數監測指標")
    st.metric(label="成人基礎纖維需求", value="34 g/day")
    st.metric(label="高血脂干預纖維目標", value="≥ 50 g/day")
