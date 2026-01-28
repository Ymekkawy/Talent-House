import streamlit as st
from supabase import create_client, Client

# 1. Database Connection (Ensure URL and Key are correct)
URL = "https://hmmtr3ka3sufgqht2qnsq.supabase.co".strip()
KEY = "YOUR_ANON_KEY_HERE".strip() # ضع هنا الـ Anon Key الخاص بك
supabase: Client = create_client(URL, KEY)

# 2. UI Customization (Dark Blue & Electric Glow)
st.set_page_config(page_title="TALENT HOUSE", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1, h2, h3, p, span, label { color: #ffffff !important; font-family: 'Arial', sans-serif; }
    
    /* Electric Blue Glowing Buttons */
    div.stButton > button:first-child {
        background-color: #00d4ff; 
        color: #000814;
        border-radius: 12px;
        box-shadow: 0px 0px 25px #00d4ff;
        width: 100%;
        font-weight: bold;
        border: none;
        height: 50px;
    }
    div.stButton > button:hover {
        background-color: #ffffff;
        box-shadow: 0px 0px 35px #ffffff;
    }
    
    /* Dark Input Fields */
    .stTextInput > div > div > input {
        background-color: #001d3d;
        color: white;
        border: 1px solid #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logic & Auth
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>⚡ TALENT HOUSE</h1>", unsafe_allow_html=True)
    mode = st.radio("Select Action:", ["Login", "Sign Up"], horizontal=True)

    if mode == "Login":
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        
        if st.button("LOGIN"):
            # Developer Account (Manual Check)
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
                    else:
                        st.error("Invalid Username or Password")
                except Exception as e:
                    st.error("Connection failed. Please use Developer login.")

    else:  # Sign Up
        nu = st.text_input("New Username")
        np = st.text_input("New Password", type="password")
        nr = st.selectbox("Register as:", ["Skiller", "Scout"])
        
        if st.button("REGISTER"):
            if nu and np:
                try:
                    # Preventing ASCII errors by ensuring clean input
                    user_data = {"username": str(nu), "password": str(np), "role": str(nr)}
                    supabase.table("users").insert(user_data).execute()
                    st.success("Account created! Now go to Login.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please fill all fields")

# 4. Dashboard
else:
    st.sidebar.write(f"Logged in as: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "Admin":
        st.title("🛠 Developer Dashboard")
        try:
            data = supabase.table("users").select("*").execute()
            st.dataframe(data.data)
        except:
            st.info("Database table is empty.")
    else:
        st.title(f"Welcome {st.session_state.role}!")
        st.write("Your specialized dashboard is coming soon.")
