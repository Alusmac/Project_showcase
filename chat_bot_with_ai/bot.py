import asyncio
import os
import tempfile
import urllib.parse
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from openai import OpenAI
from faster_whisper import WhisperModel

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("Завантаження моделей... (це може зайняти час)")
try:
    whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
    print("Whisper завантажено.")
except Exception as e:
    print(f"Помилка завантаження Whisper (перевір FFmpeg): {e}")
    whisper_model = None

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """
Ти — милий саркастичний AI-асистент.
Відповіді короткі, дружні, трохи іронічні. Спілкуйся українською.
"""

user_prompts = {}


def get_style_keyboard() -> InlineKeyboardMarkup:
    """Style keyboard
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎬 Реалізм", callback_data="style_realistic"),
            InlineKeyboardButton(text="🌸 Аніме", callback_data="style_anime")
        ],
        [
            InlineKeyboardButton(text="👾 Кіберпанк", callback_data="style_cyberpunk"),
            InlineKeyboardButton(text="🎨 Малюнок", callback_data="style_art")
        ],
        [
            InlineKeyboardButton(text="🧱 3D Рендер", callback_data="style_3d"),
            InlineKeyboardButton(text="🚫 Без стилю", callback_data="style_none")
        ]
    ])
    return keyboard


async def generate_and_send_photo(chat_id, prompt, caption_text) -> None:
    """A utility function for generating URLs and sending photos.
    """
    try:

        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

        await bot.send_photo(chat_id=chat_id, photo=url, caption=caption_text)
        return True
    except Exception as e:
        print(f"Image Generation Error: {e}")
        return False


@dp.message(CommandStart())
async def start(message: types.Message) -> None:
    """start telegram bot.
    """

    await message.answer(
        "🤖 Привіт! Я оновлений саркастичний асистент.\n\n"
        "Як миттєво щось створити:\n"
        "• `/draw [що намалювати]` — малюю відразу.\n"
        "• `/imagine [що намалювати]` — малюю з вибором стилю.\n"
        "• Просто пиши або надсилай голосові — я відповім.",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Command("draw"))
async def draw_command(message: types.Message) -> None:
    """draw pictures
    """

    prompt = message.text.replace("/draw", "").strip()

    if not prompt:
        await message.answer("Напиши: `/draw котик кіборг`")
        return

    status_msg = await message.answer(f"🎨 Малюю '{prompt}' (без стилю, бо я так бачу)...")

    success = await generate_and_send_photo(message.chat.id, prompt, f"Ось твій '{prompt}'")

    await status_msg.delete()

    if not success:
        await message.answer("❌ Здається, в мене скінчилися віртуальні фарби.")


@dp.message(Command("imagine"))
async def imagine_command(message: types.Message) -> None:
    """imagine pictures in few style
    """

    prompt = message.text.replace("/imagine", "").strip()

    if not prompt:
        await message.answer("Напиши: `/imagine котик віртуального світу`")
        return

    user_prompts[message.from_user.id] = prompt

    await message.answer(
        f"О, '{prompt}'? Цікаво (ні).\nОбери стиль для шедевра:",
        reply_markup=get_style_keyboard()
    )


@dp.callback_query(F.data.startswith("style_"))
async def process_style_choice(callback: types.CallbackQuery) -> None:
    """you can choose a style or anime
    """
    user_id = callback.from_user.id

    if user_id not in user_prompts:
        await callback.answer("❌ Промт загубився. Спробуй /imagine знову.", show_alert=True)
        await callback.message.edit_reply_markup(reply_markup=None)
        return

    style_choice = callback.data.split("_")[1]
    original_prompt = user_prompts[user_id]

    del user_prompts[user_id]

    style_modifiers = {
        "realistic": "photorealistic, highly detailed, 8k, national geographic style",
        "anime": "anime style, vibrant colors, detailed line art, studio ghibli style",
        "cyberpunk": "cyberpunk style, neon lights, futuristic city, dark atmosphere, retro-futuristic",
        "art": "digital painting, oil on canvas style, artistic, expressive brushstrokes",
        "3d": "3d render, blender style, octane render, detailed, pixar style",
        "none": ""
    }

    final_prompt = f"{original_prompt}, {style_modifiers.get(style_choice, '')}".strip(", ")

    await callback.message.edit_text(f"🎨 Малюю: '{original_prompt}' (стиль: {style_choice})...", reply_markup=None)

    success = await generate_and_send_photo(callback.message.chat.id, final_prompt,
                                            f"Ось твій '{original_prompt}' у стилі {style_choice}")

    if not success:
        await callback.message.answer("❌ Художник з мене так собі, сталася помилка.")

    await callback.answer()


@dp.message(F.voice | F.text)
async def handle_message(message: types.Message) -> None:
    """ Voice messages
    """

    if message.text and message.text.startswith("/"):
        return

    if message.voice and whisper_model is None:
        await message.answer("⚠️ Голосові недоступні. Я не чую.")
        return

    processing_msg = await message.answer("⏳ Думаю... (це рідкість)")

    try:

        if message.voice:
            file = await bot.get_file(message.voice.file_id)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp:
                await bot.download_file(file.file_path, tmp.name)
                tmp_path = tmp.name

            segments, _ = whisper_model.transcribe(tmp_path, beam_size=5, language="uk")
            user_text = " ".join([s.text for s in segments])

            os.remove(tmp_path)

            if not user_text.strip():
                await processing_msg.edit_text("😶 Я чув тільки тишу. Це був натяк?")
                return

        else:
            user_text = message.text

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )

        ai_answer = response.choices[0].message.content
        await processing_msg.edit_text(ai_answer)

    except Exception as e:
        await processing_msg.edit_text("⚠️ В мене тимчасовий збій системи (мозок відмовив).")
        print(f"General Error: {e}")


async def main() -> None:
    """main function
    """
    print("Бот запущений і готовий (ні до чого)...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнений. Пішов спати.")
