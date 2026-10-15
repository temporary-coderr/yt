# GOOGLE FREE Voice YouTube Bot - 100% FREE - BEST QUALITY

## Voice: Google FREE (not ElevenLabs)
- gTTS = 100% FREE, no key needed, Indian accent, good quality
- Google Cloud WaveNet = FREE 1M chars/month = 20 videos FREE, 90% human

## Folder Structure - All folders for it:
```
your-repo/
├── final_google_free_bot.py     <- Main bot - Google FREE voice
├── final_best_quality_bot.py    <- Same bot (backup name)
├── youtube_uploader.py          <- Uploads to YOUR YouTube channel
├── requirements.txt             <- Google FREE libraries (GitHub can install)
├── daily-bot.yml                <- Standalone YML (easy to find)
└── .github/
    └── workflows/
        └── daily-bot.yml        <- AUTO SCHEDULE - GitHub needs this path
            cron: '0 0 * * *' = Daily 5:30 AM IST
```

## YML File Location:
- GitHub auto schedule needs: .github/workflows/daily-bot.yml
- If you don't see .github (hidden), manually create:
  1. GitHub repo -> Add file -> Create new file
  2. Type: .github/workflows/daily-bot.yml
  3. Paste content from daily-bot.yml in root

## Secrets to add (only secrets, no code edit):
Repo -> Settings -> Secrets and variables -> Actions -> New repository secret

1. GROQ_API_KEY = from console.groq.com/keys (free)
2. PIXABAY_API_KEY = from pixabay.com/api/docs/ (free, Pexels dead)
3. YOUTUBE_TOKEN_JSON = token.json content (connects to YOUR channel)
4. GOOGLE_CREDENTIALS_JSON = Optional - for WaveNet human voice (free 1M chars)
   - Get: console.cloud.google.com -> Enable Cloud Text-to-Speech API -> IAM -> Service Accounts -> Create key -> Download JSON -> Copy content as secret
   - If not added, bot uses gTTS 100% free

No ELEVENLABS_API_KEY needed - Google FREE is free forever.

## How it connects to YOUR channel:
- token.json = OAuth token linked to YOUR Gmail that owns YouTube channel
- GitHub secret YOUTUBE_TOKEN_JSON = that token
- Server uses token to upload to YOUR channel

## Auto Schedule:
- YML has schedule: cron '0 0 * * *' = Daily 5:30 AM IST
- Works even when your Jagdalpur home internet off for week
- GitHub server has internet 24/7

## Test:
Actions tab -> GOOGLE FREE Voice Daily Auto -> Run workflow -> Video generates + uploads
