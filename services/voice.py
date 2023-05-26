import openai
import io
from aiogram import Bot
from aiogram.types import Voice
from pydub import AudioSegment
from config_data.config import AiConfig, load_ai


ai_config: AiConfig = load_ai('./.env')

openai.api_key = ai_config.ai.token


# TRANSCRIPT VOICE TO TEXT WITH OPEN AI
async def voice_to_text(path: str) -> str:
    with open(path, 'rb') as voice:
        transcript = openai.Audio.transcribe("whisper-1", voice)

    return transcript.text


#Saving voice to mp3
async def save_mp3(bot: Bot, voice: Voice) -> str:
    voice_info = await bot.get_file(voice.file_id)
    voice_raw = io.BytesIO()
    await bot.download_file(voice_info.file_path, voice_raw)

    voice_mp3_path = f"voice_files/voice-{voice.file_unique_id}.mp3"
    AudioSegment.from_file(voice_raw, format='ogg').export(voice_mp3_path, format='mp3')
    return voice_mp3_path