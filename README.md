# Fundamental Analysis App

**Description:** Developed a Streamlit-based web application to facilitate the fundamental analysis of companies by retrieving and displaying key financial metrics from a MySQL database.

**Watch a demo here:** https://youtu.be/co-J8sBKUto?si=IPpagbvXOFRwB_WX

# Technologies Used:

**Frontend:** Streamlit for creating the user interface and enabling interactive data filtering.

**Backend:** Python for data processing and handling business logic.

**Database:** MySQL for storing and querying company data.

**Configuration:** YAML for securely managing database credentials.

**Data Handling:** Pandas for data manipulation and display.

# Key Features:

**Dynamic Filtering:** Implemented multi-select dropdowns for filtering companies based on Ticker, Company, Sector, Industry, and Country.

**Data Visualization:** Designed a detailed breakdown of fundamental grades with color-coded ratings to enhance readability and user experience.

**Database Integration:** Established secure connections to MySQL database using credentials stored in a YAML configuration file.

**Legend Interpretation:** Integrated a visual legend to interpret grading scales, including color-coded ratings and descriptive icons.

# Responsibilities:

**Database Design and Management:** Structured and maintained a MySQL database to store and efficiently query fundamental analysis data.

**Application Development:** Built and deployed a user-friendly Streamlit application to display financial data.

**Data Processing:** Utilized Pandas for data manipulation, including filtering, aggregation, and formatting.

**User Interface Design:** Created an intuitive sidebar for user inputs and dynamic filtering, ensuring a seamless user experience.

**Security:** Implemented best practices for securing database connections and handling sensitive information.

# Impact:

**Efficiency:** Enabled users to quickly filter and analyze companies based on multiple criteria, significantly reducing the time required for fundamental analysis.

**User Experience:** Enhanced data presentation through color-coded grades and a clear legend, making it easier for users to interpret and compare financial metrics.

**Scalability:** Designed a scalable architecture that can be extended to include additional financial metrics and data sources in the future.


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

# License
This project is licensed under the MIT License - see the LICENSE file for details.

