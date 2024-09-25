import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime
import os

# MySQL connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",   # Update with your MySQL host
        user="root",        # Update with your MySQL user
        password="Omlande2512@2027", # Update with your MySQL password
        database="auth"
    )

# Functions for interacting with the MySQL database
def add_user(username, password, phone, dob):
    """Insert a new user into the database."""
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password, phone, dob) VALUES (%s, %s, %s, %s)', 
                       (username, password, phone, dob))
        conn.commit()
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def user_exists(username):
    """Check if the username already exists in the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def fetch_all_users():
    """Fetch all users from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, phone, dob FROM users')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def save_initial_csv():
    """Fetch existing users from the database and save them to a CSV file."""
    data = fetch_all_users()
    if data:
        df = pd.DataFrame(data, columns=["Username", "Phone", "DOB"])
        df.to_csv('user_data.csv', index=False)
        # st.success("CSV file created with existing database data.")
        # st.info("No users found in the database.")

def append_user_to_csv(username, phone, dob):
    """Append new user data to the CSV file."""
    file_exists = os.path.isfile('user_data.csv')
    user_data = {'Username': [username], 'Phone': [phone], 'DOB': [dob]}
    df = pd.DataFrame(user_data)
    
    # Append to CSV
    df.to_csv('user_data.csv', mode='a', header=not file_exists, index=False)

def check_login(username, password):
    """Verify if the username and password match."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None


# Check if the CSV needs to be created initially (i.e., if it's missing)
if not os.path.isfile('user_data.csv'):
    save_initial_csv()

# Streamlit App
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Sign Up", "Log In"])

if page == "Sign Up":
    st.title("Welcome to Sign Up")

    with st.form("signup_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        phone = st.text_input("Phone Number")
        dob = st.date_input("Date of Birth", min_value=datetime(1900, 1, 1))
        submit = st.form_submit_button("Sign Up")

    if submit:
        if user_exists(username):
            st.error("Username already exists. Please choose a different one.")
        else:
            # Add user to the database
            add_user(username, password, phone, dob.strftime('%Y-%m-%d'))

            # Append the new user data to the CSV file
            append_user_to_csv(username, phone, dob.strftime('%Y-%m-%d'))

            st.success("Sign Up successful! You can now log in.")

elif page == "Log In":
    st.title("Welcome to Log In")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Log In")

    if submit:
        if check_login(username, password):
            st.success("Logged in successfully!")
        else:
            st.error("Incorrect username or password.")
