import os, json, time, asyncio, requests, logging, random, re, uuid
from datetime import datetime

# إعداد المسارات
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

from groq import Groq # مكتبة Groq الصاروخية
import edge_tts
from moviepy.editor import *
import moviepy.video.fx.all as vfx

# إعدادات التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [SUPREME_COMMAND] - %(message)s')

class HalalSuperBot:
    def __init__(self, groq_key, pexels_key):
        # تفعيل Groq عوض Gemini
        self.client = Groq(api_key=groq_key)
        self.pexels_key = pexels_key
        self.pixabay_key = "48316135-2605d55681682335f60682057"
        self.temp_dir = "empire_assets"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def get_account_stats(self, platform, acc):
        return {
            "Platform": platform,
            "User": acc.get('user', 'Unknown'),
            "Status": "✅ Active (Groq Powered)",
            "Last Sync": datetime.now().strftime("%H:%M")
        }

    async def post_immediately(self, acc):
        logging.info(f"🚀 [MISSION] انطلاق المهمة بذكاء Groq لحساب: {acc['user']} | النيش: {acc['niche']}")
        return await self.execute_global_mission(acc)

    async def fetch_auto_music(self, keywords):
        """جلب موسيقى تلقائية مع Headers كاملة لتفادي حظر Pixabay"""
        try:
            query = random.choice(keywords) if keywords else "islamic calm"
            url = f"https://pixabay.com/api/audio/?key={self.pixabay_key}&q={query.replace(' ', '+')}&per_page=5"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                res = response.json()
                if res.get('hits'):
                    music_url = random.choice(res['hits'])['audio']
                    music_path = os.path.join(self.temp_dir, f"bgm_{uuid.uuid4().hex[:5]}.mp3")
                    r = requests.get(music_url, headers=headers, timeout=15)
                    with open(music_path, "wb") as f:
                        f.write(r.content)
                    logging.info(f"🎵 تم جلب الموسيقى بنجاح")
                    return music_path
            return None
        except Exception as e:
            logging.error(f"❌ خطأ جلب الموسيقى: {e}")
            return None

    async def generate_content_ai(self, niche):
        """توليد محتوى ذكي باستعمال Groq Llama 3"""
        styles = ["داعية مؤثر", "حكيم رزين", "راوي قصص إسلامي"]
        for attempt in range(3):
            try:
                chosen_style = random.choice(styles)
                prompt = f"""
                Return ONLY a valid JSON object. 
                Task: Write a 60-word emotional Islamic script about: {niche}.
                Style: {chosen_style}. No numbers, pure Arabic.
                Format:
                {{"script": "text content", "queries": ["nature", "sky"], "music_keywords": ["calm"], "hashtags": "#wisdom"}}
                """
                # استخدام موديل Llama 3.3 70B
                completion = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                
                data = json.loads(completion.choices[0].message.content)
                data['script'] = re.sub(r'\d+', '', data['script'])
                logging.info(f"✨ Groq أنتج نصاً جديداً بنجاح")
                return data
            except Exception as e:
                logging.warning(f"⚠️ محاولة Groq فاشلة {attempt+1}: {e}")
                await asyncio.sleep(2)
        
        return {"script": "إن مع العسر يسرا، فوض أمرك لله واطمئن.", "queries": ["nature"], "music_keywords": ["calm"], "hashtags": "#islam"}

    async def produce_video(self, data):
        """محرك المونتاج الاحترافي 100%"""
        try:
            # 1. الصوت
            audio_path = os.path.join(self.temp_dir, f"v_{uuid.uuid4().hex[:6]}.mp3")
            comm = edge_tts.Communicate(data['script'], "ar-SA-HamedNeural", pitch="-2Hz", rate="+5%")
            await comm.save(audio_path)
            voice = AudioFileClip(audio_path)
            duration = voice.duration

            # 2. الموسيقى
            bg_music = await self.fetch_auto_music(data.get('music_keywords'))

            # 3. الفيديوهات
            clips = []
            headers = {"Authorization": self.pexels_key}
            curr = 0
            while curr < duration:
                q = random.choice(data.get('queries', ['nature']))
                url = f"https://api.pexels.com/videos/search?query={q}&per_page=10&orientation=portrait"
                v_res = requests.get(url, headers=headers).json()
                if v_res.get('videos'):
                    v_item = random.choice(v_res['videos'])
                    v_url = v_item['video_files'][0]['link']
                    v_tmp = os.path.join(self.temp_dir, f"vid_{uuid.uuid4().hex[:5]}.mp4")
                    with open(v_tmp, "wb") as f: f.write(requests.get(v_url).content)
                    
                    c = VideoFileClip(v_tmp).without_audio().resize(height=1920)
                    take = min(5, duration - curr)
                    c = c.subclip(0, take).fx(vfx.colorx, 0.9).fx(vfx.resize, lambda t: 1 + 0.02 * t)
                    clips.append(c)
                    curr += take
                    os.remove(v_tmp)
                else: break

            video_base = concatenate_videoclips(clips, method="compose").set_duration(duration)
            
            # 4. الكتابة الديناميكية
            words = data['script'].split()
            chunk_size = 3
            chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
            text_clips = []
            part_dur = duration / max(1, len(chunks))
            
            for i, part in enumerate(chunks):
                txt = TextClip(part, fontsize=85, color='yellow', font='FreeSans-Bold', stroke_color='black', stroke_width=2.5, method='caption', size=(950, None))
                txt = txt.set_start(i*part_dur).set_duration(part_dur).set_position(('center', 1400)).crossfadein(0.2)
                text_clips.append(txt)

            overlay = ColorClip(size=(1080, 1920), color=(0,0,0), duration=duration).set_opacity(0.3)
            final_v = CompositeVideoClip([video_base, overlay] + text_clips)
            
            # 5. الصوت النهائي
            audio_layers = [voice.volumex(1.5)]
            if bg_music:
                m = AudioFileClip(bg_music).volumex(0.15).set_duration(duration).audio_fadeout(2)
                audio_layers.append(m)
            
            final_v = final_v.set_audio(CompositeAudioClip(audio_layers))
            out_file = f"FINAL_{int(time.time())}.mp4"
            final_v.write_videofile(out_file, fps=24, codec="libx264", bitrate="5000k", threads=4)
            
            if os.path.exists(audio_path): os.remove(audio_path)
            if bg_music and os.path.exists(bg_music): os.remove(bg_music)
            
            return out_file
        except Exception as e:
            logging.error(f"Render Error: {e}"); return None

    # دوال النشر
    def publish_youtube(self, video, data):
        logging.info(f"📤 [YOUTUBE] جاري النشر: {video}")
        return True

    def publish_facebook(self, video, data):
        logging.info(f"📤 [FACEBOOK] جاري النشر: {video}")
        return True

    async def execute_global_mission(self, acc):
        try:
            data = await self.generate_content_ai(acc['niche'])
            video = await self.produce_video(data)
            
            if video and os.path.exists(video):
                success = False
                if acc['platform'] == 'YouTube':
                    success = self.publish_youtube(video, data)
                elif acc['platform'] == 'FB':
                    success = self.publish_facebook(video, data)
                return success
            return False
        except Exception as e:
            logging.error(f"Mission Failed: {e}"); return False
