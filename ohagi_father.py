from ai_father import AiFather
from ai_mother import AiMother
from ohagi_sperm import OhagiSperm

class OhagiFather(AiFather):
    sperm: OhagiSperm
    
    def __init__(self):
        """
        - OhagiFatherクラスの初期化
        - OhagiSpermインスタンスを生成し、変数spermとして格納する
        """ 
        self.sperm = OhagiSperm()

    def make_sperm(self):
        """
        - Spermインスタンスから、characterを生成する
        """
        
        # personaを設定する
        personas = self.sperm.get_information()['personas']
        personas.insert(0, "# アシスタントの人格")
        
        # 箇条書きでcharactorを生成する
        personas_list = "\n- ".join(personas)

        self.sperm.set_character(personas_list)
        
        # audience_personasを設定する
        audience_personas = self.sperm.get_information()['audience_personas']
        audience_personas.insert(0, "# ユーザの人格・特徴")
        audience_personas_list = "\n- ".join(audience_personas)

        self.sperm.set_character(audience_personas_list)
        
        # promptsを設定する
        prompts = self.sperm.get_information()['prompts']
        prompts.insert(0, "# ユーザとの会話履歴")
        prompts_list =  "\n- ".join(prompts)        
        
        self.sperm.set_character(prompts_list)

    def seed(self, ai_mother: AiMother) -> None:
        """
        - AiMotherインスタンスを妊娠させる
        """
        character = self.sperm.get_character()
        if (character is None):
            raise ValueError("Spermが生成されていません")
        
        ai_mother.get_pregnant(self.sperm)