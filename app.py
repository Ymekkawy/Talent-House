import streamlit as st
from supabase import create_client, Client

# 1. Supabase Connection
url = "https://your-project-url.supabase.co"
key = "your-anon-key"
supabase: Client = create_client(url, key)

# 2. UI Styling (Dark Blue & Electric Blue)
st.set_page_config(page_title="TALENT HOUSE", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1, h2, h3, p, span, label { color: #ffffff !important; font-family: 'Arial', sans-serif; }
    div.stButton > button:first-child {
        background-color: #00d4ff; 
        color: #000814;
        border-radius: 10px;
        box-shadow: 0px 0px 20px #00d4ff;
        width: 100%;
        font-weight: bold;
    }
    .stTextInput > div > div > input {
        background-color: #001d3d;
        color: white;
        border: 1px solid #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- AUTH ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>⚡ TALENT HOUSE</h1>", unsafe_allow_html=True)
    auth_choice = st.radio("Select Action:", ["Login", "Sign Up"], horizontal=True)

    if auth_choice == "Login":
        u_in = st.text_input("Username")
        p_in = st.text_input("Password", type="password")
        if st.button("LOGIN"):
            # Special Dev Account
            if u_in == "Dev" and p_in == "152007poco":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.rerun()
            else:
                res = supabase.table("users").select("*").eq("username", u_in).eq("password", p_in).execute()
                if res.data:
                    st.session_state.logged_in = True
                    st.session_state.role = res.data[0]['role']
                    st.rerun()
                else:
                    st.error("Invalid credentials!")

    else:  # SIGN UP
        new_u = st.text_input("Username")
        new_p = st.text_input("Password", type="password")
        role_type = st.selectbox("Register as:", ["Skiller", "Scout"])
        
        if st.button("REGISTER"):
            if new_u and new_p:
                try:
                    # مصلح: إرسال البيانات بشكل صريح للجدول
                    user_data = {"username": new_u, "password": new_p, "role": role_type}
                    response = supabase.table("users").insert(user_data).execute()
                    st.success(f"Welcome {new_u}! Account created. Now go to Login.")
                except Exception as e:
                    # هيطلع لك هنا المشكلة بالظبط لو الجدول مش شغال
                    st.error(f"Database Error: {str(e)}")
            else:
                st.warning("Please fill all fields!")

# --- APP ---
else:
    st.sidebar.write(f"Logged in as: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.title(f"Welcome to the {st.session_state.role} Dashboard")
