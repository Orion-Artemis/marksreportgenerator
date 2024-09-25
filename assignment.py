import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# Paths
USER_DATA_PATH = 'credentials.json'

# Load user data from JSON file
def load_user_data():
    if os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH, 'r') as f:
            return json.load(f)
    return {}

# Save user data to JSON file
def save_user_data(users):
    with open(USER_DATA_PATH, 'w') as f:
        json.dump(users, f)

# Sign-up function (stores user credentials in JSON)
def sign_up():
    st.title("Sign Up")
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    dob = st.date_input("Date of Birth")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign Up"):
        users = load_user_data()
        if email in users:
            st.error("User with this email already exists!")
        else:
            # Save new user details in JSON file
            users[email] = {'name': name, 'phone': phone, 'dob': str(dob), 'password': password, 'marks': {}}
            save_user_data(users)
            os.makedirs(f'./data/{email}', exist_ok=True)  # Create a unique folder for each user
            st.success("User created successfully! Please log in.")

# Login function (checks credentials from JSON file)
def login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        users = load_user_data()
        if email in users and users[email]['password'] == password:
            st.session_state['logged_in'] = True
            st.session_state['email'] = email
            st.session_state['page'] = 'dashboard'  # After login, move to dashboard
            st.success(f"Welcome, {users[email]['name']}!")

        else:
            st.error("Invalid email or password")

# Marks input function with persistent sliders
def input_marks():
    st.title(f"Enter Your Marks")
    
    subjects = ['AAI', 'ATSA', 'FOML', 'VCC', 'F.D.', 'Algo Trading']
    
    # Initialize session state for sliders if not set already
    if 'marks' not in st.session_state:
        st.session_state['marks'] = {subject: 50 for subject in subjects}  # Default 50 for all subjects
    
    # Display sliders for each subject with persistent values
    for subject in subjects:
        st.session_state['marks'][subject] = st.slider(f"Enter marks for {subject}", 0, 100, st.session_state['marks'][subject])
    
    if st.button("Submit"):
        email = st.session_state['email']
        df = pd.DataFrame(list(st.session_state['marks'].items()), columns=["Subject", "Marks"])
        
        # Save marks as a unique CSV file for each user
        user_folder = f'./data/{email}'
        marks_file = f'{user_folder}/marks.csv'
        df.to_csv(marks_file, index=False)
        
        st.success(f"Marks submitted successfully! Saved to {marks_file}")
    
    if st.button("Back to Dashboard"):
        st.session_state['page'] = 'dashboard'  # Return to dashboard

# Generate and display reports
def generate_reports():
    st.title("Your Reports")
    
    email = st.session_state['email']
    marks_path = f'./data/{email}/marks.csv'
    
    if os.path.exists(marks_path):
        df = pd.read_csv(marks_path)
        
        # Bar chart
        st.subheader("Average Marks Bar Chart")
        fig_bar = px.bar(df, x="Subject", y="Marks")
        st.plotly_chart(fig_bar)
        
        # Line chart
        st.subheader("Marks per Subject Line Graph")
        fig_line = px.line(df, x="Subject", y="Marks")
        st.plotly_chart(fig_line)
        
        # Pie chart
        st.subheader("Marks per Subject Pie Chart")
        fig_pie = px.pie(df, names="Subject", values="Marks")
        st.plotly_chart(fig_pie)
    else:
        st.warning("No marks found! Please enter your marks first.")
    
    if st.button("Back to Dashboard"):
        st.session_state['page'] = 'dashboard'  # Return to dashboard

# Main app
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    
    # Sidebar logic for Login and Sign Up
    st.sidebar.title("Navigation")
    
    if not st.session_state['logged_in']:
        # Sign Up and Login options in the sidebar when not logged in
        auth_choice = st.sidebar.radio("Choose Action", ("Login", "Sign Up"))
        
        if auth_choice == "Login":
            login()
        elif auth_choice == "Sign Up":
            sign_up()
    else:
        st.sidebar.success(f"Logged in as {st.session_state['email']}")
        if st.sidebar.button("Sign Out"):
            st.session_state['logged_in'] = False
            st.session_state['email'] = ""
            st.session_state['page'] = 'login'
            st.sidebar.success("Logged out successfully!")
    
    # Dashboard logic
    if st.session_state['logged_in']:
        if st.session_state['page'] == 'dashboard':
            st.title("Dashboard")
            if st.button("Input Marks"):
                st.session_state['page'] = 'input_marks'
            if st.button("See Reports"):
                st.session_state['page'] = 'see_reports'
        elif st.session_state['page'] == 'input_marks':
            input_marks()
        elif st.session_state['page'] == 'see_reports':
            generate_reports()
    else:
        st.write("Please log in or sign up to access the app.")

