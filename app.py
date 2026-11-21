import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="WE READ",
    page_icon="📚",
    layout="wide"
)

st.title("📚 WE READ")
st.subheader("Read Together. Think Together.")

st.write("Welcome to our reading community!")
