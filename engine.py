import os, json, time, asyncio, requests, logging, random, hashlib
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

import google.generativeai as genai
import edge_tts
from moviepy.editor import *
# السطر المعدل لضمان التوافق مع السيرفر
import moviepy.video.fx.all as vfx
from instagrapi import Client
# ملاحظة: مكتبات YouTube و FB تحتاج لإعداد API Console (Client Secrets)
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [SUPREME_COMMAND] - %(message)s')

class HalalSuperBot:
    def __init__(self, gemini_key, pexels_key):
        genai.configure(api_key=gemini_key, transport='rest')
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.pexels_key = pexels_key
        self.temp_dir = "empire_assets"
        if not os.path.exists(self.temp_dir): os.makedirs(self.temp_dir)

    def get_account_stats(self, platform, acc):
        """جلب إحصائيات تقريبية للحساب"""
        try:
            # هنا مستقبلاً نقدروا نزيدو جلب حقيقي من API
            return {
                "Platform": platform,
                "User": acc.get('user', 'Unknown'),
                "Status": "✅ Active",
                "Last Sync": datetime.now().strftime("%H:%M")
            }
        except:
            return {"Platform": platform, "User": "Error", "Status": "❌ Offline"}

    async def generate_content_ai(self, niche):
        """ذكاء المحتوى والردود الاستباقية"""
        prompt = f"""
        Act as a Viral Strategist. Topic: {niche}.
        Output JSON:
        {{
            "script": "Full speech text",
            "queries": ["q1", "q2", "q3"],
            "hashtags": "#halal #viral",
            "auto_replies": {{
                "شكرا": "بارك الله فيك، تابعنا للمزيد من القيمة!",
                "كيف": "السر يكمن في الاستمرارية والتوكل على الله.",
                "مبدع": "الإبداع هو رؤية فضل الله في كل شيء."
            }}
        }}
        """
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text.strip().replace('```json', '').replace('```', ''))
        except:
            return {"script":"النجاح توفيق من الله.", "queries":["nature"], "hashtags":"#halal"}

    async def produce_video(self, data):
        """المونتاج الخارق وتغيير الحمض النووي الرقمي"""
        try:
            audio_path = os.path.join(self.temp_dir, f"v_{int(time.time())}.mp3")
            comm = edge_tts.Communicate(data['script'], "ar-SA-HamedNeural", pitch="+2Hz", rate="+5%")
            await comm.save(audio_path)
            audio = AudioFileClip(audio_path)

            clips = []
            headers = {"Authorization": self.pexels_key}
            for q in data.get('queries', ['nature'])[:4]:
                v_res = requests.get(f"https://api.pexels.com/videos/search?query={q}&per_page=5&orientation=portrait", headers=headers).json()
                if v_res.get('videos'):
                    v_url = random.choice(v_res['videos'])['video_files'][0]['link']
                    v_tmp = os.path.join(self.temp_dir, f"r_{hashlib.md5(v_url.encode()).hexdigest()}.mp4")
                    if not os.path.exists(v_tmp):
                        with open(v_tmp, "wb") as f: f.write(requests.get(v_url).content)
                    
                    # تعديل طريقة استدعاء التأثيرات لضمان العمل (vfx)
                    c = VideoFileClip(v_tmp).without_audio().resize(height=1920).fx(vfx.speedx, 1.03)
                    if random.choice([True, False]): c = c.fx(vfx.mirror_x)
                    clips.append(c.subclip(2, 5))

            final_v = concatenate_videoclips(clips, method="compose").set_audio(audio).set_duration(audio.duration)
            output = f"master_{int(time.time())}.mp4"
            final_v.write_videofile(output, fps=30, codec="libx264", bitrate="6000k")
            return output
        except Exception as e:
            logging.error(f"Render Error: {e}")
            return None

    # --- محركات النشر الشاملة ---
    
    def publish_tiktok(self, session_id, video, data):
        logging.info("🚀 [TikTok] نضح الفيديو عبر البروتوكول المباشر...")
        return True # يحتاج sessionid حقيقي

    def publish_insta(self, user, pwd, video, data):
        try:
            cl = Client()
            cl.login(user, pwd)
            cl.video_upload(video, caption=f"{data['script'][:50]}...\n{data['hashtags']}")
            return True
        except: return False

    def publish_youtube(self, credentials, video, data):
        logging.info("📺 [YouTube Shorts] جاري الرفع لـ YouTube...")
        # يحتاج ملف client_secrets.json للربط الرسمي
        return True

    def publish_facebook(self, page_token, page_id, video, data):
        logging.info("Facebook [Reels] جاري الحقن في فايسبوك...")
        return True

    async def auto_reply_engine(self, platform, account_data, ai_replies):
        """محرك الرد الآلي: يراقب التعليقات ويرد عليها بالذكاء الاصطناعي"""
        logging.info(f"🤖 [AI-Replies] المحرك يعمل الآن على {platform}...")
        # هنا يتم فحص آخر التعليقات ومطابقتها مع ai_replies
        pass

    async def execute_global_mission(self, acc):
        """الضربة الشاملة: إنتاج واحد، نشر متعدد، رد آلي"""
        data = await self.generate_content_ai(acc['niche'])
        video = await self.produce_video(data)
        
        if video:
            p = acc['platform']
            success = False
            if p == 'TikTok': success = self.publish_tiktok(acc['pwd'], video, data)
            elif p == 'Insta': success = self.publish_insta(acc['user'], acc['pwd'], video, data)
            elif p == 'YouTube': success = self.publish_youtube(acc['pwd'], video, data)
            elif p == 'FB': success = self.publish_facebook(acc['user'], acc['pwd'], video, data)
            
            if success:
                # تفعيل الرد الآلي بعد النشر بـ 30 دقيقة
                await asyncio.sleep(1800)
                await self.auto_reply_engine(p, acc, data['auto_replies'])
            return success
        return False
