import streamlit as st
from supabase import create_client, Client

# 1. Supabase Connection (IMPORTANT: Put your real URL and Key here)
url = "https://your-project-url.supabase.co"
key = "your-anon-key-from-image"
supabase: Client = create_client(url, key)

# 2. Page Config & Electric Style
st.set_page_config(page_title="Talent House", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1, h2, h3, p, span, label { color: #ffffff !important; font-family: 'Arial', sans-serif; }
    
    /* Glowing Electric Blue Buttons */
    div.stButton > button:first-child {
        background-color: #00d4ff; 
        color: #000814;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        box-shadow: 0px 0px 20px #00d4ff;
        width: 100%;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background-color: #001d3d;
        color: white;
        border: 1px solid #00d4ff;
    }
    
    /* Radio/Selectbox Label Color */
    .stRadio [data-testid="stMarkdownContainer"] p { color: #00d4ff !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Auth Interface ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>⚡ TALENT HOUSE</h1>", unsafe_allow_html=True)
    
    auth_choice = st.radio("Select Action:", ["Login", "Sign Up"], horizontal=True)

    if auth_choice == "Login":
        st.subheader("Welcome Back")
        user_input = st.text_input("Username")
        pass_input = st.text_input("Password", type="password")
        
        if st.button("LOGIN"):
            # --- THE SPECIAL DEVELOPER ACCOUNT ---
            if user_input == "Dev" and pass_input == "152007poco":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.success("Welcome, Developer!")
                st.rerun()
            # --------------------------------------
            else:
                try:
                    response = supabase.table("users").select("*").eq("username", user_input).eq("password", pass_input).execute()
                    if len(response.data) > 0:
                        st.session_state.logged_in = True
                        st.session_state.role = response.data[0]['role']
                        st.rerun()
                    else:
                        st.error("Wrong username or password!")
                except:
                    st.error("Database connection error.")

    else:  # Sign Up
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        # Roles: Skiller or Scout
        role_choice = st.selectbox("Register as:", ["Skiller", "Scout"])
        
        if st.button("REGISTER"):
            if new_user and new_pass:
                try:
                    data = {"username": new_user, "password": new_pass, "role": role_choice}
                    supabase.table("users").insert(data).execute()
                    st.success("Account created! Go to Login.")
                except:
                    st.error("Error creating account.")
            else:
                st.warning("Please fill all fields.")

# --- App Interface (After Login) ---
else:
    st.sidebar.markdown(f"<h3 style='color: #00d4ff;'>User: {st.session_state.role}</h3>", unsafe_allow_html=True)
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "Admin":
        st.title("🛠 Developer Dashboard")
        st.write("You have full control over the database.")
        # View All Users
        try:
            users_list = supabase.table("users").select("*").execute()
            st.dataframe(users_list.data)
        except:
            st.info("No users found.")
            
    elif st.session_state.role == "Skiller":
        st.title("⚽ Skiller Area")
        st.write("Welcome, Skiller! Start uploading your skills.")

    elif st.session_state.role == "Scout":
        st.title("🔍 Scout Area")
        st.write("Welcome, Scout! Search for the best talent.")
