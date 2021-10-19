from typing import List, Optional
from datetime import date


class FileManager:
    @classmethod
    def make_file(cls, articles: List[str], root: str, file_name: str, kind: str, idx: Optional[int] = None):
        if idx is not None:
            with open(f'{root}/{idx}_{file_name}_{str(date.today())}.{kind}', 'w', encoding='utf-8') as f:
                for article in articles:
                    f.write(f'{article}\n')
        else:
            pass  # todo default behavior

    @classmethod
    def read_file(cls, path:str):
        pass
    # todo - read files
