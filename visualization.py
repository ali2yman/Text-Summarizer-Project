"""
visualization.py - Simple Data Visualization Functions
Creates charts and graphs for ticket data analysis.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def create_ticket_trend_chart(df):
    """Create a timeline chart showing ticket volume over time."""
    if df is None or df.empty or 'ACCEPTANCE_TIME' not in df.columns:
        return None
    
    try:
        # Group by date
        df_temp = df.copy()
        df_temp = df_temp.dropna(subset=['ACCEPTANCE_TIME'])
        
        if df_temp.empty:
            return None
        
        df_temp['DATE'] = df_temp['ACCEPTANCE_TIME'].dt.date
        daily_counts = df_temp.groupby('DATE').size().reset_index(name='TICKET_COUNT')
        
        fig = px.line(daily_counts, x='DATE', y='TICKET_COUNT', 
                      title='Daily Ticket Volume Trend',
                      labels={'DATE': 'Date', 'TICKET_COUNT': 'Number of Tickets'})
        
        fig.update_layout(height=400)
        return fig
    except Exception as e:
        print(f"Error creating ticket trend chart: {str(e)}")
        return None

def create_product_distribution_chart(df):
    """Create pie chart showing ticket distribution by product."""
    if df is None or df.empty or 'PRODUCT' not in df.columns:
        return None
    
    try:
        product_counts = df['PRODUCT'].value_counts()
        
        if product_counts.empty:
            return None
        
        fig = px.pie(values=product_counts.values, names=product_counts.index,
                     title='Ticket Distribution by Product')
        
        fig.update_layout(height=400)
        return fig
    except Exception as e:
        print(f"Error creating product distribution chart: {str(e)}")
        return None

def create_resolution_time_chart(df):
    """Create chart showing average resolution times by product."""
    if df is None or df.empty or 'COMPLETION_TIME' not in df.columns or 'ACCEPTANCE_TIME' not in df.columns or 'PRODUCT' not in df.columns:
        return None
    
    try:
        # Calculate resolution time
        df_temp = df.copy()
        df_temp = df_temp.dropna(subset=['ACCEPTANCE_TIME', 'COMPLETION_TIME'])
        
        if df_temp.empty:
            return None
        
        df_temp['RESOLUTION_HOURS'] = (df_temp['COMPLETION_TIME'] - df_temp['ACCEPTANCE_TIME']).dt.total_seconds() / 3600
        
        # Filter out negative or unrealistic resolution times
        df_temp = df_temp[df_temp['RESOLUTION_HOURS'] >= 0]
        df_temp = df_temp[df_temp['RESOLUTION_HOURS'] <= 24*30]  # Cap at 30 days
        
        if df_temp.empty:
            return None
        
        # Group by product
        avg_resolution = df_temp.groupby('PRODUCT')['RESOLUTION_HOURS'].mean().reset_index()
        
        fig = px.bar(avg_resolution, x='PRODUCT', y='RESOLUTION_HOURS',
                     title='Average Resolution Time by Product (Hours)',
                     labels={'PRODUCT': 'Product', 'RESOLUTION_HOURS': 'Average Hours'})
        
        fig.update_layout(height=400)
        return fig
    except Exception as e:
        print(f"Error creating resolution time chart: {str(e)}")
        return None

def create_customer_activity_chart(df):
    """Create chart showing most active customers."""
    if df is None or df.empty or 'CUSTOMER_NUMBER' not in df.columns:
        return None
    
    try:
        customer_counts = df['CUSTOMER_NUMBER'].value_counts().head(10)
        
        if customer_counts.empty:
            return None
        
        fig = px.bar(x=customer_counts.index, y=customer_counts.values,
                     title='Top 10 Most Active Customers',
                     labels={'x': 'Customer Number', 'y': 'Number of Tickets'})
        
        fig.update_layout(height=400)
        return fig
    except Exception as e:
        print(f"Error creating customer activity chart: {str(e)}")
        return None

def display_analytics_dashboard(df):
    """Display complete analytics dashboard."""
    st.header("📈 Analytics Dashboard")
    
    if df is None or df.empty:
        st.warning("No data available for visualization")
        return
    
    try:
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Ticket trend
            trend_chart = create_ticket_trend_chart(df)
            if trend_chart:
                st.plotly_chart(trend_chart, use_container_width=True)
            else:
                st.info("Ticket trend chart unavailable - missing or invalid date data")
            
            # Resolution time
            resolution_chart = create_resolution_time_chart(df)
            if resolution_chart:
                st.plotly_chart(resolution_chart, use_container_width=True)
            else:
                st.info("Resolution time chart unavailable - missing completion time data")
        
        with col2:
            # Product distribution
            pie_chart = create_product_distribution_chart(df)
            if pie_chart:
                st.plotly_chart(pie_chart, use_container_width=True)
            else:
                st.info("Product distribution chart unavailable - missing product data")
            
            # Customer activity
            customer_chart = create_customer_activity_chart(df)
            if customer_chart:
                st.plotly_chart(customer_chart, use_container_width=True)
            else:
                st.info("Customer activity chart unavailable - missing customer data")
                
    except Exception as e:
        st.error(f"Error displaying analytics dashboard: {str(e)}")

def generate_business_insights(df):
    """Generate business insights from the data."""
    if df is None or df.empty:
        return "No data available for analysis."
    
    try:
        insights = []
        
        # Most problematic product
        if 'PRODUCT' in df.columns:
            product_counts = df['PRODUCT'].value_counts()
            if not product_counts.empty:
                most_tickets = product_counts.index[0]
                insights.append(f"• **{most_tickets}** has the highest ticket volume ({product_counts.iloc[0]} tickets)")
        
        # Customer patterns
        if 'CUSTOMER_NUMBER' in df.columns:
            customer_counts = df['CUSTOMER_NUMBER'].value_counts()
            if len(customer_counts) > 1:
                repeat_customers = len(customer_counts[customer_counts > 1])
                total_customers = len(customer_counts)
                repeat_rate = (repeat_customers / total_customers) * 100
                insights.append(f"• **{repeat_rate:.1f}%** of customers had multiple tickets")
        
        # Time patterns
        if 'COMPLETION_TIME' in df.columns and 'ACCEPTANCE_TIME' in df.columns:
            df_temp = df.dropna(subset=['ACCEPTANCE_TIME', 'COMPLETION_TIME'])
            if not df_temp.empty:
                resolution_times = (df_temp['COMPLETION_TIME'] - df_temp['ACCEPTANCE_TIME']).dt.total_seconds()
                # Filter out negative or unrealistic times
                valid_times = resolution_times[(resolution_times >= 0) & (resolution_times <= 24*30*3600)]
                if len(valid_times) > 0:
                    avg_hours = valid_times.mean() / 3600
                    insights.append(f"• Average resolution time: **{avg_hours:.1f} hours**")
        
        # Recent activity
        if 'ACCEPTANCE_TIME' in df.columns:
            df_dates = df.dropna(subset=['ACCEPTANCE_TIME'])
            if not df_dates.empty:
                max_date = df_dates['ACCEPTANCE_TIME'].max()
                recent_df = df_dates[df_dates['ACCEPTANCE_TIME'] >= (max_date - timedelta(days=7))]
                if not recent_df.empty:
                    insights.append(f"• **{len(recent_df)}** tickets in the last 7 days")
        
        return "\n".join(insights) if insights else "No significant patterns detected."
        
    except Exception as e:
        return f"Error generating insights: {str(e)}"