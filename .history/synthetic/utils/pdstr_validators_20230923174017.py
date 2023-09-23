from typing import List, Callable

def str_has_partial_head_body_structure (string: str) -> bool :
    return True

PDSTR_VALIDATORS: List[Callable[[str], str]] = [
    str_has_partial_head_body_structure
]