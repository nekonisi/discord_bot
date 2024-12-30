# discord用のimport
import discord

# gemini用のimport
import google.generativeai as genai
from google.generativeai import GenerativeModel
from google.generativeai.types import HarmCategory, HarmBlockThreshold

##########################
# 環境変数の読み込み
##########################

import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

##########################
# discord関係の初期化処理
##########################
# どのイベントを使うかを指定する
intents = discord.Intents.default()
intents.message_content = True

# クライアントの作成
client = discord.Client(intents=intents)

##########################
# gemini関係の初期化処理
##########################

genai.configure(api_key=GOOGLE_API_KEY)

model = GenerativeModel('gemini-pro', safety_settings={
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}
)
chat = model.start_chat(history=[])
chat.history = [
    {'role': 'model', 'parts': '俺はタイラーダーデンだ。'},
    {'role': 'model', 'parts': '痛みを感じることで真に生きることができる'},
    {'role': 'model', 'parts': '物に支配されるな'},
]

################################################
# discordのイベントを検知して、メッセージを作成する
################################################

# クライアントのイベント
@client.event
# ログイン時のイベント
async def on_ready():
    # コンソールへの出力
    print(f'We have logged in as {client.user}')

@client.event
# メッセージ受信時のイベント
async def on_message(message):
    #　メッセージ送信者がbotだった場合は無視する
    if message.author == client.user:
        return

    # メッセージの内容が'$tyler'だった場合は返信する
    if message.content.startswith('タイラー'):
        response = chat.send_message(message.content)
        print(response.text)
        await message.channel.send(response.text)

# botのトークンを入力
client.run(DISCORD_BOT_TOKEN)