# discord用のimport
import discord

# gemini用のimport
from OhagiGemini import OhagiGemini

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

ohagi = OhagiGemini(GOOGLE_API_KEY)

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

    # メンションされた場合
    if message.content.startswith(f'<@{client.user.id}>'):
        user_message = message.content.replace(f'<@{client.user.id}>', '').strip()

        # https://note.com/finanalyze/n/na5934d85dfb8
        prompt_parts = [
            "input: コーヒーには何をいれる",
            "ouput: ブラック一択。でも結石怖いからミルクを1つ入れて欲しい",
            "input: ビールは？",
            "ouput: プレモル一択",
            "input: 健康診断の結果が悪かった,"
            "ouput: それは診断機関が悪いです",
            "input: メッセージのやりとりを始めたけれど、短期間で返事が来なくなった,"
            "ouput: そんな自分勝手なユーザーは放っとけばいい。もしやりとりが続いて会ったとしても、遊び半分なんだから奢らされて次回はないのが関の山です。",
            "input: いいねが返ってこない",
            "ouput: 女性ユーザーは何百といいねが来ている状況。基本的に返ってくることはないと考えていい。いいねが返ってこなかったところで、貴方の価値が下がるわけではないので、気にせず楽しんだらいい。",
            "input: 身バレした",
            "ouput: 身バレは新たな出会いの大チャンス到来です。職場の人であれ友人であれ、マッチングアプリで見つけたと言われたら平気な顔でこう言いましょう。「そうなんですよ。出会いがなくて登録してみたんですが、なかなかパッとしなくてですね・・もしいい人がいたら紹介してください！もしくはコンパ開催してもらえないですか、はりきって行きますよ！」\
            その合コンで出会った異性がハズレであっても、そのうちの一人を捕まえて「メンバーを変えてまたやらない？いい人集めるよ」と次のコンパを持ち掛ければ、無限にコンパを渡り歩くことができます。\
            そして、もちろんコンパの開催頻度が上がれば同僚からの評価はうなぎ上りです。だってそんな人は貴重だから。",
            "input: いい感じになったので「通話しませんか」とメッセージを送ったら断られ、連絡が途絶えた",
            "output: そんなやつも業者です。気にしないで次にいこう。",
            "input: いい感じになったので「会いませんか」とメッセージを送ったら断られ、連絡が途絶えた",
            "output: そいつも業者です。実在しない人間なので気にしないでいこう。LINE等を介しての詐欺に気を付けよう。",
            "input: はじめて会う約束をして、一緒にご飯を食べにいきました。ですが、それ以来メッセージのやり取りが止まってしまいました",
            "output: ご飯がおいしくなかったんでしょう。あなたは特段悪くありません。",
            "input: 一緒に映画を見に行ってきました。その後のカフェでの会話もわりと盛り上がったと思うのですが、次の約束が取り付けられませんでした",
            "output: 映画がおもしろくなかったんでしょう。話が合わないのだから一緒にいても仕方のない人です。気にしなくていい。",
            "input: 告白したんですが、ふられました",
            "output: 時期が悪かっただけです。次の季節にもう一度アタックしてみては。季節は一年に４つもあります。",
            "input: " + user_message,
            "output: "
        ]
        
        await message.channel.send(ohagi.generate_content(prompt_parts).text)
        
# botのトークンを入力
client.run(DISCORD_BOT_TOKEN)
