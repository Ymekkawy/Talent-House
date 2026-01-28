import streamlit as st
from supabase import create_client, Client

# --- 1. البيانات المسحوبة من صورك (ممنوع تغييرها) ---
# الرابط والـ Key دول اللي ظهروا في صورك السابقة
URL = "https://hmmtr3ka3sufgqht2qnsq.supabase.co".strip()
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhtbXRyM2thM3N1ZmdxaHQycW5zcSIsInJvbGUiOiJhbm9uIiwiaWF0IjoxNzM1OTMwNjkzLCJleHAiOjIwNTE1MDY2OTN9.vV_Hn6E0fF7o7rX-Qh7l9Z9n3n5v8p8f5w5r5" 

# التأكد من الاتصال
try:
    supabase: Client = create_client(URL, KEY)
except Exception as e:
    st.error(f"Connection Setup Error: {e}")

# --- 2. ستايل "البرق اللامع" (Dark Blue & Neon) ---
st.set_page_config(page_title="TALENT HOUSE", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1, h2, h3, p, span, label { color: #ffffff !important; }
    div.stButton > button:first-child {
        background-color: #00d4ff; color: #000814;
        border-radius: 12px; box-shadow: 0px 0px 30px #00d4ff;
        width: 100%; font-weight: bold; border: none; height: 55px;
        font-size: 20px;
    }
    div.stButton > button:hover {
        background-color: #ffffff; box-shadow: 0px 0px 40px #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #001d3d; color: white; border: 1px solid #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- 3. نظام الدخول والتسجيل ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>⚡ TALENT HOUSE</h1>", unsafe_allow_html=True)
    mode = st.radio("Select Action:", ["Login", "Sign Up"], horizontal=True)

    if mode == "Login":
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("LOGIN"):
            # الحساب المميز بتاعك شغال أوفلاين كحماية إضافية
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
                    else: st.error("Invalid Username or Password!")
                except Exception as e:
                    st.error(f"Database Error: {e}")

    else: # SIGN UP
        nu = st.text_input("New Username (English only)")
        np = st.text_input("New Password", type="password")
        nr = st.selectbox("I am a:", ["Skiller", "Scout"])
        
        if st.button("REGISTER"):
            if nu and np:
                try:
                    # بنسجل البيانات والـ ID بيتعمل لوحده في القاعدة
                    user_data = {"username": str(nu).strip(), "password": str(np).strip(), "role": nr}
                    supabase.table("users").insert(user_data).execute()
                    st.success("Account Created! Now switch to Login tab.")
                except Exception as e:
                    st.error(f"Registration Error: {e}")
            else: st.warning("Please fill all fields.")

else:
    # لوحة التحكم بعد الدخول
    st.sidebar.markdown(f"<h3 style='color: #00d4ff;'>Hello, {st.session_state.role}</h3>", unsafe_allow_html=True)
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    if st.session_state.role == "Admin":
        st.title("🛠 Developer Dashboard")
        data = supabase.table("users").select("*").execute()
        st.dataframe(data.data)
    else:
        st.title(f"Welcome to {st.session_state.role} Panel")
