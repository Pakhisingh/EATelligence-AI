import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from nutrition_utils import load_nutrition_data, get_nutrition_info, assess_health_impact
from food_recognition import FoodRecognizer
from recipe_generator import RecipeGenerator
from disease_recommender import DiseaseRecommender
from healthy_alternatives import HealthyAlternatives
import json

# Set page config - MUST be the first Streamlit command
st.set_page_config(
    page_title="EATelligence AI",
    page_icon="🍛",
    layout="wide"
)

# Custom CSS for the entire app
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: #F0F7F0 !important;  /* Very light pastel green */
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)),
                    url('https://images.unsplash.com/photo-1498837167922-ddd27525d352?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        padding: 40px 20px;
        margin: -20px -20px 20px -20px;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', cursive;
        color: #2E7D32;
        font-size: 2.8em;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        font-weight: bold;
        letter-spacing: 1px;
    }
    
    .header-subtitle {
        color: #666;
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 20px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: rgba(255, 255, 255, 0.9);
    }
    
    .sidebar-content {
        background-color: rgba(46, 125, 50, 0.1);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .sidebar-title {
        color: #2E7D32;
        font-size: 1.2em;
        margin-bottom: 10px;
    }
    
    /* Hide Streamlit warnings */
    .stDeployButton {
        display: none;
    }
    
    /* Hide secrets warning */
    .stAlert {
        display: none;
    }
    
    /* Content area styling */
    .main-content {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Remove white box from health impact */
    .health-impact {
        background-color: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">Welcome to EATelligence AI! Discover the Nutritional Secrets of Your Food</h1>
    <p class="header-subtitle">Your AI-powered nutrition and diet planning assistant</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content" style='margin-bottom: 30px;'>
        <h3 class="sidebar-title">About</h3>
        <p style='color: #666; font-size: 0.95em; line-height: 1.5;'>
            EATelligence AI is an AI-powered food analyzer and recommendation system designed to promote healthy eating habits. The app enables users to analyze nutritional content in real-time, receive healthier food alternatives, and explore AI-driven innovative food blends using traditional Indian ingredients. It also offers personalized meal suggestions tailored to common lifestyle diseases, helping users make informed and balanced dietary choices.
        </p>
    </div>
    
    <div class="sidebar-content" style='margin-bottom: 30px;'>
        <h3 class="sidebar-title">Key Features</h3>
        <div style='background-color: rgba(255, 255, 255, 0.7); padding: 15px; border-radius: 8px; margin-top: 10px;'>
            <ul style='list-style-type: none; padding: 0; color: #2E7D32; font-size: 0.95em;'>
                <li style='margin-bottom: 12px; padding-left: 20px; position: relative;'>
                    <span style='position: absolute; left: 0; color: #2E7D32;'>•</span>
                    Food Recognition
                </li>
                <li style='margin-bottom: 12px; padding-left: 20px; position: relative;'>
                    <span style='position: absolute; left: 0; color: #2E7D32;'>•</span>
                    Nutrition Analysis
                </li>
                <li style='margin-bottom: 12px; padding-left: 20px; position: relative;'>
                    <span style='position: absolute; left: 0; color: #2E7D32;'>•</span>
                    Diet Planning
                </li>
                <li style='margin-bottom: 12px; padding-left: 20px; position: relative;'>
                    <span style='position: absolute; left: 0; color: #2E7D32;'>•</span>
                    AI Recipe Generation
                </li>
            </ul>
        </div>
    </div>
    
    <div class="sidebar-content">
        <h3 style='color: #2E7D32; margin-bottom: 15px;'>Developed by:</h3>
        <p style='margin: 5px 0;'>Pakhi Singh Tak</p>
        <p style='margin: 5px 0;'>Ilansha Singh Sisodia</p>
        <p style='margin-top: 15px; font-style: italic; color: #666;'>
            This project has been developed as part of a B.Tech Final Year Project.
        </p>
    </div>
    """, unsafe_allow_html=True)

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
    
    st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: rgba(255, 255, 255, 0.9); border-radius: 10px; margin-bottom: 20px;'>
        <h2 style='color: #2E7D32; margin-bottom: 10px;'>🍽️ Food Analyzer</h2>
        <p style='color: #666; font-size: 1.1em;'>Upload a food image or enter a food name to get detailed nutritional information and health impact assessment.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📸 Upload Food Image")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Food Image", use_column_width=True)
            
            # Get food recognition
            food_name = components['food_recognizer'].recognize_food(image)
            if food_name:
                st.success(f"Recognized Food: {food_name}")
                
                # Get nutrition info
                nutrition_info = get_nutrition_info(food_name)
                if nutrition_info:
                    # Display nutrition info in a styled table
                    st.markdown("### 📊 Nutritional Information")
                    nutrition_df = pd.DataFrame([nutrition_info])
                    st.markdown("""
                    <style>
                    .nutrition-table {
                        background-color: rgba(255, 255, 255, 0.9);
                        border-radius: 10px;
                        padding: 20px;
                        margin: 10px 0;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="nutrition-table">', unsafe_allow_html=True)
                    st.dataframe(nutrition_df, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Create pie chart for macronutrients
                    macronutrients = pd.DataFrame({
                        'Nutrient': ['Protein', 'Fat', 'Carbohydrates'],
                        'Amount': [
                            nutrition_info['protein'],
                            nutrition_info['fat'],
                            nutrition_info['carbs']
                        ]
                    })
                    
                    fig = px.pie(
                        macronutrients,
                        values='Amount',
                        names='Nutrient',
                        title="Macronutrient Distribution",
                        color_discrete_sequence=['#2E7D32', '#81C784', '#A5D6A7'],
                        hole=0.4  # Creates a donut chart
                    )
                    
                    # Update layout for better appearance
                    fig.update_traces(
                        textposition='inside',
                        textinfo='percent+label',
                        insidetextfont=dict(size=14, color='white'),
                        marker=dict(line=dict(color='white', width=2))
                    )
                    
                    fig.update_layout(
                        title_x=0.5,
                        title_font_size=20,
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="center",
                            x=0.5
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Health Impact Assessment
                    st.markdown("### 🏥 Health Impact Assessment")
                    health_impact = assess_health_impact(nutrition_info)
                    
                    # Display health impacts with color coding
                    for impact, details in health_impact.items():
                        impact_class = "positive" if "positive" in details.lower() else "caution" if "moderate" in details.lower() else "negative"
                        st.markdown(f"""
                        <div class="impact-item {impact_class}">
                            <h4 style='margin: 0;'>{impact}</h4>
                            <p style='margin: 5px 0;'>{details}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Nutritional information not available for this food item.")
            else:
                st.error("Could not recognize the food in the image. Please try another image or use text input.")
    
    with col2:
        st.markdown("### 🔍 Search by Name")
        food_name = st.text_input("Enter food name")
        
        if food_name:
            nutrition_info = get_nutrition_info(food_name)
            if nutrition_info:
                # Display nutrition info in a styled table
                st.markdown("### 📊 Nutritional Information")
                nutrition_df = pd.DataFrame([nutrition_info])
                st.markdown("""
                <style>
                .nutrition-table {
                    background-color: rgba(255, 255, 255, 0.9);
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px 0;
                }
                </style>
                """, unsafe_allow_html=True)
                st.markdown('<div class="nutrition-table">', unsafe_allow_html=True)
                st.dataframe(nutrition_df, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Create pie chart for macronutrients
                macronutrients = pd.DataFrame({
                    'Nutrient': ['Protein', 'Fat', 'Carbohydrates'],
                    'Amount': [
                        nutrition_info['protein'],
                        nutrition_info['fat'],
                        nutrition_info['carbs']
                    ]
                })
                
                fig = px.pie(
                    macronutrients,
                    values='Amount',
                    names='Nutrient',
                    title="Macronutrient Distribution",
                    color_discrete_sequence=['#2E7D32', '#81C784', '#A5D6A7'],
                    hole=0.4  # Creates a donut chart
                )
                
                # Update layout for better appearance
                fig.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    insidetextfont=dict(size=14, color='white'),
                    marker=dict(line=dict(color='white', width=2))
                )
                
                fig.update_layout(
                    title_x=0.5,
                    title_font_size=20,
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="center",
                        x=0.5
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Health Impact Assessment
                st.markdown("### 🏥 Health Impact Assessment")
                health_impact = assess_health_impact(nutrition_info)
                
                # Display health impacts with color coding
                for impact, details in health_impact.items():
                    impact_class = "positive" if "positive" in details.lower() else "caution" if "moderate" in details.lower() else "negative"
                    st.markdown(f"""
                    <div class="impact-item {impact_class}">
                        <h4 style='margin: 0;'>{impact}</h4>
                        <p style='margin: 5px 0;'>{details}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Nutritional information not available for this food item.")

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
