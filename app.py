import streamlit as st
from supabase import create_client, Client

# --- ضبط الرابط والـ Key (تأكد من نقلهم من صفحة API في Supabase) ---
URL = "https://hmmtr3ka3sufgqht2qnsq.supabase.co".strip()
KEY = "ضع_هنا_الـ_anon_key_بتاعك_بالكامل".strip() 

# محاولة الاتصال مع فحص الأخطاء
try:
    supabase: Client = create_client(URL, KEY)
except Exception as e:
    st.error(f"Critical Connection Error: {e}")

# --- التصميم (أزرق غامق وبرق لامع) ---
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

# --- النظام ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>⚡ TALENT HOUSE</h1>", unsafe_allow_html=True)
    mode = st.radio("Action:", ["Login", "Sign Up"], horizontal=True)

    if mode == "Login":
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("LOGIN"):
            # الحساب المميز (Dev) هيدخلك دايماً أوفلاين كـ Admin
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
                    else: st.error("Wrong Username or Password!")
                except Exception as e:
                    st.error(f"Login failed: {e}")

    else: # SIGN UP
        st.subheader("Create Account")
        nu = st.text_input("New Username (English letters)")
        np = st.text_input("New Password", type="password")
        nr = st.selectbox("I am a:", ["Skiller", "Scout"])
        
        if st.button("REGISTER"):
            if nu and np:
                try:
                    # تحويل المدخلات لنصوص نظيفة لمنع خطأ ASCII
                    clean_u = str(nu).strip()
                    clean_p = str(np).strip()
                    # التسجيل بدون ID (القاعدة ستنشئه تلقائياً)
                    supabase.table("users").insert({"username": clean_u, "password": clean_p, "role": nr}).execute()
                    st.success("Account created! Switch to Login tab.")
                except Exception as e:
                    st.error(f"Database says: {e}")
            else: st.warning("Please fill all fields.")
else:
    st.sidebar.write(f"User: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    st.title(f"Welcome to {st.session_state.role} Dashboard")
