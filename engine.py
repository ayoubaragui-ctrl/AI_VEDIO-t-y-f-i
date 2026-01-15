import os, json, time, asyncio, requests, logging, random, hashlib
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

import google.generativeai as genai
import edge_tts
from moviepy.editor import *
import moviepy.video.fx.all as vfx
from instagrapi import Client
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [SUPREME_COMMAND] - %(message)s')

class HalalSuperBot:
    def __init__(self, gemini_key, pexels_key):
        # إعداد Gemini بطريقة تضمن عدم توقف الشات
        try:
            genai.configure(api_key=gemini_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.pexels_key = pexels_key
            self.temp_dir = "empire_assets"
            if not os.path.exists(self.temp_dir): os.makedirs(self.temp_dir)
            logging.info("✅ تم تفعيل العقل الذكي بنجاح")
        except Exception as e:
            logging.error(f"❌ خطأ في إعداد الذكاء الاصطناعي: {e}")

    def get_account_stats(self, platform, acc):
        try:
            return {
                "Platform": platform,
                "User": acc.get('user', 'Unknown'),
                "Status": "✅ Active",
                "Last Sync": datetime.now().strftime("%H:%M")
            }
        except:
            return {"Platform": platform, "User": "Error", "Status": "❌ Offline"}

    async def post_immediately(self, acc):
        logging.info(f"🚀 [IMMEDIATE_HIT] محاولة النشر الفوري لـ {acc['user']}...")
        return await self.execute_global_mission(acc)

    async def generate_content_ai(self, niche):
        """توليد المحتوى مع تنظيف النص لضمان عمل الشات"""
        prompt = f"Act as a Viral Strategist. Topic: {niche}. Output ONLY valid JSON: {{\"script\": \"text\", \"queries\": [\"q1\"], \"hashtags\": \"#tags\"}}"
        try:
            response = self.model.generate_content(prompt)
            # تنظيف الرد من أي علامات زائدة كتعطل الشات
            clean_text = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(clean_text)
        except Exception as e:
            logging.error(f"⚠️ AI Content Error: {e}")
            return {"script": "توكل على الله واستمر في العمل.", "queries": ["nature"], "hashtags": "#halal #islam"}

    async def produce_video(self, data):
        try:
            # 1. الصوت
            audio_path = os.path.join(self.temp_dir, f"v_{int(time.time())}.mp3")
            comm = edge_tts.Communicate(data['script'], "ar-SA-HamedNeural", pitch="+2Hz", rate="+5%")
            await comm.save(audio_path)
            audio = AudioFileClip(audio_path)

            # 2. الكليبات (Pexels)
            clips = []
            headers = {"Authorization": self.pexels_key}
            for q in data.get('queries', ['nature'])[:3]:
                try:
                    v_res = requests.get(f"https://api.pexels.com/videos/search?query={q}&per_page=3&orientation=portrait", headers=headers).json()
                    if v_res.get('videos'):
                        v_url = v_res['videos'][0]['video_files'][0]['link']
                        v_tmp = os.path.join(self.temp_dir, f"r_{hashlib.md5(v_url.encode()).hexdigest()}.mp4")
                        if not os.path.exists(v_tmp):
                            with open(v_tmp, "wb") as f: f.write(requests.get(v_url).content)
                        
                        c = VideoFileClip(v_tmp).without_audio().resize(height=1920).fx(vfx.speedx, 1.1)
                        clips.append(c.subclip(0, min(4, c.duration)))
                except: continue

            if not clips: return None

            final_v = concatenate_videoclips(clips, method="compose").set_audio(audio).set_duration(audio.duration)
            output = f"master_{int(time.time())}.mp4"
            final_v.write_videofile(output, fps=24, codec="libx264")
            return output
        except Exception as e:
            logging.error(f"❌ Render Error: {e}")
            return None

    def publish_insta(self, user, pwd, video, data):
        try:
            cl = Client()
            cl.login(user, pwd)
            cl.video_upload(video, caption=f"{data['script'][:100]}\n.\n{data['hashtags']}")
            return True
        except Exception as e:
            logging.error(f"❌ Instagram Login/Upload Error: {e}")
            return False

    async def execute_global_mission(self, acc):
        data = await self.generate_content_ai(acc['niche'])
        video = await self.produce_video(data)
        if video:
            p = acc['platform']
            if p == 'Insta': return self.publish_insta(acc['user'], acc['pwd'], video, data)
            logging.info(f"✅ تم تنفيذ المهمة لـ {p} (محاكاة)")
            return True
        return False
