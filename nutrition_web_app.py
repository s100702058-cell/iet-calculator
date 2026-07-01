import streamlit as st

st.set_page_config(page_title="Clinical Nutrition OS", page_icon="🧬", layout="wide")

# 🔒 強行注入側邊欄常數，逼迫多頁面導覽大門重開
st.sidebar.markdown("### 🗂️ 臨床 OS 模組導航系統")
st.sidebar.info("💡 請點選下方分頁進入臨床運算")

st.title("🏥 Clinical Nutrition Operating System (CNOS)")
st.subheader("未來頂尖營養師的專屬臨床決策支援平台")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 🚀 系統核心模組已成功解耦 (Decoupled)
    本作業系統已將臨床病理計算、管灌配方決策與大量製備管理進行模組化拆分：
    
    * **🎨 頁面 01：精準營養配對 (含餐次、重症低渣與生化警報)**
      - 內建 **Albumin, K, P, HbA1c** 臨床紅綠燈即時雙向連動警報系統。
      - 自動生成符合 NCP 規範之 **PES 營養診斷陳述報告**。
      - 導入 ONS 商業營養品扣除演算法與台灣在地四季時蔬成本去鉀 CCP 管制。
    * **🧪 頁面 02：商業管灌配方輔助決策系統**
      - 完整收錄「聚合、單體、特殊疾病、單素」四大型男配方。
    * **🏥 頁面 03：團膳供應管理與 HACCP 🚨CCP 核檢**
      - 完美對齊採購、驗收冷鏈、備料解凍至「100-150g 留樣 48 小時」之安全鏈。
    """)
    st.success("📢 導航受體已激活！請點擊左側邊欄蹦出的選單，切換進入特定臨床照護模組！")

with col2:
    st.info("""
    ### 🩺 國考破體心法
    菜單設計題，永遠先找**「服務對象」**，再確立**「營養需求」**，最後才回推**「食物代換」**。這套平台的切頁架構正是遵循此核心臨床思維建構而成！
    """)
    st.metric(label="成人基礎纖維需求", value="34 g/day")
    st.metric(label="高血脂干預纖維目標", value="≥ 50 g/day")
