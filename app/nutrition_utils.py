import pandas as pd
import numpy as np
from pathlib import Path

def load_nutrition_data(file_path: str = '../data/Indian_Food_Nutrition_Processed.csv') -> pd.DataFrame:
    """
    Load and clean Indian food nutrition data from a CSV file.
    
    Args:
        file_path (str): Path to the nutrition data CSV file
        
    Returns:
        pd.DataFrame: Cleaned and standardized nutrition data
        
    The function:
    1. Loads the CSV file
    2. Removes rows with null values
    3. Standardizes columns: 'Calories', 'Protein', 'Fat', 'Carbs'
    4. Renames columns to match standard format
    """
    # Load the data
    df = pd.read_csv(file_path)
    
    # Rename columns to standard format
    column_mapping = {
        'Dish Name': 'Food',
        'Calories (kcal)': 'Calories',
        'Protein (g)': 'Protein',
        'Fats (g)': 'Fat',
        'Carbohydrates (g)': 'Carbs'
    }
    df = df.rename(columns=column_mapping)
    
    # Select only the columns we need
    columns_to_keep = ['Food', 'Calories', 'Protein', 'Fat', 'Carbs']
    df = df[columns_to_keep]
    
    # Remove rows with null values
    df = df.dropna()
    
    # Convert numeric columns to float
    numeric_columns = ['Calories', 'Protein', 'Fat', 'Carbs']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove any rows that became NaN after conversion
    df = df.dropna(subset=numeric_columns)
    
    # Reset index after dropping rows
    df = df.reset_index(drop=True)
    
    return df
