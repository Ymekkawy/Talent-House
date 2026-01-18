import streamlit as st
from supabase import create_client, Client

# 1. التوصيل بقاعدة البيانات (تم نقل الروابط بدقة من صورك)
url = "https://hmmtr3ka3sufgqht2qnsq.supabase.co"
# تأكد إن الـ Key ده هو اللي بيبدأ بـ ey وموجود في صفحة الـ API عندك
key = "PASTE_YOUR_FULL_ANON_KEY_HERE" 

try:
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error(f"Connection Setup Error: {e}")

# 2. تصميم الموقع (أزرق غامق وبرق لامع)
st.set_page_config(page_title="TALENT HOUSE", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1, h2, h3, p, span, label { color: #ffffff !important; }
    div.stButton > button:first-child {
        background-color: #00d4ff; color: #000814;
        border-radius: 12px; box-shadow: 0px 0px 25px #00d4ff;
        width: 100%; font-weight: bold; border: none; height: 50px;
    }
    .stTextInput > div > div > input {
        background-color: #001d3d; color: white; border: 1px solid #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- واجهة الدخول والتسجيل ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>⚡ TALENT HOUSE</h1>", unsafe_allow_html=True)
    auth_choice = st.radio("Action:", ["Login", "Sign Up"], horizontal=True)

    if auth_choice == "Login":
        u_in = st.text_input("Username")
        p_in = st.text_input("Password", type="password")
        if st.button("LOGIN"):
            # حساب المطور (Dev) هيدخلك دايماً حتى لو الداتا بيز وقعت
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
                    st.error(f"Database Error: {e}")

    else:  # واجهة الـ Sign Up
        new_u = st.text_input("Choose Username")
        new_p = st.text_input("Choose Password", type="password")
        role_type = st.selectbox("I am a:", ["Skiller", "Scout"])
        
        if st.button("REGISTER"):
            if new_u and new_p:
                try:
                    # بنبعت البيانات من غير الـ id عشان ميعملش "Username taken"
                    user_data = {"username": new_u, "password": new_p, "role": role_type}
                    supabase.table("users").insert(user_data).execute()
                    st.success("Account created! Go to Login tab.")
                except Exception as e:
                    # لو الرابط غلط، السطر ده هيقولك [Errno -2] تاني
                    st.error(f"System Message: {e}")
            else:
                st.warning("Please fill all fields.")
else:
    st.sidebar.write(f"Logged in as: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    st.title(f"Welcome to {st.session_state.role} Dashboard")
