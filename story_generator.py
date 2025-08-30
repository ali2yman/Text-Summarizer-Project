"""
story_generator.py - Gemini-Powered Story Generation
Uses Google Gemini AI to create intelligent storytelling summaries from ticket data.
"""

import pandas as pd
import google.generativeai as genai
import os
from config import STORY_SECTIONS

def setup_gemini():
    """Setup Gemini API key from environment variable."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("Please set GEMINI_API_KEY environment variable")
    genai.configure(api_key=api_key)

def list_available_models():
    """
    List all available Gemini models for debugging.
    """
    try:
        setup_gemini()
        models = []
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                models.append(model.name)
        return models
    except Exception as e:
        return [f"Error listing models: {str(e)}"]

def divide_tickets_into_sections(df):
    """
    Divide tickets into 5 chronological sections for storytelling.
    """
    if df.empty:
        return {section: pd.DataFrame() for section in STORY_SECTIONS}
    
    total_tickets = len(df)
    section_size = max(1, total_tickets // 5)
    
    sections = {}
    for i, section_name in enumerate(STORY_SECTIONS):
        start_idx = i * section_size
        if i == len(STORY_SECTIONS) - 1:  # Last section gets remaining tickets
            end_idx = total_tickets
        else:
            end_idx = (i + 1) * section_size
        
        sections[section_name] = df.iloc[start_idx:end_idx]
    
    return sections

def prepare_ticket_data_for_gemini(section_df):
    """
    Prepare ticket data in a format suitable for Gemini processing.
    """
    if section_df.empty:
        return "No tickets in this section."
    
    ticket_summaries = []
    for _, ticket in section_df.iterrows():
        ticket_info = f"""
Ticket: {ticket['ORDER_NUMBER']}
Date: {ticket['ACCEPTANCE_TIME'].strftime('%B %d, %Y')}
Customer: {ticket['CUSTOMER_NUMBER']}
Issue: {ticket['ORDER_DESCRIPTION_1']} - {ticket['ORDER_DESCRIPTION_2']}
Resolution: {ticket['COMPLETION_RESULT_KB']}
Notes: {ticket.get('NOTE_MAXIMUM', 'No additional notes')}
"""
        ticket_summaries.append(ticket_info.strip())
    
    return "\n---\n".join(ticket_summaries)

def generate_gemini_narrative(ticket_data, section_name, product_name):
    """
    Use Gemini AI to generate narrative for a section of tickets.
    """
    try:
        setup_gemini()
        
        # Try different model names in order of preference
        model_names = [
            'gemini-1.5-flash',
            'gemini-1.5-pro', 
            'gemini-pro',
            'models/gemini-1.5-flash',
            'models/gemini-pro'
        ]
        
        for model_name in model_names:
            try:
                # Initialize Gemini model
                model = genai.GenerativeModel(model_name)
                
                prompt = f"""
You are a customer service analyst creating a professional narrative summary for {product_name} services.

Section: {section_name}
Ticket Data:
{ticket_data}

Please create a narrative summary that:
1. Describes the customer experience during this period
2. Highlights key issues and how they were resolved
3. Shows the timeline of events
4. Uses a professional, storytelling tone
5. Focuses on the customer journey

Keep the narrative concise (2-3 sentences) and professional.
"""

                response = model.generate_content(prompt)
                return response.text.strip()
                
            except Exception as model_error:
                print(f"Failed with model {model_name}: {str(model_error)}")
                continue
        
        # If all models fail, raise the last error
        raise Exception("All Gemini models failed")
        
    except Exception as e:
        # Fallback to simple narrative if Gemini fails
        ticket_count = len(ticket_data.split('---')) if '---' in ticket_data else 1
        return f"During this {section_name.lower()} period, {ticket_count} tickets were processed for {product_name} services. The team worked on resolving various technical issues and maintaining service quality. (AI summary unavailable: {str(e)})"

def create_product_summary_with_gemini(df, product_name):
    """
    Create complete storytelling summary for a product using Gemini AI.
    """
    if df.empty:
        return f"# {product_name} Service Summary\n\nNo tickets found for this product category."
    
    # Divide into sections
    sections = divide_tickets_into_sections(df)
    
    # Build summary
    summary = f"# {product_name} Service Journey\n\n"
    
    for section_name, section_df in sections.items():
        if section_df.empty:
            continue
        
        summary += f"## {section_name}\n\n"
        
        # Timeframe
        if not section_df.empty:
            start_date = section_df['ACCEPTANCE_TIME'].min().strftime('%B %d, %Y')
            end_date = section_df['ACCEPTANCE_TIME'].max().strftime('%B %d, %Y')
            if start_date == end_date:
                summary += f"**Timeframe:** {start_date}\n\n"
            else:
                summary += f"**Timeframe:** {start_date} to {end_date}\n\n"
        
        # Ticket numbers
        ticket_numbers = section_df['ORDER_NUMBER'].tolist()
        summary += f"**Ticket Numbers:** {', '.join(ticket_numbers[:5])}"
        if len(ticket_numbers) > 5:
            summary += f" (and {len(ticket_numbers)-5} more)"
        summary += "\n\n"
        
        # Gemini-generated narrative
        ticket_data = prepare_ticket_data_for_gemini(section_df)
        narrative = generate_gemini_narrative(ticket_data, section_name, product_name)
        summary += f"**Narrative:** {narrative}\n\n"
        summary += "---\n\n"
    
    return summary

def generate_all_summaries_with_gemini(df):
    """
    Generate Gemini-powered summaries for all products in the dataset.
    """
    summaries = {}
    
    for product in df['PRODUCT'].unique():
        product_df = df[df['PRODUCT'] == product]
        summaries[product] = create_product_summary_with_gemini(product_df, product)
    
    return summaries