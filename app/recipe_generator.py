import openai
from typing import List, Dict
import os
from dotenv import load_dotenv
import json

class RecipeGenerator:
    def __init__(self):
        load_dotenv()
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Define common Indian ingredients
        self.ingredients = {
            'grains': [
                'ragi', 'bajra', 'jowar', 'quinoa', 'brown rice', 'red rice',
                'foxtail millet', 'little millet', 'kodo millet', 'barnyard millet'
            ],
            'pulses': [
                'moong dal', 'toor dal', 'chana dal', 'urad dal', 'masoor dal',
                'horse gram', 'black gram', 'green gram', 'red gram'
            ],
            'vegetables': [
                'palak', 'methi', 'lauki', 'tinda', 'karela', 'bhindi',
                'baingan', 'gajar', 'shimla mirch', 'tamatar'
            ],
            'spices': [
                'turmeric', 'cumin', 'coriander', 'mustard seeds', 'fenugreek',
                'asafoetida', 'curry leaves', 'cinnamon', 'cardamom', 'cloves'
            ],
            'healthy_fats': [
                'coconut oil', 'ghee', 'sesame oil', 'mustard oil', 'peanuts',
                'almonds', 'cashews', 'walnuts', 'flaxseeds', 'chia seeds'
            ]
        }
    
    def generate_recipe(self, selected_ingredients: List[str]) -> Dict:
        """
        Generate a unique recipe using selected ingredients
        
        Args:
            selected_ingredients (List[str]): List of ingredients to use in the recipe
            
        Returns:
            Dict containing:
            - recipe_name: Name of the recipe
            - ingredients: List of ingredients with quantities
            - instructions: Step-by-step cooking instructions
            - nutritional_benefits: List of nutritional benefits
        """
        # Prepare the prompt for GPT
        prompt = f"""
        Create a unique, healthy Indian recipe using these ingredients: {', '.join(selected_ingredients)}.
        The recipe should be:
        1. Nutritious and balanced
        2. Easy to prepare
        3. Use traditional Indian cooking methods
        4. Include specific quantities for ingredients
        5. Have clear step-by-step instructions
        6. Include nutritional benefits
        
        Format the response as a JSON with these keys:
        - recipe_name: Creative name for the recipe
        - ingredients: List of ingredients with quantities
        - instructions: Step-by-step cooking instructions
        - nutritional_benefits: List of nutritional benefits
        
        Make the recipe innovative while keeping it authentic to Indian cuisine.
        """
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional Indian chef and nutritionist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            # Parse the response
            recipe_text = response.choices[0].message.content
            recipe = json.loads(recipe_text)
            return recipe
            
        except Exception as e:
            print(f"Error generating recipe: {str(e)}")
            return {
                "error": str(e),
                "recipe_name": "Error in recipe generation",
                "ingredients": [],
                "instructions": [],
                "nutritional_benefits": []
            }
    
    def get_ingredient_categories(self) -> Dict[str, List[str]]:
        """
        Get all available ingredient categories and their items
        
        Returns:
            Dict[str, List[str]]: Dictionary of ingredient categories and their items
        """
        return self.ingredients 