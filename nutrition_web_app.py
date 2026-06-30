{\rtf1\ansi\ansicpg950\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 cat << 'EOF' > nutrition_web_app.py\
import streamlit as st\
import pandas as pd\
\
# \uc0\u35373 \u23450 \u32178 \u38913 \u27161 \u38988 \u33287 \u39080 \u26684 \
st.set_page_config(page_title="\uc0\u31934 \u28310 \u29151 \u39178 \u31070 \u31639 \u37197 \u23565 \u22120 ", page_icon="\u55358 \u56663 ", layout="centered")\
\
# \uc0\u32178 \u38913 \u35222 \u35258 \u22823 \u27161 \
st.title("\uc0\u55358 \u56663  \u31934 \u28310 \u29151 \u39178 \u31070 \u31639 \u37197 \u23565 \u22120  (Dietitian Calculator)")\
st.write("\uc0\u36879 \u36942 \u33256 \u24202 \u29151 \u39178 \u23416 \u39135 \u29289 \u20132 \u25563 \u34920 \u28436 \u31639 \u27861 \u65292 \u23559 \u39636 \u37325 \u33287 \u29105 \u37327 \u31934 \u28310 \u37197 \u23565 \u33267 \u20845 \u22823 \u39006 \u39135 \u29289 \u20811 \u25976 \u65281 ")\
\
st.markdown("---")\
\
# ==================== Sidebar: \uc0\u20351 \u29992 \u32773 \u36664 \u20837 \u21312  ====================\
st.sidebar.header("\uc0\u55357 \u56523  \u31532 \u19968 \u27493 \u65306 \u36664 \u20837 \u20491 \u26696 \u22522 \u26412 \u36039 \u26009 ")\
weight = st.sidebar.number_input("\uc0\u35531 \u36664 \u20837 \u39636 \u37325  (kg):", min_value=30.0, max_value=200.0, value=60.0, step=0.5)\
\
activity_level = st.sidebar.selectbox(\
    "\uc0\u35531 \u36984 \u25799 \u27599 \u26085 \u27963 \u21205 \u24375 \u24230  (Physical Activity Level):",\
    ["\uc0\u36629 \u24230 \u27963 \u21205  (30 kcal/kg) - \u36774 \u20844 \u12289 \u38748 \u24907 \u29983 \u27963 ", \
     "\uc0\u20013 \u24230 \u27963 \u21205  (35 kcal/kg) - \u32147 \u24120 \u36208 \u21205 \u12289 \u23478 \u21209 \u12289 \u36629 \u24230 \u36939 \u21205 ", \
     "\uc0\u37325 \u24230 \u27963 \u21205  (40 kcal/kg) - \u37325 \u39636 \u21147 \u21214 \u21205 \u12289 \u39640 \u24375 \u24230 \u36939 \u21205 \u35347 \u32244 "]\
)\
\
# \uc0\u35299 \u26512 \u27963 \u21205 \u29105 \u37327 \u20418 \u25976 \
if "\uc0\u36629 \u24230 " in activity_level:\
    activity_factor = 30\
elif "\uc0\u20013 \u24230 " in activity_level:\
    activity_factor = 35\
else:\
    activity_factor = 40\
\
st.sidebar.markdown("---")\
st.sidebar.header("\uc0\u9878 \u65039  \u31532 \u20108 \u27493 \u65306 \u19977 \u22823 \u29151 \u39178 \u32032 \u27604 \u20363 \u20998 \u37197 ")\
p_ratio = st.sidebar.slider("\uc0\u34507 \u30333 \u36074 \u27604 \u20363  (Protein %):", 10, 35, 20, step=5)\
f_ratio = st.sidebar.slider("\uc0\u33026 \u32938 \u27604 \u20363  (Lipid %):", 15, 40, 30, step=5)\
c_ratio = 100 - p_ratio - f_ratio\
\
st.sidebar.info(f"\uc0\u30070 \u21069 \u37197 \u23565 \u27604 \u20363 \u65306 \\n- \u37283 \u39006  (CHO): \{c_ratio\}%\\n- \u34507 \u30333 \u36074  (PRO): \{p_ratio\}%\\n- \u33026 \u32938  (FAT): \{f_ratio\}%")\
\
if c_ratio < 0:\
    st.sidebar.error("\uc0\u10060  \u27604 \u20363 \u21152 \u32317 \u36229 \u36942  100%\u65292 \u35531 \u37325 \u26032 \u35519 \u25972 \u34507 \u30333 \u36074 \u33287 \u33026 \u32938 \u27604 \u20363 \u65281 ")\
\
# ==================== Core Algorithm: \uc0\u29151 \u39178 \u35336 \u31639 \u26680 \u24515  ====================\
# 1. \uc0\u35336 \u31639  TDEE\
tdee = weight * activity_factor\
\
# 2. \uc0\u35336 \u31639 \u19977 \u22823 \u29151 \u39178 \u32032 \u30446 \u27161 \u20811 \u25976  (Target Grams)\
target_cho_g = (tdee * (c_ratio / 100)) / 4\
target_pro_g = (tdee * (p_ratio / 100)) / 4\
target_fat_g = (tdee * (f_ratio / 100)) / 9\
\
# 3. \uc0\u39135 \u29289 \u20132 \u25563 \u34920 \u33258 \u21205 \u23186 \u21512 \u28436 \u31639 \u27861  (Food Exchange List Matching Algorithm)\
# \uc0\u38928 \u35373 \u33256 \u24202 \u24120 \u35211 \u20043 \u34092 \u33756 \u12289 \u27700 \u26524 \u12289 \u20083 \u21697 \u22522 \u26412 \u25885 \u21462 \u20221 \u25976  (\u20316 \u28858 \u35336 \u31639 \u22522 \u24213 )\
veg_servings = 3.0    # \uc0\u34092 \u33756 \u39006 \u22522 \u26412  3 \u20221 \
fruit_servings = 2.0  # \uc0\u27700 \u26524 \u39006 \u22522 \u26412  2 \u20221 \
milk_servings = 1.0   # \uc0\u20083 \u21697 \u39006 (\u20302 \u33026 )\u22522 \u26412  1 \u20221 \
\
# \uc0\u21508 \u22522 \u30990 \u39006 \u21029 \u29151 \u39178 \u32032 \u35336 \u31639 \
# \uc0\u34092 \u33756  1\u20221 : P=1g, C=5g, F=0g\
# \uc0\u27700 \u26524  1\u20221 : P=0g, C=15g, F=0g\
# \uc0\u20302 \u33026 \u20083 \u21697  1\u20221 : P=8g, C=12g, F=4g\
base_cho = (veg_servings * 5) + (fruit_servings * 15) + (milk_servings * 12)\
base_pro = (veg_servings * 1) + (fruit_servings * 0) + (milk_servings * 8)\
base_fat = (veg_servings * 0) + (fruit_servings * 0) + (milk_servings * 4)\
\
# \uc0\u25187 \u38500 \u22522 \u26412 \u20221 \u25976 \u24460 \u65292 \u21097 \u39192 \u38656 \u20998 \u37197 \u30340 \u38928 \u31639 \
rem_cho = target_cho_g - base_cho\
rem_pro = target_pro_g - base_pro\
\
# \uc0\u21033 \u29992 \u36088 \u39192 \u37283 \u39006 \u35336 \u31639 \u12300 \u20840 \u31296 \u38620 \u31975 \u39006 \u12301 \u20221 \u25976  (1\u20221 \u20840 \u31296 : C=15g, P=2g, F=0g)\
grain_servings = max(0.0, rem_cho / 15)\
\
# \uc0\u25187 \u38500 \u20840 \u31296 \u38620 \u31975 \u39006 \u24118 \u20358 \u30340 \u34507 \u30333 \u36074 \u24460 \u65292 \u21097 \u39192 \u34507 \u30333 \u36074 \u30001 \u12300 \u35910 \u39770 \u34507 \u32905 \u39006 \u12301 \u35036 \u36275  (\u20197 \u20013 \u33026 \u32905 \u39006 \u20272 \u31639 : P=7g, F=5g)\
rem_pro_after_grain = rem_pro - (grain_servings * 2)\
meat_servings = max(0.0, rem_pro_after_grain / 7)\
\
# \uc0\u35336 \u31639 \u30446 \u21069 \u32047 \u35336 \u30340 \u33026 \u32938 \u37327 \u65292 \u19981 \u36275 \u30340 \u30001 \u12300 \u27833 \u33026 \u33287 \u22533 \u26524 \u31278 \u23376 \u39006 \u12301 \u35036 \u40778  (1\u20221 \u27833 \u33026 : F=5g)\
current_fat = base_fat + (meat_servings * 5)\
rem_fat = target_fat_g - current_fat\
fat_servings = max(0.0, rem_fat / 5)\
\
# ==================== Dashboard: \uc0\u32178 \u38913 \u32080 \u26524 \u21576 \u29694  ====================\
if c_ratio >= 0:\
    # \uc0\u32113 \u35336 \u25351 \u27161 \u22294 \u21345 \
    col1, col2, col3 = st.columns(3)\
    col1.metric("\uc0\u55357 \u56522  \u32317 \u29105 \u37327 \u38656 \u27714  (TDEE)", f"\{tdee:.0f\} kcal")\
    col2.metric("\uc0\u55356 \u57175  \u30446 \u27161 \u34507 \u30333 \u36074 ", f"\{target_pro_g:.1f\} g")\
    col3.metric("\uc0\u55356 \u57178  \u30446 \u27161 \u37283 \u39006 ", f"\{target_cho_g:.1f\} g")\
\
    st.markdown("### \uc0\u55356 \u57263  \u19977 \u22823 \u29986 \u33021 \u29151 \u39178 \u32032 \u30446 \u27161 \u37197 \u23565 ")\
    macro_df = pd.DataFrame(\{\
        "\uc0\u29151 \u39178 \u32032  (Nutrients)": ["\u37283 \u39006  (Carbohydrates)", "\u34507 \u30333 \u36074  (Proteins)", "\u33026 \u32938  (Lipids)"],\
        "\uc0\u20998 \u37197 \u27604 \u20363  (%)": [c_ratio, p_ratio, f_ratio],\
        "\uc0\u30446 \u27161 \u20811 \u25976  (g)": [round(target_cho_g, 1), round(target_pro_g, 1), round(target_fat_g, 1)]\
    \})\
    st.table(macro_df)\
\
    st.markdown("### \uc0\u55356 \u57213 \u65039  \u25563 \u31639 \u20845 \u22823 \u39006 \u39135 \u29289 \u31934 \u28310 \u20221 \u25976 \u33287 \u20811 \u25976 ")\
    st.write("\uc0\u26681 \u25818 \u21488 \u28771 \u34907 \u31119 \u37096 \u27599 \u26085 \u39154 \u39135 \u25351 \u21335 \u20043 \u27599 \u20221 \u29983 \u37325 \u20272 \u31639 \u65306 ")\
    \
    # \uc0\u24314 \u31435 \u20845 \u22823 \u39006 \u39135 \u29289 \u36664 \u20986 \u34920 \u26684 \
    food_groups_data = \{\
        "\uc0\u20845 \u22823 \u39006 \u39135 \u29289 \u21517 \u31281  (Food Groups)": [\
            "\uc0\u20840 \u31296 \u38620 \u31975 \u39006  (Whole Grains)",\
            "\uc0\u35910 \u39770 \u34507 \u32905 \u39006  (Beans, Fish, Eggs, Meat)",\
            "\uc0\u20302 \u33026 \u20083 \u21697 \u39006  (Low-fat Dairy)",\
            "\uc0\u34092 \u33756 \u39006  (Vegetables)",\
            "\uc0\u27700 \u26524 \u39006  (Fruits)",\
            "\uc0\u27833 \u33026 \u33287 \u22533 \u26524 \u31278 \u23376 \u39006  (Fats & Oils)"\
        ],\
        "\uc0\u35336 \u31639 \u20986 \u20043 \u31934 \u28310 \u20221 \u25976  (Servings)": [\
            f"\{grain_servings:.1f\} \uc0\u20221 ",\
            f"\{meat_servings:.1f\} \uc0\u20221 ",\
            f"\{milk_servings:.1f\} \uc0\u20221 ",\
            f"\{veg_servings:.1f\} \uc0\u20221 ",\
            f"\{fruit_servings:.1f\} \uc0\u20221 ",\
            f"\{fat_servings:.1f\} \uc0\u20221 "\
        ],\
        "\uc0\u24120 \u35211 \u29983 \u37325 \u25563 \u31639 \u21443 \u32771  (Grams/Reference)": [\
            f"\uc0\u32004  \{grain_servings*25:.1f\} \u20811 \u30340 \u26410 \u29087 \u20094 \u31296  (\u20381 \u29983 \u37325 20-30g\u25563 \u31639 \u65292 \u32004 1/4\u30871 \u39151 )",\
            f"\uc0\u32004  \{meat_servings*35:.1f\} \u20811 \u29983 \u32905  (\u19968 \u20221 \u32004 \u31561 \u26044 \u29983 \u37325 30-35g/\u19968 \u21488 \u20841 )",\
            f"\uc0\u32004  \{milk_servings*240:.1f\} \u27627 \u21319 \u28082 \u24907 \u22902  (\u19968 \u20221 \u32004 \u31561 \u26044 240ml)",\
            f"\uc0\u32004  \{veg_servings*100:.1f\} \u20811 \u29983 \u33756  (\u19968 \u20221 \u32004 \u31561 \u26044 \u21487 \u39135 \u29983 \u37325 100g)",\
            f"\uc0\u32004  \{fruit_servings*100:.1f\} \u20811 \u20999 \u22602 \u27700 \u26524  (\u19968 \u20221 \u32004 \u31561 \u26044 \u30871 \u35037 8\u20998 \u28415 /\u32004 100g)",\
            f"\uc0\u32004  \{fat_servings*5:.1f\} \u20811 \u28921 \u35519 \u27833  (\u19968 \u20221 \u32004 \u31561 \u26044 \u31934 \u35069 \u27833 5g/\u19968 \u33590 \u21273 )"\
        ]\
    \}\
    \
    st.dataframe(pd.DataFrame(food_groups_data), use_container_width=True)\
    \
    st.success("\uc0\u55356 \u57225  \u36939 \u31639 \u25104 \u21151 \u65281 \u36889 \u22871 \u36984 \u21934 \u23601 \u20687 \u23436 \u32654 \u30340 \u24773 \u20154 \u65292 \u31934 \u28310 \u28415 \u36275 \u20320 \u36523 \u39636 \u30340 \u27599 \u19968 \u20998 \u38928 \u31639 \u65281 ")\
else:\
    st.warning("\uc0\u9888 \u65039  \u35531 \u20462 \u27491 \u24038 \u20596 \u37002 \u27396 \u30340 \u19977 \u22823 \u29151 \u39178 \u32032 \u30334 \u20998 \u27604 \u65292 \u20351 \u20854 \u21152 \u32317 \u31561 \u26044  100% \u20197 \u21855 \u21205 \u31070 \u31639 \u22823 \u24107 \u12290 ")\
EOF}