import streamlit as st
from supabase import create_client

st.set_page_config(page_title="WE READ", page_icon="📚")

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

st.title("📚 WE READ")
st.caption("Read Together. Think Together.")

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:

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

            if profile.data["status"] == "approved":
                st.session_state.user = profile.data
                st.rerun()
            else:
                st.warning("Your account is awaiting approval.")

        except Exception as e:
    st.error(f"Login error: {e}")

else:

    profile = st.session_state.user

    st.success("Welcome to WE READ!")

    if profile["role"] == "admin":

        st.header("🛠️ Admin Dashboard")

        st.subheader("Member Management")

        try:
            members = supabase.table("profiles").select("*").execute()
            st.dataframe(members.data)
        except Exception:
            st.error("Could not load members.")

    else:
        st.header("📚 Member Dashboard")

    if st.button("Logout"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()
