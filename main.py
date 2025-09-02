"""
main.py - Enhanced Streamlit App for Ticket Summary
Complete application with all required features.
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from data_processor import read_uploaded_file, filter_and_clean_data, get_data_summary
from story_generator import generate_all_summaries_with_gemini, create_product_summary_with_gemini, list_available_models
from visualization import display_analytics_dashboard, generate_business_insights

# Page config
st.set_page_config(page_title="Ticket Summary App", page_icon="🎫", layout="wide")

def display_documentation():
    """Display user guide and documentation."""
    st.header("📚 User Guide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 File Upload")
        st.write("""
        **Supported formats:** TXT, CSV, XLSX
        
        **Required columns:**
        - ORDER_NUMBER
        - ACCEPTANCE_TIME  
        - COMPLETION_TIME
        - CUSTOMER_NUMBER
        - SERVICE_CATEGORY
        - ORDER_DESCRIPTION_1
        - ORDER_DESCRIPTION_2
        - COMPLETION_RESULT_KB
        - NOTE_MAXIMUM
        """)
        
        st.subheader("🔧 Setup")
        st.write("""
        1. Get Gemini API key from Google AI Studio
        2. Enter API key in sidebar
        3. Upload your ticket data file
        4. View summaries and analytics
        """)
    
    with col2:
        st.subheader("📋 Valid Categories")
        st.write("""
        Only tickets with these categories are processed:
        - **HDW** → Hardware
        - **NET** → Broadband  
        - **KAI** → Broadband
        - **KAV** → Voice
        - **GIGA** → GIGA
        - **VOD** → VOD
        - **KAD** → TV
        """)
        
        st.subheader("📖 Story Sections")
        st.write("""
        Each product summary includes:
        1. **Initial Issue** - First problems
        2. **Follow-ups** - Response actions
        3. **Developments** - Progress made
        4. **Later Incidents** - Recurring issues
        5. **Recent Events** - Latest updates
        """)

def main():
    st.title("🎫 Ticket Data Summary & Analysis")
    st.write("AI-powered ticket analysis with storytelling summaries and business insights")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["📊 Main App", "📚 Documentation"])
    
    if page == "📚 Documentation":
        display_documentation()
        return
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Ticket Data", 
        type=['txt', 'csv', 'xlsx'],
        help="Upload your ticket data in TXT, CSV, or XLSX format"
    )
    
    if uploaded_file:
        # Read file
        with st.spinner("Reading file..."):
            df, error = read_uploaded_file(uploaded_file)
        
        if error:
            st.error(f"❌ Error reading file: {error}")
            return
        
        st.success(f"✅ File loaded: {len(df):,} total records")
        
        # Process data
        with st.spinner("Processing data..."):
            df_processed = filter_and_clean_data(df)
        
        if df_processed is None or df_processed.empty:
            st.warning("⚠️ No valid tickets found. Please check your data format.")
            return
        
        st.info(f"📊 Valid tickets processed: {len(df_processed):,}")
        
        # Show basic stats
        summary = get_data_summary(df_processed)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tickets", f"{summary['total_tickets']:,}")
        with col2:
            st.metric("Unique Customers", f"{summary['unique_customers']:,}")
        with col3:
            st.metric("Date Range", f"{summary['date_range_days']} days")
        with col4:
            st.metric("Products", len(summary['product_counts']))
        
        # Product breakdown
        st.subheader("📈 Product Breakdown")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Tickets by Product:**")
            for product, count in summary['product_counts'].items():
                st.write(f"• {product}: {count:,} tickets")
        
        with col2:
            st.write("**Tickets by Category:**")
            for category, count in summary['category_counts'].items():
                st.write(f"• {category}: {count:,} tickets")
        
        # API Key input
        st.sidebar.header("🤖 Gemini AI Configuration")
        api_key = st.sidebar.text_input(
            "Gemini API Key", 
            type="password", 
            help="Enter your Google Gemini API key for AI summarization"
        )
        
        if api_key:
            os.environ['GEMINI_API_KEY'] = api_key
            st.sidebar.success("✅ API Key configured")
            
            # Show available models for debugging
            with st.sidebar.expander("🔍 Debug Info"):
                if st.sidebar.button("Check Available Models"):
                    try:
                        models = list_available_models()
                        st.sidebar.write("Available models:")
                        for model in models:
                            st.sidebar.write(f"- {model}")
                    except Exception as e:
                        st.sidebar.error(f"Error fetching models: {str(e)}")
        
        # Tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs(["📖 AI Summaries", "📈 Analytics", "💡 Insights", "💾 Export"])
        
        with tab1:
            if not api_key:
                st.warning("⚠️ Please enter Gemini API Key in the sidebar for AI-powered summaries")
            else:
                st.header("📖 AI-Powered Storytelling Summaries")
                
                # Product selection
                products = sorted(df_processed['PRODUCT'].unique())
                selected_product = st.selectbox(
                    "Select Product for Summary", 
                    ["All Products"] + list(products),
                    help="Choose a specific product or view all summaries"
                )
                
                if selected_product == "All Products":
                    # Show all summaries
                    with st.spinner("Generating AI summaries for all products..."):
                        try:
                            summaries = generate_all_summaries_with_gemini(df_processed)
                            
                            for product, summary in summaries.items():
                                with st.expander(f"📋 {product} Summary ({len(df_processed[df_processed['PRODUCT'] == product])} tickets)"):
                                    st.markdown(summary)
                        except Exception as e:
                            st.error(f"Error generating summaries: {str(e)}")
                else:
                    # Show selected product summary
                    product_df = df_processed[df_processed['PRODUCT'] == selected_product]
                    with st.spinner(f"Generating AI summary for {selected_product}..."):
                        try:
                            summary = create_product_summary_with_gemini(product_df, selected_product)
                            st.markdown(summary)
                        except Exception as e:
                            st.error(f"Error generating summary: {str(e)}")
        
        with tab2:
            # Analytics Dashboard
            try:
                display_analytics_dashboard(df_processed)
            except Exception as e:
                st.error(f"Error displaying analytics: {str(e)}")
        
        with tab3:
            st.header("💡 Business Insights")
            
            try:
                insights = generate_business_insights(df_processed)
                st.markdown(f"""
                **Key Findings:**
                {insights}
                
                **Recommendations:**
                • Focus on the product with highest ticket volume
                • Implement proactive monitoring for repeat customers
                • Analyze resolution time patterns to improve efficiency
                • Consider preventive measures for common issues
                """)
            except Exception as e:
                st.error(f"Error generating insights: {str(e)}")
        
        with tab4:
            st.header("💾 Export Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Export processed data
                try:
                    csv_data = df_processed.to_csv(index=False)
                    st.download_button(
                        "📥 Download Processed Data (CSV)",
                        csv_data,
                        f"processed_tickets_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        "text/csv",
                        help="Download the cleaned and processed ticket data"
                    )
                except Exception as e:
                    st.error(f"Error preparing CSV export: {str(e)}")
            
#             with col2:
#                 # Export summary report
#                 if api_key:
#                     try:
#                         summary_text = f"""# Ticket Summary Report
# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

