import streamlit as st
from supabase import create_client, Client

# 1. إعدادات الاتصال بـ Supabase
url = "https://your-project-url.supabase.co"
key = "your-anon-key-from-image"
supabase: Client = create_client(url, key)

# 2. إعدادات الصفحة والألوان (البرق اللامع والأزرق الغامق)
st.set_page_config(page_title="Talent House", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1, h2, h3, p, span, label { color: #ffffff !important; }
    div.stButton > button:first-child {
        background-color: #00d4ff; 
        color: #000814;
        border-radius: 10px;
        box-shadow: 0px 0px 20px #00d4ff;
        width: 100%;
    }
    .stTextInput > div > div > input {
        background-color: #001d3d;
        color: white;
        border: 1px solid #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. نظام الحالة
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- واجهة الدخول والتسجيل ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>⚡ Talent House</h1>", unsafe_allow_html=True)
    
    # اختيار بين تسجيل الدخول أو إنشاء حساب
    choice = st.radio("اختار العملية:", ["Login", "Sign Up"], horizontal=True)

    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username == "Dev" and password == "152007poco":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.rerun()
            else:
                response = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
                if len(response.data) > 0:
                    st.session_state.logged_in = True
                    st.session_state.role = response.data[0]['role']
                    st.rerun()
                else:
                    st.error("البيانات غلط!")

    else:  # واجهة الـ Sign Up
        new_user = st.text_input("Choose Username")
        new_pass = st.text_input("Choose Password", type="password")
        role = st.selectbox("I am a:", ["Talent", "Scout"])
        
        if st.button("Create Account"):
            if new_user and new_pass:
                data = {"username": new_user, "password": new_pass, "role": role}
                try:
                    supabase.table("users").insert(data).execute()
                    st.success("تم إنشاء الحساب بنجاح! روح اعمل Login بقا.")
                except:
                    st.error("اليوزر ده موجود قبل كده أو فيه مشكلة في السيرفر.")
            else:
                st.warning("املأ البيانات الأول يا بطل!")

# --- واجهة الموقع بعد الدخول ---
else:
    st.sidebar.markdown(f"<h2 style='color: #00d4ff;'>مرحباً {st.session_state.role}</h2>", unsafe_allow_html=True)
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "Admin":
        st.markdown("<h1 style='color: #00d4ff;'>🛠 لوحة التحكم</h1>", unsafe_allow_html=True)
        users = supabase.table("users").select("*").execute()
        st.dataframe(users.data)
    else:
        st.title(f"Welcome to Talent House ({st.session_state.role})")
