import re
from typing import List, Callable

def str_has_head_body_structure (string: str) -> bool :
    split_by_tag = re.compile(r"[<>]gm")
    list_str = re.split(pattern=split_by_tag, string=string)
    
    print(list_str)


VALIDATORS: List[Callable[[str], bool]] = [
    str_has_head_body_structure
]
