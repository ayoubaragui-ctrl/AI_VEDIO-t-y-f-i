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
    st.header("👤 ربط حسابات المنصات")
    platform = st.selectbox("اختر المنصة", ["Instagram", "Facebook Reels", "TikTok", "YouTube Shorts"])
    
    # خانات متغيرة على حساب المنصة
    user_input = st.text_input("Username / Email / Page ID")
    
    if platform == "Facebook Reels":
        pass_input = st.text_input("Access Token (Page)", type="password", help="حط الـ Token ديال الصفحة هنا")
    elif platform == "TikTok":
        pass_input = st.text_input("Session ID", type="password", help="حط الـ Session ID من الكوكيز")
    else:
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
            st.success(f"تم تسجيل {user_input} في {platform}!")
        else:
            st.error("عمر كاع الخانات عفاك!")

# عرض الحسابات النشطة بتنسيق جديد
st.subheader("📊 إمبراطورية الحسابات المتصلة")
if st.session_state['accounts']:
    cols = st.columns(min(len(st.session_state['accounts']), 4))
    for idx, acc in enumerate(st.session_state['accounts']):
        col_idx = idx % 4
        with cols[col_idx]:
            st.metric(label=acc['platform'], value=acc['user'], delta="جاهز للنشر")
else:
    st.warning("لا توجد حسابات نشطة حالياً. أضف حساباً من القائمة الجانبية لبدء العمل.")

st.divider()

# محرك التشغيل الأوتوماتيكي المطور
if st.button("🔥 إطلاق الوحش العابر للمنصات (Global Pilot)"):
    if not st.session_state['accounts']:
        st.error("لازم تزيد حساب واحد على الأقل!")
    elif not pexels_key:
        st.error("Pexels Key ضروري للمونتاج!")
    else:
        bot = HalalSuperBot(gemini_key, pexels_key)
        st.success("✅ تم تفعيل الذكاء السيادي! النظام سيقوم بالنشر على جميع المنصات المرتبطة.")
        
        async def run_autonomous_loop():
            status_container = st.empty()
            while True:
                for acc in st.session_state['accounts']:
                    status_container.write(f"⏳ جاري تجهيز فيديو مخصص لـ {acc['user']} على {acc['platform']}...")
                    try:
                        # 1. صنع المحتوى (Gemini)
                        data = await bot.generate_content_ai(acc['niche'])
                        # 2. المونتاج (MoviePy)
                        video_file = await bot.produce_video(data)
                        
                        # 3. النشر الذكي حسب المنصة
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
                            st.toast(f"✅ تم النشر بنجاح على {acc['platform']} ({acc['user']})!", icon='🚀')
                    except Exception as e:
                        st.error(f"❌ وقع مشكل في منصة {acc['platform']} ({acc['user']}): {e}")
                
                status_container.write("😴 اكتملت دورة النشر العالمية. سأرتاح لـ 8 ساعات.")
                await asyncio.sleep(28800) # 8 ساعات

        # تعديل تقني لضمان تشغيل asyncio داخل Streamlit
        try:
            asyncio.run(run_autonomous_loop())
        except Exception as e:
            # معالجة مشكلة Event Loop في حالة إعادة التشغيل
            loop = asyncio.new_event_loop()
            loop.run_until_complete(run_autonomous_loop())
