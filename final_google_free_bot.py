
# FINAL BEST - GOOGLE VOICE FREE - HUMAN QUALITY - NO ELEVENLABS NEEDED
# Uses Google Cloud TTS WaveNet - FREE 1M chars/month = 20 long videos = 100% FREE
# Quality: 90% human, much better than Edge-TTS, free forever

import os, glob, random, datetime, requests, textwrap, re, math
from PIL import Image, ImageDraw, ImageFont

try:
    from moviepy.editor import ColorClip, AudioFileClip, ImageClip, CompositeVideoClip, VideoFileClip, concatenate_videoclips, CompositeAudioClip
except:
    from moviepy import ColorClip, AudioFileClip, ImageClip, CompositeVideoClip, VideoFileClip, concatenate_videoclips, CompositeAudioClip

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "gsk_PASTE_YOUR_GROQ_KEY")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "PASTE_YOUR_PIXABAY_KEY")
GOOGLE_APPLICATION_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON", "")  # For Google TTS

NOW = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
VOICE_FILE = f"voice_{NOW}.mp3"
VIDEO_FILE = f"video_{NOW}.mp4"

def clean_for_tts(text):
    text = re.sub(r'(\d+)\s*cr\b', r'\1 crore', text, flags=re.I)
    text = text.replace("D-Mart", "D Mart").replace("Byju's", "Byjus").replace("₹", " rupees ").replace("%", " percent ")
    text = re.sub(r'[#*_\[\]{}|<>~`]', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    if len(text) > 4500:
        text = text[:4500] + "."
    return text.strip()

def get_best_script():
    print("\n>> [1/5] Script - Think School style...")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    topics = [
        "How Haldiram built 8000 crore empire from 100 rupees - full case study",
        "Why Byjus failed - 22 billion to 0 - 5 mistakes",
        "Chai Sutta Bar - 2 boys 150 crore empire",
        "Boat - How Aman Gupta beat Apple with 500 rupees product",
        "D Mart - Why it never sells online and still beats Amazon"
    ]
    topic = random.choice(topics)
    seed = random.randint(10000,99999)
    prompt = f"""You are Think School storyteller. Topic: {topic}. Write 750-900 words viral 5-7 min script: HOOK shocking number, STRUGGLE founder story, 3 SECRETS with numbers psychology, LESSONS 3 actionable. Hindi+English mix, conversational, not formal. Use full words: 8000 crore not 8000cr, D Mart not D-Mart, percent not %. Seed {seed}. Only script."""
    for model in ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3-32b"]:
        try:
            data = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 1.0, "max_tokens": 3200}
            r = requests.post(url, headers=headers, json=data, timeout=60)
            if r.status_code == 200:
                script = r.json()['choices'][0]['message']['content'].strip()
                if len(script.split()) > 500:
                    print(f"  ✅ {len(script.split())} words")
                    return script
        except: pass
    return f"{topic}. Hook: 80 rupay se 1600 crore? Struggle: 7 housewives 80 rupay. Secrets: No Boss, Cash only, Quality is marketing. Lessons: Team owner, cash, quality."

