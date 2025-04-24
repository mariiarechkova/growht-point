from abc import ABC, abstractmethod


class BaseMessenger(ABC):
    @abstractmethod
    def send_letter(self, to: str, text: str) -> None:
        pass
