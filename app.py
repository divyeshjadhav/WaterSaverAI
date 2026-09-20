"""
WATER CONSERVATION CHATBOT - MAIN APP
Run: streamlit run app.py
"""

import streamlit as st
from datetime import datetime
import sys
import os

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "utils"))

from ai_engine import AIEngine
from tips_database import get_tips_by_category, get_categories, calculate_impact

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(page_title="WaterSaver AI", page_icon="💧", layout="wide")

# =============================================================================
# SESSION STATE
# =============================================================================
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "completed_tips" not in st.session_state:
    st.session_state.completed_tips = []
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""
if "last_source" not in st.session_state:
    st.session_state.last_source = ""
if "ai_engine" not in st.session_state:
    st.session_state.ai_engine = AIEngine()


def current_stats():
    """Get current impact stats"""
    impact = calculate_impact(st.session_state.completed_tips)
    score = min(10, 5 + len(st.session_state.completed_tips))
    impact["score"] = score
    return impact


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.title("💧 WaterSaver AI")
    st.caption("Free • Local AI • Personalised")
    st.markdown("---")

    engine = st.session_state.ai_engine
    if engine.is_ollama_running():
        if engine.is_model_available():
            st.success(f"🟢 AI online ({engine.model})")
        else:
            st.warning(f"🟠 Model missing. Run: ollama pull {engine.model}")
    else:
        st.warning("🟠 Ollama offline. Run: ollama serve")

    st.markdown("---")

    # Profile creation
    if st.session_state.user_profile is None:
        st.subheader("👤 Create your profile")
        with st.form("profile_form"):
            family_size = st.selectbox("Family size", ["1-2 people", "3-4 people", "5+ people"])
            housing_type = st.selectbox("Home type", ["Apartment", "Independent House", "Bungalow/Villa"])
            main_concern = st.selectbox("Main concern", ["Bathroom", "Kitchen", "Laundry", "Outdoor", "Leaks", "General"])
            
            if st.form_submit_button("✅ Create Profile"):
                st.session_state.user_profile = {
                    "family_size": family_size,
                    "housing_type": housing_type,
                    "main_concern": main_concern,
                }
                st.rerun()
    else:
        p = st.session_state.user_profile
        stats = current_stats()
        st.subheader("👤 Your profile")
        st.write(f"👥 {p['family_size']}")
        st.write(f"🏠 {p['housing_type']}")
        st.write(f"🎯 {p['main_concern']}")
        c1, c2 = st.columns(2)
        c1.metric("Score", f"{stats['score']}/10")
        c2.metric("₹/month", stats["rupees_per_month"])
        if st.button("🔄 Reset"):
            st.session_state.user_profile = None
            st.session_state.chat_history = []
            st.session_state.completed_tips = []
            st.rerun()

    st.markdown("---")
    st.markdown("**Quick ideas:**\n- Shower tips\n- Dripping tap fix\n- Laundry advice\n- 7-day challenge")

# =============================================================================
# MAIN AREA
# =============================================================================
st.title("💧 Water Conservation Chatbot")
st.markdown("·  AI-powered ·  Personalised ·  Impact tracking")

# Safety check
if st.session_state.user_profile is None:
    st.info(" Create your profile in sidebar")
    st.stop()

profile = st.session_state.user_profile
stats = current_stats()

# Dashboard
st.subheader("📊 Your impact")
m1, m2, m3, m4 = st.columns(4)
m1.metric("💧 Water", f"{stats['litres_per_month']:,} L/month")
m2.metric("💰 Money", f"₹{stats['rupees_per_month']}")
m3.metric("🌍 CO₂", f"{stats['co2_kg_per_month']} kg/month")
m4.metric("🏆 Score", f"{stats['score']}/10")
st.progress(stats["score"] / 10)
st.markdown("---")

# Chat
st.subheader("💬 Chat")
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask anything about water saving...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            answer, prompt_used, source = st.session_state.ai_engine.generate_response(
                user_input=user_input,
                user_profile=profile,
                chat_history=st.session_state.chat_history[:-1],
                stats=stats,
            )
        st.markdown(answer)

    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    st.session_state.last_prompt = prompt_used
    st.session_state.last_source = source
    st.rerun()


st.markdown("---")

# Tips checklist
st.subheader("✅ Mark tips done to raise score")
concern = profile["main_concern"].lower()
show_cats = [concern] if concern in get_categories() else ["bathroom"]

for cat in show_cats:
    tips = get_tips_by_category(cat)
    if not tips:
        continue
    st.markdown(f"### {cat.title()}")
    for tip in tips:
        done = tip["id"] in st.session_state.completed_tips
        c1, c2 = st.columns([5, 1])
        with c1:
            st.markdown(f"**{tip['emoji']} {tip['title']}** — _{tip['description']}_")
            st.caption(f"💧 {tip['water_saved']} L/day · 💰 ₹{tip['cost_saved']}/month")
        with c2:
            if done:
                st.button("✔", disabled=True, key=f"d_{tip['id']}")
            else:
                if st.button("Done", key=f"b_{tip['id']}"):
                    st.session_state.completed_tips.append(tip["id"])
                    st.balloons()
                    st.rerun()
    st.markdown("---")

st.caption("Save water, save money, save the planet! 🌍💧")