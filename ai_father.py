from abc import ABC, abstractmethod
from sperm import Sperm
from ai_mother import AiMother

class AiFather(ABC):
    sperm: 'Sperm'

    @abstractmethod
    def seed(self, ai_mother: 'AiMother') -> None:
        """
        - AiMotherインスタンスを受取り、seedする
        """
        pass

    @abstractmethod
    def make_sperm(self) -> None:
        """
        - Spermインスタンスから、ai_characterを生成する
        """
        pass
    