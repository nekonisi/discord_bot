from google import generativeai as genai
from google.generativeai import ChatSession
from google.generativeai import GenerativeModel
from google.generativeai.types import HarmCategory
from google.generativeai.types import HarmBlockThreshold

class AiAssistant:
    # system_instructions
    ai_character: list
    # model, safety_settings
    ai_param: list
    chat: ChatSession
    model: GenerativeModel

    def __init__(self, api_key: str, ai_character: list = None) -> None:
        """
        - ai_assistant自体の初期化を行う
        
        Parameters
        ----------
        api_key : str
            Google CloudのAPIキー
        
        ai_character : list, optional
            AIのキャラクターを指定する。デフォルトはNone。
            Noneの場合は、デフォルトのキャラクターが設定される。

        Returns
        -------
        None
        
        """
        self.ai_character = ai_character
        self.__prepare(api_key)
        # HACK: モデルを選択できるようにする
        self.model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                           safety_settings=genai.safety_settings,
                                           system_instruction=self.ai_character)
        self.chat = None
        self.start_chat()
        
    def __prepare(self, api_key: str) -> None:
        """
        - AIの初期化を行うための準備を行う
        
        Parameters
        ----------
        api_key : str
            Google CloudのAPIキー
        
        Returns
        -------
        None
        """
        # デフォルトの設定
        # HACK: モデルを選択できるようにする
        genai.configure(api_key=api_key)
        # 全ての有害カテゴリーをブロックしない
        genai.safety_settings = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }
        
    def generate_response(self, message: str) -> str:
        """
        - メッセージを受け取り、AIからの応答を生成する
        
        Parameters
        ----------
        message: str
            ユーザーからのメッセージ
                
        Returns
        -------
        response: str
            AIからの応答
        """
        response = self.chat.send_message(message)
        return response.text

    def start_chat(self) -> None:
        """
        - `ai_character`（デフォルトの命令）を元にChatを開始する
        - 既にChatが存在する場合は何もしない。
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if (self.chat == None):
            self.chat = self.model.start_chat()

    def reset_chat(self) -> None:
        """
        - Chatをリセットする
        """
        # HACK: チャットセッションを保存する機構を作りたい
        self.chat = None