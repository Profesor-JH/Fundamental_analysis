import streamlit as st
import mysql.connector
import yaml
import pandas as pd

# Read the configuration file
with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

# Access database credentials from the configuration
db_host = config['database']['host']
db_name = config['database']['database']
db_user = config['database']['user']
db_password = config['database']['password']

# Establish a connection to the MySQL database
connection = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)

# Define inputs for the Streamlit app
inputs = {
    "Ticker": "Dimension_Company",
    "Company": "Dimension_Company",
    "Sector": "Dimension_Sector",
    "Industry": "Dimension_Industry",
    "Country": "Dimension_Country"
}

def get_distinct_values(column_name, table_name, selected_values):
    cursor = connection.cursor()

    # Join statements for tables that need to be joined
    joins = {
        "Ticker": ["Dimension_Company", "b", "ON a.Ticker = b.Ticker"],
        "Company": ["Dimension_Company", "c", "ON a.Ticker = c.Ticker"],
        "Sector": ["Dimension_Sector", "d", "ON a.Ticker = d.Ticker"],
        "Industry": ["Dimension_Industry", "e", "ON a.Ticker = e.Ticker"],
        "Country": ["Dimension_Country", "f", "ON a.Ticker = f.Ticker"]
    }

    query = f"SELECT DISTINCT a.`{column_name}` FROM `{table_name}` a"

    # Add conditions based on selected values
    conditions = []
    for column, value in selected_values.items():
        #print(f"the current selected values are {selected_values}")
        if column in joins:
            join_table, alias, join_condition = joins[column]
            # Construct the query with the join
            query += f" JOIN {join_table} {alias} {join_condition}"
            if value is not None and value != [] and value != "None":
                if isinstance(value, str):
                    # Quote string values
                    conditions.append(f"{alias}.{column} = '{value}'")
                else:
                    if None in value:
                        # Handle None values
                        conditions.append(f"{alias}.{column} IS NULL")
                    else:
                        # Quote each value in the list
                        quoted_values = ",".join([f"'{v}'" for v in value])
                        conditions.append(f"{alias}.{column} IN ({quoted_values})")
        else:
            # For inputs without joins, add conditions directly on the main table
            if value is not None and value != [] and value != "None":
                if isinstance(value, str):
                    # Quote string values
                    conditions.append(f"a.{column_name} = '{value}'")
                else:
                    if None in value:
                        # Handle None values
                        conditions.append(f"a.{column_name} IS NULL")
                    else:
                        # Quote each value in the list
                        quoted_values = ",".join([f"'{v}'" for v in value])
                        conditions.append(f"a.{column_name} IN ({quoted_values})")

    # Add WHERE clause if there are conditions
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    print(query)
    cursor.execute(query)
    distinct_values = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return distinct_values



def fetch_data(connection, company=None, sector=None, industry=None, country=None):
    cursor = connection.cursor()
    query = """
        SELECT a.Date as Analysis_Date,Company,Sector, Industry, Country,a.Valuation_Grade,
        a.Profitability_Grade, a.Growth_Grade, a.Performance_Grade, a.Overall_Rating
        FROM Fundamental_Profiling a
        JOIN Dimension_Company ON a.Ticker = Dimension_Company.Ticker
        JOIN Dimension_Sector ON a.Ticker = Dimension_Sector.Ticker
        JOIN Dimension_Industry ON a.Ticker = Dimension_Industry.Ticker
        JOIN Dimension_Country ON a.Ticker = Dimension_Country.Ticker
        WHERE 1=1
    """
    params = []

    if company is not None and company != []:
        query += " AND Dimension_Company.Company IN (" + ",".join(["%s"] * len(company)) + ")"
        params.extend(company)
    if sector is not None and sector != []:
        query += " AND Dimension_Sector.Sector IN (" + ",".join(["%s"] * len(sector)) + ")"
        params.extend(sector)
    if industry is not None and industry != []:
        query += " AND Dimension_Industry.Industry IN (" + ",".join(["%s"] * len(industry)) + ")"
        params.extend(industry)
    if country is not None and country != []:
        query += " AND Dimension_Country.Country IN (" + ",".join(["%s"] * len(country)) + ")"
        params.extend(country)
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    return data

