from typing import List


class Config:
    def __init__(self) -> None:
        self.pages: List[str] = []
        self.extensions: List[str] = []

    def update(self, config: dict) -> None:
        for k, v in config.items():
            setattr(self, k, v)
