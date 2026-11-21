import streamlit as st
from supabase import create_client

st.set_page_config(page_title="WE READ", page_icon="📚")

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

st.title("📚 WE READ")
st.caption("Read Together. Think Together.")

menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Register"]
)

if menu == "Register":
    st.subheader("Create your account")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        try:
            result = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            st.success("Account created! Wait for admin approval.")

        except Exception as e:
            st.error(str(e))

elif menu == "Login":
    st.subheader("Member Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            result = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            user_id = result.user.id

            profile = supabase.table("profiles").select(
                "*"
            ).eq("id", user_id).single().execute()

            if profile.data["status"] != "approved":
                st.warning("Your account is awaiting approval.")
            else:
                st.session_state["user"] = profile.data
                st.success("Welcome to WE READ!")

                if profile.data["role"] == "admin":
                    st.header("Admin Dashboard")
                    st.write("Member Management")

                    members = supabase.table(
                        "profiles"
                    ).select("*").execute()

                    st.dataframe(members.data)

        except Exception:
            st.error("Login failed. Please check your credentials.")
