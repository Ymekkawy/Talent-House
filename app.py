import streamlit as st
from supabase import create_client, Client

# 1. Supabase Connection (Fixed URL from your previous images)
url = "https://hmmtr3ka3sufgqht2qnsq.supabase.co"
# Note: Ensure you paste your full 'anon public' key below
key = "PASTE_YOUR_FULL_ANON_KEY_HERE" 
supabase: Client = create_client(url, key)

# 2. UI Styling (Dark Blue & Electric Glow)
st.set_page_config(page_title="TALENT HOUSE", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1, h2, h3, p, span, label { color: #ffffff !important; font-family: 'Arial', sans-serif; }
    
    /* Glowing Electric Blue Buttons */
    div.stButton > button:first-child {
        background-color: #00d4ff; 
        color: #000814;
        border-radius: 10px;
        box-shadow: 0px 0px 25px #00d4ff;
        width: 100%;
        font-weight: bold;
        border: none;
        height: 45px;
    }
    div.stButton > button:hover {
        background-color: #ffffff;
        box-shadow: 0px 0px 35px #ffffff;
    }
    
    /* Input Fields Style */
    .stTextInput > div > div > input {
        background-color: #001d3d;
        color: white;
        border: 1px solid #00d4ff;
    }
    
    /* Radio Button Text Color */
    .stRadio [data-testid="stMarkdownContainer"] p { color: #00d4ff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Session State Logic
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

# --- AUTH INTERFACE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>⚡ TALENT HOUSE</h1>", unsafe_allow_html=True)
    
    auth_choice = st.radio("Select Action:", ["Login", "Sign Up"], horizontal=True)

    if auth_choice == "Login":
        st.subheader("Welcome Back")
        u_input = st.text_input("Username")
        p_input = st.text_input("Password", type="password")
        
        if st.button("LOGIN"):
            # --- THE SPECIAL DEVELOPER ACCOUNT ---
            if u_input == "Dev" and p_input == "152007poco":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.rerun()
            # --- REGULAR USER LOGIN ---
            else:
                try:
                    res = supabase.table("users").select("*").eq("username", u_input).eq("password", p_input).execute()
                    if res.data:
                        st.session_state.logged_in = True
                        st.session_state.role = res.data[0]['role']
                        st.rerun()
                    else:
                        st.error("Invalid Username or Password!")
                except Exception as e:
                    st.error(f"Database Error: {str(e)}")

    else:  # SIGN UP INTERFACE
        st.subheader("Create New Account")
        new_u = st.text_input("Username")
        new_p = st.text_input("Password", type="password")
        role_type = st.selectbox("I am a:", ["Skiller", "Scout"])
        
        if st.button("REGISTER"):
            if new_u and new_p:
                try:
                    user_data = {"username": new_u, "password": new_p, "role": role_type}
                    supabase.table("users").insert(user_data).execute()
                    st.success("Registration Successful! Please go to Login.")
                except Exception as e:
                    st.error("Error: This username might be taken.")
            else:
                st.warning("Please fill all fields!")

# --- APP INTERFACE (AFTER LOGIN) ---
else:
    st.sidebar.markdown(f"<h3 style='color: #00d4ff;'>User: {st.session_state.role}</h3>", unsafe_allow_html=True)
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "Admin":
        st.title("🛠 Admin Dashboard")
        st.write("Welcome Boss. Managing all system users:")
        try:
            users_list = supabase.table("users").select("*").execute()
            st.dataframe(users_list.data)
        except:
            st.info("No users found in database.")
            
    elif st.session_state.role == "Skiller":
        st.title("⚽ Skiller Dashboard")
        st.write("Show your best skills here!")

    elif st.session_state.role == "Scout":
        st.title("🔍 Scout Discovery")
        st.write("Search for the next star!")
