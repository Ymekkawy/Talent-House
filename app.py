import streamlit as st
from supabase import create_client, Client

# 1. Supabase Connection (Ensure your URL and Key are here)
url = "https://your-project-url.supabase.co"
key = "your-anon-key-from-image"
supabase: Client = create_client(url, key)

# 2. Page Config & Custom CSS (Dark Blue & Electric Glow)
st.set_page_config(page_title="Talent House", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1, h2, h3, p, span, label { color: #ffffff !important; font-family: 'Arial', sans-serif; }
    
    /* Electric Blue Glowing Buttons */
    div.stButton > button:first-child {
        background-color: #00d4ff; 
        color: #000814;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        box-shadow: 0px 0px 20px #00d4ff;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #ffffff;
        box-shadow: 0px 0px 30px #ffffff;
    }
    
    /* Input Fields Style */
    .stTextInput > div > div > input {
        background-color: #001d3d;
        color: white;
        border: 1px solid #00d4ff;
    }
    /* Radio Button & Selectbox color fix */
    .stRadio [data-testid="stMarkdownContainer"] p { color: #00d4ff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Auth Interface (Login / Sign Up) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>⚡ TALENT HOUSE</h1>", unsafe_allow_html=True)
    
    # Selection Tab
    choice = st.radio("Select Action:", ["Login", "Sign Up"], horizontal=True)

    if choice == "Login":
        st.subheader("Welcome Back")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("LOGIN"):
            # Developer Account
            if username == "Dev" and password == "152007poco":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.rerun()
            else:
                try:
                    response = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
                    if len(response.data) > 0:
                        st.session_state.logged_in = True
                        st.session_state.role = response.data[0]['role']
                        st.rerun()
                    else:
                        st.error("Invalid Username or Password!")
                except:
                    st.error("Connection Error. Check your Database.")

    else:  # Sign Up Interface
        st.subheader("Create New Account")
        new_user = st.text_input("Choose Username")
        new_pass = st.text_input("Choose Password", type="password")
        # Custom roles: Scout or Skiller
        role = st.selectbox("I am a:", ["Skiller", "Scout"])
        
        if st.button("REGISTER"):
            if new_user and new_pass:
                data = {"username": new_user, "password": new_pass, "role": role}
                try:
                    supabase.table("users").insert(data).execute()
                    st.success("Account created successfully! Please Login.")
                except:
                    st.error("Username already exists or Database error.")
            else:
                st.warning("Please fill all fields!")

# --- Main App Interface ---
else:
    st.sidebar.markdown(f"<h2 style='color: #00d4ff;'>Hello, {st.session_state.role}</h2>", unsafe_allow_html=True)
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "Admin":
        st.markdown("<h1 style='color: #00d4ff;'>🛠 Admin Dashboard</h1>", unsafe_allow_html=True)
        st.write("Developer Mode: Full access granted.")
        # Displaying users
        try:
            users = supabase.table("users").select("*").execute()
            st.dataframe(users.data)
        except:
            st.info("No data found in 'users' table.")
    
    elif st.session_state.role == "Skiller":
        st.title("⚽ Skiller Dashboard")
        st.write("Showcase your skills and get noticed!")

    elif st.session_state.role == "Scout":
        st.title("🔍 Scout Dashboard")
        st.write("Find the best talents in the house.")