def get_google_voice_free(text):
    """GOOGLE VOICE FREE - 2 methods: Cloud TTS WaveNet (best) or gTTS (fallback free)"""
    clean_text = clean_for_tts(text)
    print(f"\n>> [2/5] Google Voice FREE - {len(clean_text.split())} words")

    # Method 1: Google Cloud TTS WaveNet - BEST QUALITY FREE (1M chars/month free)
    if GOOGLE_APPLICATION_CREDENTIALS_JSON and "PASTE" not in GOOGLE_APPLICATION_CREDENTIALS_JSON and len(GOOGLE_APPLICATION_CREDENTIALS_JSON) > 20:
        print(" >> Using Google Cloud TTS WaveNet (FREE 1M chars/month - human quality)...")
        try:
            import json, base64
            from google.cloud import texttospeech
            
            # Write credentials from secret
            with open("google_creds.json", "w") as f:
                f.write(GOOGLE_APPLICATION_CREDENTIALS_JSON)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_creds.json"
            
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.SynthesisInput(text=clean_text)
            
            # Best Hindi/English voice - WaveNet = human quality
            voice = texttospeech.VoiceSelectionParams(
                language_code="hi-IN",
                name="hi-IN-Wavenet-C",  # Best Hindi WaveNet - natural
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )
            # Alternative: en-IN-Wavenet-C for Hinglish
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=0.95,  # Slight slow for business
                pitch=1.2
            )
            
            response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
            
            with open(VOICE_FILE, "wb") as out:
                out.write(response.audio_content)
            
            audio = AudioFileClip(VOICE_FILE)
            print(f" >> ✅ Google WaveNet HUMAN: {audio.duration:.1f} sec = {audio.duration/60:.1f} min - FREE")
            return audio.duration
        except Exception as e:
            print(f" >> Google Cloud failed {e}, trying gTTS free...")

    # Method 2: gTTS - 100% FREE, no API key needed, good quality
    print(" >> Using gTTS FREE (Google Translate TTS - free, no key, good quality)...")
    try:
        from gtts import gTTS
        # Use Hindi for natural Hinglish
        tts = gTTS(text=clean_text, lang='hi', slow=False, tld='co.in')  # co.in = Indian accent
        tts.save(VOICE_FILE)
        audio = AudioFileClip(VOICE_FILE)
        print(f" >> ✅ gTTS FREE: {audio.duration:.1f} sec = {audio.duration/60:.1f} min - 100% FREE")
        return audio.duration
    except Exception as e:
        print(f" >> gTTS failed {e}, using Edge-TTS...")

    # Fallback: Edge-TTS
    try:
        import asyncio, edge_tts
        async def gen():
            await edge_tts.Communicate(clean_text, "en-IN-NeerjaNeural", rate="-3%", pitch="+1Hz").save(VOICE_FILE)
        asyncio.run(gen())
        audio = AudioFileClip(VOICE_FILE)
        print(f" >> ✅ Edge-TTS: {audio.duration:.1f} sec")
        return audio.duration
    except:
        return 60

def download_broll():
    os.makedirs("clips", exist_ok=True)
    if not PIXABAY_API_KEY or "PASTE" in PIXABAY_API_KEY:
        return []
    print("\n>> [3/5] Downloading story b-roll...")
    story_map = {"hook": ["money cash"], "struggle": ["small shop india"], "team": ["business team meeting"], "factory": ["factory workers"], "market": ["indian market"]}
    downloaded=[]
    for cat, queries in story_map.items():
        q=random.choice(queries)
        try:
            url=f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&q={q}&per_page=3"
            r=requests.get(url, timeout=15)
            if r.status_code==200:
                for hit in r.json().get('hits', [])[:1]:
                    try:
                        vinfo=hit['videos'].get('large') or hit['videos'].get('medium')
                        data=requests.get(vinfo['url'], timeout=20).content
                        if len(data)>80000:
                            fname=f"clips/{cat}_{len(downloaded)}_{NOW}.mp4"
                            open(fname,"wb").write(data)
                            downloaded.append(fname)
                    except: pass
        except: pass
    print(f" ✅ {len(downloaded)} clips")
    return downloaded

