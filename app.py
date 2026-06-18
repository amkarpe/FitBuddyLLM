import streamlit as st
from src.planner import (
    build_plan_summary,
    generate_workout_plan,
    generate_diet_plan
)
from src.prompts import SYSTEM_PROMPT, CHAT_PROMPT_TEMPLATE
from src.retriever import retrieve_context, format_context
from src.generator import generate_response
from src.food_db import select_foods_for_plan, clean_food_list

st.set_page_config(page_title="FitBuddy", page_icon="💪", layout="wide")

st.title("💪 FitBuddy")
st.subheader("Beginner Fat-Loss Fitness Assistant")

st.markdown(
    """
This tool provides general fitness and nutrition guidance for educational purposes only.
It is **not medical advice**.
"""
)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("User Profile")

    height = st.number_input("Height (cm)", min_value=120, max_value=250, value=175)
    weight = st.number_input("Weight (kg)", min_value=35, max_value=250, value=75)

    activity_level = st.selectbox(
        "Activity Level",
        ["sedentary", "lightly active", "moderately active", "very active"]
    )

    training_days = st.selectbox(
        "Training Days / Week",
        [2, 3, 4, 5, 6],
        index=3
    )

    diet_preference = st.selectbox(
        "Diet Preference",
        ["no preference", "high protein", "vegetarian", "halal", "low carb"]
    )

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["Generate Plan", "Ask Questions"])

# ================= PLAN TAB =================
with tab1:

    # ---------- STEP 1 ----------
    st.markdown("### Step 1: Generate Plan Summary")

    if st.button("Generate Plan Summary"):
        summary_data = build_plan_summary(
            height,
            weight,
            activity_level,
            training_days,
            diet_preference
        )
        st.session_state["summary"] = summary_data

    if "summary" in st.session_state:
        st.markdown("## Your Plan Summary")

        st.write(st.session_state["summary"]["summary"])

        st.markdown("### Calories")
        st.write(st.session_state["summary"]["calories"])

        st.markdown("### Protein")
        st.write(st.session_state["summary"]["protein"])


    # ---------- STEP 2 ----------
    st.markdown("---")
    st.markdown("### Step 2: Generate Workout Plan")

    if st.button("Generate Workout Plan"):
        workout = generate_workout_plan(
            height,
            weight,
            training_days,
            diet_preference
        )
        st.session_state["workout"] = workout

    if "workout" in st.session_state:
        st.markdown("## Your Workout Plan")
        st.write(st.session_state["workout"])


    # ---------- STEP 3 ----------
    st.markdown("---")
    st.markdown("### Step 3: Generate Diet Plan")

    if st.button("Generate Diet Plan"):

        # get foods
        foods = select_foods_for_plan(diet_preference)
        clean_foods = clean_food_list(foods)

        # ensure summary exists
        calories = st.session_state.get("summary", {}).get("calories", "2000 kcal/day")
        protein = st.session_state.get("summary", {}).get("protein", "120 g/day")

        diet = generate_diet_plan(
            clean_foods,
            diet_preference,
            calories,
            protein
        )

        st.session_state["diet"] = diet

    if "diet" in st.session_state:
        st.markdown("## Your Diet Plan")
        st.write(st.session_state["diet"])


# ================= CHAT TAB =================
with tab2:

    st.markdown("### Ask a fitness question")

    question = st.text_input("Example: Is creatine useful during fat loss?")

    if st.button("Ask FitBuddy"):

        if not question.strip():
            st.warning("Please enter a question.")

        else:
            profile = {
                "height_cm": height,
                "weight_kg": weight,
                "activity_level": activity_level,
                "training_days": training_days,
                "diet_preference": diet_preference,
            }

            docs = retrieve_context(question)
            context = format_context(docs)

            user_prompt = CHAT_PROMPT_TEMPLATE.format(
                question=question,
                profile=profile,
                context=context,
            )

            with st.spinner("Thinking..."):
                answer = generate_response(SYSTEM_PROMPT, user_prompt)

            st.markdown("## Answer")
            st.write(answer)

            with st.expander("Retrieved Context"):
                for doc in docs:
                    st.markdown(f"**{doc['title']}**")
                    st.write(doc["text"])