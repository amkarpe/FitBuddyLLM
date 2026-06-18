import streamlit as st
from src.planner import build_plan
from src.prompts import SYSTEM_PROMPT, CHAT_PROMPT_TEMPLATE
from src.retriever import retrieve_context, format_context
from src.generator import generate_response

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

    training_days = st.selectbox("Training Days / Week", [2, 3, 4, 5, 6], index=1)

    diet_preference = st.selectbox(
        "Diet Preference",
        ["no preference", "high protein", "vegetarian", "halal", "low carb"]
    )

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["Generate Plan", "Ask Questions"])

# ================= PLAN TAB =================
with tab1:
    st.markdown("### Create your beginner fat-loss plan")

    if st.button("Generate My Plan"):
        with st.spinner("Building your plan..."):
            plan, docs, weekly_plan, foods = build_plan(
                height=height,
                weight=weight,
                activity_level=activity_level,
                training_days=training_days,
                diet_preference=diet_preference,
            )

        st.markdown("## Your Plan")

        # ---------- Goal ----------
        st.markdown("### 1. Goal Summary")
        st.write(plan["goal_summary"])

        # ---------- Calories ----------
        st.markdown("### 2. Daily Calorie Guidance")
        st.write(plan["calories"])

        # ---------- Protein ----------
        st.markdown("### 3. Protein Guidance")
        st.write(plan["protein"])

        # ---------- Workout ----------
        st.markdown("### 4. Weekly Workout Plan")

        for day in plan["weekly_plan"]:
            st.markdown(f"**{day['day']} — {day['focus']}**")
            st.write(day["details"])

            for ex in day["exercises"]:
                st.write(f"- {ex}")

        # ---------- Meals ----------
        st.markdown("### 5. Meal Structure")

        st.write("**Breakfast:**")
        for f in plan["meals"]["breakfast"]:
            st.write(f"- {f}")

        st.write("**Lunch:**")
        for f in plan["meals"]["lunch"]:
            st.write(f"- {f}")

        st.write("**Dinner:**")
        for f in plan["meals"]["dinner"]:
            st.write(f"- {f}")

        st.write("**Snacks:**")
        for f in plan["meals"]["snacks"]:
            st.write(f"- {f}")

        # ---------- Tips ----------
        st.markdown("### 6. Tips for Adherence")
        for tip in plan["tips"]:
            st.write(f"- {tip}")

        # ---------- Disclaimer ----------
        st.markdown("### 7. Safety Disclaimer")
        st.write(plan["disclaimer"])

        # ---------- DEBUG (optional) ----------
        with st.expander("🔍 Retrieved Context"):
            for doc in docs:
                st.markdown(f"**Title:** {doc['title']}")
                st.write(doc["text"])

        with st.expander("🍽️ Food Suggestions Used"):
            for food in foods:
                st.write(food.get("description", "Unknown"))

# ================= CHAT TAB =================
with tab2:
    st.markdown("### Ask a follow-up question")

    question = st.text_input(
        "Example: Is creatine useful during fat loss?"
    )

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
                    st.markdown(f"**Title:** {doc['title']}")
                    st.write(doc["text"])