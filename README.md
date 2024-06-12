# Fundamental Analysis App
Fundamental analysis with ease.

# Project Structure
```
Fundamental_analysis/
├── app.py               # Streamlit application entry point
├── config.yaml          # Database configuration file
├── README.md            # Project README file
├── requirements.txt     # Project dependencies
└── __pycache__/         # Compiled Python files
```

# Overview
Fundamental Analysis app is a Streamlit application designed to facilitate fundamental analysis of companies. The app connects to a MySQL database to retrieve and display fundamental metrics, allowing users to filter companies based on various criteria such as sector, industry, and country.

# Features
* Dynamic Filtering: Users can filter companies based on Ticker, Company, Sector, Industry, and Country.
* Data Visualization: The app provides a detailed breakdown of fundamental grades (Valuation, Profitability, Growth, Performance) with color-coded ratings.
* Database Integration: Securely connects to a MySQL database using credentials stored in a configuration file.

# Installation
1. Clone the repository:
```
git clone https://github.com/Profesor-JH/Fundamental_analysis.git
cd Fundamental_analysis
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Configure the database:
```
Update the config.yaml file with your MySQL database credentials:
```
```
database:
  host: your_db_host
  database: your_db_name
  user: your_db_user
  password: your_db_password
```

4. Run the application:

```
streamlit run app.py
```

# Usage
1. Select Filters: Use the sidebar to select filters such as Ticker, Company, Sector, Industry, and Country.
2. Apply Selection: Click on "Apply Selection" to update the filter options dynamically based on selected criteria.
3. Run Analysis: Click on "Run Analysis" to fetch and display the data based on the selected filters.
4. Reset Selections: Click on "Reset Selections" to clear all filters.


# Example
## Fundamental Analysis by Rating
The app includes a legend to interpret the grading scale:

``` 
<div style='border: 0.6px solid white; padding: 20px; margin: 5px; margin-right: -170px;'>
  <div style='display:flex; justify-content:space-between; font-size: small;'>
    <div style='margin-right: 40px; text-align: center;'>❌<br><span style='color:#FF6347; font-size: x-large;'>D-</span><br><span style='font-size: x-small;'>Poor</span></div>
    <div style='margin-right: 40px; text-align: center;'>⚠️<br><span style='color:#FFA07A; font-size: x-large;'>D</span><br><span style='font-size: x-small;'>Below Average</span></div>
    <div style='margin-right: 40px; text-align: center;'>🟡<br><span style='color:#FFD700; font-size: x-large;'>D+</span><br><span style='font-size: x-small;'>Average</span></div>
    <div style='margin-right: 40px; text-align: center;'>🟡<br><span style='color:#FFD700; font-size: x-large;'>C-</span><br><span style='font-size: x-small;'>Average</span></div>
    <div style='margin-right: 40px; text-align: center;'>✔️<br><span style='color:#ADFF2F; font-size: x-large;'>C</span><br><span style='font-size: x-small;'>Above Average</span></div>
    <div style='margin-right: 40px; text-align: center;'>✅<br><span style='color:#32CD32; font-size: x-large;'>C+</span><br><span style='font-size: x-small;'>Good</span></div>
    <div style='margin-right: 40px; text-align: center;'>✅<br><span style='color:#32CD32; font-size: x-large;'>B-</span><br><span style='font-size: x-small;'>Good</span></div>
    <div style='margin-right: 40px; text-align: center;'>💯<br><span style='color:#00BFFF; font-size: x-large;'>B</span><br><span style='font-size: x-small;'>Very Good</span></div>
    <div style='margin-right: 40px; text-align: center;'>💫<br><span style='color:#1E90FF; font-size: x-large;'>B+</span><br><span style='font-size: x-small;'>Excellent</span></div>
    <div style='margin-right: 40px; text-align: center;'>💫<br><span style='color:#1E90FF; font-size: x-large;'>A-</span><br><span style='font-size: x-small;'>Excellent</span></div>
    <div style='margin-right: 40px; text-align: center;'>🚀<br><span style='color:#9400D3; font-size: x-large;'>A</span><br><span style='font-size: x-small;'>Outstanding</span></div>
    <div style='margin-right: 40px; text-align: center;'>🌟<br><span style='color:#8A2BE2; font-size: x-large;'>A+</span><br><span style='font-size: x-small;'>Exceptional</span></div>
  </div>
</div>
```

# License
This project is licensed under the MIT License - see the LICENSE file for details.

