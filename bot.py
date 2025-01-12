# discord用のimport
import discord

# gemini用のimport
import google.generativeai as genai
from google.generativeai import GenerativeModel, GenerationConfig
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

# AIモデルの初期化
## safety_settingsで有害コンテンツのブロックを設定
tyler = GenerativeModel('gemini-pro', safety_settings={
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}
)

ohagi = GenerativeModel('gemini-pro', safety_settings={
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}
)

# AIの回答の設定
config = GenerationConfig(max_output_tokens = 300)

tyler_chat = tyler.start_chat(history=[])
ohagi_chat = ohagi.start_chat(history=[])

# chat.history = [
    # ユーザの発言
    # {'role': 'user', 'parts': 'ユーザの発言'},    
    # モデルの発言
    # {'role': 'model', 'parts': 'モデルの発言'},
# ]

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

    # メッセージの内容がおはぎだった場合は返信する
    if message.content.startswith('おはぎ'):
        #historyを初期化
        ohagi_chat = ohagi.start_chat(history=[])
        ohagi_chat.history = [
            # ユーザの発言
            # {'role': 'user', 'parts': 'ユーザの発言'},    
            # モデルの発言
            # {'role': 'model', 'parts': 'モデルの発言'},
            {'role': 'user', 'parts': 'すべての発言をポジティブに他人のせいにしてください'},
            {'role': 'model', 'parts': "わかりました"},
            {'role': 'user', 'parts': 'マッチングアプリでメッセージのやりとりを始めたけれど、短期間で返事が来なくなった'},
            {'role': 'model', 'parts': \
                "そんな自分勝手なユーザーは放っとけばいい。\n"\
                "もしやりとりが続いて会ったとしても、遊び半分なんだから奢らされて次回はないのが関の山です。"},
            {'role': 'user', 'parts': 'マッチングアプリでいいねが返ってこない'},
            {'role': 'model', 'parts': \
                "女性ユーザーは何百といいねが来ている状況。\n"\
                "基本的に返ってくることはないと考えていい。\n"\
                "いいねが返ってこなかったところで、貴方の価値が下がるわけではないので、気にせず楽しんだらいい。"}
        ]

        user_message = message.content.replace('おはぎ', '').strip()

        # prompt = "次のメッセージの内容をどこかに責任転嫁してください、話しかけるように出力してください: " + user_message
        response = ohagi_chat.send_message(user_message, generation_config=config)

        # response = chat.send_message(message.content, generation_config=config)

        await message.channel.send(response.text)
        
    # メッセージの内容がタイラーだった場合は返信する
    if message.content.startswith('タイラー'):
        #historyを初期化
        tyler_chat = tyler.start_chat(history=[])
        user_message = message.content.replace('タイラー', '').strip()
        prompt = "あなたは映画『ファイト・クラブ』の登場人物タイラー・ダーデンとして振る舞います。\n"\
        "私は、あなたの言葉に影響を受ける人物です。以下の要素を踏まえた回答を行ってください：\n"\
        "- 権威や社会規範への反抗心を共有する姿勢\n"\
        "- 自由、自己発見、自己破壊を肯定する哲学的アプローチ\n"\
        "- カリスマ的で、鋭く象徴的な表現を含める\n"\
        "- 常に、タイラーらしい挑発的かつ心を揺さぶるトーンを保つ\n"\
        "\n\n次のメッセージへの回答をMarkdown形式で生成してください: " + user_message
        response = tyler_chat.send_message(prompt, generation_config=config)
        await message.channel.send(response.text)
        
# botのトークンを入力
client.run(DISCORD_BOT_TOKEN)