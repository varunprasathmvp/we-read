import streamlit as st
from supabase import create_client

st.set_page_config(page_title="WE READ", page_icon="📚")

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

st.title("📚 WE READ")
st.subheader("Read Together. Think Together.")

menu = st.selectbox("Choose an option", ["Login", "Register"])

if menu == "Register":
    st.header("Create Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        try:
            supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            st.success("Registration successful! Wait for admin approval.")
        except Exception as e:
            st.error(str(e))

else:
    st.header("Member Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            result = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            st.success("Login successful!")
            st.write("Welcome to WE READ!")
        except Exception as e:
            st.error("Login failed. Check your email and password.")
