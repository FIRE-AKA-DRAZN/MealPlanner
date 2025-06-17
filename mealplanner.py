import streamlit as st
import random
import json
from datetime import datetime
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="Weekly Meal Planner",
    page_icon="🍽️",
    layout="centered"
)

# Title and description
st.title("Weekly Meal Planner 🍳")
st.markdown("Generate your weekly meal plan with a single click!")

# List of meals
meals = [
    "SpagBol",
    "Mac & Cheese",
    "Tomato Soup",
    "Peanut Potato Soup",
    "Beans and Toast",
    "Gyousa & Noodles",
    "Kebabs & Curry couscous",
    "Kebabs & Stir-fry Rice",
    "Lost the Pot Noodle Tea",
    "Lasagne",
    "Baked Potatos",
    "Stir-fry",
    "Shepard's Pie",
    "Pasta & Pesto",
    "Pea & Ham soup"
]

# Initialize weekly plan
def init_weekly_plan():
    return {
        "Monday": None,
        "Tuesday": None,
        "Wednesday": None,
        "Thursday": None,
        "Friday": None,
        "Saturday": None,
        "Sunday": "Pizza and salad"  # Fixed meal for Sunday
    }

def create_weekly_plan(meal_list, meal_plan):
    # Get recently used meals from history
    history = load_meal_history()
    recent_meals = set()
    for past_plan in history["history"][-2:]:  # Last 2 weeks
        recent_meals.update(past_plan["meals"].values())
    
    # Prioritize unused meals
    available_meals = [m for m in meal_list.copy() if m not in recent_meals]
    if len(available_meals) < 6:  # If not enough unused meals, add some back
        available_meals.extend([m for m in meal_list if m not in available_meals])
    
    for day in meal_plan:
        if meal_plan[day] is not None and meal_plan[day] != "No meal assigned":
            continue
            
        if available_meals:
            chosen_meal = random.choice(available_meals)
            meal_plan[day] = chosen_meal
            available_meals.remove(chosen_meal)
        else:
            meal_plan[day] = "No meal assigned"
    return meal_plan

def load_meal_history():
    history_file = Path("meal_history.json")
    if history_file.exists():
        with open(history_file, "r") as f:
            return json.load(f)
    return {"history": []}

def save_meal_history(meal_plan):
    history_file = Path("meal_history.json")
    history = load_meal_history()
    history["history"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "meals": meal_plan
    })
    # Keep only last 4 weeks of history
    history["history"] = history["history"][-4:]
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)

def clear_meal_history():
    history_file = Path("meal_history.json")
    if history_file.exists():
        with open(history_file, "w") as f:
            json.dump({"history": []}, f)
    st.session_state.meal_history = {"history": []}
    
# Initialize session state for history
if 'meal_history' not in st.session_state:
    st.session_state.meal_history = load_meal_history()

# Create columns for layout
col1, col2, col3 = st.columns([1, 2, 1])

# Center the generate button in the middle column
with col2:
    if st.button("Generate New Meal Plan! 🎲", use_container_width=True):
        weekly_plan = create_weekly_plan(meals, init_weekly_plan())
        save_meal_history(weekly_plan)
        st.session_state.meal_history = load_meal_history()
        
        # Display the meal plan in a nice format
        st.markdown("### Your Weekly Meal Plan:")
        for day, meal in weekly_plan.items():
            st.markdown(
                f"""
                <div style='
                    padding: 10px;
                    border-radius: 5px;
                    margin: 5px 0;
                    background-color: #222222;
                    border-left: 5px solid #ff4b4b;
                '>
                    <strong>{day}:</strong> {meal}
                </div>
                """,
                unsafe_allow_html=True
            )

# Add history display below the meal plan
if st.session_state.meal_history["history"]:  # Check if there's any history
    if len(st.session_state.meal_history["history"]) > 1:  # More than just current plan
        # Create a header row with the title and clear button
        hist_col1, hist_col2 = st.columns([3, 1])
        with hist_col1:
            st.markdown("### Previous Meal Plans")
        with hist_col2:
            if st.button("Clear History 🗑️", type="secondary", use_container_width=True):
                clear_meal_history()
                st.rerun()  # Refresh the app to show cleared history               

        # Display history (skip the current plan)
        for past_plan in reversed(st.session_state.meal_history["history"][:-1]):
            st.markdown(f"#### Week of {past_plan['date']}")
            for day, meal in past_plan["meals"].items():
                st.markdown(
                    f"""
                    <div style='
                        padding: 5px;
                        border-radius: 3px;
                        margin: 2px 0;
                        background-color: #1a1a1a;
                        border-left: 3px solid #666666;
                        font-size: 0.9em;
                    '>
                        <strong>{day}:</strong> {meal}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown("---")