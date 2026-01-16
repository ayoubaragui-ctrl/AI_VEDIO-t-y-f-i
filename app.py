import streamlit as st
import asyncio
import time
import pandas as pd
import json
import os
from datetime import datetime
from engine import HalalSuperBot

# --- إعدادات نظام المونتاج (ImageMagick) للسيرفر ---
from moviepy.config import change_settings
if os.name != 'nt':
    change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

# إعداد الصفحة
st.set_page_config(page_title="The Sovereign AI Bot v3.0 - Groq Edition", layout="wide", page_icon="📖")

# --- جلب المفاتيح بأمان من Streamlit Secrets ---
try:
    # هنا حيدنا السوارت من وسط الكود
    groq_key = st.secrets["GROQ_KEY"]
    pexels_key = st.secrets["PEXELS_KEY"]
except Exception as e:
    st.error("⚠️ خطأ: المفاتيح غير موجودة في إعدادات Secrets الخاصة بـ Streamlit")
    st.info("تأكد من إضافة GROQ_KEY و PEXELS_KEY في لوحة تحكم Streamlit.")
    st.stop()

# ستايل CSS فخم
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #e0e0e0; }
    .status-online { color: #2ea043; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .stMetric { background-color: #0d1117; border: 1px solid #30363d; border-radius: 15px; padding: 10px; }
    .log-container { background: #111418; padding: 15px; border-radius: 10px; border: 1px solid #30363d; height: 400px; overflow-y: auto; font-family: monospace; border-left: 4px solid #2ea043; }
    .log-success { color: #2ea043; margin-bottom: 5px; border-bottom: 1px solid #1b1f23; padding-bottom: 2px; }
    .log-error { color: #f85149; margin-bottom: 5px; border-bottom: 1px solid #1b1f23; padding-bottom: 2px; }
    </style>
    """, unsafe_allow_html=True)

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

st.title("📖 مركز القيادة الإمبراطوري | التحكم السيادي")
st.markdown(f"**الحالة:** <span class='status-online'>● الماكينة القرآنية جاهزة بذكاء Groq ⚡</span>", unsafe_allow_html=True)

col_left, col_right = st.columns([0.6, 0.4])

with col_left:
    st.subheader("📊 إحصائيات النظام")
    c1, c2, c3 = st.columns(3)
    c1.metric("الحسابات", len(st.session_state['accounts']))
    c2.metric("المحرك", "Groq Llama 3")
    c3.metric("المونتاج", "Ready ✅")

    st.divider()

    # --- إدارة النيش ---
    st.subheader("🎯 التحكم في النيش")
    if st.session_state['accounts']:
        with st.expander("🛠️ تعديل النيش الفوري"):
            all_users = [acc['user'] for acc in st.session_state['accounts']]
            selected_acc_user = st.selectbox("اختر الحساب", ["الكل"] + all_users)
            new_niche_val = st.text_input("النيش الجديد (مثال: قصص الأنبياء)")
            
            if st.button("حفظ التعديلات"):
                for acc in st.session_state['accounts']:
                    if selected_acc_user == "الكل" or acc['user'] == selected_acc_user:
                        acc['niche'] = new_niche_val
                save_accounts(st.session_state['accounts'])
                st.success("✅ تم تحديث النيش!")
                st.rerun()
    
    st.divider()
    
    if st.session_state['accounts']:
        st.write("📋 الحسابات النشطة:")
        bot_temp = HalalSuperBot(groq_key, pexels_key)
        stats = []
        for acc in st.session_state['accounts']:
            stat = bot_temp.get_account_stats(acc['platform'], acc)
            stat['Niche'] = acc.get('niche', 'N/A')
            stats.append(stat)
        st.dataframe(pd.DataFrame(stats), width='stretch')
    else:
        st.info("لا توجد حسابات. أضف حساباً من القائمة الجانبية للبدء.")

    if st.button("🔥 إطلاق الوحش (Start Production)"):
        bot = HalalSuperBot(groq_key, pexels_key)
        
        async def run_smart_scheduler():
            status_container = st.empty()
            log_placeholder = col_right.empty() 
            logs = []
            
            while True:
                st.session_state['accounts'] = load_accounts()
                if not st.session_state['accounts']:
                    status_container.warning("لا توجد حسابات نشطة.")
                    await asyncio.sleep(60); continue

                for acc in st.session_state['accounts']:
                    status_container.info(f"⌛ جاري العمل لـ: {acc['user']} ({acc['niche']})")
                    try:
                        result = await bot.post_immediately(acc)
                        if result:
                            msg = f"[{datetime.now().strftime('%H:%M')}] ✅ تم بنجاح: {acc['user']}"
                            logs.append(f"<div class='log-success'>{msg}</div>")
                        else:
                            logs.append(f"<div class='log-error'>❌ فشل الإنتاج لـ: {acc['user']}</div>")
                    except Exception as err:
                        logs.append(f"<div class='log-error'>❌ خطأ تقني: {str(err)}</div>")
                    
                    log_placeholder.markdown(f"<div class='log-container'>{''.join(logs[::-1])}</div>", unsafe_allow_html=True)
                    await asyncio.sleep(30)
                
                status_container.success("💤 الدورة اكتملت. سأعود للعمل تلقائياً بعد 6 ساعات.")
                await asyncio.sleep(21600) 

        asyncio.run(run_smart_scheduler())

with col_right:
    st.subheader("📜 السجل المباشر (Groq Logs)")
    log_area = st.empty()
    log_area.markdown("<div class='log-container'>في انتظار الأوامر...</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("👤 إضافة حساب")
    p_form = st.selectbox("المنصة", ["YouTube", "FB"])
    u_form = st.text_input("اسم القناة / الصفحة")
    pass_form = st.text_input("Session ID / API Key", type="password")
    niche_form = st.text_input("النيش", "مواعظ إسلامية")
    
    if st.button("➕ إضافة"):
        if u_form and pass_form:
            new_acc = {"user": u_form, "pwd": pass_form, "platform": p_form, "niche": niche_form}
            st.session_state['accounts'].append(new_acc)
            save_accounts(st.session_state['accounts'])
            st.rerun()

    st.divider()
    st.header("🗑️ مسح حساب")
    if st.session_state['accounts']:
        acc_to_del = st.selectbox("اختر للمسح", [f"{a['user']} ({a['platform']})" for a in st.session_state['accounts']])
        if st.button("❌ مسح نهائي"):
            u_rem = acc_to_del.split(" (")[0]
            st.session_state['accounts'] = [a for a in st.session_state['accounts'] if a['user'] != u_rem]
            save_accounts(st.session_state['accounts'])
            st.rerun()

    if st.button("⚠️ فورماط كامل"):
        st.session_state['accounts'] = []
        if os.path.exists(ACCOUNTS_FILE): os.remove(ACCOUNTS_FILE)
        st.rerun()
