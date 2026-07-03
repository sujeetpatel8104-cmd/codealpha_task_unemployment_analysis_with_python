import pandas as pd
import numpy as np
import plotly.express as px
import os

def load_and_clean_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found!")
        print(f"Current working directory: {os.getcwd()}")
        print("Please make sure 'Unemployment_in_India.csv' is placed in the same folder as this script.")
        return None
        
    print("Loading dataset...")
    df = pd.read_csv(file_path)
    
    df.columns = df.columns.str.strip()
    df = df.dropna()
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df['Month'] = df['Date'].dt.strftime('%B')
    df['Year'] = df['Date'].dt.year
    
    print(f"Data cleaning successful! Total rows processed: {df.shape[0]}\n")
    return df

def analyze_urban_vs_rural(df):
    print("Generating Urban vs Rural analysis chart...")
    area_df = df.groupby(['Region', 'Area'])['Estimated Unemployment Rate (%)'].mean().reset_index()
    
    fig = px.bar(area_df, 
x='Region', 
y='Estimated Unemployment Rate (%)', 
color='Area',
barmode='group',
title='Average Unemployment Rate by State and Area (Urban/Rural)',
labels={'Estimated Unemployment Rate (%)': 'Unemployment Rate (%)'})
    fig.show()

def analyze_covid_impact(df):
    print("Generating COVID-19 impact timeline chart...")
    timeline = df.groupby('Date')['Estimated Unemployment Rate (%)'].mean().reset_index()
    
    fig = px.line(timeline, 
x='Date', 
y='Estimated Unemployment Rate (%)',
title='Unemployment Rate Trends Over Time (COVID-19 Impact Analysis)',
markers=True)
    
    lockdown_date = '2020-03-25'
    fig.add_vline(x=pd.Timestamp(lockdown_date), line_width=2, line_dash="dash", line_color="red")
    fig.add_annotation(x=pd.Timestamp(lockdown_date), y=max(timeline['Estimated Unemployment Rate (%)']) - 2, 
text="Start of National Lockdown", showarrow=True, arrowhead=1)
    fig.show()

def analyze_seasonal_distribution(df):
    print("Generating seasonal hierarchy sunburst chart...")
    sunburst_data = df.groupby(['Year', 'Month'])['Estimated Unemployment Rate (%)'].mean().reset_index()
    
    fig = px.sunburst(sunburst_data, 
path=['Year', 'Month'], 
values='Estimated Unemployment Rate (%)',
title='Hierarchical Distribution of Unemployment by Year and Month',
color='Estimated Unemployment Rate (%)',
color_continuous_scale='RdBu_r')
    fig.show()

if __name__ == "__main__":
    # This automatically finds the CSV file right next to your script file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(script_dir, "Unemployment_in_India.csv")
    
    df = load_and_clean_data(DATA_PATH)
    
    if df is not None:
        analyze_urban_vs_rural(df)
        analyze_covid_impact(df)
        analyze_seasonal_distribution(df)