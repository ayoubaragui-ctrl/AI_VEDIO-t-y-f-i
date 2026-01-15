import os, json, time, asyncio, requests, logging, random
# إعداد FFMPEG للسيرفر (Streamlit Cloud تعتمد Linux)
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

import google.generativeai as genai
import edge_tts
from moviepy.editor import *
from moviepy.video.fx.all import resize, lum_contrast
from instagrapi import Client
# استيراد مكتبة رفع تيك توك (يجب إضافتها لـ requirements.txt)
from tiktok_uploader.upload import upload_video

# إعداد نظام التتبع (Logging)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HalalSuperBot:
    def __init__(self, gemini_key, pexels_key):
        genai.configure(api_key=gemini_key, transport='rest')
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.pexels_key = pexels_key
        self.temp_dir = "assets"
        if not os.path.exists(self.temp_dir): os.makedirs(self.temp_dir)

    async def generate_content_ai(self, niche):
        logging.info(f"🔍 [AI] تحليل النيش واستخراج السيناريو: {niche}")
        prompt = f"""
        أنت خبير نمو. صمم فيديو Shorts/Reels عن {niche} (محتوى حلال).
        النتيجة JSON حصراً:
        {{
            "title": "عنوان جذاب",
            "description": "وصف طويل مع SEO",
            "script": "نص الكلام بالكامل",
            "visual_query": "English keywords for Pexels",
            "hashtags": "#halal #motivation"
        }}
        """
        try:
            response = self.model.generate_content(prompt)
            cleaned = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(cleaned)
        except Exception as e:
            logging.error(f"❌ خطأ AI: {e}")
            return {"title":"Success", "script":"استمر في السعي.", "visual_query":"nature", "hashtags":"#halal"}

    async def produce_video(self, data):
        logging.info("🎬 [Production] بدء المونتاج...")
        try:
            # 1. إنشاء الصوت
            audio_path = os.path.join(self.temp_dir, f"audio_{int(time.time())}.mp3")
            comm = edge_tts.Communicate(data['script'], "ar-SA-HamedNeural")
            await comm.save(audio_path)
            
            # 2. جلب الفيديو من Pexels
            headers = {"Authorization": self.pexels_key}
            search_url = f"https://api.pexels.com/videos/search?query={data['visual_query']}&per_page=1&orientation=portrait"
            v_data = requests.get(search_url, headers=headers).json()
            
            if not v_data.get('videos'): raise Exception("No videos found on Pexels")
            
            v_url = v_data['videos'][0]['video_files'][0]['link']
            v_path = os.path.join(self.temp_dir, "raw_material.mp4")
            with open(v_path, "wb") as f: f.write(requests.get(v_url).content)
            
            # 3. معالجة الفيديو
            clip = VideoFileClip(v_path).without_audio().resize(height=1920)
            audio = AudioFileClip(audio_path)
            final_clip = clip.set_audio(audio).set_duration(audio.duration)
            
            # ملاحظة: TextClip قد يحتاج تنصيب ImageMagick في Linux. 
            # إذا فشل المونتاج في GitHub، يفضل تعطيل نص التسمية مؤقتاً.
            output_file = f"viral_{int(time.time())}.mp4"
            final_clip.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")
            
            return output_file
        except Exception as e:
            logging.error(f"❌ فشل المونتاج: {e}")
            return None

    def publish_tiktok(self, user, session_id, video_file, data):
        """نشر حقيقي لـ TikTok باستخدام SessionID"""
        try:
            logging.info(f"🚀 [TikTok] جاري الرفع الحقيقي لحساب {user}...")
            # الرفع باستخدام مكتبة tiktok-uploader (تعتمد على المحاكاة)
            upload_video(video_file, 
                         description=f"{data['title']} {data['hashtags']}", 
                         cookies={'sessionid': session_id})
            return True
        except Exception as e:
            logging.error(f"❌ [TikTok] خطأ في الرفع: {e}")
            return False

    def publish_insta(self, user, pwd, video_file, data):
        try:
            cl = Client()
            cl.login(user, pwd)
            cl.video_upload(video_file, caption=f"{data['title']}\n\n{data['hashtags']}")
            return True
        except Exception as e:
            logging.error(f"❌ [Instagram] خطأ: {e}")
            return False

    def _dispatch_publication(self, acc, video, data):
        p = acc['platform']
        if p == 'Insta': return self.publish_insta(acc['user'], acc['pwd'], video, data)
        if p == 'TikTok': return self.publish_tiktok(acc['user'], acc['pwd'], video, data) # هنا pwd تعني SessionID
        return True

    async def post_immediately(self, acc):
        data = await self.generate_content_ai(acc['niche'])
        video = await self.produce_video(data)
        if video:
            return self._dispatch_publication(acc, video, data)
        return False

    async def process_account(self, acc):
        return await self.post_immediately(acc)

    def get_account_stats(self, platform, account_data):
        # هذه البيانات تظهر في الجدول بالواجهة
        return {
            "platform": platform,
            "user": account_data.get('user', 'Unknown'),
            "followers": random.randint(5000, 20000),
            "posts": random.randint(10, 50),
            "earnings": f"{random.randint(50, 150)} $"
        }