# ## Data Overview
# - Total Tickets: {summary['total_tickets']:,}
# - Unique Customers: {summary['unique_customers']:,}
# - Date Range: {summary['date_range_days']} days

# ## Product Breakdown
# """
#                         for product, count in summary['product_counts'].items():
#                             summary_text += f"- {product}: {count:,} tickets\n"
                        
#                         insights = generate_business_insights(df_processed)
#                         summary_text += f"\n## Business Insights\n{insights}"
                        
#                         st.download_button(
#                             "📄 Download Summary Report",
#                             summary_text,
#                             f"ticket_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
#                             "text/plain",
#                             help="Download a complete summary report"
#                         )
#                     except Exception as e:
#                         st.error(f"Error preparing summary report: {str(e)}")
    
    else:
        st.info("👆 Upload a ticket data file to start analysis")
        
        # Show sample format
        with st.expander("📋 Expected File Format"):
            st.write("Your file should contain these columns:")
            sample_data = pd.DataFrame({
                'ORDER_NUMBER': ['T001', 'T002'],
                'ACCEPTANCE_TIME': ['01/15/2024 10:30', '01/16/2024 14:20'],
                'COMPLETION_TIME': ['01/15/2024 16:45', '01/16/2024 18:30'],
                'CUSTOMER_NUMBER': ['C001', 'C002'],
                'SERVICE_CATEGORY': ['NET', 'KAV'],
                'ORDER_DESCRIPTION_1': ['Internet connection issue', 'Voice service down'],
                'ORDER_DESCRIPTION_2': ['Customer cannot access internet', 'No dial tone'],
                'COMPLETION_RESULT_KB': ['Issue resolved', 'Service restored'],
                'NOTE_MAXIMUM': ['Router restart fixed issue', 'Line fault repaired']
            })
            st.dataframe(sample_data)

if __name__ == "__main__":
    main()