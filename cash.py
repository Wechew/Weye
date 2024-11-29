import streamlit as st
import pandas as pd
import plotly.express as px
import bcrypt
from datetime import datetime

# Set the page layout
st.set_page_config(page_title="ESX Cash Market Dashboard", layout="wide")

# Login credentials dictionary
USER_CREDENTIALS = {
    "admin@esx.et": bcrypt.hashpw("Laabza^09".encode(), bcrypt.gensalt()).decode('utf-8'),
    "tadele@esx.et": bcrypt.hashpw("esx123".encode(), bcrypt.gensalt()).decode('utf-8')
    "dawit.sernessa@esx.et": bcrypt.hashpw("esx123".encode(), bcrypt.gensalt()).decode('utf-8'),
    "eskedar.sileshi@esx.et": bcrypt.hashpw("esx123".encode(), bcrypt.gensalt()).decode('utf-8'),
    "michael.habte@esx.et": bcrypt.hashpw("esx123".encode(), bcrypt.gensalt()).decode('utf-8')

}

# Function to validate login
def validate_login(email, password):
    if email in USER_CREDENTIALS:
        stored_password = USER_CREDENTIALS[email]
        return bcrypt.checkpw(password.encode(), stored_password.encode('utf-8'))
    return False

# Function to handle login
def login():
    st.markdown('''
    # ESX Inter-Bank Market Data Analytics Dashboard
    Welcome to the ESX Cash Market Data Analytics Dashboard! This dashboard provides interactive visualizations and analyses of ESX's Cash (Inter-bank) market data.
    ''')
    st.image("AAE.png", width=600)

    with st.sidebar:
        st.title("Login")
        email = st.text_input("Email", placeholder="example@esx.et")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login", disabled=st.session_state.get("login_attempt", False))

        if login_button:
            st.session_state["login_attempt"] = True
            if validate_login(email, password):
                st.session_state["authenticated"] = True
                st.session_state["email"] = email
                st.success("Login successful! Redirecting...")
                st.experimental_rerun()  # Force rerun to switch screens
            else:
                st.error("Invalid email or password. Please try again.")
                st.session_state["login_attempt"] = False

        # Footer section for login screen
        st.markdown("---")
        st.markdown("### About the Dashboard")
        st.info("This ESX Cash Market Dashboard provides interactive analytics and visualizations for inter-bank market data. Built with 💻 by Tadele Bizuye.")

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Logout functionality
def logout():
    st.session_state["authenticated"] = False
    st.session_state["login_attempt"] = False
    st.sidebar.info("You have been logged out.")
    st.experimental_rerun()

@st.cache_data
def load_data():
    try:
        url = "https://drive.google.com/uc?id=12Asx-60KIlFtg7iZ2aXJlwOy_BC1cEC_"
        data = pd.read_csv(url, on_bad_lines='skip')
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        return data.dropna(subset=['Date'])  # Drop rows with invalid dates
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

def filter_data(data):
    st.sidebar.subheader("Filters")
    start_date = st.sidebar.date_input("Start Date", datetime(2024, 10, 31))
    end_date = st.sidebar.date_input("End Date", datetime(2025, 12, 30))

    # Ensure the 'Date' column is datetime
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    # Convert start_date and end_date to pandas Timestamp
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter data using 'Date' column
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    return filtered_data


# Calculate KPIs
def calculate_kpis(data):
    # Ensure 'Amount' is numeric and coerce errors to NaN
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')
    # Fill missing values in 'Amount' with 0 or another suitable value
    data['Amount'] = data['Amount'].fillna(0)

    return {
        "Total Volume": f"{data['Amount'].sum():,.2f}",
        "Average Volume": f"{data['Amount'].mean():,.2f}",
        "Trading Days": f"{data['Date'].nunique()}",
        "Max Volume": f"{data['Amount'].max():,.2f}",
        "Min Volume": f"{data['Amount'].min():,.2f}",
        "WAIR": f"{data['WAIR'].mean():,.2f}",
        "Average Price": f"{data['Current'].mean():,.2f}",
        "Total Trades": f"{data['Trades'].sum()}",
    }


# Visualizations
def visualize_data(data):
    st.subheader("Volume Analysis")
    st.plotly_chart(px.bar(data, x='Date', y='Amount', title="Volume Analysis", labels={'Amount': 'Volume', 'Date': 'Date'}))

    st.subheader("Close Price Trends")
    st.plotly_chart(px.line(data, x='Date', y='Current', title="Close Price Trends", labels={'Current': 'Close Price', 'Date': 'Date'}))

    st.subheader("WAIR Trends")
    st.plotly_chart(px.line(data, x='Date', y='WAIR', title="WAIR Trends", labels={'WAIR': 'WAIR', 'Date': 'Date'}))

def main():
    st.title("💰Cash Market Dashboard")
    st.markdown("""Welcome to the **ESX Cash Market Dashboard**. This tool provides insights into daily cash transactions among Ethiopian banks.""")

    # Load and filter data
    # Display Key Metrics with adjusted font sizes
    data = load_data()
    filtered_data = filter_data(data)
    st.header(" 🔑 Key Metrics")
    metrics = calculate_kpis(filtered_data)

    # Custom HTML/CSS for styling
    def custom_metric(label, value):
     return f"""
    <div style="text-align: center; margin: 10px;">
        <p style="font-size:20px; font-weight: bold; margin: 0;">{label}</p>
        <p style="font-size:16px; color: #333333; margin: 0;">{value}</p>
    </div>
    """

    # Columns layout for metrics
    col1, col2, col3, col4 = st.columns(4)
    col5, col6, col7, col8 = st.columns(4)

    col1.markdown(custom_metric("Total Volume", metrics["Total Volume"]), unsafe_allow_html=True)
    col2.markdown(custom_metric("Average Volume", metrics["Average Volume"]), unsafe_allow_html=True)
    col3.markdown(custom_metric("Trading Days", metrics["Trading Days"]), unsafe_allow_html=True)
    col4.markdown(custom_metric("Max Volume", metrics["Max Volume"]), unsafe_allow_html=True)
    col5.markdown(custom_metric("Min Volume", metrics["Min Volume"]), unsafe_allow_html=True)
    col6.markdown(custom_metric("WAIR", metrics["WAIR"]), unsafe_allow_html=True)
    col7.markdown(custom_metric("Average Price", metrics["Average Price"]), unsafe_allow_html=True)
    col8.markdown(custom_metric("Total Trades", metrics["Total Trades"]), unsafe_allow_html=True)


    # Sidebar Menu
    st.sidebar.header("Menu")
    menu = st.sidebar.selectbox("Menu", ["Data Overview", "Charts", "Bar Graph"])

    # Display content based on menu selection
    if menu == "Data Overview":
        st.subheader("Filtered Data")
        st.dataframe(filtered_data)

    elif menu == "Charts":
        visualize_data(filtered_data)

    elif menu == "Bar Graph":
        st.subheader("Bar Graph")
        st.plotly_chart(px.bar(filtered_data, x='Date', y='Amount', color='Current', title="Bar Graph"))

# App logic
if st.session_state["authenticated"]:
    st.sidebar.button("Logout", on_click=logout)
    main()
else:
    login()
