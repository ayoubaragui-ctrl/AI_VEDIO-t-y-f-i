import streamlit as st
import asyncio
import time
from engine import HalalSuperBot

st.set_page_config(page_title="Halal AI Bot v2.0", layout="wide", page_icon="🤖")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 نظام النشر الآلي الخارق | عقل اصطناعي سيادي")
st.info("هذا النظام مبرمج للنشر التلقائي (3 فيديوهات يومياً) بأعلى جودة خوارزمية.")

# إدارة الحسابات في ذاكرة الجلسة
if 'accounts' not in st.session_state:
    st.session_state['accounts'] = []

with st.sidebar:
    st.header("🔑 إعدادات الوصول")
    gemini_key = st.text_input("Gemini API Key", value="AIzaSyCbjx_aXkoZ5vll8WvSNJbsGJfLe6o3xcQ")
    pexels_key = st.text_input("Pexels API Key (ضروري)", type="password")
    
    st.divider()
    st.header("👤 ربط حسابات جديدة")
    platform = st.selectbox("المنصة", ["Instagram", "TikTok", "YouTube Shorts"])
    user_input = st.text_input("Username / Email")
    pass_input = st.text_input("Password", type="password")
    niche_input = st.text_input("المجال (Niche)", "مواعظ وقصص إسلامية")
    
    if st.button("➕ إضافة الحساب للجدولة"):
        if user_input and pass_input and pexels_key:
            st.session_state['accounts'].append({
                "user": user_input, 
                "pwd": pass_input, 
                "platform": platform,
                "niche": niche_input
            })
            st.success(f"تم تسجيل {user_input} بنجاح!")
        else:
            st.error("عمر كاع الخانات عفاك!")

# عرض الحسابات النشطة
st.subheader("📊 الحسابات المتصلة الآن")
if st.session_state['accounts']:
    cols = st.columns(len(st.session_state['accounts']))
    for idx, acc in enumerate(st.session_state['accounts']):
        cols[idx].metric(acc['platform'], acc['user'], "Active")
else:
    st.warning("لا توجد حسابات نشطة حالياً. أضف حساباً من القائمة الجانبية.")

st.divider()

# محرك التشغيل الأوتوماتيكي
if st.button("🔥 تفعيل الوحش (Auto-Pilot Mode)"):
    if not st.session_state['accounts']:
        st.error("لازم تزيد حساب واحد على الأقل!")
    else:
        bot = HalalSuperBot(gemini_key, pexels_key)
        st.success("✅ النظام فايق دابا! كيتسنى وقت الذروة باش ينشر.")
        
        async def run_autonomous_loop():
            status_container = st.empty()
            while True:
                for acc in st.session_state['accounts']:
                    status_container.write(f"⏳ جاري تجهيز فيديو لـ {acc['user']} ({acc['platform']})...")
                    try:
                        # 1. صنع المحتوى
                        data = await bot.generate_content_ai(acc['niche'])
                        # 2. المونتاج
                        video_file = await bot.produce_video(data)
                        # 3. النشر الذكي
                        success = bot.publish_insta(acc['user'], acc['pwd'], video_file, data)
                        
                        if success:
                            st.toast(f"✅ تم النشر بنجاح على {acc['user']}!", icon='🚀')
                    except Exception as e:
                        st.error(f"❌ وقع مشكل مع {acc['user']}: {e}")
                
                status_container.write("😴 تمت دورة النشر. سأرتاح لـ 8 ساعات قبل الفيديو القادم.")
                await asyncio.sleep(28800) # 8 ساعات

        asyncio.run(run_autonomous_loop())
