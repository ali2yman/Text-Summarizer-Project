"""
main.py - Simple Streamlit App for Ticket Summary
Main application interface with essential features only.
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from data_processor import read_uploaded_file, filter_and_clean_data, get_data_summary
from story_generator import generate_all_summaries_with_gemini, create_product_summary_with_gemini, list_available_models

# Page config
st.set_page_config(page_title="Ticket Summary App", page_icon="🎫", layout="wide")

def main():
    st.title("🎫 Ticket Data Summary")
    st.write("Upload your ticket data to generate AI-powered summaries")
    
    # File upload
    uploaded_file = st.file_uploader("Upload File", type=['txt', 'csv', 'xlsx'])
    
    if uploaded_file:
        # Read file
        df, error = read_uploaded_file(uploaded_file)
        
        if error:
            st.error(f"Error reading file: {error}")
            return
        
        st.success(f"✅ File loaded: {len(df)} total records")
        
        # Process data
        df_processed = filter_and_clean_data(df)
        
        if df_processed.empty:
            st.warning("No valid tickets found")
            return
        
        st.info(f"📊 Valid tickets: {len(df_processed)}")
        
        # Show basic stats
        summary = get_data_summary(df_processed)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tickets", summary['total_tickets'])
        with col2:
            st.metric("Customers", summary['unique_customers'])
        with col3:
            st.metric("Days Range", summary['date_range_days'])
        
        # API Key input
        st.sidebar.header("🤖 Gemini AI Configuration")
        api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API key for AI summarization")
        
        if api_key:
            os.environ['GEMINI_API_KEY'] = api_key
            
            # Show available models for debugging
            with st.sidebar.expander("🔍 Debug Info"):
                if st.button("Check Available Models"):
                    models = list_available_models()
                    st.write("Available models:")
                    for model in models:
                        st.write(f"- {model}")
        
        if not api_key:
            st.warning("⚠️ Please enter Gemini API Key in the sidebar for AI-powered summaries")
            return
        
        # Generate summaries
        st.header("📖 AI Summaries")
        
        # Product selection
        products = df_processed['PRODUCT'].unique()
        selected_product = st.selectbox("Select Product", ["All Products"] + list(products))
        
        if selected_product == "All Products":
            # Show all summaries
            summaries = generate_all_summaries_with_gemini(df_processed)
            for product, summary in summaries.items():
                with st.expander(f"{product} Summary"):
                    st.markdown(summary)
        else:
            # Show selected product summary
            product_df = df_processed[df_processed['PRODUCT'] == selected_product]
            summary = create_product_summary_with_gemini(product_df, selected_product)
            st.markdown(summary)
        
        # Export data
        st.header("💾 Download")
        csv_data = df_processed.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            csv_data,
            f"tickets_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            "text/csv"
        )
    
    else:
        st.info("👆 Upload a file to start")
        
        # Show sample format
        with st.expander("📋 Required Columns"):
            st.write("Your file should contain these columns:")
            st.code("""
ORDER_NUMBER, ACCEPTANCE_TIME, COMPLETION_TIME, CUSTOMER_NUMBER,
SERVICE_CATEGORY, ORDER_DESCRIPTION_1, ORDER_DESCRIPTION_2, 
COMPLETION_RESULT_KB, NOTE_MAXIMUM
            """)

if __name__ == "__main__":
    main()