import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from nutrition_utils import load_nutrition_data
from food_recognition import FoodRecognizer
from recipe_generator import RecipeGenerator
from disease_recommender import DiseaseRecommender
from healthy_alternatives import HealthyAlternatives
import json

# Set page config - MUST be the first Streamlit command
st.set_page_config(
    page_title="Welcome to EATelligence AI 
Your smart AI-powered food companion!
This app helps analyze food nutrition, suggest healthier alternatives, create innovative Indian food combos, and give disease-specific diet advice.",
    page_icon="🍛",
    layout="wide"
)

# Add Google Fonts and blur background
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1500&q=80");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .main-header {
        width: 100%;
        text-align: center;
        font-family: 'Pacifico', cursive;
        font-size: 2.7em;
        color: #3CB371;
        margin-top: 0.5em;
        margin-bottom: 0.5em;
        background: rgba(255,255,255,0.7);
        border-radius: 20px;
        padding: 1em;
        box-shadow: 0 4px 24px 0 rgba(44,62,80,0.07);
    }
    .health-badge {
        display: inline-block;
        padding: 0.4em 1em;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1em;
        margin: 0.2em 0.4em 0.2em 0;
    }
    .badge-green { background: #B8E0D2; color: #2C3E50; }
    .badge-yellow { background: #FFF3CD; color: #856404; }
    .badge-red { background: #F8D7DA; color: #721C24; }
    </style>
''', unsafe_allow_html=True)

# Replace header card with playful headline
st.markdown('''
    <div class="main-header">
        "The Greatest Wealth Is <span style='color:#6FCF97;'>Health</span>"
    </div>
''', unsafe_allow_html=True)

# Enhanced professional CSS
st.markdown("""
    <style>
        /* Main app background */
        .stApp {
            background-color: #E8F5E9 !important;  /* Pastel light green */
        }
        section[data-testid="stSidebar"] {
            background-color: #E8F5E9 !important;  /* Match main background */
            border-radius: 0 20px 20px 0;
        }
        .sidebar-title {
            font-size: 1.3em;
            font-weight: 600;
            color: #2C3E50;
            margin-bottom: 0.5em;
        }
        .sidebar-section {
            margin-bottom: 1.5em;
        }
        .sidebar-link {
            font-size: 1.1em;
            color: #2C3E50;
            margin-left: 0.5em;
            font-weight: 500;
        }
        .sidebar-divider {
            height: 2px;
            background: linear-gradient(90deg, #B8E0D2 0%, #95C9B9 100%);
            border-radius: 2px;
            margin: 1em 0;
        }
        .sidebar-footer {
            font-size: 0.95em;
            color: #2C3E50;
            margin-top: 2em;
            border-top: 1px solid #B8E0D2;
            padding-top: 1em;
        }
        /* Professional header card */
        .header-card {
            background: linear-gradient(90deg, #E8F5E9 60%, #B8E0D2 100%);
            box-shadow: 0 4px 24px 0 rgba(44,62,80,0.07);
            border-radius: 18px;
            padding: 32px 24px 24px 24px;
            margin-bottom: 40px;
            text-align: center;
        }
        .header-title {
            color: #2C3E50;
            font-size: 2.7em;
            font-weight: 700;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }
        .header-subtitle {
            color: #2C3E50;
            font-size: 1.3em;
            font-weight: 500;
            margin-top: 0;
            margin-bottom: 8px;
        }
        .header-desc {
            color: #2C3E50;
            font-size: 1.08em;
            margin-bottom: 0;
        }
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #B8E0D2;
            color: #2C3E50;
            border-radius: 8px 8px 0 0;
            padding: 0.7rem 1.3rem;
            font-size: 1.1em;
            font-weight: 700;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px 0 rgba(44,62,80,0.04);
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #95C9B9;
            color: #2C3E50;
        }
        .stTabs [aria-selected="true"] {
            background-color: #E8F5E9;
            color: #2C3E50;
            border-bottom: 3px solid #2C3E50;
        }
        /* Input field styling */
        .stTextInput > div > div > input {
            background-color: #FFFFFF;
            border: 2px solid #B8E0D2;
            border-radius: 8px;
            padding: 0.5rem;
            font-weight: 500;
        }
        .stSelectbox > div > div > div {
            background-color: #FFFFFF;
            border: 2px solid #B8E0D2;
            border-radius: 8px;
            font-weight: 500;
        }
        /* Pastel divider for sections */
        .pastel-divider {
            height: 3px;
            background: linear-gradient(90deg, #B8E0D2 0%, #95C9B9 100%);
            border-radius: 2px;
            margin-bottom: 1.5em;
            margin-top: 0.5em;
        }
        /* Section header spacing */
        .block-container {
            padding-top: 0.5rem;
        }
        /* Make subheaders more visible */
        h3 {
            color: #2C3E50;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        /* Make input labels more visible */
        .stTextInput > label, .stSelectbox > label {
            font-weight: 600;
            color: #2C3E50;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar content
st.sidebar.markdown("""
    <style>
        /* Remove sidebar scrollbar */
        section[data-testid="stSidebar"] > div {
            overflow: hidden !important;
        }
        .sidebar-section {
            background-color: #FFFFFF;
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1.2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        .sidebar-title {
            font-size: 1.2em;
            font-weight: 700;
            color: #2C3E50;
            margin-bottom: 0.6rem;
            display: block;
        }
        .sidebar-content {
            font-size: 0.95em;
            line-height: 1.5;
            color: #4A4A4A;
        }
        .feature-item {
            background-color: #F5F9F5;
            padding: 0.7rem;
            margin-bottom: 0.6rem;
            border-radius: 8px;
            font-weight: 500;
            color: #2C3E50;
        }
        .sidebar-divider {
            height: 1px;
            background: linear-gradient(90deg, #B8E0D2 0%, #95C9B9 100%);
            margin: 1.2rem 0;
        }
        .sidebar-footer {
            font-size: 0.9em;
            color: #4A4A4A;
            margin-top: 1.5rem;
            padding-top: 0.8rem;
            border-top: 1px solid #B8E0D2;
        }
        .project-note {
            font-size: 0.95em;
            color: #2C8A7D;
            text-align: center;
            margin-top: 1.5rem;
            padding-top: 0.8rem;
            border-top: 1px solid #B8E0D2;
            font-style: italic;
            font-weight: 500;
            line-height: 1.4;
        }
    </style>
    
    <div class="sidebar-section">
        <span class="sidebar-title">About</span>
        <div class="sidebar-content">
            EATelligence AI is an AI-powered food analyzer and recommendation system designed to promote healthy eating habits. The app enables users to analyze nutritional content in real-time, receive healthier food alternatives, and explore AI-driven innovative food blends using traditional Indian ingredients. It also offers personalized meal suggestions tailored to common lifestyle diseases, helping users make informed and balanced dietary choices.
        </div>
    </div>
    
    <div class="sidebar-divider"></div>
    
    <div class="sidebar-section">
        <span class="sidebar-title">Key Features</span>
        <div class="feature-item">Food Analyzer</div>
        <div class="feature-item">AI-Based Food Innovation</div>
        <div class="feature-item">Disease-Specific Diets</div>
        <div class="feature-item">Healthier Alternatives</div>
    </div>
    
    <div class="sidebar-footer">
        <b>Developed by:</b><br>
        Pakhi Singh Tak<br>
        Ilansha Singh Sisodia
    </div>
    
    <div class="project-note">
        This project has been developed as part of a B.Tech Final Year Project
    </div>
""", unsafe_allow_html=True)

# Professional header card
st.markdown("""
    <div class="header-card">
        <div class="header-title">Welcome to EATelligence AI</div>
        <div class="header-subtitle">Your smart AI-powered food companion!</div>
        <div class="header-desc">This app helps analyze food nutrition, suggest healthier alternatives, create innovative Indian food combos, and give disease-specific diet advice.</div>
    </div>
""", unsafe_allow_html=True)

# Add a gap between header and tabs
st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def load_components():
    return {
        'nutrition_data': load_nutrition_data(),
        'food_recognizer': FoodRecognizer(),
        'recipe_generator': RecipeGenerator(),
        'disease_recommender': DiseaseRecommender(),
        'healthy_alternatives': HealthyAlternatives()
    }

components = load_components()

# Create tabs
food_tab, recipe_tab, disease_tab, alt_tab = st.tabs([
    "🍽️ Food Analyzer",
    "🧪 AI-Based Food Innovation",
    "🩺 Disease-Specific Diets",
    "🥗 Healthier Alternatives"
])

# Pastel divider HTML (now using class for consistency)
pastel_divider = "<div class='pastel-divider'></div>"

# Food Analyzer Tab
with food_tab:
    st.subheader("🍽️ Food Analyzer")
    st.markdown(pastel_divider, unsafe_allow_html=True)
    food_name = st.text_input("Enter food name")
    uploaded_file = st.file_uploader("Or upload a food image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        result = components['food_recognizer'].process_image(image)
        if result:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(result['display_image'], caption="Uploaded Food Image", use_column_width=True)
            with col2:
                if 'name' in result:
                    st.markdown(f"**Recognized Food:** {result['name']}")
                    st.markdown("**Nutrition Information:**")
                    st.markdown(f"- Calories: {result['calories']} kcal")
                    st.markdown(f"- Protein: {result['protein']}g")
                    st.markdown(f"- Fat: {result['fat']}g")
                    st.markdown(f"- Carbohydrates: {result['carbs']}g")
                    macronutrients = pd.DataFrame({
                        'Nutrient': ['Protein', 'Fat', 'Carbs'],
                        'Amount': [result['protein'], result['fat'], result['carbs']]
                    })
                    fig = px.pie(
                        macronutrients,
                        values='Amount',
                        names='Nutrient',
                        title="Macronutrient Distribution",
                        color_discrete_sequence=['#FF6B6B', '#B8E0D2', '#95C9B9']
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    # --- Health Impact Assessment ---
                    st.markdown("<h4>Health Impact Assessment</h4>", unsafe_allow_html=True)
                    assessment, badges = get_health_impact_assessment(result)
                    st.markdown(f"<div style='margin-bottom:0.5em;'>{assessment}</div>", unsafe_allow_html=True)
                    st.markdown(' '.join(badges), unsafe_allow_html=True)
                else:
                    st.warning("Could not recognize the food in the image. Please try another image or use the text input.")

# AI-Based Food Innovation Tab
with recipe_tab:
    st.subheader("🧪 AI-Based Food Innovation")
    st.markdown(pastel_divider, unsafe_allow_html=True)
    
    # Define ingredient combinations and their innovations
    food_innovations = {
        "Ragi-Nutri Bar": {
            "ingredients": ["Ragi (Finger Millet)", "Jaggery", "Almonds", "Flaxseeds", "Curd"],
            "why": [
                "Ragi & Almond Flour (Rich in calcium & protein)",
                "Jaggery & Dates (Natural sweeteners, rich in iron)",
                "Flaxseeds (Omega-3 & fiber boost)",
                "Curd-based fermentation (Probiotic benefits for gut health)"
            ],
            "outcome": "A healthier alternative to processed energy bars, offering high nutrition with traditional Indian flavors while catering to fitness-conscious individuals and those with lifestyle diseases like diabetes."
        },
        "Foxtail Moong Protein Dosa": {
            "ingredients": ["Foxtail millet", "Moong dal", "Chia seeds", "Curry leaves"],
            "why": [
                "Foxtail millet (Gluten-free, high in fiber)",
                "Moong dal (Rich in plant-based protein)",
                "Chia seeds (Omega-3 & antioxidants)",
                "Curry leaves (Iron & digestive benefits)"
            ],
            "outcome": "A crispy, high-protein, gut-friendly dosa with a healthier nutrient profile than regular rice-based dosa. Ideal for diabetics and weight-conscious individuals."
        },
        "Makhana Beetroot Choco Shake": {
            "ingredients": ["Makhana (fox nuts)", "Dark cocoa", "Beetroot powder", "Dates", "Almonds"],
            "why": [
                "Makhana (Low-calorie, high in calcium & protein)",
                "Beetroot powder (Iron-rich, great for hemoglobin)",
                "Dark cocoa (Antioxidants & heart health)",
                "Dates & almonds (Natural sweetness & healthy fats)"
            ],
            "outcome": "A nutrient-dense, caffeine-free chocolate shake that can be a great energy booster for kids, anemic patients, and fitness enthusiasts."
        },
        "Quinoa Paneer Power Bowl": {
            "ingredients": ["Quinoa", "Paneer", "Spinach", "Turmeric", "Ginger"],
            "why": [
                "Quinoa (Complete protein, high in fiber)",
                "Paneer (Rich in calcium and protein)",
                "Spinach (Iron and vitamin K powerhouse)",
                "Turmeric & Ginger (Anti-inflammatory and digestive benefits)"
            ],
            "outcome": "A balanced, protein-rich bowl that combines the goodness of plant and dairy proteins, perfect for muscle building and maintaining bone health."
        },
        "Bajra Berry Smoothie Bowl": {
            "ingredients": ["Bajra (Pearl Millet)", "Mixed Berries", "Yogurt", "Honey", "Chia Seeds"],
            "why": [
                "Bajra (Rich in iron and magnesium)",
                "Mixed Berries (Antioxidants and vitamin C)",
                "Yogurt (Probiotics and protein)",
                "Honey & Chia Seeds (Natural energy and omega-3)"
            ],
            "outcome": "A refreshing, nutrient-packed smoothie bowl that provides sustained energy, supports gut health, and helps in managing blood sugar levels."
        },
        "Jowar Methi Roti": {
            "ingredients": ["Jowar (Sorghum)", "Methi (Fenugreek)", "Ajwain", "Ghee", "Curd"],
            "why": [
                "Jowar (Gluten-free, rich in fiber and minerals)",
                "Methi (Blood sugar control, digestive aid)",
                "Ajwain (Digestive health, anti-inflammatory)",
                "Curd (Probiotics, protein source)"
            ],
            "outcome": "A nutritious, gluten-free roti that helps in managing diabetes, aids digestion, and provides sustained energy. Perfect for those with gluten sensitivity and diabetes."
        },
        "Sprouted Moong Chaat": {
            "ingredients": ["Sprouted Moong", "Pomegranate", "Cucumber", "Mint", "Lemon"],
            "why": [
                "Sprouted Moong (Enhanced protein and enzyme content)",
                "Pomegranate (Antioxidants and heart health)",
                "Cucumber (Hydration and low calories)",
                "Mint & Lemon (Digestive aid and vitamin C)"
            ],
            "outcome": "A refreshing, protein-rich chaat that's perfect for weight management, provides essential nutrients, and helps in maintaining gut health."
        },
        "Oats Idli with Sambar": {
            "ingredients": ["Oats", "Urad Dal", "Vegetables", "Sambar Powder", "Coconut"],
            "why": [
                "Oats (Beta-glucan for heart health)",
                "Urad Dal (Complete protein source)",
                "Vegetables (Fiber and micronutrients)",
                "Sambar Powder (Digestive spices)"
            ],
            "outcome": "A heart-healthy twist to traditional idli, rich in fiber and protein, perfect for breakfast or light meals. Helps in managing cholesterol and blood sugar levels."
        },
        "Ragi Ladoo": {
            "ingredients": ["Ragi Flour", "Jaggery", "Dry Fruits", "Ghee", "Cardamom"],
            "why": [
                "Ragi (Calcium and iron rich)",
                "Jaggery (Natural sweetener with minerals)",
                "Dry Fruits (Healthy fats and protein)",
                "Cardamom (Digestive aid)"
            ],
            "outcome": "A nutritious sweet treat that provides energy, supports bone health, and is perfect for growing children and pregnant women. A healthier alternative to traditional sweets."
        },
        "Bajra Khichdi": {
            "ingredients": ["Bajra", "Moong Dal", "Vegetables", "Ghee", "Spices"],
            "why": [
                "Bajra (Rich in iron and magnesium)",
                "Moong Dal (Easy to digest protein)",
                "Vegetables (Fiber and vitamins)",
                "Spices (Digestive and anti-inflammatory)"
            ],
            "outcome": "A wholesome, one-pot meal that's perfect for all age groups. Provides complete nutrition, aids digestion, and helps in maintaining energy levels throughout the day."
        },
        "Whole Wheat Cauliflower Pizza": {
            "ingredients": ["Whole Wheat Flour", "Cauliflower", "Low-fat Cheese", "Fresh Vegetables", "Herbs"],
            "why": [
                "Whole Wheat Flour (High fiber, complex carbs)",
                "Cauliflower Base (Low-calorie, vitamin-rich)",
                "Low-fat Cheese (Reduced saturated fat)",
                "Fresh Vegetables (Antioxidants and fiber)"
            ],
            "outcome": "A guilt-free pizza alternative that's high in fiber and nutrients while being lower in calories and fat. Perfect for weight management and maintaining healthy cholesterol levels."
        },
        "Quinoa Pasta Primavera": {
            "ingredients": ["Quinoa Pasta", "Fresh Vegetables", "Olive Oil", "Herbs", "Parmesan"],
            "why": [
                "Quinoa Pasta (Complete protein, gluten-free)",
                "Fresh Vegetables (Fiber and micronutrients)",
                "Olive Oil (Heart-healthy fats)",
                "Herbs (Antioxidants and flavor)"
            ],
            "outcome": "A protein-rich pasta dish that's gluten-free and packed with nutrients. Ideal for those with gluten sensitivity and anyone looking for a healthier pasta option."
        },
        "Lentil Burger with Sweet Potato Bun": {
            "ingredients": ["Lentils", "Sweet Potato", "Quinoa", "Vegetables", "Spices"],
            "why": [
                "Lentils (Plant-based protein, iron)",
                "Sweet Potato (Complex carbs, vitamin A)",
                "Quinoa (Complete protein, fiber)",
                "Vegetables (Fiber and antioxidants)"
            ],
            "outcome": "A nutritious burger alternative that's high in protein and fiber while being lower in calories and fat. Perfect for vegetarians and health-conscious individuals."
        }
    }
    
    # Display food innovations
    selected_innovation = st.selectbox(
        "Your go-to Healthy food",
        list(food_innovations.keys())
    )
    
    if selected_innovation:
        innovation = food_innovations[selected_innovation]
        
        # Display ingredients
        st.subheader("✅ Ingredients Analyzed:")
        for ingredient in innovation["ingredients"]:
            st.write(f"- {ingredient}")
        
        # Display why
        st.subheader("✅ Why?")
        for reason in innovation["why"]:
            st.write(f"- {reason}")
        
        # Display outcome
        st.subheader("🔹 Outcome:")
        st.write(innovation["outcome"])
        
        # Add a note about the innovation
        st.info("💡 This AI-suggested food innovation combines traditional ingredients with modern nutritional science to create healthier alternatives to conventional foods.")

# Disease-Specific Diets Tab
with disease_tab:
    st.subheader("🩺 Disease-Specific Diets")
    st.markdown(pastel_divider, unsafe_allow_html=True)
    
    # Define disease-specific diets
    disease_diets = {
        "Diabetes": {
            "recommended": [
                "Whole grains (bajra, jowar, ragi)",
                "Vegetables (bitter gourd, fenugreek, spinach)",
                "Legumes (moong dal, chana dal)",
                "Nuts and seeds (almonds, flaxseeds)",
                "Low-fat dairy (curd, buttermilk)",
                "Vegetarian protein sources (tofu, paneer, legumes)",
                "Vegetable-based soups and salads",
                "Sprouted grains and pulses",
                "Quinoa and millet-based dishes",
                "Vegetable curries with minimal oil",
                "Lentil-based dishes (dal, khichdi)",
                "Vegetable pulao with brown rice",
                "Grilled fish (2-3 times a week)",
                "Egg whites (2-3 times a week)",
                "Lean chicken (1-2 times a week)"
            ],
            "avoid": [
                "Refined carbohydrates",
                "Sugary foods and drinks",
                "Processed foods",
                "High-fat dairy products",
                "Fried foods",
                "Sweetened beverages",
                "White rice and maida products",
                "Red meat",
                "Processed meats"
            ],
            "tips": [
                "Eat small, frequent meals",
                "Include protein with every meal",
                "Choose low glycemic index foods",
                "Stay hydrated with water and herbal teas",
                "Include fiber-rich vegetables",
                "Opt for plant-based protein sources",
                "Use healthy cooking methods (steaming, grilling)",
                "Include sprouted salads",
                "Try vegetable-based smoothies",
                "Balance vegetarian and non-vegetarian proteins"
            ]
        },
        "Hypertension": {
            "recommended": [
                "Fresh fruits and vegetables",
                "Whole grains",
                "Low-fat dairy products",
                "Plant-based proteins (legumes, nuts)",
                "Herbs and spices (garlic, turmeric)",
                "Vegetable soups and salads",
                "Sprouted grains",
                "Leafy greens",
                "Vegetable stir-fries",
                "Lentil-based dishes",
                "Vegetable pulao",
                "Grilled vegetable dishes",
                "Grilled fish (2-3 times a week)",
                "Egg whites (2-3 times a week)",
                "Lean chicken (1-2 times a week)"
            ],
            "avoid": [
                "Processed foods",
                "Canned foods",
                "Pickles and papads",
                "High-sodium foods",
                "Fried foods",
                "Processed meats",
                "Salted snacks",
                "Red meat",
                "High-sodium processed foods"
            ],
            "tips": [
                "Limit salt intake",
                "Read food labels",
                "Cook at home",
                "Use herbs for flavor",
                "Choose fresh over processed",
                "Include potassium-rich foods",
                "Stay hydrated with water",
                "Try vegetable-based smoothies",
                "Include sprouted salads",
                "Balance vegetarian and non-vegetarian proteins"
            ]
        },
        "Heart Disease": {
            "recommended": [
                "Whole grains",
                "Fresh fruits and vegetables",
                "Legumes and pulses",
                "Nuts and seeds",
                "Low-fat dairy",
                "Plant-based proteins",
                "Vegetable-based soups",
                "Sprouted grains",
                "Vegetable curries",
                "Lentil-based dishes",
                "Vegetable pulao",
                "Grilled vegetable dishes",
                "Grilled fish (2-3 times a week)",
                "Egg whites (2-3 times a week)",
                "Lean chicken (1-2 times a week)"
            ],
            "avoid": [
                "Fried foods",
                "Processed foods",
                "High-fat dairy",
                "Red meat",
                "Sugary foods",
                "Refined carbohydrates",
                "High-sodium foods",
                "Processed meats",
                "High-fat animal products"
            ],
            "tips": [
                "Choose healthy fats",
                "Eat fiber-rich foods",
                "Limit salt intake",
                "Stay active",
                "Maintain healthy weight",
                "Include omega-3 rich foods",
                "Opt for plant-based meals",
                "Try vegetable-based smoothies",
                "Include sprouted salads",
                "Balance vegetarian and non-vegetarian proteins"
            ]
        },
        "Obesity": {
            "recommended": [
                "High-fiber vegetables",
                "Whole grains",
                "Lean proteins (legumes, tofu)",
                "Low-fat dairy",
                "Fresh fruits",
                "Vegetable soups",
                "Sprouted grains",
                "Plant-based proteins",
                "Vegetable stir-fries",
                "Lentil-based dishes",
                "Vegetable pulao",
                "Grilled vegetable dishes",
                "Grilled fish (2-3 times a week)",
                "Egg whites (2-3 times a week)",
                "Lean chicken (1-2 times a week)"
            ],
            "avoid": [
                "Processed foods",
                "Sugary drinks",
                "Fried foods",
                "High-fat dairy",
                "Refined carbohydrates",
                "Sweetened foods",
                "High-calorie snacks",
                "Red meat",
                "Processed meats"
            ],
            "tips": [
                "Control portion sizes",
                "Eat slowly",
                "Stay hydrated",
                "Include protein in meals",
                "Choose whole foods",
                "Plan meals ahead",
                "Opt for plant-based options",
                "Try vegetable-based smoothies",
                "Include sprouted salads",
                "Balance vegetarian and non-vegetarian proteins"
            ]
        }
    }
    
    # Disease selection
    diseases = ["diabetes", "heart_disease", "hypertension", "obesity", "pcos", "thyroid", "arthritis"]
    disease_names = {
        "diabetes": "Diabetes",
        "heart_disease": "Heart Disease",
        "hypertension": "Hypertension",
        "obesity": "Obesity",
        "pcos": "PCOS",
        "thyroid": "Thyroid Disorders",
        "arthritis": "Arthritis"
    }
    
    selected_disease = st.selectbox(
        "Select a health condition",
        diseases,
        format_func=lambda x: disease_names[x]
    )
    
    # Get daily calorie target
    daily_calories = st.slider(
        "Daily Calorie Target",
        min_value=1200,
        max_value=3000,
        value=2000,
        step=100
    )
    
    if st.button("Generate Diet Plan"):
        diet_plan = components['disease_recommender'].get_diet_plan(selected_disease, daily_calories)
        
        if diet_plan and 'description' in diet_plan:
            st.subheader(f"Diet Plan for {disease_names[selected_disease]}")
            st.info(diet_plan['description'])
            
            # Display meals
            st.subheader("Daily Meal Plan")
            for meal_type, meal_info in diet_plan['meals'].items():
                with st.expander(f"{meal_type.title()} ({int(daily_calories * components['disease_recommender'].meal_types[meal_type])} calories)"):
                    st.write("Foods:")
                    for food in meal_info['foods']:
                        st.write(f"- {food}")
                    
                    st.write("Nutritional Information:")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Calories", f"{meal_info['nutrition']['calories']:.0f}")
                    with col2:
                        st.metric("Protein", f"{meal_info['nutrition']['protein']:.1f}g")
                    with col3:
                        st.metric("Fat", f"{meal_info['nutrition']['fat']:.1f}g")
                    with col4:
                        st.metric("Carbs", f"{meal_info['nutrition']['carbs']:.1f}g")
            
            # Display nutritional summary
            st.subheader("Daily Nutritional Summary")
            summary = diet_plan['nutritional_summary']
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Calories", f"{summary['calories']:.0f}")
            with col2:
                st.metric("Total Protein", f"{summary['protein']:.1f}g")
            with col3:
                st.metric("Total Fat", f"{summary['fat']:.1f}g")
            with col4:
                st.metric("Total Carbs", f"{summary['carbs']:.1f}g")
            
            # Display suitable foods
            st.subheader("Suitable Foods")
            suitable_foods = components['disease_recommender'].get_suitable_foods(selected_disease)
            st.dataframe(suitable_foods[['Food', 'Calories', 'Protein', 'Fat', 'Carbs']])
        else:
            st.error("Could not generate diet plan. Please try again.")

# Healthier Alternatives Tab
with alt_tab:
    st.subheader("🥗 Healthier Alternatives")
    st.markdown(pastel_divider, unsafe_allow_html=True)
    
    # Food input
    food_name = st.text_input("Enter a food item to find healthier alternatives")
    
    if food_name:
        alternatives = components['healthy_alternatives'].get_alternatives(food_name)
        if alternatives is not None:
            # Convert list to DataFrame if needed
            if isinstance(alternatives, list):
                if not alternatives:  # Check if list is empty
                    st.error("Could not find healthier alternatives for this food.")
                else:
                    # Convert list to DataFrame
                    alternatives_df = pd.DataFrame(alternatives)
                    st.subheader("Healthier Alternatives")
                    st.dataframe(alternatives_df)
                    
                    # Create comparison chart
                    try:
                        # Ensure column names match the DataFrame
                        if 'name' in alternatives_df.columns:
                            x_column = 'name'
                        elif 'Food' in alternatives_df.columns:
                            x_column = 'Food'
                        else:
                            st.error("Could not find food name column in the data")
                            x_column = None
                        
                        if x_column:
                            fig = px.bar(
                                alternatives_df,
                                x=x_column,
                                y=['Calories', 'Protein', 'Fat', 'Carbs'],
                                title="Nutritional Comparison",
                                barmode='group',
                                color_discrete_sequence=['#FF6B6B', '#B8E0D2', '#95C9B9', '#F8E8E8']
                            )
                            st.plotly_chart(fig)
                    except Exception as e:
                        st.error(f"Error creating comparison chart: {str(e)}")
            else:
                # Handle DataFrame case
                if not alternatives.empty:
                    st.subheader("Healthier Alternatives")
                    st.dataframe(alternatives)
                    
                    # Create comparison chart
                    try:
                        # Ensure column names match the DataFrame
                        if 'name' in alternatives.columns:
                            x_column = 'name'
                        elif 'Food' in alternatives.columns:
                            x_column = 'Food'
                        else:
                            st.error("Could not find food name column in the data")
                            x_column = None
                        
                        if x_column:
                            fig = px.bar(
                                alternatives,
                                x=x_column,
                                y=['Calories', 'Protein', 'Fat', 'Carbs'],
                                title="Nutritional Comparison",
                                barmode='group',
                                color_discrete_sequence=['#FF6B6B', '#B8E0D2', '#95C9B9', '#F8E8E8']
                            )
                            st.plotly_chart(fig)
                    except Exception as e:
                        st.error(f"Error creating comparison chart: {str(e)}")
                else:
                    st.error("Could not find healthier alternatives for this food.")
        else:
            st.error("Could not find healthier alternatives for this food.")

def show_recipe_generator():
    st.subheader("AI Recipe Generator")
    st.write("Get personalized recipe suggestions based on your available ingredients!")
    
    # Get user input
    ingredients = st.text_input("Enter ingredients (comma-separated):")
    cuisine = st.selectbox("Select cuisine type:", ["Indian", "Italian", "Chinese", "Mexican", "Mediterranean"])
    
    if st.button("Generate Recipe"):
        if ingredients:
            with st.spinner("Generating your recipe..."):
                try:
                    recipe = components['recipe_generator'].generate_recipe(
                        ingredients=[i.strip() for i in ingredients.split(',')],
                        cuisine=cuisine
                    )
                    
                    if isinstance(recipe, str):
                        try:
                            recipe = json.loads(recipe)
                        except json.JSONDecodeError:
                            st.error("Error parsing recipe data. Please try again.")
                            return
                    
                    # Display recipe
                    st.success("Here's your personalized recipe!")
                    
                    # Recipe name
                    st.markdown(f"### {recipe['name']}")
                    
                    # Ingredients
                    st.markdown("#### Ingredients:")
                    for ingredient in recipe['ingredients']:
                        st.write(f"- {ingredient}")
                    
                    # Instructions
                    st.markdown("#### Instructions:")
                    for i, step in enumerate(recipe['instructions'], 1):
                        st.write(f"{i}. {step}")
                    
                    # Nutrition info
                    st.markdown("#### Nutritional Information:")
                    nutrition = recipe.get('nutrition', {})
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Calories", f"{nutrition.get('calories', 'N/A')} kcal")
                    with col2:
                        st.metric("Protein", f"{nutrition.get('protein', 'N/A')}g")
                    with col3:
                        st.metric("Carbs", f"{nutrition.get('carbs', 'N/A')}g")
                    with col4:
                        st.metric("Fat", f"{nutrition.get('fat', 'N/A')}g")
                    
                    # Health benefits
                    st.markdown("#### Health Benefits:")
                    for benefit in recipe.get('health_benefits', []):
                        st.write(f"- {benefit}")
                        
                except Exception as e:
                    st.error(f"Error generating recipe: {str(e)}")
        else:
            st.warning("Please enter at least one ingredient.")

# Add the health impact assessment function

def get_health_impact_assessment(nutrition):
    # Simple rules for demonstration
    calories = nutrition.get('calories', 0)
    protein = nutrition.get('protein', 0)
    fat = nutrition.get('fat', 0)
    carbs = nutrition.get('carbs', 0)
    assessment = []
    badges = []
    if calories < 120:
        assessment.append("Low in calories. Good for weight management.")
        badges.append("<span class='health-badge badge-green'>Low Calorie</span>")
    elif calories < 250:
        assessment.append("Moderate calories. Suitable for most diets.")
        badges.append("<span class='health-badge badge-yellow'>Moderate Calorie</span>")
    else:
        assessment.append("High in calories. Consume in moderation.")
        badges.append("<span class='health-badge badge-red'>High Calorie</span>")
    if protein > 5:
        assessment.append("Good source of protein.")
        badges.append("<span class='health-badge badge-green'>High Protein</span>")
    if fat > 10:
        assessment.append("High in fat. Limit intake if on a low-fat diet.")
        badges.append("<span class='health-badge badge-red'>High Fat</span>")
    if carbs > 30:
        assessment.append("High in carbohydrates. Suitable for energy needs.")
        badges.append("<span class='health-badge badge-yellow'>High Carbs</span>")
    return ' '.join(assessment), badges
