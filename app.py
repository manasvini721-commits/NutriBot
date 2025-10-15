# app.py 
import random
import os
import streamlit as st
import numpy as np
from pathlib import Path
from PIL import Image
# Gemini imports
import google.generativeai as genai

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error fetching Gemini response: {e}")
        return None

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="NutriX: The Secret to Your Health", layout="wide")

# -------------------------
# Sidebar Navigation
# -------------------------
st.sidebar.title("Navigation")
pages = ["Home", "Health Planner", "NutriX Chat", "Doctors", "Help & Contact"]
choice = st.sidebar.radio("Go to:", pages, key="main_navigation")

# -------------------------
# Custom CSS Styling
# -------------------------
st.markdown("""
<style>
body { background-color: #E6E6FA; font-family: "Helvetica Neue", sans-serif; }
h1.title { font-size: 60px; font-weight: 900; color: #6a4b9c; text-align: center; margin-bottom: 1rem; }
.card { padding: 1.5rem; margin-bottom: 1.5rem; border-radius: 16px; box-shadow: 0px 6px 16px rgba(0,0,0,0.08); color: #1a202c; background-color: #F5F0FA; }
.meal-card { background-color: #F8E6FF; }
.exercise-card { background-color: #E6FAF8; }
.body-card { background-color: #F0E6FF; }
.report-card { background-color: #E6F8FA; }
.tips-card { background-color: #FFF0E6; }
.input-card { background-color: #F5F0FA; padding: 1.5rem; margin-bottom: 1.5rem; border-radius: 16px; box-shadow: 0px 6px 16px rgba(0,0,0,0.08); }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Helper Functions
# -------------------------
def calculate_bmi(weight, height):
    height_m = height / 100
    return round(weight / (height_m**2), 1)

def generate_meal_plan(preference, goal):
    meal_options = {
        "Weight Loss": {
            "Breakfast": {
                "Vegan": [
                    "Overnight oats with chia (~180 kcal)", "Green smoothie (~200 kcal)", "Fruit salad with nuts (~190 kcal)",
                    "Avocado toast (~210 kcal)", "Tofu scramble (~220 kcal)", "Chia pudding (~200 kcal)",
                    "Vegan protein shake (~230 kcal)", "Quinoa porridge (~190 kcal)", "Almond butter toast (~200 kcal)"
                ],
                "Vegetarian": [
                    "Poha (~180 kcal)", "Idli with sambar (~200 kcal)", "Vegetable oats (~210 kcal)",
                    "Upma (~190 kcal)", "Moong dal chilla (~200 kcal)", "Vegetable sandwich (~220 kcal)",
                    "Dosa with chutney (~230 kcal)", "Paneer bhurji (~210 kcal)", "Paratha with yogurt (~220 kcal)"
                ],
                "Non-Veg": [
                    "Egg white omelette (~200 kcal)", "Boiled eggs with toast (~210 kcal)", "Grilled chicken salad (~220 kcal)",
                    "Scrambled eggs with veggies (~230 kcal)", "Smoked salmon wrap (~240 kcal)", "Turkey slices with toast (~220 kcal)",
                    "Chicken soup (~200 kcal)", "Egg curry (~210 kcal)", "Tuna salad (~220 kcal)"
                ],
                "Eggetarian": [
                    "Poha with boiled egg (~200 kcal)", "Upma with paneer (~210 kcal)", "Vegetable oats (~190 kcal)",
                    "Dosa with egg bhurji (~220 kcal)", "Scrambled eggs with spinach (~230 kcal)", "Paneer sandwich (~210 kcal)",
                    "Idli with egg curry (~220 kcal)", "Paratha with boiled egg (~230 kcal)", "Egg and vegetable salad (~200 kcal)"
                ]
            },
            "Lunch": {
                "Vegan": [
                    "Quinoa salad (~320 kcal)", "Lentil curry (~330 kcal)", "Tofu stir fry (~340 kcal)",
                    "Chickpea curry (~350 kcal)", "Buddha bowl (~360 kcal)", "Veg soup + bread (~310 kcal)",
                    "Vegan pasta (~340 kcal)", "Brown rice with beans (~330 kcal)", "Roasted veggie quinoa (~320 kcal)"
                ],
                "Vegetarian": [
                    "Rajma rice (~350 kcal)", "Dal with chapati (~340 kcal)", "Vegetable khichdi (~330 kcal)",
                    "Palak paneer with 1 roti (~360 kcal)", "Veg pulao (~350 kcal)", "Curd rice (~320 kcal)",
                    "Paneer bhurji (~370 kcal)", "Methi thepla (~330 kcal)", "Stuffed paratha with salad (~340 kcal)"
                ],
                "Non-Veg": [
                    "Grilled chicken (~350 kcal)", "Fish curry with 1 roti (~360 kcal)", "Egg curry (~330 kcal)",
                    "Chicken salad (~320 kcal)", "Chicken soup with bread (~310 kcal)", "Baked fish (~340 kcal)",
                    "Boiled egg curry (~300 kcal)", "Turkey salad (~350 kcal)", "Grilled shrimp (~360 kcal)"
                ],
                "Eggetarian": [
                    "Dal with boiled egg (~340 kcal)", "Egg curry with roti (~350 kcal)", "Vegetable khichdi (~330 kcal)",
                    "Paneer bhurji with boiled egg (~360 kcal)", "Rajma rice (~350 kcal)", "Scrambled eggs with vegetables (~340 kcal)",
                    "Vegetable pulao (~330 kcal)", "Stuffed paratha with egg (~350 kcal)", "Palak paneer with boiled egg (~360 kcal)"
                ]
            },
            "Snack": {
                "Vegan": [
                    "Nuts (~180 kcal)", "Fruit chaat (~150 kcal)", "Hummus with carrots (~170 kcal)",
                    "Granola bar (~190 kcal)", "Roasted chickpeas (~160 kcal)", "Vegan protein shake (~200 kcal)",
                    "Soy milk smoothie (~180 kcal)", "Trail mix (~190 kcal)", "Apple with peanut butter (~170 kcal)"
                ],
                "Vegetarian": [
                    "Sprouts chaat (~150 kcal)", "Fruit yogurt (~170 kcal)", "Corn chaat (~160 kcal)",
                    "Khakhra (~120 kcal)", "Paneer cubes (~190 kcal)", "Vegetable sandwich (~200 kcal)",
                    "Stuffed paratha roll (~210 kcal)", "Cheese cubes (~180 kcal)", "Boiled corn (~150 kcal)"
                ],
                "Non-Veg": [
                    "Boiled eggs (~140 kcal)", "Chicken soup (~160 kcal)", "Tuna salad (~180 kcal)",
                    "Chicken sticks (~190 kcal)", "Egg bhurji (~180 kcal)", "Grilled chicken wrap (~200 kcal)",
                    "Fish soup (~170 kcal)", "Turkey slices (~180 kcal)", "Egg salad (~160 kcal)"
                ],
                "Eggetarian": [
                    "Boiled egg with nuts (~180 kcal)", "Scrambled eggs with spinach (~170 kcal)", "Paneer cubes (~180 kcal)",
                    "Egg sandwich (~190 kcal)", "Fruit salad with boiled egg (~160 kcal)", "Vegetable sandwich (~180 kcal)",
                    "Stuffed paratha with egg (~200 kcal)", "Sprouts chaat with boiled egg (~170 kcal)", "Egg dosa (~190 kcal)"
                ]
            },
            "Dinner": {
                "Vegan": [
                    "Veg stir fry (~320 kcal)", "Lentil soup (~280 kcal)", "Tofu quinoa bowl (~330 kcal)",
                    "Roasted veggies (~300 kcal)", "Vegan chili (~350 kcal)", "Stuffed bell peppers (~310 kcal)",
                    "Vegan curry (~340 kcal)", "Brown rice with vegetables (~320 kcal)", "Zucchini noodles (~300 kcal)"
                ],
                "Vegetarian": [
                    "Vegetable soup (~300 kcal)", "Dal fry with 1 roti (~320 kcal)", "Methi thepla with yogurt (~340 kcal)",
                    "Paneer tikka (~360 kcal)", "Vegetable khichdi (~330 kcal)", "Stuffed paratha with curd (~350 kcal)",
                    "Palak paneer (~340 kcal)", "Vegetable pulao (~330 kcal)", "Mixed veg curry (~320 kcal)"
                ],
                "Non-Veg": [
                    "Grilled chicken (~340 kcal)", "Salmon with veggies (~360 kcal)", "Egg curry with rice (~330 kcal)",
                    "Chicken soup (~320 kcal)", "Fish fry (~350 kcal)", "Chicken stew (~360 kcal)",
                    "Egg fried rice (~340 kcal)", "Baked fish with vegetables (~350 kcal)", "Grilled shrimp (~360 kcal)"
                ],
                "Eggetarian": [
                    "Dal with boiled egg (~330 kcal)", "Paneer bhurji with boiled egg (~340 kcal)", "Vegetable pulao (~320 kcal)",
                    "Egg curry with roti (~340 kcal)", "Scrambled eggs with veggies (~330 kcal)", "Upma with boiled egg (~320 kcal)",
                    "Stuffed paratha with egg (~340 kcal)", "Poha with boiled egg (~320 kcal)", "Palak paneer with egg (~330 kcal)"
                ]
            }
        },

        "Weight Gain": {
            "Breakfast": {
                "Vegan": [
                    "Peanut butter toast (~350 kcal)", "Banana smoothie (~380 kcal)", "Vegan pancakes (~400 kcal)",
                    "Tofu paratha (~420 kcal)", "Nut butter oats (~370 kcal)", "Granola with soy milk (~380 kcal)",
                    "Avocado sandwich (~390 kcal)", "Vegan protein smoothie (~400 kcal)", "Chia pudding with nuts (~390 kcal)"
                ],
                "Vegetarian": [
                    "Paneer paratha (~400 kcal)", "Cheese dosa (~380 kcal)", "Vegetable upma with ghee (~390 kcal)",
                    "Stuffed poha (~370 kcal)", "Masala dosa (~400 kcal)", "Paneer sandwich (~420 kcal)",
                    "Idli with butter sambar (~390 kcal)", "Paratha with curd (~400 kcal)", "Vegetable mix (~380 kcal)"
                ],
                "Non-Veg": [
                    "Chicken sandwich (~420 kcal)", "Omelette with cheese (~400 kcal)", "Scrambled eggs with chicken (~430 kcal)",
                    "Smoked salmon bagel (~440 kcal)", "Chicken sausage with toast (~410 kcal)", "Egg bhurji with butter (~390 kcal)",
                    "Turkey sandwich (~420 kcal)", "Grilled chicken with toast (~430 kcal)", "Egg and cheese toast (~400 kcal)"
                ],
                "Eggetarian": [
                    "Poha with boiled egg (~400 kcal)", "Paneer paratha with egg (~410 kcal)", "Scrambled eggs with vegetables (~420 kcal)",
                    "Masala dosa with boiled egg (~400 kcal)", "Upma with boiled egg (~390 kcal)", "Paneer sandwich with egg (~400 kcal)",
                    "Egg bhurji with chapati (~410 kcal)", "Vegetable omelette (~400 kcal)", "Egg and cheese toast (~420 kcal)"
                ]
            },
            "Lunch": {
                "Vegan": [
                    "Chickpea curry with rice (~450 kcal)", "Tofu stir fry with quinoa (~440 kcal)", "Vegan pasta (~460 kcal)",
                    "Lentil soup with bread (~430 kcal)", "Vegan Buddha bowl (~450 kcal)", "Brown rice with beans (~440 kcal)",
                    "Vegetable curry with millet (~460 kcal)", "Vegan wrap (~450 kcal)", "Quinoa salad with nuts (~440 kcal)"
                ],
                "Vegetarian": [
                    "Paneer butter masala with roti (~500 kcal)", "Vegetable pulao (~450 kcal)", "Dal makhani with rice (~470 kcal)",
                    "Rajma rice (~460 kcal)", "Chole with bhature (~480 kcal)", "Paneer bhurji with paratha (~450 kcal)",
                    "Vegetable khichdi with ghee (~440 kcal)", "Methi paratha with yogurt (~450 kcal)", "Stuffed capsicum (~460 kcal)"
                ],
                "Non-Veg": [
                    "Grilled chicken with rice (~480 kcal)", "Fish curry with roti (~470 kcal)", "Egg curry with rice (~450 kcal)",
                    "Chicken stew with bread (~460 kcal)", "Turkey sandwich (~450 kcal)", "Baked salmon with veggies (~480 kcal)",
                    "Chicken biryani (~500 kcal)", "Egg fried rice (~470 kcal)", "Grilled shrimp with quinoa (~480 kcal)"
                ],
                "Eggetarian": [
                    "Paneer bhurji with boiled egg (~460 kcal)", "Egg curry with roti (~470 kcal)", "Vegetable pulao with boiled egg (~450 kcal)",
                    "Dal makhani with egg (~460 kcal)", "Scrambled eggs with vegetables (~470 kcal)", "Rajma rice with boiled egg (~450 kcal)",
                    "Stuffed paratha with egg (~460 kcal)", "Palak paneer with boiled egg (~470 kcal)", "Egg fried rice (~480 kcal)"
                ]
            },
            "Snack": {
                "Vegan": [
                    "Trail mix (~250 kcal)", "Peanut butter smoothie (~260 kcal)", "Vegan protein bar (~270 kcal)",
                    "Roasted chickpeas (~240 kcal)", "Vegan shake (~260 kcal)", "Nuts and dried fruits (~250 kcal)",
                    "Vegan muffins (~270 kcal)", "Soy milk with granola (~260 kcal)", "Avocado toast (~250 kcal)"
                ],
                "Vegetarian": [
                    "Paneer cubes (~260 kcal)", "Cheese sandwich (~270 kcal)", "Fruit yogurt (~250 kcal)",
                    "Khakhra with ghee (~240 kcal)", "Vegetable sandwich (~260 kcal)", "Stuffed paratha (~270 kcal)",
                    "Boiled corn with butter (~250 kcal)", "Sprouts chaat (~240 kcal)", "Banana smoothie (~260 kcal)"
                ],
                "Non-Veg": [
                    "Boiled eggs (~250 kcal)", "Chicken sticks (~270 kcal)", "Tuna salad (~260 kcal)",
                    "Egg sandwich (~250 kcal)", "Chicken wrap (~270 kcal)", "Egg bhurji (~260 kcal)",
                    "Grilled chicken (~270 kcal)", "Turkey slices (~250 kcal)", "Egg salad (~260 kcal)"
                ],
                "Eggetarian": [
                    "Boiled egg with nuts (~260 kcal)", "Scrambled eggs with paneer (~270 kcal)", "Egg sandwich (~260 kcal)",
                    "Paneer cubes with boiled egg (~250 kcal)", "Vegetable sandwich with egg (~260 kcal)", "Stuffed paratha with egg (~270 kcal)",
                    "Sprouts chaat with boiled egg (~250 kcal)", "Egg dosa (~260 kcal)", "Banana smoothie with egg (~270 kcal)"
                ]
            },
            "Dinner": {
                "Vegan": [
                    "Tofu stir fry with rice (~450 kcal)", "Vegan chili (~460 kcal)", "Brown rice with vegetables (~440 kcal)",
                    "Vegan curry with millet (~450 kcal)", "Quinoa bowl (~460 kcal)", "Roasted veggie quinoa (~450 kcal)",
                    "Vegan pasta (~470 kcal)", "Lentil soup with bread (~440 kcal)", "Chickpea curry with rice (~460 kcal)"
                ],
                "Vegetarian": [
                    "Paneer tikka with roti (~500 kcal)", "Vegetable pulao (~470 kcal)", "Dal makhani with rice (~480 kcal)",
                    "Rajma rice (~460 kcal)", "Chole with bhature (~490 kcal)", "Paneer bhurji with paratha (~470 kcal)",
                    "Vegetable khichdi with ghee (~450 kcal)", "Methi paratha with yogurt (~470 kcal)", "Stuffed capsicum (~460 kcal)"
                ],
                "Non-Veg": [
                    "Grilled chicken with rice (~480 kcal)", "Egg curry with roti (~470 kcal)", "Baked fish with veggies (~480 kcal)",
                    "Chicken biryani (~500 kcal)", "Chicken stew (~460 kcal)", "Egg fried rice (~470 kcal)",
                    "Grilled shrimp (~480 kcal)", "Turkey slices with bread (~460 kcal)", "Fish curry with rice (~470 kcal)"
                ],
                "Eggetarian": [
                    "Paneer bhurji with boiled egg (~470 kcal)", "Egg curry with roti (~470 kcal)", "Vegetable pulao with egg (~460 kcal)",
                    "Dal makhani with boiled egg (~470 kcal)", "Scrambled eggs with vegetables (~470 kcal)", "Rajma rice with boiled egg (~460 kcal)",
                    "Stuffed paratha with egg (~470 kcal)", "Palak paneer with egg (~470 kcal)", "Egg fried rice (~480 kcal)"
                ]
            }
        },

        "Maintain": {
            "Breakfast": {
                "Vegan": [
                    "Overnight oats (~250 kcal)", "Banana smoothie (~260 kcal)", "Avocado toast (~270 kcal)",
                    "Chia pudding (~250 kcal)", "Vegan protein shake (~260 kcal)", "Tofu scramble (~270 kcal)",
                    "Granola with soy milk (~260 kcal)", "Quinoa porridge (~250 kcal)", "Peanut butter toast (~260 kcal)"
                ],
                "Vegetarian": [
                    "Poha (~250 kcal)", "Upma (~260 kcal)", "Vegetable oats (~270 kcal)",
                    "Dosa with chutney (~260 kcal)", "Idli with sambar (~250 kcal)", "Paneer bhurji (~270 kcal)",
                    "Paratha with curd (~260 kcal)", "Vegetable sandwich (~250 kcal)", "Moong dal chilla (~260 kcal)"
                ],
                "Non-Veg": [
                    "Boiled eggs with toast (~260 kcal)", "Scrambled eggs with veggies (~270 kcal)", "Egg white omelette (~250 kcal)",
                    "Grilled chicken salad (~270 kcal)", "Egg curry (~260 kcal)", "Turkey slices with toast (~260 kcal)",
                    "Chicken soup (~250 kcal)", "Smoked salmon wrap (~270 kcal)", "Tuna salad (~260 kcal)"
                ],
                "Eggetarian": [
                    "Poha with boiled egg (~260 kcal)", "Upma with paneer (~270 kcal)", "Vegetable oats with egg (~260 kcal)",
                    "Dosa with egg bhurji (~270 kcal)", "Scrambled eggs with spinach (~260 kcal)", "Paneer sandwich with egg (~270 kcal)",
                    "Idli with egg curry (~260 kcal)", "Paratha with boiled egg (~270 kcal)", "Egg and vegetable salad (~260 kcal)"
                ]
            },
            "Lunch": {
                "Vegan": [
                    "Quinoa salad (~350 kcal)", "Lentil curry with rice (~360 kcal)", "Tofu stir fry (~350 kcal)",
                    "Chickpea curry (~360 kcal)", "Brown rice with beans (~350 kcal)", "Vegan pasta (~360 kcal)",
                    "Roasted veggie quinoa (~350 kcal)", "Vegan Buddha bowl (~360 kcal)", "Veg soup with bread (~350 kcal)"
                ],
                "Vegetarian": [
                    "Dal with chapati (~360 kcal)", "Rajma rice (~370 kcal)", "Palak paneer with 1 roti (~360 kcal)",
                    "Vegetable pulao (~350 kcal)", "Paneer bhurji (~360 kcal)", "Vegetable khichdi (~350 kcal)",
                    "Curd rice (~360 kcal)", "Methi thepla (~350 kcal)", "Stuffed paratha with salad (~360 kcal)"
                ],
                "Non-Veg": [
                    "Grilled chicken (~360 kcal)", "Egg curry with rice (~350 kcal)", "Fish curry with roti (~360 kcal)",
                    "Chicken salad (~350 kcal)", "Chicken soup with bread (~340 kcal)", "Baked fish (~360 kcal)",
                    "Boiled egg curry (~350 kcal)", "Turkey salad (~360 kcal)", "Grilled shrimp (~360 kcal)"
                ],
                "Eggetarian": [
                    "Dal with boiled egg (~360 kcal)", "Egg curry with roti (~360 kcal)", "Vegetable khichdi (~350 kcal)",
                    "Paneer bhurji with boiled egg (~360 kcal)", "Rajma rice with egg (~360 kcal)", "Scrambled eggs with vegetables (~360 kcal)",
                    "Vegetable pulao with boiled egg (~360 kcal)", "Stuffed paratha with egg (~360 kcal)", "Palak paneer with egg (~360 kcal)"
                ]
            },
            "Snack": {
                "Vegan": [
                    "Nuts (~200 kcal)", "Fruit chaat (~180 kcal)", "Hummus with carrots (~200 kcal)",
                    "Trail mix (~210 kcal)", "Granola bar (~200 kcal)", "Vegan protein shake (~210 kcal)",
                    "Soy milk smoothie (~200 kcal)", "Roasted chickpeas (~190 kcal)", "Apple with peanut butter (~200 kcal)"
                ],
                "Vegetarian": [
                    "Sprouts chaat (~200 kcal)", "Fruit yogurt (~210 kcal)", "Corn chaat (~200 kcal)",
                    "Khakhra (~190 kcal)", "Paneer cubes (~210 kcal)", "Vegetable sandwich (~200 kcal)",
                    "Stuffed paratha roll (~210 kcal)", "Cheese cubes (~200 kcal)", "Boiled corn (~190 kcal)"
                ],
                "Non-Veg": [
                    "Boiled eggs (~200 kcal)", "Chicken soup (~210 kcal)", "Tuna salad (~200 kcal)",
                    "Chicken sticks (~210 kcal)", "Egg bhurji (~200 kcal)", "Grilled chicken wrap (~210 kcal)",
                    "Fish soup (~200 kcal)", "Turkey slices (~200 kcal)", "Egg salad (~210 kcal)"
                ],
                "Eggetarian": [
                    "Boiled egg with nuts (~210 kcal)", "Scrambled eggs with spinach (~210 kcal)", "Paneer cubes (~210 kcal)",
                    "Egg sandwich (~210 kcal)", "Fruit salad with boiled egg (~200 kcal)", "Vegetable sandwich with egg (~210 kcal)",
                    "Stuffed paratha with egg (~210 kcal)", "Sprouts chaat with boiled egg (~210 kcal)", "Egg dosa (~210 kcal)"
                ]
            },
            "Dinner": {
                "Vegan": [
                    "Veg stir fry (~350 kcal)", "Lentil soup (~340 kcal)", "Tofu quinoa bowl (~350 kcal)",
                    "Roasted veggies (~340 kcal)", "Vegan chili (~360 kcal)", "Stuffed bell peppers (~350 kcal)",
                    "Vegan curry (~360 kcal)", "Brown rice with vegetables (~350 kcal)", "Zucchini noodles (~340 kcal)"
                ],
                "Vegetarian": [
                    "Vegetable soup (~350 kcal)", "Dal fry with 1 roti (~360 kcal)", "Methi thepla with yogurt (~350 kcal)",
                    "Paneer tikka (~360 kcal)", "Vegetable khichdi (~350 kcal)", "Stuffed paratha with curd (~360 kcal)",
                    "Palak paneer (~360 kcal)", "Vegetable pulao (~350 kcal)", "Mixed veg curry (~350 kcal)"
                ],
                "Non-Veg": [
                    "Grilled chicken (~360 kcal)", "Salmon with veggies (~370 kcal)", "Egg curry with rice (~360 kcal)",
                    "Chicken soup (~350 kcal)", "Fish fry (~360 kcal)", "Chicken stew (~360 kcal)",
                    "Egg fried rice (~360 kcal)", "Baked fish with vegetables (~360 kcal)", "Grilled shrimp (~370 kcal)"
                ],
                "Eggetarian": [
                    "Dal with boiled egg (~360 kcal)", "Paneer bhurji with boiled egg (~360 kcal)", "Vegetable pulao with egg (~360 kcal)",
                    "Egg curry with roti (~360 kcal)", "Scrambled eggs with vegetables (~360 kcal)", "Upma with boiled egg (~360 kcal)",
                    "Stuffed paratha with egg (~360 kcal)", "Poha with boiled egg (~360 kcal)", "Palak paneer with egg (~360 kcal)"
                ]
            }
        }
    }

     # Generate 7-day meal plan
    week_plan = []
    for day in range(7):
        day_plan = {}
        for meal in ["Breakfast", "Lunch", "Snack", "Dinner"]:
            day_plan[meal] = random.choice(meal_options[goal][meal][preference])
        week_plan.append(day_plan)
    return week_plan

def generate_exercise_plan(level):
    mapping = {
        "Sedentary": [
            "Light walking – 20 min", "Stretching – 15 min", "Yoga breathing – 10 min",
            "Neck & shoulder mobility – 5 min", "Ankle mobility – 5 min", "Wall push-ups – 2x10",
            "Seated leg raises – 2x10"
        ],
        "Lightly Active": [
            "Brisk walking – 30 min", "Yoga – 20 min", "Bodyweight squats – 3x12",
            "Push-ups – 3x10", "Plank – 3x30 sec", "Glute bridges – 3x12",
            "Cat-cow stretch – 10 reps"
        ],
        "Moderately Active": [
            "Jogging – 25 min", "Jump rope – 10 min", "Push-ups – 3x12",
            "Lunges – 3x12 per leg", "Plank – 3x45 sec", "Bicycle crunches – 3x15",
            "Mountain climbers – 3x20"
        ],
        "Active": [
            "Running – 30 min", "Pull-ups – 3x8", "Weighted squats – 4x10",
            "Deadlifts – 4x10", "Bench press – 4x10", "Shoulder press – 3x12",
            "Burpees – 3x15", "Plank to push-up – 3x10"
        ],
        "Very Active": [
            "HIIT – 20 min (30s on/30s off)", "Sprints – 10x100m",
            "Power cleans – 4x8", "Deadlifts – 4x8", "Front squats – 4x10",
            "Pull-ups – 4x12", "Dips – 3x15", "Box jumps – 3x12", "Battle ropes – 3x45s",
            "Farmer’s carry – 3x40m"
        ]
    }
    return mapping.get(level, ["Walking – 20 min", "Stretching – 10 min"])

# Body images
image_paths = {
    "Slim": "images/Slim.png.png",
    "Athletic": "images/Athletic.png.png",
    "Average": "images/Average.png.png",
    "Overweight": "images/Overweight.png.png",
    "Obese": "images/Obese.png.png"
}

def display_body_image(shape_name, label):
    img_path = Path(image_paths.get(shape_name, ""))
    if img_path.exists():
        try:
            img = Image.open(img_path)
            st.image(img, caption=label, width=250)
        except Exception as e:
            st.error(f"Error opening {img_path.name}: {e}")
    else:
        st.warning(f"Image for {shape_name} not found at {img_path}")

def create_gemini_chat(model_name="models/gemini-2.5-flash"):
    return genai.GenerativeModel(model_name).start_chat(history=[])

def ask_gemini(chat, prompt):
    try:
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error fetching Gemini response: {e}")
        return None

# -------------------------
# HOME PAGE
# -------------------------
if choice == "Home":
    # Title + Logo
    st.markdown(
    """
    <style>
        .logo {
            position: absolute;
            top: 20px;
            right: 40px;
            width: 200px;
        }
    </style>

    <div style='position: relative;'>
        <img src="https://raw.githubusercontent.com/manasvini721-commits/NutriBot/master/images/logo.png" class='logo'>
        <h1 style='text-align: center; font-size: 100px; color: #6a4b9c; margin-bottom: 0;'>NutriX</h1>
        <h2 style='text-align: center; color: #b595c4; margin-top: 0; font-size: 75px;'>The Secret to Your Health</h2>
    </div>
    """,
    unsafe_allow_html=True
)

    # Two images side-by-side at the same level
    col1, col2 = st.columns(2)
    with col1:
        st.image('images/health_banner.png.png', width="stretch")
    with col2:
        st.image('images/health_banner2.png', width="stretch")
        # Large text below both images
    st.markdown("""
        <h1 style='text-align: center; font-size: 80px; color: black; margin-top: 40px;'>
            YOUR HEALTH, OUR PRIORITY
        </h1>
        """, unsafe_allow_html=True)

# -------------------------
# HEALTH PLANNER PAGE
# -------------------------
elif choice == "Health Planner":
    st.markdown('<h1 class="title">NutriX Health Planner</h1>', unsafe_allow_html=True)

    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 10, 100, 25, key="age_hp")
        height = st.number_input("Height (cm)", 120, 220, 170, key="height_hp")
        weight = st.number_input("Weight (kg)", 30, 200, 70, key="weight_hp")
        activity_level = st.selectbox("Activity Level", ["Sedentary","Lightly Active","Moderately Active","Active","Very Active"], key="activity_hp")
        meal_pref = st.selectbox("Meal Preference", ["Vegan","Vegetarian","Non-Veg","Eggetarian"], key="meal_pref_hp")
        goal = st.selectbox("Goal", ["Weight Loss","Weight Gain","Maintain"], key="goal_hp")

    with col2:
        sleep_hours = st.slider("Average Sleep per Night (hours)", 4, 12, 7, key="sleep_hp")
        stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"], key="stress_hp")
        current_shape = st.selectbox("Current Body Shape", ["Slim","Athletic","Average","Overweight","Obese"], key="current_shape_hp")
        target_shape = st.selectbox("Target Body Shape", ["Slim","Athletic","Average","Overweight","Obese"], key="target_shape_hp")

    # Save inputs to session state
    st.session_state['meal_pref'] = meal_pref
    st.session_state['goal'] = goal
    st.session_state['activity_level'] = activity_level
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Generate Health Report", key="generate_report_hp"):
        bmi = calculate_bmi(weight,height)
        meal_plan_week = generate_meal_plan(meal_pref, goal)
        exercises = generate_exercise_plan(activity_level)

        # Meal Plan Display
        st.markdown('<div class="card meal-card">', unsafe_allow_html=True)
        st.subheader("7-Day Personalized Meal Plan")
        for i, day_plan in enumerate(meal_plan_week, 1):
            with st.expander(f"Day {i}"):
                for meal, food in day_plan.items():
                    st.write(f"**{meal}:** {food}")
        st.markdown('</div>', unsafe_allow_html=True)

        # Exercise Plan
        st.markdown('<div class="card exercise-card">', unsafe_allow_html=True)
        st.subheader("Recommended Exercise Routine")
        for ex in exercises:
            st.write(f"- {ex}")
        st.markdown('</div>', unsafe_allow_html=True)

        # Body Projection
        st.markdown('<div class="card body-card">', unsafe_allow_html=True)
        st.subheader("Body Figure Projection")
        col_a, col_b = st.columns(2)
        with col_a:
            display_body_image(current_shape, "Current Shape")
        with col_b:
            display_body_image(target_shape, "Target Shape")
        st.markdown('</div>', unsafe_allow_html=True)

        # Report Card
        st.markdown('<div class="card report-card">', unsafe_allow_html=True)
        st.subheader("Detailed Health Report Card")
        st.write(f"**BMI:** {bmi}")
        if bmi < 18.5:
            st.write("Status: Underweight — Risk of nutritional deficiencies.")
        elif bmi < 24.9:
            st.write("Status: Normal — Healthy weight.")
        elif bmi < 29.9:
            st.write("Status: Overweight — Elevated risk of lifestyle diseases.")
        else:
            st.write("Status: Obese — High risk of cardiovascular and metabolic issues.")
        st.write(f"**Sleep:** {sleep_hours} hrs/night")
        st.write(f"**Stress Level:** {stress_level}")
        st.write(f"**Goal Chosen:** {goal}")
        st.markdown('</div>', unsafe_allow_html=True)

        # Lifestyle Tips
        st.markdown('<div class="card tips-card">', unsafe_allow_html=True)
        st.subheader("Lifestyle Recommendations")
        st.info("Stay hydrated: Aim for 2.5–3 liters/day.")
        st.info("Include protein in every meal for satiety & muscle repair.")
        st.info("Reduce processed foods & added sugars.")
        st.info("Engage in 30–40 minutes of activity daily.")
        st.info("Maintain a consistent sleep schedule.")
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# NUTRIX CHAT
# -------------------------
elif choice == "NutriX Chat":
    st.subheader("Chat with NutriX")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Optional: health issue selector
    issue = st.selectbox(
        "Select your health issue (optional, for personalized diet suggestions):",
        ["None", "Diabetes", "PCOS", "Weight Loss", "Weight Gain", "Thyroid", "General Wellness"]
    )

    # User query input
    query = st.text_area("Ask anything about health, fitness, or nutrition:")

    if st.button("Send"):
        if query.strip():
            # Construct context-aware prompt
            meal_pref = st.session_state.get("meal_pref", "General")
            goal = st.session_state.get("goal", "Maintain")
            activity_level = st.session_state.get("activity_level", "Moderately Active")

            full_prompt = f"""
            You are NutriX, a friendly and knowledgeable health assistant.
            The user prefers {meal_pref} meals, has the goal: {goal}, and activity level: {activity_level}.
            You provide evidence-based answers about health, nutrition, and wellness in a friendly tone.
            """

            if issue != "None":
                full_prompt += f"The user has {issue}. Provide safe diet and lifestyle advice accordingly.\n"

            full_prompt += f"User question: {query}\n"

            try:
                import google.generativeai as genai
                model = genai.GenerativeModel("gemini-2.5-flash")

                response = model.generate_content(full_prompt)

                st.session_state.chat_history.append(("🧑 You", query))
                st.session_state.chat_history.append(("NutriX", response.text))

            except Exception as e:
                st.error(f"Error fetching Gemini response: {e}")

    # Display conversation history
    for speaker, msg in st.session_state.chat_history:
        st.markdown(f"**{speaker}:** {msg}")


# -------------------------
# DOCTOR CHAT
# -------------------------
elif choice == "Doctors":
    st.subheader("Consult with Doctor")

    # Doctor type selection
    doc_type = st.radio("Choose Doctor Type:", ["Homeopathic", "Ayurvedic", "Allopathic"])
    st.write(f"You are chatting with a **{doc_type} Doctor**")

    # Input for user question
    question = st.text_area("Enter your health concern:")

    # Initialize Gemini doctor chat session
    if 'doctor_gemini_chat' not in st.session_state:
        st.session_state.doctor_gemini_chat = create_gemini_chat()
    
    # Initialize doctor chat history
    if 'doctor_chat_history' not in st.session_state:
        st.session_state.doctor_chat_history = []

    if st.button("Send to Doctor"):
       if question.strip():   
        # Construct Gemini prompt including doctor type
        prompt = f"You are a {doc_type} doctor. Answer the patient question in simple, clear, helpful terms. Patient asks: {question}"
        response = ask_gemini(st.session_state.doctor_gemini_chat, prompt)
        
        if response:
            # Save in chat history
            st.session_state.doctor_chat_history.append(("You", question))
            st.session_state.doctor_chat_history.append((f"{doc_type} Doctor", response))

        # Clear input after sending
        question = ""
    else:
        st.warning("Please describe your issue before sending.")

    # Display doctor chat history
    for speaker, msg in st.session_state.doctor_chat_history:
        st.markdown(f"**{speaker}:** {msg}")


# -------------------------
# HELP & CONTACT
# -------------------------
if choice == "Help & Contact":
    st.subheader("📞 Need Help?")
    st.info("You can reach out for support using the options below:")
    st.write("**Email:** support@nutrix.com")
    st.write("**Phone:** +91 12345 67890")

    # Upload file (image only)
    uploaded_file = st.file_uploader("Upload an Image (Prescription / Report)", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Convert the uploaded file into a PIL image
        image = Image.open(uploaded_file)

        if st.button("Analyze Report"):
            try:
                model = genai.GenerativeModel("gemini-2.0-flash-exp-image-generation")
                response = model.generate_content([
                    "Analyze this medical report image and summarize key findings clearly for a patient.",
                    image  # ← pass PIL image here
                ])
                st.write(response.text)
            except Exception as e:
                st.error(f"Error fetching Gemini response: {e}")
