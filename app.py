import streamlit as st
from supabase import create_client, Client

# --- ضبط الرابط والـ Key بدون مسافات ---
# تأكد يدويًا أن الرابط يبدأ بـ https:// ولا يوجد مسافة في آخره
SUPABASE_URL = "https://hmmtr3ka3sufgqht2qnsq.supabase.co".strip()
SUPABASE_KEY = "حط_هنا_الـ_key_بتاعك_بالكامل".strip()

# إنشاء الاتصال مع صيد الخطأ فوراً
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Critical Connection Error: {e}")

# --- واجهة المستخدم ---
st.set_page_config(page_title="TALENT HOUSE", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1, h2, h3, p, span, label { color: #ffffff !important; }
    div.stButton > button:first-child {
        background-color: #00d4ff; color: #000814;
        border-radius: 12px; box-shadow: 0px 0px 25px #00d4ff;
        width: 100%; font-weight: bold; height: 50px;
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
            # الحساب المميز (Dev) يدخل فوراً مهما كانت حالة الشبكة
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
                    else: st.error("Wrong credentials")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")

    else:
        nu = st.text_input("New Username")
        np = st.text_input("New Password", type="password")
        nr = st.selectbox("Role:", ["Skiller", "Scout"])
        if st.button("REGISTER"):
            if nu and np:
                try:
                    # نرسل فقط البيانات الأساسية ونترك الـ ID للقاعدة
                    supabase.table("users").insert({"username": nu, "password": np, "role": nr}).execute()
                    st.success("Account created! Go to Login.")
                except Exception as e:
                    # لو ظهر Errno -2 هنا، يبقى الرابط اللي نسخته في الكود "مكتوب غلط"
                    st.error(f"System Check: {e}")
else:
    st.title(f"Welcome {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
