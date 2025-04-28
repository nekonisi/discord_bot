from ai_assistant import AiAssistant
from sperm import Sperm
from dotenv import load_dotenv
import os

class AiMother:
    GOOGLE_API_TOKEN: str
    baby: AiAssistant
    
    def __init__(self):
        """
        - AiMotherクラスの初期化
        - 環境変数、あるいは、dotenvファイルからGoogle APIトークンを取得して設定する
        """
        load_dotenv()
        self.GOOGLE_API_TOKEN = os.getenv('GOOGLE_API_KEY')
        self.baby = None
        if self.GOOGLE_API_TOKEN is None:
            raise ValueError("Google API Tokenが設定されていません")        

    def get_pregnant(self, sperm: Sperm) -> None:
        """
        - AiFatherインスタンスからSpermインスタンスを受取り、妊娠する
            - 妊娠: AiAssistantインスタンスを生成し、変数babyとして格納する
        
        Parameters
        ----------
        sperm: Sperm
            Spermインスタンス
        """
        character = sperm.get_character()
        self.baby = AiAssistant(self.GOOGLE_API_TOKEN, ai_character=character)

    def bear(self) -> 'AiAssistant':
        """
        - 出産する
            - 出産: AiAssistantインスタンスを返す
        """
        if (self.baby is None):
            raise ValueError("妊娠していません")
        return self.baby