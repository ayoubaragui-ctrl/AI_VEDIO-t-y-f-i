import os, json, time, asyncio, requests, logging, random
import google.generativeai as genai
import edge_tts
from moviepy.editor import *
from moviepy.video.fx.all import resize, lum_contrast
from instagrapi import Client

# إعداد نظام التتبع (Logging)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HalalSuperBot:
    def __init__(self, gemini_key, pexels_key):
        genai.configure(api_key=gemini_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.pexels_key = pexels_key
        self.temp_dir = "assets"
        if not os.path.exists(self.temp_dir): os.makedirs(self.temp_dir)

    async def generate_content_ai(self, niche):
        """ذكاء خارق لتحليل التريند وصياغة السيناريو"""
        logging.info(f"🔍 تحليل الموضوع: {niche}")
        # تطوير الـ Prompt باش يجيب إعدادات النشر كاملة
        prompt = f"""
        أنت خبير نمو (Growth Hacker) وصانع محتوى فيروسي. صمم فيديو لـ Shorts/Reels عن {niche} بشرط:
        1. المحتوى حلال 100%. 2. البداية (Hook) صاعقة. 3. لهجة بيضاء مفهومة.
        النتيجة JSON حصراً بنفس هاد المفاتيح:
        {{
            "title": "عنوان جذاب جداً مع SEO",
            "description": "وصف طويل فيه شرح وقيمة مضافة",
            "script": "نص الكلام بالكامل",
            "visual_query": "English keywords for cinematic 4k footage",
            "hashtags": "#halal #success #motivation",
            "platform_strategy": "أفضل وقت للنشر"
        }}
        """
        response = self.model.generate_content(prompt)
        return json.loads(response.text.replace('```json', '').replace('```', '').strip())

    async def produce_video(self, data):
        """المونتاج الآلي بأعلى جودة"""
        # 1. الصوت
        audio_path = os.path.join(self.temp_dir, f"audio_{int(time.time())}.mp3")
        comm = edge_tts.Communicate(data['script'], "ar-SA-HamedNeural")
        await comm.save(audio_path)
        
        # 2. اللقطات (Pexels API)
        headers = {"Authorization": self.pexels_key}
        search_url = f"https://api.pexels.com/videos/search?query={data['visual_query']}&per_page=3&orientation=portrait"
        v_data = requests.get(search_url, headers=headers).json()
        
        clips = []
        for i, v in enumerate(v_data['videos'][:2]):
            v_url = v['video_files'][0]['link']
            v_path = os.path.join(self.temp_dir, f"raw_{i}.mp4")
            with open(v_path, "wb") as f: f.write(requests.get(v_url).content)
            
            clip = VideoFileClip(v_path).without_audio().resize(height=1920)
            # إضافة تحسين بصري (Contrast)
            clip = lum_contrast(clip, lum=0.1, contrast=0.1)
            clips.append(clip.subclip(0, 5))

        # 3. الدمج والترجمة
        final_video = concatenate_videoclips(clips, method="compose")
        audio = AudioFileClip(audio_path)
        final_video = final_video.set_audio(audio).set_duration(audio.duration)
        
        # إضافة ترجمة ذكية (Dynamic Text)
        txt = TextClip(data['script'], fontsize=55, color='yellow', font='Arial-Bold', 
                       method='caption', size=(final_video.w*0.8, None))
        txt = txt.set_duration(audio.duration).set_pos(('center', 1400))
        
        output_file = f"viral_video_{int(time.time())}.mp4"
        result = CompositeVideoClip([final_video, txt])
        result.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")
        return output_file

    def publish_insta(self, user, pwd, video_file, data):
        """نشر أوتوماتيكي بإعدادات كاملة (عام، عنوان، وصف)"""
        try:
            cl = Client()
            cl.login(user, pwd)
            
            # صياغة المنشور (العنوان + الوصف + الهاشتاقات)
            full_caption = f"🌟 {data['title']}\n\n📝 {data['description']}\n\n{data['hashtags']}"
            
            # النشر كـ Reel (أوتوماتيكياً كيكون Public)
            cl.video_upload(
                video_file, 
                caption=full_caption,
                share_to_feed=True
            )
            logging.info("✅ تم النشر بنجاح: الفيديو عام ومحسن للخوارزميات!")
            return True
        except Exception as e:
            logging.error(f"❌ خطأ في النشر: {e}")
            return False

    async def start_autonomous_loop(self, user, pwd, niche):
        """نظام النشر الذاتي: 3 فيديوهات يومياً"""
        while True:
            logging.info("🕒 بدء دورة إنتاج ونشر جديدة...")
            try:
                data = await self.generate_content_ai(niche)
                video = await self.produce_video(data)
                self.publish_insta(user, pwd, video, data)
                
                # الانتظار لمدة 8 ساعات (24 ساعة / 3 فيديوهات)
                logging.info("😴 تمت العملية. سأرتاح لـ 8 ساعات...")
                await asyncio.sleep(8 * 3600) 
            except Exception as e:
                logging.error(f"⚠️ مشكل في الدورة: {e}. سأحاول مجدداً بعد ساعة.")
                await asyncio.sleep(3600)
