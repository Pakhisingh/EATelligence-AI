import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from nutrition_utils import load_nutrition_data
import streamlit as st
import warnings
import re
from difflib import SequenceMatcher
import os
from pathlib import Path

# Suppress PyTorch warnings
warnings.filterwarnings('ignore', category=UserWarning)

class FoodRecognizer:
    def __init__(self):
        try:
            # Load the nutrition data
            self.df = load_nutrition_data()
            
            # Initialize the model (we'll use a pre-trained model)
            self.model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet50', pretrained=True)
            self.model.eval()
            
            # Define image transformations
            self.transform = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
            
            # Load ImageNet labels
            self.labels = self._load_imagenet_labels()
            
            # Load preset images
            self.preset_images = self._load_preset_images()
            
            # Map common food items to our dataset with variations
            self.food_mapping = {
                # Breakfast items
                'idli': ['idli', 'steamed rice cake', 'rice cake', 'rice dumpling', 'steamed cake', 'south indian breakfast'],
                'dosa': ['dosa', 'crepe', 'pancake', 'thin pancake', 'rice pancake', 'south indian crepe'],
                'upma': ['upma', 'semolina porridge', 'semolina dish', 'savory porridge', 'south indian breakfast'],
                'poha': ['poha', 'flattened rice', 'beaten rice', 'rice flakes', 'indian breakfast', 'rice dish'],
                'dhokla': ['dhokla', 'steamed cake', 'fermented cake', 'gram flour cake', 'gujarati snack'],
                
                # Main dishes
                'sambar': ['sambar', 'lentil stew', 'vegetable stew', 'south indian stew', 'dal stew', 'soup'],
                'curry': ['curry', 'gravy', 'sauce', 'stew', 'masala', 'spiced dish', 'indian dish'],
                'rice': ['rice', 'biryani', 'pulao', 'fried rice', 'steamed rice', 'boiled rice', 'indian rice'],
                'dal': ['dal', 'lentil', 'lentil soup', 'pulse', 'legume', 'bean soup', 'indian dal'],
                'roti': ['roti', 'chapati', 'flatbread', 'wheat bread', 'indian bread', 'whole wheat bread'],
                'naan': ['naan', 'leavened bread', 'tandoori bread', 'indian flatbread', 'bread'],
                'paneer': ['paneer', 'cottage cheese', 'cheese', 'indian cheese', 'fresh cheese', 'dairy'],
                'biryani': ['biryani', 'rice dish', 'spiced rice', 'indian rice dish', 'mixed rice'],
                'pulao': ['pulao', 'pilaf', 'rice pilaf', 'fried rice dish', 'indian rice'],
                'paratha': ['paratha', 'stuffed bread', 'layered bread', 'indian flatbread', 'bread'],
                'puri': ['puri', 'fried bread', 'deep fried bread', 'puffed bread', 'indian bread'],
                
                # Snacks
                'samosa': ['samosa', 'stuffed pastry', 'fried pastry', 'indian snack', 'savory pastry'],
                'pakora': ['pakora', 'fritter', 'bhajji', 'fried snack', 'vegetable fritter', 'indian snack'],
                'vada': ['vada', 'savory donut', 'lentil fritter', 'south indian snack', 'fried snack'],
                'bhel puri': ['bhel puri', 'puffed rice snack', 'chaat', 'indian street food', 'snack'],
                'pav bhaji': ['pav bhaji', 'bread and curry', 'vegetable curry', 'mumbai street food', 'snack'],
                
                # Sweets
                'kheer': ['kheer', 'rice pudding', 'milk pudding', 'indian dessert', 'sweet dish'],
                'gulab jamun': ['gulab jamun', 'milk sweet', 'syrup sweet', 'indian sweet', 'dessert'],
                'jalebi': ['jalebi', 'sweet pretzel', 'syrup sweet', 'indian sweet', 'dessert'],
                'rasgulla': ['rasgulla', 'cheese ball', 'milk sweet', 'bengali sweet', 'dessert'],
                'laddu': ['laddu', 'sweet ball', 'indian sweet', 'round sweet', 'dessert'],
                'barfi': ['barfi', 'milk fudge', 'indian sweet', 'milk sweet', 'dessert'],
                
                # Common ingredients
                'potato': ['potato', 'aloo', 'spud', 'tuber', 'vegetable'],
                'tomato': ['tomato', 'tamatar', 'red fruit', 'vegetable'],
                'onion': ['onion', 'pyaz', 'bulb', 'vegetable'],
                'garlic': ['garlic', 'lehsun', 'clove', 'spice'],
                'ginger': ['ginger', 'adrak', 'root', 'spice'],
                'chili': ['chili', 'mirchi', 'pepper', 'spice'],
                'coriander': ['coriander', 'dhania', 'herb', 'green'],
                'cumin': ['cumin', 'jeera', 'seed', 'spice'],
                'turmeric': ['turmeric', 'haldi', 'spice', 'yellow'],
                'ghee': ['ghee', 'clarified butter', 'fat', 'oil']
            }
            
            # Create reverse mapping for easier lookup
            self.reverse_mapping = {}
            for key, variations in self.food_mapping.items():
                for variation in variations:
                    self.reverse_mapping[variation] = key
            
            # Create a list of all possible food names for similarity matching
            self.all_food_names = []
            for variations in self.food_mapping.values():
                self.all_food_names.extend(variations)
            
        except Exception as e:
            st.error(f"Error initializing food recognizer: {str(e)}")
            self.model = None
    
    def _load_imagenet_labels(self):
        """Load ImageNet labels"""
        try:
            import json
            import urllib
            url = 'https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json'
            response = urllib.request.urlopen(url)
            return json.loads(response.read())
        except Exception as e:
            st.error(f"Error loading ImageNet labels: {str(e)}")
            return []
    
    def _load_preset_images(self):
        """Load preset food images and their features"""
        preset_images = {}
        preset_dir = Path(__file__).parent / 'preset_images'
        
        if not preset_dir.exists():
            st.warning("Preset images directory not found. Creating directory...")
            preset_dir.mkdir(parents=True)
            return preset_images
        
        try:
            # Load each image in the preset directory
            for image_path in preset_dir.glob('*.jpg'):
                food_name = image_path.stem  # Get filename without extension
                try:
                    image = Image.open(image_path)
                    # Get image features
                    features = self._get_image_features(image)
                    preset_images[food_name] = {
                        'image': image,
                        'features': features
                    }
                except Exception as e:
                    st.warning(f"Error loading preset image {food_name}: {str(e)}")
            
            return preset_images
        except Exception as e:
            st.error(f"Error loading preset images: {str(e)}")
            return {}
    
    def _get_image_features(self, image: Image.Image) -> torch.Tensor:
        """Extract features from an image using the model"""
        try:
            # Preprocess the image
            img_tensor = self.transform(image).unsqueeze(0)
            
            # Get features
            with torch.no_grad():
                features = self.model(img_tensor)
                return features
        except Exception as e:
            st.error(f"Error extracting features: {str(e)}")
            return None
    
    def _compare_with_preset(self, image_features):
        """Compare uploaded image features with preset images."""
        if not self.preset_images:
            return None, 0.0
            
        # Ensure image_features is a 1D tensor
        if len(image_features.shape) > 1:
            image_features = image_features.flatten()
            
        best_match = None
        best_similarity = 0.0
        
        for food_name, preset_data in self.preset_images.items():
            preset_features = preset_data['features']
            
            # Ensure preset_features is a 1D tensor
            if len(preset_features.shape) > 1:
                preset_features = preset_features.flatten()
                
            # Calculate cosine similarity
            similarity = torch.nn.functional.cosine_similarity(
                image_features.unsqueeze(0),
                preset_features.unsqueeze(0),
                dim=1
            ).item()
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = food_name
                
        return best_match, best_similarity
    
    def _clean_text(self, text: str) -> str:
        """Clean text for better matching"""
        return re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    
    def _similarity_ratio(self, a: str, b: str) -> float:
        """Calculate similarity ratio between two strings"""
        return SequenceMatcher(None, a, b).ratio()
    
    def _find_best_match(self, text: str, threshold: float = 0.6) -> str:
        """Find the best matching food name"""
        text = self._clean_text(text)
        best_match = None
        best_score = 0
        
        for food_name in self.all_food_names:
            score = self._similarity_ratio(text, self._clean_text(food_name))
            if score > best_score and score >= threshold:
                best_score = score
                best_match = food_name
        
        return best_match
    
    def recognize_food(self, image: Image.Image) -> str:
        """
        Recognize food from an image
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            str: Recognized food name or None if not recognized
        """
        if self.model is None:
            return None
            
        try:
            # First try to match with preset images
            if self.preset_images:
                preset_match, _ = self._compare_with_preset(self._get_image_features(image))
                if preset_match:
                    return preset_match
            
            # If no preset match, fall back to the original recognition method
            # Preprocess the image
            img_tensor = self.transform(image).unsqueeze(0)
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(img_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                
                # Get top 10 predictions
                top10_prob, top10_catid = torch.topk(probabilities, 10)
                
                # Set confidence threshold
                CONFIDENCE_THRESHOLD = 0.2  # Lowered threshold for better matching
                
                # Try to match each prediction
                for prob, catid in zip(top10_prob, top10_catid):
                    predicted_label = self.labels[catid.item()]
                    cleaned_label = self._clean_text(predicted_label)
                    confidence = prob.item()
                    
                    # Skip if confidence is too low
                    if confidence < CONFIDENCE_THRESHOLD:
                        continue
                    
                    # First, try to match with our specific food items
                    for food_name, variations in self.food_mapping.items():
                        for variation in variations:
                            if variation in cleaned_label:
                                st.info(f"Recognized as {food_name} (confidence: {confidence:.2f})")
                                return food_name
                    
                    # If no direct match, try similarity matching with higher threshold
                    best_match = self._find_best_match(cleaned_label, threshold=0.6)  # Lowered threshold
                    if best_match:
                        food_name = self.reverse_mapping[best_match]
                        st.info(f"Recognized as {food_name} (confidence: {confidence:.2f})")
                        return food_name
                
                # If still no match, try to find any food-related words
                food_related_words = ['food', 'dish', 'meal', 'cuisine', 'cooking', 'recipe', 'eat', 'dining', 'indian', 'spice', 'vegetable', 'rice', 'bread', 'sweet', 'snack']
                for prob, catid in zip(top10_prob, top10_catid):
                    predicted_label = self.labels[catid.item()]
                    cleaned_label = self._clean_text(predicted_label)
                    
                    if any(word in cleaned_label for word in food_related_words):
                        st.warning("Detected food in the image but couldn't identify the specific dish. Please try another image or use the text input.")
                        return None
            
            st.warning("Could not recognize the food in the image. Please try another image or use the text input.")
            return None
        except Exception as e:
            st.error(f"Error recognizing food: {str(e)}")
            return None
    
    def get_nutrition_info(self, food_name: str) -> dict:
        """
        Get nutrition information for a recognized food
        
        Args:
            food_name (str): Name of the food
            
        Returns:
            dict: Nutrition information or None if not found
        """
        try:
            # Try exact match first
            food_data = self.df[self.df['Food'].str.lower() == food_name.lower()]
            
            # If no exact match, try partial match
            if len(food_data) == 0:
                food_data = self.df[self.df['Food'].str.contains(food_name, case=False, na=False)]
            
            if len(food_data) > 0:
                food_info = food_data.iloc[0]
                return {
                    'name': food_info['Food'],
                    'calories': food_info['Calories'],
                    'protein': food_info['Protein'],
                    'fat': food_info['Fat'],
                    'carbs': food_info['Carbs']
                }
            
            st.warning(f"No nutrition information found for {food_name}")
            return None
        except Exception as e:
            st.error(f"Error getting nutrition info: {str(e)}")
            return None
    
    def process_image(self, image: Image.Image) -> dict:
        """
        Process an image to recognize food and get nutrition information
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            dict: Dictionary containing nutrition information and the processed image
        """
        try:
            # Create a copy of the image for display
            display_image = image.copy()
            # Resize image for display while maintaining aspect ratio
            max_size = (300, 300)
            display_image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Recognize the food
            food_name = self.recognize_food(image)
            
            if food_name:
                # Get nutrition information
                nutrition_info = self.get_nutrition_info(food_name)
                if nutrition_info:
                    nutrition_info['display_image'] = display_image
                    return nutrition_info
            return {'display_image': display_image}
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            return None 