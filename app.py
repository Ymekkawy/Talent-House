import streamlit as st
from supabase import create_client, Client

# 1. إعدادات الاتصال بـ Supabase (تأكد من وضع بياناتك هنا)
url = "https://your-project-url.supabase.co"
key = "your-anon-key-from-image"
supabase: Client = create_client(url, key)

# 2. إعدادات الصفحة والألوان (Custom CSS)
st.set_page_config(page_title="Talent House", layout="centered")

st.markdown("""
    <style>
    /* تغيير خلفية الموقع للأزرق الغامق */
    .stApp {
        background-color: #000814;
    }
    
    /* جعل النصوص واضحة باللون الأبيض */
    h1, h2, h3, p, span, label {
        color: #ffffff !important;
        font-family: 'Arial', sans-serif;
    }

    /* ألوان البرق اللامع للأزرار */
    div.stButton > button:first-child {
        background-color: #00d4ff; /* لون برق لامع */
        color: #000814;
        border-radius: 10px;
        border: 2px solid #00d4ff;
        font-weight: bold;
        box-shadow: 0px 0px 15px #00d4ff; /* توهج */
    }

    div.stButton > button:hover {
        background-color: #ffffff;
        color: #00d4ff;
        border: 2px solid #ffffff;
    }

    /* ستايل خاص لمدخلات النصوص */
    .stTextInput > div > div > input {
        background-color: #001d3d;
        color: white;
        border: 1px solid #00d4ff;
    }
    </style>
    """, unsafe_allow_input=True)

# 3. نظام الحالة (Session State)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

# --- واجهة تسجيل الدخول ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>⚡ Talent House</h1>", unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # بيانات المطور
        admin_user = "Dev"
        admin_pass = "152007poco"
        
        if username == admin_user and password == admin_pass:
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
                    st.error("بيانات الدخول غلط يا بطل!")
            except Exception as e:
                st.error("تأكد من ربط قاعدة البيانات بشكل صحيح")

# --- واجهة الموقع بعد الدخول ---
else:
    st.sidebar.markdown(f"<h2 style='color: #00d4ff;'>Welcome, {st.session_state.role}</h2>", unsafe_allow_html=True)
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "Admin":
        st.markdown("<h1 style='color: #00d4ff;'>🛠 لوحة تحكم المطورين</h1>", unsafe_allow_html=True)
        st.write("أهلاً بيك يا Boss.. الموقع تحت سيطرتك.")
        
        # عرض البيانات بشكل منظم
        try:
            users = supabase.table("users").select("*").execute()
            st.subheader("المستخدمين الحاليين")
            st.dataframe(users.data) # عرض جدول تفاعلي
        except:
            st.info("في انتظار ربط الجداول في Supabase")

    else:
        st.markdown(f"<h1>🌟 Talent House - {st.session_state.role} Interface</h1>", unsafe_allow_html=True)
        st.write("مرحباً بك في عالم المواهب.")
