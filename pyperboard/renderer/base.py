from typing import Any, List, Mapping

from markdown.extensions import Extension


class Renderer:

    CUSTOM_EXTENSIONS_MAPPING: Mapping[str, Extension] = {}

    def __init__(self, extensions: List[str] = []):
        self.extensions = self._process_extensions(extensions)

    def render(self, page: str) -> str:
        raise NotImplementedError()

    def _process_extensions(self, extensions: List[str]) -> List[Any]:
        processed_extensions = []

        for ext in extensions:
            processed_extension = self.CUSTOM_EXTENSIONS_MAPPING.get(ext, ext)
            processed_extensions.append(processed_extension)

        print(processed_extensions)

        return processed_extensions
