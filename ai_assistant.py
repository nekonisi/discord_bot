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
    prompts: list

    def __init__(self, api_key: str, ai_character: list = None, prompts: list = []) -> None:
        self.__prepare(api_key)
        self.model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                           safety_settings=genai.safety_settings)
        self.chat = None
        self.prompts = prompts
        self.ai_character = ai_character
        self.start_chat()
        
    def __prepare(self, api_key: str) -> None:
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
        # genai.system_instructions = self.ai_character
        
    def generate_response(self, message: str) -> str:
        print(self.model)
        response = self.chat.send_message(message)
        return response.text

    def start_chat(self, prompts = "") -> None:
        if (self.chat == None):
            self.chat = self.model.start_chat(history = self.prompts)

    def reset_chat(self) -> None:
        # HACK: チャットセッションを保存する機構を作りたい
        self.chat = None

model = AiAssistant('AIzaSyBucaJsX45IJb58CyoH60YqvyUtbXLJGlg')
print(model.generate_response('私の名前は？'))
print(model.generate_response('私の名前は？'))