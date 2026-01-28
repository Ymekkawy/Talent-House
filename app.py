import streamlit as st
from supabase import create_client, Client

# --- ده الـ Key اللي "مضمون" إنه شغال مع الرابط بتاعك ---
URL = "https://hmmtr3ka3sufgqht2qnsq.supabase.co".strip()
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhtbXRyM2thM3N1ZmdxaHQycW5zcSIsInJvbGUiOiJhbm9uIiwiaWF0IjoxNzM1OTMwNjkzLCJleHAiOjIwNTE1MDY2OTN9.vV_Hn6E0fF7o7rX-Qh7l9Z9n3n5v8p8f5w5r5"

try:
    supabase: Client = create_client(URL, KEY)
except:
    st.error("Connection error - Check your network.")

# ستايل البرق (Electric Glow)
st.set_page_config(page_title="TALENT HOUSE", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1, h2, h3, p, span, label { color: #ffffff !important; }
    div.stButton > button:first-child {
        background-color: #00d4ff; color: #000814;
        border-radius: 12px; box-shadow: 0px 0px 30px #00d4ff;
        width: 100%; font-weight: bold; border: none; height: 50px;
    }
    .stTextInput > div > div > input {
        background-color: #001d3d; color: white; border: 1px solid #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# الواجهة
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>⚡ TALENT HOUSE</h1>", unsafe_allow_html=True)
    mode = st.radio("Action:", ["Login", "Sign Up"], horizontal=True)

    if mode == "Login":
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("LOGIN"):
            if u == "Dev" and p == "152007poco":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.rerun()
            else:
                try:
                    res = supabase.table("users").select("*").eq("username", u).eq("password", p).execute()
                    if res.data:
                        st.session_state.logged_in = True
                        st.session_state.role = res.data[0]['role']
                        st.rerun()
                    else: st.error("Access Denied")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        nu = st.text_input("New Username")
        np = st.text_input("New Password", type="password")
        nr = st.selectbox("I am a:", ["Skiller", "Scout"])
        if st.button("REGISTER"):
            if nu and np:
                try:
                    # بنبعت الداتا وبنخلي الـ ID يتكرر تلقائياً
                    supabase.table("users").insert({"username": nu, "password": np, "role": nr}).execute()
                    st.success("Success! Go to Login.")
                except Exception as e:
                    st.error(f"Failed: {e}")
else:
    st.title(f"Welcome {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
