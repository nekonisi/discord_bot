from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.generativeai import GenerativeModel, GenerationConfig

# singletonモデル
class OhagiGemini():
    _instance = None

    # コンストラクタ
    def __new__(cls, api_key):
        if cls._instance is None:
            cls._instance = super(OhagiGemini, cls).__new__(cls)
            cls._instance.api_key = api_key
            cls._instance.safety_settings = {
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            }
            cls._instance.config = GenerationConfig(
                temperature=0,
                top_p=0,
            )
            cls._instance.model = GenerativeModel('gemini-1.5-flash', safety_settings=cls._instance.safety_settings, generation_config=cls._instance.config)
        return cls._instance.model