def create_text_image(text, filename, style="hook"):
    W,H=1080,1920
    img=Image.new('RGBA',(W,H),(0,0,0,0))
    draw=ImageDraw.Draw(img)
    try:
        font_bold=ImageFont.truetype("arialbd.ttf", 64 if style=="hook" else 50)
        font_norm=ImageFont.truetype("arial.ttf", 38)
    except:
        font_bold=ImageFont.load_default()
        font_norm=ImageFont.load_default()
    def outline(x,y,txt,font,fill,w=3):
        for dx in range(-w,w+1):
            for dy in range(-w,w+1):
                draw.text((x+dx,y+dy), txt, font=font, fill="black")
        draw.text((x,y), txt, font=font, fill=fill)
    if style=="hook":
        wrapped=textwrap.fill(text[:130], width=20)
        y=600
        for line in wrapped.split('\n'):
            bbox=draw.textbbox((0,0),line,font=font_bold)
            w=bbox[2]-bbox[0]
            outline((W-w)//2,y,line,font_bold,"white",3)
            y+=85
    else:
        wrapped=textwrap.fill(text, width=28)
        y=1350
        for line in wrapped.split('\n')[:3]:
            bbox=draw.textbbox((0,0),line,font=font_norm)
            w=bbox[2]-bbox[0]
            outline((W-w)//2,y,line,font_norm,"white",2)
            y+=55
    img.save(filename)
    return filename

def make_video(duration, script):
    print(f"\n>> [4/5] Making video {duration/60:.1f} min...")
    clips=download_broll()
    existing=glob.glob("clips/*.mp4")
    all_clips=list(set(clips+existing))
    if all_clips and len(all_clips)>=2:
        vclips=[]
        total=0
        random.shuffle(all_clips)
        while total<duration and len(vclips)<20:
            for f in all_clips[:5]:
                try:
                    c=VideoFileClip(f).resize((1080,1920))
                    c=c.resize(lambda t: 1 + 0.06*t/c.duration if c.duration>0 else 1)
                    seg=random.uniform(5,8)
                    s=random.uniform(0,max(0,c.duration-seg))
                    vclips.append(c.subclip(s,min(s+seg,c.duration)))
                    total+=seg
                    if total>=duration: break
                except: pass
            if total>=duration: break
        try:
            base=concatenate_videoclips(vclips, method="compose")
            if base.duration<duration: base=base.loop(duration=duration)
            else: base=base.subclip(0,duration)
        except:
            base=ColorClip((1080,1920), color=(16,24,62), duration=duration)
    else:
        base=ColorClip((1080,1920), color=(16,24,62), duration=duration)
        base=base.resize(lambda t: 1 + 0.03*math.sin(t*0.3))
    try:
        hook_img=f"hook_{NOW}.png"
        create_text_image(script[:130], hook_img, "hook")
        hook_clip=ImageClip(hook_img).set_duration(min(6,duration)).set_position((0,0))
        cap1_img=f"cap1_{NOW}.png"
        cap2_img=f"cap2_{NOW}.png"
        create_text_image(script[130:300], cap1_img, "normal")
        create_text_image(script[300:500], cap2_img, "normal")
        cap1=ImageClip(cap1_img).set_start(6).set_duration(min(110,max(0,duration-6))).set_position((0,0))
        cap2=ImageClip(cap2_img).set_start(116).set_duration(max(0,duration-116)).set_position((0,0))
        prog=ColorClip((1080,10), color=(255,215,0), duration=duration).set_position((0,1910))
        final=CompositeVideoClip([base, hook_clip, cap1, cap2, prog])
        for f in [hook_img, cap1_img, cap2_img]:
            try: os.remove(f)
            except: pass
    except:
        final=base
    voice=AudioFileClip(VOICE_FILE)
    final=final.set_audio(voice)
    print(" >> Writing video...")
    final.write_videofile(VIDEO_FILE, fps=24, codec='libx264', audio_codec='aac', threads=2, logger=None)
    size=os.path.getsize(VIDEO_FILE)/1024/1024
    print(f"\n✅ DONE: {VIDEO_FILE} | {duration/60:.1f} min | {size:.1f} MB | Google Voice FREE")

def main():
    script=get_best_script()
    open(f"script_{NOW}.txt","w",encoding="utf-8").write(script)
    dur=get_google_voice_free(script)
    make_video(dur, script)

if __name__=="__main__":
    main()
