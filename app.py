# app.py
import streamlit as st
import numpy as np
from pathlib import Path
from PIL import Image

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="NutriBot: The Secret to Your Health", layout="wide")

# -------------------------
# Custom CSS Styling
# -------------------------
st.markdown("""
<style>
    body { background-color: #E6E6FA; font-family: "Helvetica Neue", sans-serif; }
    h1.title {
        font-size: 70px;
        font-weight: 900;
        color: #6a4b9c;
        text-align: center;
        margin-bottom: 1rem;
    }
    .card { padding: 1.5rem; margin-bottom: 1.5rem; border-radius: 16px;
            box-shadow: 0px 6px 16px rgba(0,0,0,0.08); color: #1a202c; background-color: #F5F0FA; }
    .meal-card { background-color: #F8E6FF; }
    .exercise-card { background-color: #E6FAF8; }
    .body-card { background-color: #F0E6FF; }
    .report-card { background-color: #E6F8FA; }
    .tips-card { background-color: #FFF0E6; }
    .input-card { background-color: #F5F0FA; padding: 1.5rem; margin-bottom: 1.5rem;
                  border-radius: 16px; box-shadow: 0px 6px 16px rgba(0,0,0,0.08); }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Helper Functions
# -------------------------
def calculate_bmi(weight, height):
    height_m = height / 100
    return round(weight / (height_m**2), 1)

def generate_meal_plan(preference):
    options = {
        "Breakfast": {
            "Vegan": ["Oatmeal (~150-200 kcal)", "Smoothie (~200-400 kcal)", "Tofu scramble (~100-365 kcal)", "Overnight oats with chia seeds (~280-545 kcal)", "Sprouted moong dal chilla (~160 kcal per 2 medium)"],
            "Vegetarian": ["Yogurt & fruits (~75-150 kcal)", "Sprouts salad (~100-200 kcal)", "Moong dal chilla (~120-130 kcal)", "Upma (~150-200 kcal)", "Poha (~150-200 kcal)"],
            "Non-Veg": ["Egg omelette (~220-300 kcal)", "Chicken toast (~277-337 kcal)", "Chicken oats porridge (~370-400 kcal)", "Salmon and avocado toast (~245-270 kcal)", "Green omelette with chicken sausage (~370-660 kcal)"],
            "Eggetarian": ["Boiled eggs (~65-75 kcal per medium egg)", "Masala egg bhurji (~120-150 kcal)", "Egg omelette (~220-300 kcal)", "Egg and cheese sandwich (~340 kcal)", "Vegetable omelette (~106 kcal)"]
        },
        "Lunch": {
            "Vegan": ["Quinoa salad (~300-450 kcal)", "Lentil curry (~350-500 kcal)", "Tofu curry (~250-350 kcal)", "Black bean quinoa bowl (~350-450 kcal)", "Stuffed bell peppers (~250-350 kcal)"],
            "Vegetarian": ["Roasted vegetable and bean salad (~200-350 kcal)", "Veg biryani (~450-550 kcal)", "Rajma rice (~300-400 kcal)", "Mixed dal with roti (~350-450 kcal)", "Matar paneer with roti (~400 kcal)"],
            "Non-Veg": ["Grilled chicken (~188 kcal)", "Salmon salad (~323 kcal)", "Tandoori chicken (~145 kcal)", "Chicken curry with rice (~490 kcal)", "Chicken stir-fry with vegetables (~250-400 kcal)"],
            "Eggetarian": ["Egg curry (~200-250 kcal)", "Egg salad (~200-350 kcal)", "Boiled eggs and sprouts salad (~180-250 kcal)", "Masala egg bhurji with roti (~220-250 kcal)", "Egg and veggie wrap (~300-400 kcal)"]
        },
        "Snack": {
            "Vegan": ["Chana Masala (~400-500 kcal)", "Nuts (~160-200 kcal)", "Roasted chickpeas (~135 kcal)", "Edamame (~90 kcal)", "Fruit chaat (~100-200 kcal)"],
            "Vegetarian": ["Roasted chickpeas (~135 kcal)", "Chana Masala (~400-500 kcal)", "Moong dal dahi vada (~150-200 kcal)", "Whole wheat methi khakhra (~50 kcal)", "Sprouts chaat (~100-200 kcal)"],
            "Non-Veg": ["Boiled eggs (~65-75 kcal)", "Chicken sticks (~100-200 kcal)", "Tandoori chicken tikka (~100-150 kcal)", "Chicken and vegetable skewers (~150-250 kcal)", "Egg bhurji (~120-150 kcal)"],
            "Eggetarian": ["Boiled eggs (~65-75 kcal)", "Roasted vegetable and bean salad (~200-350 kcal)", "Masala egg bhurji (~120-150 kcal)", "Egg salad sandwich (~150-200 kcal)", "Quinoa egg muffins (~150-200 kcal)"]
        },
        "Dinner": {
            "Vegan": ["Veg stir fry (~320 kcal)", "Lentil soup (~280 kcal)", "Quinoa & roasted veggies (~350 kcal)", "Chickpea curry with brown rice (~400 kcal)", "Grilled tofu with salad (~310 kcal)"],
            "Vegetarian": ["Veg curry (~340 kcal)", "Grilled vegetables (~300 kcal)", "Paneer & spinach curry (~380 kcal)", "Vegetable khichdi (~360 kcal)", "Mushroom soup with whole wheat bread (~330 kcal)"],
            "Non-Veg": ["Baked fish (~350 kcal)", "Grilled chicken (~370 kcal)", "Chicken & vegetable stew (~390 kcal)", "Salmon with quinoa (~420 kcal)", "Turkey stir fry (~400 kcal)"],
            "Eggetarian": ["Egg curry (~350 kcal)", "Omelette with salad (~300 kcal)", "Egg fried rice (~400 kcal)", "Scrambled eggs with spinach (~320 kcal)", "Boiled eggs with roasted veggies (~280 kcal)"]
        }
    }

    plan = []
    for _ in range(7):
        day = {}
        for meal in ["Breakfast","Lunch","Snack","Dinner"]:
            day[meal] = np.random.choice(options[meal][preference])
        plan.append(day)
    return plan

def generate_exercise_plan(level):
    mapping = {
        "Sedentary": ["Light walking 20 min","Stretching 10 min"],
        "Lightly Active": ["Brisk walking 30 min","Yoga 20 min","Light bodyweight exercises 15 min"],
        "Moderately Active": ["Jogging 30 min","Bodyweight workout 20 min","Cycling 20 min"],
        "Active": ["Running 30 min","Strength training 30 min","Swimming 20 min"],
        "Very Active": ["HIIT 30 min","Gym full-body 45 min","Running or cycling 45 min"]
    }
    return mapping.get(level, ["Walking","Stretching"])

# -------------------------
# Body Image Loader (absolute paths)
# -------------------------
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
            st.image(img, caption=label, width="stretch")
        except Exception as e:
            st.error(f"Error opening {img_path.name}: {e}")
    else:
        st.warning(f"Image for {shape_name} not found at {img_path}")

# -------------------------
# Input Section
# -------------------------
st.markdown('<h1 class="title">NutriBot: The Secret of Your Health</h1>', unsafe_allow_html=True)

st.markdown('<div class="input-card">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", 10, 100, 25)
    height = st.number_input("Height (cm)", 120, 220, 170)
    weight = st.number_input("Weight (kg)", 30, 200, 70)
    activity_level = st.selectbox("Activity Level", ["Sedentary","Lightly Active","Moderately Active","Active","Very Active"])
    meal_pref = st.selectbox("Meal Preference", ["Vegan","Vegetarian","Non-Veg","Eggetarian"])
with col2:
    sleep_hours = st.slider("Average Sleep per Night (hours)", 4, 12, 7)
    stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])
    current_shape = st.selectbox("Current Body Shape", ["Slim","Athletic","Average","Overweight","Obese"])
    target_shape = st.selectbox("Target Body Shape", ["Slim","Athletic","Average","Overweight","Obese"])
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Generate Report
# -------------------------
if st.button("Generate Health Report"):
    bmi = calculate_bmi(weight,height)
    meal_plan = generate_meal_plan(meal_pref)
    exercises = generate_exercise_plan(activity_level)

    # Meal Plan
    st.markdown('<div class="card meal-card">', unsafe_allow_html=True)
    st.subheader("7-Day Personalized Meal Plan")
    for i, day in enumerate(meal_plan, 1):
        with st.expander(f"Day {i}"):
            for meal, food in day.items():
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
    col_a,col_b = st.columns(2)
    with col_a:
        display_body_image(current_shape, "Current Shape")
    with col_b:
        display_body_image(target_shape, "Target Shape")
    st.markdown('</div>', unsafe_allow_html=True)

    # Health Report Card
    st.markdown('<div class="card report-card">', unsafe_allow_html=True)
    st.subheader("Detailed Health Report Card")
    st.write(f"**BMI:** {bmi}")
    if bmi < 18.5: st.write("Status: Underweight — Risk of nutritional deficiencies.")
    elif bmi < 24.9: st.write("Status: Normal — Healthy weight.")
    elif bmi < 29.9: st.write("Status: Overweight — Elevated risk of lifestyle diseases.")
    else: st.write("Status: Obese — High risk of cardiovascular and metabolic issues.")
    
    st.write(f"**Sleep:** {sleep_hours} hrs/night")
    st.write(f"**Stress Level:** {stress_level}")
    
    # Health Score
    score = 0
    score += 30 if 18.5 <= bmi <= 24.9 else (20 if 25 <= bmi <= 29.9 else 10)
    activity_points = {"Sedentary":5,"Lightly Active":15,"Moderately Active":25,"Active":30,"Very Active":35}
    score += activity_points.get(activity_level,0)
    if 7 <= sleep_hours <= 8: score += 20
    elif 6 <= sleep_hours < 7 or 8 < sleep_hours <= 9: score += 10
    else: score += 5
    stress_points = {"Low":15,"Medium":10,"High":5}
    score += stress_points.get(stress_level,0)
    score = min(score,100)
    st.write(f"**Health Score:** {score}/100")
    st.progress(score)
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
