from abc import ABC, abstractmethod

class Sperm(ABC):
    personas: list
    audience_personas: list[str]
    params: list
    prompts: list
    character: list

    @abstractmethod
    def get_information(self) -> dict:
        pass

    def set_character(self, character:list) -> list:
        self.character.append(character)
    
    def get_character(self) -> list:
        return self.character
    