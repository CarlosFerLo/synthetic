import re
from typing import List, Callable

def str_has_head_body_structure (string: str) -> bool :
    split_by_tag = re.compile(r"^<HEAD>(.*)</HEAD>(\w*)<START>(.*)<END>$")

VALIDATORS: List[Callable[[str], bool]] = [
    str_has_head_body_structure
]
