"""
居家轻症护理助手
运行方式: streamlit run app.py
"""

import streamlit as st
from datetime import datetime

# ==================== 规则库 ====================

SYMPTOM_CLASSIFICATION = {
    "高危": ["呼吸困难", "胸痛", "意识模糊", "咯血", "口唇发紫", "严重喘息"],
    "中危": [
        "持续发热超过3天", "咳嗽伴有黄痰或绿痰",
        "静息时心率超过100次/分", "高热（体温≥39℃）",
        "持续呕吐无法进食", "精神状态明显变差"
    ],
    "低危": [
        "偶尔干咳", "喉咙痛", "低烧（37.3-38℃）",
        "流鼻涕", "轻微头痛", "乏力", "打喷嚏"
    ]
}

ADVICE_MAP = {
    "高危": {
        "level": "high", "icon": "🔴",
        "advice": "⚠️ 高风险提醒\n\n您描述的症状存在严重风险。\n【建议】立即前往医院急诊科就诊，或拨打120。\n不要自行用药，以免掩盖病情。"
    },
    "中危": {
        "level": "medium", "icon": "🟡",
        "advice": "⚡ 中等风险提醒\n\n请密切观察。\n【建议】每4小时测体温、多饮温水、避免劳累。\n若24小时内无好转或加重，请就医。"
    },
    "低危": {
        "level": "low", "icon": "🟢",
        "advice": "✅ 低风险提醒\n\n可以通过居家护理缓解。\n【建议】多饮水、保证睡眠、饮食清淡。\n如出现呼吸困难或持续高热，请就医。"
    }
}

DISCLAIMER = "\n\n⚠️ 重要免责声明：本工具仅提供健康信息辅助参考，不构成医疗诊断。如有不适请及时就医。"


def classify_symptom(symptom):
    for level, symptoms in SYMPTOM_CLASSIFICATION.items():
        if symptom in symptoms:
            return level
    return None


def assess_risk(selected_symptoms):
    if not selected_symptoms:
        return {"level": "unknown", "icon": "⚪", "advice": "请至少选择一个症状。"}

    classified = {}
    for s in selected_symptoms:
        lv = classify_symptom(s)
        if lv:
            classified[s] = lv

    high = [s for s, l in classified.items() if l == "高危"]
    medium = [s for s, l in classified.items() if l == "中危"]
    low = [s for s, l in classified.items() if l == "低危"]

    if high:
        result_level = "高危"
    elif medium:
        result_level = "中危"
    elif low:
        result_level = "低危"
    else:
        return {"level": "unrecognized", "icon": "⚪", "advice": "您选择的症状暂不在评估范围内，建议咨询医生。"}

    advice_data = ADVICE_MAP[result_level]
    return {
        "level": advice_data["level"],
        "icon": advice_data["icon"],
        "advice": advice_data["advice"] + DISCLAIMER,
        "red_flags": high
    }


def get_symptoms_by_category():
    return {
        "⚠️ 危险信号（需立即就医）": SYMPTOM_CLASSIFICATION["高危"],
        "⚡ 需密切关注的症状": SYMPTOM_CLASSIFICATION["中危"],
        "🏠 适合居家护理的轻症": SYMPTOM_CLASSIFICATION["低危"]
    }


# ==================== Streamlit 界面 ====================

st.set_page_config(page_title="居家轻症护理助手", page_icon="🏠", layout="centered")

st.title("🏠 居家轻症护理助手")
st.caption("仅限发热、咳嗽等常见轻症的居家护理建议 · 不替代医生诊断")

st.warning("⚠️ 重要声明：本工具仅提供健康信息辅助参考，不构成医疗诊断。如有身体不适，请及时就医。")

with st.expander("📖 使用说明"):
    st.write("1. 勾选您当前的症状（可多选）")
    st.write("2. 点击【开始评估】按钮")
    st.write("3. 查看风险等级和护理建议")

st.subheader("🩺 请选择您目前的症状")

symptoms_by_category = get_symptoms_by_category()
selected_symptoms = []

for cat_name, symptoms in symptoms_by_category.items():
    with st.expander(cat_name, expanded=True):
        cols = st.columns(3)
        for i, symptom in enumerate(symptoms):
            with cols[i % 3]:
                if st.checkbox(symptom, key=f"s_{symptom}"):
                    selected_symptoms.append(symptom)

if selected_symptoms:
    st.info(f"已选 {len(selected_symptoms)} 个症状：{'、'.join(selected_symptoms)}")

if st.button("🔍 开始评估", type="primary", use_container_width=True):
    if not selected_symptoms:
        st.warning("请至少选择一个症状")
    else:
        result = assess_risk(selected_symptoms)
        st.markdown("---")
        st.subheader("📋 评估结果")

        if result["level"] == "high":
            st.error(result["advice"])
            if result["red_flags"]:
                st.error(f'🚨 红旗症状：{"、".join(result["red_flags"])}，请立即就医！')
        elif result["level"] == "medium":
            st.warning(result["advice"])
        elif result["level"] == "low":
            st.info(result["advice"])
        else:
            st.warning(result["advice"])

st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>居家轻症护理助手 · 不替代医生诊断</p>", unsafe_allow_html=True)