# Define main function
def main():

    # Define the name of the app and a brief description
    app_name = "QuantSniper - Vision noc"
    app_description = "Fundamental analysis with ease."

    # Define the legend for the grading scale with descriptions and corresponding colors
    legend = {
        "D-": ("Poor", "#FF6347", '❌'),  # Red cross mark for lowest grade
        "D": ("Below Average", "#FFA07A", '⚠️'),  # Warning icon for low grade
        "D+": ("Average", "#FFD700", '🟡'),  # Yellow circle for average grade
        "C-": ("Average", "#FFD700", '🟡'),  # Yellow circle for average grade
        "C": ("Above Average", "#ADFF2F", '✔️'),  # Checkmark for above average grade
        "C+": ("Good", "#32CD32", '✅'),  # Green checkmark for good grade
        "B-": ("Good", "#32CD32", '✅'),  # Green checkmark for good grade
        "B": ("Very Good", "#00BFFF", '💯'),  # Hundred points icon for very good grade
        "B+": ("Excellent", "#1E90FF", '💫'),  # Shooting star for excellent grade
        "A-": ("Excellent", "#1E90FF", '💫'),  # Shooting star for excellent grade
        "A": ("Outstanding", "#9400D3", '🚀'),  # Rocket icon for outstanding grade
        "A+": ("Exceptional", "#8A2BE2", '🌟')  # Star icon for exceptional grade
    }

    # Display the legend horizontally with color-coded text
    st.subheader("Fundamental Analysis by Rating")
    legend_html = "<div style='border: 0.6px solid white; padding: 20px; margin: 5px; margin-right: -170px;'>"
    legend_html += "<div style='display:flex; justify-content:space-between; font-size: small;'>"
    for grade, (description, color, icon)  in legend.items():
        legend_html += f"<div style='margin-right: 40px; text-align: center;'>{icon}<br><span style='color:{color}; font-size: x-large;'>{grade}</span><br><span style='font-size: x-small;'>{description}</span></div>"
    legend_html += "</div>"
    legend_html += "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)






    # Display the app name and description in the sidebar
    st.sidebar.markdown(f"<h1 style='text-align: left; color: white; font-size: 36px;'>{app_name}</h1>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p style='text-align: left; font-size: 20px; color: white;'>{app_description}</p>", unsafe_allow_html=True)
    
    # Define default values for inputs
    default_values = {
        "Ticker": [],
        "Company": [],
        "Sector": [],
        "Industry": [],
        "Country": []
    }
    
    # Initialize selected values
    selected_values = {}

    # Read user input for all inputs and update default_values
    for input_name, table_name in inputs.items():
        default_values[input_name] = st.sidebar.multiselect(f"Select {input_name}", get_distinct_values(input_name, table_name, default_values), key=f"{input_name}_multiselect")

    if st.sidebar.button("Apply Selection"):
    # Render select inputs for user input
        for input_name, table_name in inputs.items():
            selected_values[input_name] = st.session_state[f"{input_name}_multiselect"]
            # Make the select input reactive to changes in any other input

        for other_input_name in inputs.keys():
            if other_input_name != input_name:
                selected_values[input_name] = st.session_state[f"{other_input_name}_multiselect"]

    # Button to apply selections
    if st.sidebar.button("Run Analysis"):
        # Print the contents of default_values for debugging
        print(f"default_values: {default_values}")

        # Create selected_values dictionary excluding keys with empty values
        selected_values = {key: value for key, value in list(default_values.items())[1:]}

        print(f"the selected value for data {selected_values}")

        # Fetch data based on selected filters
        company = tuple(selected_values['Company']) if selected_values['Company'] else None
        sector = tuple(selected_values['Sector']) if selected_values['Sector'] else None
        industry = tuple(selected_values['Industry']) if selected_values['Industry'] else None
        country = tuple(selected_values['Country']) if selected_values['Country'] else None

        data = fetch_data(connection, company, sector, industry, country)
        # Display the fetched data in a nice format
        out_put = pd.DataFrame(data)
        out_put.columns = ['Date','Company','Sector', 'Industry', 'Country','Valuation Grade',
          'Profitability Grade', 'Growth Grade', 'Performance Grade', 'Overall Rating']
        
        # Reset index before applying styling
        out_put.reset_index(drop=True, inplace=True)
        # Round 'Overall Rating' column to 2 decimal places
        # Format "Overall Rating" column as percentage with two decimal places
        out_put["Overall Rating"] = out_put["Overall Rating"].apply(lambda x: f"{x:.2f}%")

        out_put.drop(columns="Date", inplace=True)

        # Define the colors for each grade
        grade_colors = {
            "D-": "#FF6347",  # Tomato
            "D": "#FFA07A",   # LightSalmon
            "D+": "#FFD700",  # Gold
            "C-": "#FFD700",  # Gold
            "C": "#ADFF2F",   # GreenYellow
            "C+": "#32CD32",  # LimeGreen
            "B-": "#32CD32",  # LimeGreen
            "B": "#00BFFF",   # DeepSkyBlue
            "B+": "#1E90FF",  # DodgerBlue
            "A-": "#1E90FF",  # DodgerBlue
            "A": "#9400D3",   # DarkViolet
            "A+": "#8A2BE2"   # BlueViolet
        }
        # Function to apply color formatting to the grades
        def color_format(grade):
            color = grade_colors.get(grade, 'black')  # Default to black if grade not found in grade_colors
            return f"color: {color}; font-weight: bold"

        # Apply color formatting to the grade columns
        for col in ['Valuation Grade', 'Profitability Grade', 'Growth Grade', 'Performance Grade']:
            out_put[col] = out_put[col].apply(lambda x: f"<span style='{color_format(x)}'>{x}</span>")
        

        # Apply conditional formatting with color bars
        color_map = {
            "0-50": "red",
            "50-75": "orange",
            "75-100": "green"
        }

        def color_bar(val):
            val = float(val[:-1])  # Remove '%' and convert to float
            if val <= 50:
                color = color_map["0-50"]
            elif val <= 75:
                color = color_map["50-75"]
            else:
                color = color_map["75-100"]
            return f"background-color: {color}; color: white;"

        # Apply color bar formatting to the "Overall Rating" column
        styled_output = out_put.style.applymap(color_bar, subset=["Overall Rating"])

        # Set CSS properties for table styling
        table_styles = [
            {'selector': 'th', 'props': [('font-weight', 'bold'), ('font-size', 'small')]},
            {'selector': 'td', 'props': [('font-size', 'small')]},
            {'selector': 'table', 'props': [('border', '1px solid white'), ('border-collapse', 'collapse'), ('margin-top', '30px')]}  # Add margin to the top of the table

        ]
        # Assuming 'Analysis Date' is the name of your date column
        #out_put['Date'] = pd.to_datetime(out_put['Date'])
        #out_put['Date'] = out_put['Date'].dt.strftime('%b-%d')  # Format date as Month Abbreviation - Day
        # Reset index before converting to HTML
        #out_put.reset_index(drop=True, inplace=True)

        # Apply table styling and display the output table
        styled_output = styled_output.set_table_styles(table_styles)
        st.write("\n")
        st.write(styled_output.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Button to reset selections
    if st.sidebar.button("Reset Selections"):
        default_values = {input_name: [] for input_name in inputs}

    connection.close()

# Run the main function
if __name__ == "__main__":
    main()
