import streamlit as st
from supabase import create_client, Client
import uuid

# --- 1. إعدادات الاتصال بـ Supabase ---
# تم استخراج البيانات من صورتك
SUPABASE_URL = "https://zlsqokeylcbsemdvvqal.supabase.co"
SUPABASE_KEY = "sb_publishable_am-S-1xfHkCQZASKMeh-ZI7Q_OU11X..." # يفضل استخدام الـ Anon Key الكامل من الخانة الأولى

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("خطأ في الاتصال بالسيرفر. تأكد من الـ Keys.")

# --- 2. تصميم الواجهة (نيون مودرن) ---
st.set_page_config(page_title="Talent House 2026", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050510; color: white; }
    .talent-card {
        background: rgba(20, 20, 35, 0.9);
        padding: 25px; border-radius: 15px;
        border: 1px solid #21d4fd;
        box-shadow: 0 0 15px rgba(33, 212, 253, 0.2);
        margin-bottom: 20px;
    }
    .neon-blue { color: #21d4fd; text-shadow: 0 0 10px #21d4fd; }
    .neon-purple { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; }
    .stButton>button {
        background: linear-gradient(90deg, #21d4fd 0%, #bc13fe 100%);
        color: white; border-radius: 10px; border: none; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. منطق الجلسة (Session) ---
if 'user' not in st.session_state:
    st.session_state.user = None

# --- 4. واجهة تسجيل الدخول ---
def login_page():
    st.markdown("<h1 class='neon-blue' style='text-align: center;'>TALENT HOUSE</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        tab1, tab2 = st.tabs(["Login", "Join the House"])
        with tab1:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("Log In"):
                if u == "admin_dev" and p == "power_2026": # أكونت المطور
                    st.session_state.user = {"username": "admin_dev", "role": "Admin", "tokens": 9999}
                    st.rerun()
                # هنا يتم التحقق من قاعدة البيانات للمستخدمين العاديين
                res = supabase.table("profiles").select("*").eq("username", u).eq("password", p).execute()
                if res.data:
                    st.session_state.user = res.data[0]
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
        
        with tab2:
            new_u = st.text_input("New Username")
            new_p = st.text_input("New Password", type="password")
            role = st.selectbox("Role", ["Talent", "Scout"])
            if st.button("Sign Up"):
                data = {"username": new_u, "password": new_p, "role": role, "tokens": 50}
                supabase.table("profiles").insert(data).execute()
                st.success("Account Created! Now Login.")

# --- 5. التطبيق الرئيسي بعد الدخول ---
def main_app():
    user = st.session_state.user
    st.sidebar.markdown(f"<h2 class='neon-purple'>Welcome, {user['username']}</h2>", unsafe_allow_html=True)
    st.sidebar.write(f"Tokens: {user['tokens']} ⚡")
    
    if st.sidebar.button("Log Out"):
        st.session_state.user = None
        st.rerun()

    # --- لوحة المطور (Admin) ---
    if user['username'] == "admin_dev":
        st.header("🛠 Developer Control Hub")
        users_list = supabase.table("profiles").select("*").execute().data
        for u in users_list:
            col1, col2 = st.columns([3,1])
            col1.write(f"👤 {u['username']} | Role: {u['role']} | Tokens: {u['tokens']}")
            if col2.button(f"Ban", key=u['username']):
                supabase.table("profiles").delete().eq("username", u['username']).execute()
                st.rerun()

    # --- واجهة الموهوب (Talent) ---
    elif user['role'] == "Talent":
        st.header("Post Your Talent")
        with st.expander("➕ Upload New Work (30 Tokens)"):
            cat = st.selectbox("Category", ["Singer", "Actor", "Developer", "Gamer", "Sportsman", "Musician"])
            content = st.text_area("Share your link or story")
            if st.button("Publish"):
                if user['tokens'] >= 30:
                    new_tokens = user['tokens'] - 30
                    supabase.table("posts").insert({"author": user['username'], "category": cat, "content": content}).execute()
                    supabase.table("profiles").update({"tokens": new_tokens}).eq("username", user['username']).execute()
                    st.session_state.user['tokens'] = new_tokens
                    st.success("Published!")
                else:
                    st.error("Not enough tokens!")

        # المتجر ببياناتك الحقيقية
        st.markdown("---")
        st.subheader("🛒 Tokens Store")
        st.info(f"Vodafone Cash: **+20 101 008 0975**")
        st.warning(f"InstaPay (Telda): **5484 4608 6486 5852**")
        st.write("100 EGP = 10 Tokens. Upload receipt for approval.")

    # --- واجهة الكشاف (Scout) ---
    elif user['role'] == "Scout":
        st.header("🎯 Discover Talents")
        posts = supabase.table("posts").select("*").execute().data
        for p in posts:
            st.markdown(f"""<div class='talent-card'>
                <h3 class='neon-blue'>{p['author']}</h3>
                <p>Category: {p['category']}</p>
                <p>{p['content']}</p>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Award 40 Tokens (Good Rating)", key=p['id']):
                # إضافة توكنات للموهوب
                target = supabase.table("profiles").select("tokens").eq("username", p['author']).single().execute().data
                supabase.table("profiles").update({"tokens": target['tokens'] + 40}).eq("username", p['author']).execute()
                st.success(f"Tokens sent to {p['author']}!")

# تشغيل
if st.session_state.user is None:
    login_page()
else:
    main_app()
