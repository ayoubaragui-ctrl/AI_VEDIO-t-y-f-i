import streamlit as st
import asyncio
import time
from engine import HalalSuperBot

st.set_page_config(page_title="Halal AI Bot v2.0 - Universal", layout="wide", page_icon="🌍")

# ستايل احترافي مع دعم المنصات
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #28a745; color: white; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 نظام النشر الآلي العالمي | 4 منصات في نظام واحد")
st.info("النظام الآن يدعم: Instagram, Facebook, TikTok, YouTube Shorts بنشر ذكي ومتزامن.")

# إدارة الحسابات في ذاكرة الجلسة
if 'accounts' not in st.session_state:
    st.session_state['accounts'] = []

with st.sidebar:
    st.header("🔑 إعدادات الوصول العامة")
    gemini_key = st.text_input("Gemini API Key", value="AIzaSyCbjx_aXkoZ5vll8WvSNJbsGJfLe6o3xcQ")
    pexels_key = st.text_input("Pexels API Key (ضروري)", type="password")
    
    st.divider()
    st.header("👤 ربط الحسابات (4 منصات)")
    
    # استخدام Tabs باش يبانو الخانات منظمين وكلهم متاحين
    t1, t2, t3, t4 = st.tabs(["Insta", "FB", "TikTok", "YouTube"])
    
    with t1:
        u_insta = st.text_input("Insta User", key="ui")
        p_insta = st.text_input("Insta Pass", type="password", key="pi")
        if st.button("➕ ربط Instagram"):
            if u_insta and p_insta:
                st.session_state['accounts'].append({"user": u_insta, "pwd": p_insta, "platform": "Instagram", "niche": "مواعظ"})
                st.success("تم!")

    with t2:
        u_fb = st.text_input("Page ID", key="ufb")
        p_fb = st.text_input("Access Token", type="password", key="pfb")
        if st.button("➕ ربط Facebook"):
            if u_fb and p_fb:
                st.session_state['accounts'].append({"user": u_fb, "pwd": p_fb, "platform": "Facebook Reels", "niche": "مواعظ"})
                st.success("تم!")

    with t3:
        u_tk = st.text_input("TikTok User", key="utk")
        p_tk = st.text_input("Session ID", type="password", key="ptk")
        if st.button("➕ ربط TikTok"):
            if u_tk and p_tk:
                st.session_state['accounts'].append({"user": u_tk, "pwd": p_tk, "platform": "TikTok", "niche": "مواعظ"})
                st.success("تم!")

    with t4:
        u_yt = st.text_input("Channel Name", key="uyt")
        p_yt = st.text_input("Auth Data", type="password", key="pyt")
        if st.button("➕ ربط YouTube"):
            if u_yt and p_yt:
                st.session_state['accounts'].append({"user": u_yt, "pwd": p_yt, "platform": "YouTube Shorts", "niche": "مواعظ"})
                st.success("تم!")

# عرض الحسابات النشطة بتنسيق جديد
st.subheader("📊 إمبراطورية الحسابات المتصلة")
if st.session_state['accounts']:
    cols = st.columns(min(len(st.session_state['accounts']), 4))
    for idx, acc in enumerate(st.session_state['accounts']):
        col_idx = idx % 4
        with cols[col_idx]:
            st.metric(label=acc['platform'], value=acc['user'], delta="جاهز للنشر")
else:
    st.warning("لا توجد حسابات نشطة حالياً.")

st.divider()

# محرك التشغيل الأوتوماتيكي المطور
if st.button("🔥 إطلاق الوحش العابر للمنصات (Global Pilot)"):
    if not st.session_state['accounts']:
        st.error("لازم تزيد حساب واحد على الأقل!")
    elif not pexels_key:
        st.error("Pexels Key ضروري للمونتاج!")
    else:
        bot = HalalSuperBot(gemini_key, pexels_key)
        st.success("✅ تم تفعيل الذكاء السيادي!")
        
        async def run_autonomous_loop():
            status_container = st.empty()
            while True:
                for acc in st.session_state['accounts']:
                    status_container.write(f"⏳ جاري تجهيز فيديو لـ {acc['user']} على {acc['platform']}...")
                    try:
                        data = await bot.generate_content_ai(acc['niche'])
                        video_file = await bot.produce_video(data)
                        
                        success = False
                        if acc['platform'] == "Instagram":
                            success = bot.publish_insta(acc['user'], acc['pwd'], video_file, data)
                        elif acc['platform'] == "Facebook Reels":
                            success = bot.publish_facebook(acc['user'], acc['pwd'], video_file, data)
                        elif acc['platform'] == "TikTok":
                            success = bot.publish_tiktok(acc['user'], acc['pwd'], video_file, data)
                        elif acc['platform'] == "YouTube Shorts":
                            success = bot.publish_youtube(acc['user'], acc['pwd'], video_file, data)
                        
                        if success:
                            st.toast(f"✅ تم النشر على {acc['platform']}!", icon='🚀')
                    except Exception as e:
                        st.error(f"❌ مشكل في {acc['platform']}: {e}")
                
                status_container.write("😴 سأرتاح لـ 8 ساعات.")
                await asyncio.sleep(28800)

        try:
            asyncio.run(run_autonomous_loop())
        except Exception as e:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(run_autonomous_loop())