if __name__ == "__main__":
    main()



# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# import json
# import datetime
 
# # Constants
# USER_DATA_FILE = 'users.json'
 
# # Helper Functions
# def load_user_data():
#     if os.path.exists(USER_DATA_FILE):
#         with open(USER_DATA_FILE, 'r') as f:
#             return json.load(f)
#     return {}
 
# def save_user_data(users):
#     with open(USER_DATA_FILE, 'w') as f:
#         json.dump(users, f)
 
# def create_user_folder(email):
#     if not os.path.exists(email):
#         os.mkdir(email)
 
# def save_marks(email, marks_df):
#     csv_path = os.path.join(email, 'marks.csv')
#     marks_df.to_csv(csv_path, index=False)
 
# def generate_charts(marks_df):
#     # Bar Chart for Average Marks
#     avg_marks = marks_df.mean().reset_index()
#     avg_marks.columns = ['Subject', 'Average Marks']
#     bar_fig = px.bar(avg_marks, x ='Subject', y ='Average Marks', title="Average Marks Per Subject")
 
#     # Line Chart for Marks
#     line_fig = px.line(marks_df.T, title="Marks Per Subject", labels={"value": "Marks", "index": "Subject"})
 
#     # Pie Chart for Marks Distribution
#     total_marks = marks_df.sum().reset_index()
#     total_marks.columns = ['Subject', 'Total Marks']
#     pie_fig = px.pie(total_marks, names = 'Subject', values = 'Total Marks', title = "Marks Distribution")
 
#     return bar_fig, line_fig, pie_fig
 
# # Pages
# def sign_up():
#     st.title("Sign Up Page")
#     name = st.text_input("Name")
#     phone = st.text_input("Phone")
#     dob = st.date_input("DOB", min_value = datetime.datetime(1999, 1, 1))
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
   
#     if st.button("Sign Up"):
#         users = load_user_data()
#         if email in users:
#             st.error("User with this email already exists!")
#         else:
#             users[email] = {"name": name, "phone": phone, "dob": str(dob), "password": password}
#             save_user_data(users)
#             create_user_folder(email)
#             st.success("User registered successfully! Please log in.")
 
# def login():
#     st.title("Login Page")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
   
#     if st.button("Login"):
#         users = load_user_data()
#         if email in users and users[email]["password"] == password:
#             st.session_state["user"] = email
#             st.success("Logged in successfully!")
#             st.experimental_rerun()
#         else:
#             st.error("Invalid email or password")
 
# def enter_marks():
#     st.title(f"Welcome {st.session_state['user']}")
   
#     subjects = ["Maths", "Science", "English", "History", "Geography", "Physics", "Chemistry"]
#     marks = {}
   
#     for subject in subjects:
#         marks[subject] = st.slider(f"Choose your marks for {subject}", 0, 100, 0)
 
#     if st.button("Submit"):
#         marks_df = pd.DataFrame([marks])
#         save_marks(st.session_state["user"], marks_df)
#         st.success("Marks submitted successfully!")
 
# def view_reports():
#     st.title("Your Reports are Ready!")
#     email = st.session_state["user"]
#     csv_path = os.path.join(email, 'marks.csv')
 
#     if os.path.exists(csv_path):
#         marks_df = pd.read_csv(csv_path)
 
#         # Generate charts
#         bar_fig, line_fig, pie_fig = generate_charts(marks_df)
 
#         # Display charts
#         st.plotly_chart(bar_fig)
#         st.plotly_chart(line_fig)
#         st.plotly_chart(pie_fig)
#     else:
#         st.error("No marks data found!")
 
# # Main App Logic
# st.sidebar.title("Navigation")
# page = st.sidebar.selectbox("Go to", ["Sign Up", "Log In", "Enter Marks", "View Reports"])
 
# if "user" not in st.session_state:
#     st.session_state["user"] = None
 
# if page == "Sign Up":
#     sign_up()
# elif page == "Log In":
#     login()
# elif page == "Enter Marks" and st.session_state["user"]:
#     enter_marks()
# elif page == "View Reports" and st.session_state["user"]:
#     view_reports()
# else:
#     st.error("Please log in to access this page.")
 
 