"""
data_processor.py - Data Processing Functions
Handles file upload, data cleaning, filtering, and preprocessing.
"""

import pandas as pd
import io
from datetime import datetime
from config import SELECTED_COLUMNS, VALID_CATEGORIES, CATEGORY_MAPPING, DATE_FORMAT

def read_uploaded_file(uploaded_file):
    """
    Read uploaded file and convert to DataFrame.
    Supports txt, csv, and xlsx files.
    """
    try:
        if uploaded_file.type == "text/plain":
            # Read text file and convert to CSV
            text_content = str(uploaded_file.read(), "utf-8")
            df = pd.read_csv(io.StringIO(text_content))
        elif uploaded_file.name.endswith('.xlsx'):
            # Read Excel file
            df = pd.read_excel(uploaded_file)
        else:
            # Read CSV file
            df = pd.read_csv(uploaded_file)
        
        return df, None
    except Exception as e:
        return None, str(e)

def filter_and_clean_data(df):
    """
    Filter data to keep only selected columns and valid categories.
    Clean and process the data for analysis.
    """
    # Keep only selected columns that exist in the data
    available_columns = [col for col in SELECTED_COLUMNS if col in df.columns]
    df_filtered = df[available_columns].copy()
    
    # Filter by valid service categories
    df_filtered = df_filtered[df_filtered['SERVICE_CATEGORY'].isin(VALID_CATEGORIES)]
    
    # Convert date columns
    for date_col in ['ACCEPTANCE_TIME', 'COMPLETION_TIME', 'CUSTOMER_COMPLETION_TIME']:
        if date_col in df_filtered.columns:
            df_filtered[date_col] = pd.to_datetime(df_filtered[date_col], format=DATE_FORMAT, errors='coerce')
    
    # Add product mapping
    df_filtered['PRODUCT'] = df_filtered['SERVICE_CATEGORY'].map(CATEGORY_MAPPING)
    
    # Sort by acceptance time
    df_filtered = df_filtered.sort_values('ACCEPTANCE_TIME')
    
    # Fill missing values
    text_columns = ['ORDER_DESCRIPTION_1', 'ORDER_DESCRIPTION_2', 'COMPLETION_RESULT_KB', 'NOTE_MAXIMUM']
    for col in text_columns:
        if col in df_filtered.columns:
            df_filtered[col] = df_filtered[col].fillna('No information available')
    
    return df_filtered

def get_data_summary(df):
    """
    Generate basic summary statistics about the processed data.
    """
    summary = {
        'total_tickets': len(df),
        'unique_customers': df['CUSTOMER_NUMBER'].nunique(),
        'date_range_days': (df['ACCEPTANCE_TIME'].max() - df['ACCEPTANCE_TIME'].min()).days,
        'product_counts': df['PRODUCT'].value_counts().to_dict(),
        'category_counts': df['SERVICE_CATEGORY'].value_counts().to_dict()
    }
    return summary