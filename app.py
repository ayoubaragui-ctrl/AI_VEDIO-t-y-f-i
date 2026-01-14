import streamlit as st
import asyncio
import time
import pandas as pd
from engine import HalalSuperBot

# إعداد الصفحة لتكون احترافية وعريضة
st.set_page_config(page_title="Halal AI Bot v2.0 - Dashboard", layout="wide", page_icon="🌍")

# ستايل CSS متطور لتحسين المظهر وتنسيق الجداول
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e2130; border-radius: 5px 5px 0px 0px; padding: 10px 20px; color: white;
    }
    .stMetric { background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; }
    .account-card {
        padding: 15px; border-radius: 10px; border: 1px solid #2ea043; background-color: #0d1117; margin-bottom: 10px;
    }
    .stats-header { color: #2ea043; font-weight: bold; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 لوحة التحكم السيادية | إدارة الحسابات المتعددة")
st.markdown("---")

# إدارة الحسابات في ذاكرة الجلسة
if 'accounts' not in st.session_state:
    st.session_state['accounts'] = []

# القائمة الجانبية لإعدادات الوصول وإضافة الحسابات
with st.sidebar:
    st.header("🔑 إعدادات الوصول")
    gemini_key = st.text_input("Gemini API Key", value="AIzaSyCbjx_aXkoZ5vll8WvSNJbsGJfLe6o3xcQ")
    pexels_key = st.text_input("Pexels API Key", type="password")
    
    st.divider()
    st.header("👤 إضافة حساب جديد")
    platform = st.selectbox("اختار المنصة", ["Insta", "TikTok", "FB", "YouTube"])
    
    # نموذج إدخال ديناميكي حسب المنصة
    with st.expander("بيانات الدخول", expanded=True):
        u = st.text_input("اسم المستخدم / ID")
        p = st.text_input("الكلمة السرية / Token", type="password")
        niche = st.text_input("نيش المحتوى (Niche)", value="مواعظ إسلامية")
        
        if st.button("➕ إضافة الحساب للقائمة"):
            if u and p:
                new_acc = {"user": u, "pwd": p, "platform": platform, "niche": niche}
                st.session_state['accounts'].append(new_acc)
                st.success(f"تمت إضافة {u} بنجاح!")
            else:
                st.error("عمر البيانات كاملة!")

    if st.button("🗑️ مسح جميع الحسابات"):
        st.session_state['accounts'] = []
        st.rerun()

# القسم العلوي: إحصائيات الأداء العام (لوحة المعلومات)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("إجمالي الحسابات", len(st.session_state['accounts']))
with col2:
    st.metric("الحالة التشغيلية", "Active" if st.session_state['accounts'] else "Idle")
with col3:
    st.metric("المنصات المدعومة", "4")
with col4:
    st.metric("تحديث البيانات", "تلقائي")

st.divider()

# القسم الأوسط: إدارة وتحليل الحسابات المتصلة
st.subheader("📊 تحليل أداء إمبراطورية الحسابات")

if st.session_state['accounts']:
    # تجهيز البيانات للعرض في جدول احترافي
    bot_temp = HalalSuperBot(gemini_key, "temp")
    stats_list = []
    
    for acc in st.session_state['accounts']:
        # جلب الإحصائيات من المحرك (Engine)
        stat = bot_temp.get_account_stats(acc['platform'], acc)
        stats_list.append(stat)
    
    df = pd.DataFrame(stats_list)
    # تجميل الجدول
    st.table(df)

    # عرض الحسابات كبطاقات تفاعلية
    st.write("### 🗂️ قائمة الحسابات النشطة")
    cols = st.columns(3)
    for idx, acc in enumerate(st.session_state['accounts']):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="account-card">
                <span class="stats-header">{acc['platform']}</span><br>
                <b>User:</b> {acc['user']}<br>
                <b>Niche:</b> {acc['niche']}<br>
                <span style="color: #8b949e; font-size: 0.8em;">Status: Ready to Post</span>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("قم بإضافة حساباتك من القائمة الجانبية للبدء.")

st.divider()

# محرك التشغيل الأوتوماتيكي
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
                status_container.info("🔄 بدأت دورة النشر الشاملة لجميع الحسابات...")
                
                # إرسال قائمة الحسابات كاملة للمحرك
                try:
                    # استدعاء الدالة المطورة في Engine التي تدعم القائمة
                    await bot.start_autonomous_loop(st.session_state['accounts'], st.session_state['accounts'][0]['niche'])
                except Exception as e:
                    st.error(f"⚠️ خطأ في المحرك الرئيسي: {e}")
                    await asyncio.sleep(60)

        # تشغيل الحلقة
        try:
            asyncio.run(run_autonomous_loop())
        except:
            # حل لمشكل تداخل حلقات asyncio في Streamlit
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            new_loop.run_until_complete(run_autonomous_loop())
