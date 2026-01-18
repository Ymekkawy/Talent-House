import streamlit as st
from supabase import create_client, Client

# 1. إعدادات الاتصال بـ Supabase (حط بياناتك هنا)
url = "https://your-project-url.supabase.co"
key = "your-anon-key-from-image"
supabase: Client = create_client(url, key)

# 2. إعدادات الصفحة والألوان
st.set_page_config(page_title="Talent House", layout="centered")

# الـ CSS المتصلح (تغيير allow_input لـ allow_html)
st.markdown("""
    <style>
    .stApp {
        background-color: #000814; /* أزرق غامق جداً */
    }
    h1, h2, h3, p, span, label {
        color: #ffffff !important;
    }
    /* لون البرق اللامع للأزرار مع توهج */
    div.stButton > button:first-child {
        background-color: #00d4ff; 
        color: #000814;
        border-radius: 10px;
        border: 2px solid #00d4ff;
        font-weight: bold;
        box-shadow: 0px 0px 20px #00d4ff;
    }
    /* ستايل مدخلات النصوص */
    .stTextInput > div > div > input {
        background-color: #001d3d;
        color: white;
        border: 1px solid #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True) # تم التصحيح هنا

# 3. نظام تسجيل الدخول
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>⚡ Talent House</h1>", unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # بيانات المطور (صلاحيات كاملة)
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
                    st.error("بيانات الدخول غلط يا بطل!")
            except:
                st.error("تأكد من إعدادات قاعدة البيانات")

else:
    st.sidebar.markdown(f"<h2 style='color: #00d4ff;'>مرحباً {st.session_state.role}</h2>", unsafe_allow_html=True)
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "Admin":
        st.markdown("<h1 style='color: #00d4ff;'>🛠 لوحة تحكم المطورين</h1>", unsafe_allow_html=True)
        st.write("أهلاً بيك يا Boss.. الموقع دلوقتى شغال تمام.")
        # عرض بيانات المستخدمين
        try:
            users = supabase.table("users").select("*").execute()
            st.dataframe(users.data)
        except:
            st.info("في انتظار بيانات من Supabase")
