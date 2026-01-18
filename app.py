import streamlit as st
from supabase import create_client, Client

# 1. Connection (Links you provided)
url = "https://hmmtr3ka3sufgqht2qnsq.supabase.co"
key = "PASTE_YOUR_ANON_KEY_HERE" 
supabase: Client = create_client(url, key)

# 2. UI Styling (Dark Blue & Electric Glow)
st.set_page_config(page_title="TALENT HOUSE", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1, h2, h3, p, span, label { color: #ffffff !important; font-family: 'Arial', sans-serif; }
    div.stButton > button:first-child {
        background-color: #00d4ff; color: #000814;
        border-radius: 12px; box-shadow: 0px 0px 25px #00d4ff;
        width: 100%; font-weight: bold; border: none; height: 50px;
    }
    .stTextInput > div > div > input {
        background-color: #001d3d; color: white;
        border: 1px solid #00d4ff;
    }
    .stRadio [data-testid="stMarkdownContainer"] p { color: #00d4ff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

# --- AUTH ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>⚡ TALENT HOUSE</h1>", unsafe_allow_html=True)
    auth_choice = st.radio("Select Action:", ["Login", "Sign Up"], horizontal=True)

    if auth_choice == "Login":
        u_in = st.text_input("Username")
        p_in = st.text_input("Password", type="password")
        if st.button("LOGIN"):
            # --- الـ DEV ACCOUNT شغال مهما حصل في الداتا بيز ---
            if u_in == "Dev" and p_in == "152007poco":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.rerun()
            else:
                try:
                    res = supabase.table("users").select("*").eq("username", u_in).eq("password", p_in).execute()
                    if res.data:
                        st.session_state.logged_in = True
                        st.session_state.role = res.data[0]['role']
                        st.rerun()
                    else:
                        st.error("Invalid credentials!")
                except Exception as e:
                    st.error("Database error. Use Dev account.")

    else:  # SIGN UP (The Fixed Part)
        new_u = st.text_input("Username")
        new_p = st.text_input("Password", type="password")
        role_type = st.selectbox("I am a:", ["Skiller", "Scout"])
        
        if st.button("REGISTER"):
            if new_u and new_p:
                try:
                    # تعديل: بنبعت البيانات ونخلي الداتا بيز تتعامل مع الـ ID براحتها
                    user_data = {"username": new_u, "password": new_p, "role": role_type}
                    supabase.table("users").insert(user_data).execute()
                    st.success("Account created! Go to Login.")
                except Exception as e:
                    # هيطلع لك هنا السبب الحقيقي (زي Permission denied لو الـ RLS مفتوح)
                    st.error(f"System Error: {str(e)}")
            else:
                st.warning("Please fill all fields!")

# --- DASHBOARD ---
else:
    st.sidebar.write(f"Logged in as: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    if st.session_state.role == "Admin":
        st.title("🛠 Developer Dashboard")
        try:
            all_users = supabase.table("users").select("*").execute()
            st.dataframe(all_users.data)
        except:
            st.warning("Table is empty or not found.")
    else:
        st.title(f"Welcome {st.session_state.role}!")
