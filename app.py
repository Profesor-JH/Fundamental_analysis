import streamlit as st
import mysql.connector
import yaml
import pandas as pd
import base64

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
    joins = {
        "Ticker": ["Dimension_Company", "b", "ON a.Ticker = b.Ticker"],
        "Company": ["Dimension_Company", "c", "ON a.Ticker = c.Ticker"],
        "Sector": ["Dimension_Sector", "d", "ON a.Ticker = d.Ticker"],
        "Industry": ["Dimension_Industry", "e", "ON a.Ticker = e.Ticker"],
        "Country": ["Dimension_Country", "f", "ON a.Ticker = f.Ticker"]
    }

    query = f"SELECT DISTINCT a.`{column_name}` FROM `{table_name}` a"
    conditions = []
    for column, value in selected_values.items():
        if column in joins:
            join_table, alias, join_condition = joins[column]
            query += f" JOIN {join_table} {alias} {join_condition}"
            if value is not None and value != [] and value != "None":
                if isinstance(value, str):
                    conditions.append(f"{alias}.{column} = '{value}'")
                else:
                    if None in value:
                        conditions.append(f"{alias}.{column} IS NULL")
                    else:
                        quoted_values = ",".join([f"'{v}'" for v in value])
                        conditions.append(f"{alias}.{column} IN ({quoted_values})")
        else:
            if value is not None and value != [] and value != "None":
                if isinstance(value, str):
                    conditions.append(f"a.{column_name} = '{value}'")
                else:
                    if None in value:
                        conditions.append(f"a.{column_name} IS NULL")
                    else:
                        quoted_values = ",".join([f"'{v}'" for v in value])
                        conditions.append(f"a.{column_name} IN ({quoted_values})")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    cursor.execute(query)
    distinct_values = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return distinct_values

def fetch_data(connection, company=None, sector=None, industry=None, country=None):
    cursor = connection.cursor()
    query = """
        SELECT a.Date as Analysis_Date, Company, Sector, Industry, Country, a.Valuation_Grade,
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
    cursor.close()
    return data

def main():
    @st.cache_data
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    def set_png_as_page_bg(png_file1, png_file2):
        bin_str1 = get_base64_of_bin_file(png_file1)
        bin_str2 = get_base64_of_bin_file(png_file2)
        page_bg_img = f'''
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{bin_str1}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white;
        }}
        [data-testid="stSidebar"] {{
            background-image: url("data:image/png;base64,{bin_str2}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)

    set_png_as_page_bg("Quant_5.png", "Quant_5.png")

    app_name = "S.n.i.p.e.r"

    # Gradient colors from red to green
    legend = {
        "D-": ("Poor", "#FF0000"),
        "D": ("Below Average", "#FF4500"),
        "D+": ("Average", "#FFA500"),
        "C-": ("Average", "#FFD700"),
        "C": ("Above Average", "#ADFF2F"),
        "C+": ("Good", "#7FFF00"),
        "B-": ("Good", "#32CD32"),
        "B": ("Very Good", "#00FF00"),
        "B+": ("Excellent", "#00FA9A"),
        "A-": ("Excellent", "#00CED1"),
        "A": ("Outstanding", "#1E90FF"),
        "A+": ("Exceptional", "#9400D3")
    }

    st.markdown(f"<h1 style='font-family: Georgia, serif; color: white;'>{app_name}</h1>", unsafe_allow_html=True)


    legend_html = "<div style='border: 0.6px solid black; padding: 20px; margin: 5px 0; margin-right: -170px;border-radius: 10px; background: linear-gradient(to right, rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.1)); width: 200%;'>"
    legend_html += "<div style='display:flex; justify-content:space-between; font-size: medium; font-weight: bold; color: black;'>"

    for grade, (description, color) in legend.items():
        legend_html += f"<div style='margin-right: 40px; text-align: center;'><br><span style='color:{color}; font-size: x-large;'>{grade}</span><br><span style='color: {color};font-size: x-medium;font-weight: bold'>{description}</span></div>"

    
    legend_html += "</div>"
    legend_html += "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)
    # Custom CSS for sidebar width and styling
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            min-width: 300px;
            max-width: 300px;
            background-color: #4CAF50; /* Sidebar background color */
            background: linear-gradient(to right, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.1));
            color: white; /* Text color */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        /* Style for sidebar buttons */
        [data-testid="stSidebar"] button {
            background-color: #008CBA; /* Button background color */
            color: white; /* Button text color */
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }

        /* Hover effect for sidebar buttons */
        [data-testid="stSidebar"] button:hover {
            background-color: #005266; /* Darker background color on hover */
        }

        /* Style for custom buttons */
        [data-testid="custom-button"] {
            background-color: #8A2BE2; /* Luxurious purple background */
            color: white; /* Button text color */
            border: none;
            padding: 12px 24px; /* Larger padding for a luxurious feel */
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 18px; /* Larger font size for a luxurious feel */
            margin: 6px 3px;
            cursor: pointer;
            border-radius: 8px; /* More rounded corners for a luxurious feel */
            transition: background-color 0.3s ease, transform 0.3s ease; /* Smooth transition effects */
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3); /* Add a shadow for a luxurious feel */
        }

        /* Hover effect for custom buttons */
        [data-testid="custom-button"]:hover {
            background-color: #5D3FD3; /* Darker luxurious purple on hover */
            transform: translateY(-2px); /* Slight lift effect on hover */
        }
        </style>
        """,
        unsafe_allow_html=True
    )



    # Enhance sidebar texts
    #st.sidebar.markdown(f"<h1 style='text-align: left; color: white; font-size: 36px;'>{app_name}</h1>", unsafe_allow_html=True)
    #st.sidebar.markdown(f"<p style='text-align: left; font-size: 20px; color: white;'>Select criteria to filter the fundamental analysis data.</p>", unsafe_allow_html=True)

    default_values = {
        "Ticker": [],
        "Company": [],
        "Sector": [],
        "Industry": [],
        "Country": []
    }

    selected_values = {}

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
            "D-": "#FF0000",  # Tomato
            "D": "FF4500",   # LightSalmon
            "D+": "#FFA500",  # Gold
            "C-": "#FFD700",  # Gold
            "C": "#ADFF2F",   # GreenYellow
            "C+": "#7FFF00",  # LimeGreen
            "B-": "#32CD32",  # LimeGreen
            "B": "#00FF00",   # DeepSkyBlue
            "B+": "#00FA9A",  # DodgerBlue
            "A-": "#00CED1",  # DodgerBlue
            "A": "#1E90FF",   # DarkViolet
            "A+": "#9400D3"   # BlueViolet
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


        # Generate HTML for the styled output
        styled_html = styled_output.to_html(escape=False, index=False)

        # Wrap HTML in a container div
        table_html = f"""
            <div class="table-container">
                {styled_html}
            </div>
        """

        # Display the HTML in Streamlit
        st.markdown(table_html, unsafe_allow_html=True)

        st.markdown(
        """
        <style>
        .table-container {
            width: 200%;
            border: 1px solid black;
            border-collapse: collapse;
            margin-top: 30px;
            background: linear-gradient(to right, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.1));
        }
        .table-container th {
            font-weight: bold;
            font-size: medium;
            color: black
        }
        .table-container td {
            font-size: medium;
        }
        .table-container tbody tr:hover {
            background-color: #005266;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Button to reset selections
    if st.sidebar.button("Reset Selections"):
        default_values = {input_name: [] for input_name in inputs}

    connection.close()

# Run the main function
if __name__ == "__main__":
    main()
