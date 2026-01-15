import streamlit as st
import asyncio
import time
import pandas as pd
import json
import os
from datetime import datetime
import google.generativeai as genai
from engine import HalalSuperBot

# --- إعدادات نظام المونتاج (ImageMagick) للسيرفر ---
from moviepy.config import change_settings
if os.name != 'nt':
    change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})
# -----------------------------------------------

# إعداد الصفحة لتكون احترافية وعريضة
st.set_page_config(page_title="The Sovereign AI Bot v3.0", layout="wide", page_icon="🔱")

# جلب السوارت بأمان
try:
    gemini_key = st.secrets["GEMINI_KEY"]
    pexels_key = st.secrets["PEXELS_KEY"]
    genai.configure(api_key=gemini_key)
    chat_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ خطأ في المفاتيح! تأكد من إعداد Secrets.")
    st.stop()

# ستايل CSS إمبراطوري
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #e0e0e0; }
    .chat-box { background: #111418; border-left: 5px solid #2ea043; padding: 20px; border-radius: 10px; margin: 10px 0; }
    .status-online { color: #2ea043; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .stMetric { background-color: #0d1117; border: 1px solid #30363d; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- نظام التخزين ---
ACCOUNTS_FILE = "accounts_data.json"
def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f: json.dump(accounts, f)
def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, "r") as f: return json.load(f)
        except: return []
    return []

if 'accounts' not in st.session_state:
    st.session_state['accounts'] = load_accounts()

# --- واجهة المستخدم ---
st.title("🦾 مركز القيادة الإمبراطوري | التحكم السيادي")
st.markdown(f"**الحالة:** <span class='status-online'>● متصل بالسيرفر العالمي</span>", unsafe_allow_html=True)

# تقسيم الصفحة إلى قسمين (التحكم و الشات)
col_left, col_right = st.columns([0.6, 0.4])

with col_left:
    st.subheader("📊 إحصائيات الإمبراطورية")
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الحسابات", len(st.session_state['accounts']))
    c2.metric("الحالة", "الوحش جاهز" if st.session_state['accounts'] else "في انتظار الأوامر")
    c3.metric("قوة المعالجة", "100%")

    st.divider()
    
    # إدارة الحسابات
    if st.session_state['accounts']:
        bot_temp = HalalSuperBot(gemini_key, pexels_key)
        stats = [bot_temp.get_account_stats(acc['platform'], acc) for acc in st.session_state['accounts']]
        st.dataframe(pd.DataFrame(stats), use_container_width=True)
    else:
        st.info("لا توجد حسابات نشطة حالياً.")

    if st.button("🔥 إطلاق الوحش العابر للمنصات (Global Pilot)"):
        bot = HalalSuperBot(gemini_key, pexels_key)
        st.toast("🚀 جاري تفعيل البروتوكولات السيادية...")
        
        async def run_smart_scheduler():
            status_container = st.empty()
            while True:
                current_hour = datetime.now().hour
                for i, acc in enumerate(st.session_state['accounts']):
                    status_container.info(f"⌛ مراقبة الحساب: {acc['user']} ({acc['platform']})")
                    # النشر الفوري للتجربة أو الجدولة
                    if acc.get('needs_test', True):
                        await bot.post_immediately(acc)
                        st.session_state['accounts'][i]['needs_test'] = False
                        save_accounts(st.session_state['accounts'])
                        st.toast(f"✅ تم نشر فيديو التجربة لـ {acc['user']}")
                
                status_container.info(f"💤 الوحش يراقب الساعة الآن: {current_hour}:00")
                await asyncio.sleep(3600)

        asyncio.run(run_smart_scheduler())

with col_right:
    st.subheader("💬 مستشارك الخاص (AI Empire Chat)")
    st.markdown("اسألني عن أي شيء يخص الحسابات، الاستراتيجيات، أو ماذا يفعل الوحش الآن.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض المحادثة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("تكلم مع الوحش..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # نظام الرد الذكي: يعرف معلومات حساباتك ويحللها
            context = f"أنت العقل المدبر لنظام HalalSuperBot. الحسابات الحالية هي: {st.session_state['accounts']}. أجب بلهجة قوية واحترافية."
            full_prompt = f"{context}\nUser: {prompt}"
            
            response = chat_model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# القائمة الجانبية (إضافة الحسابات)
with st.sidebar:
    st.header("👤 إضافة حساب إمبراطوري")
    p_form = st.selectbox("المنصة", ["Insta", "TikTok", "YouTube", "FB"])
    u_form = st.text_input("اسم المستخدم")
    pass_form = st.text_input("SessionID / Password", type="password")
    niche_form = st.text_input("نيش المحتوى", "مواعظ إسلامية")
    
    if st.button("➕ تثبيت الحساب"):
        if u_form and pass_form:
            new_acc = {"user": u_form, "pwd": pass_form, "platform": p_form, "niche": niche_form, "needs_test": True}
            st.session_state['accounts'].append(new_acc)
            save_accounts(st.session_state['accounts'])
            st.success("تم التثبيت بنجاح!")
        else:
            st.error("أدخل البيانات كاملة!")

    if st.button("🗑️ تصفير النظام"):
        st.session_state['accounts'] = []
        if os.path.exists(ACCOUNTS_FILE): os.remove(ACCOUNTS_FILE)
        st.rerun()
