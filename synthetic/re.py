from typing import Dict

from re import *
from re import compile as std_compile, findall as std_findall

_GET_KEY_NAMES = std_compile(r"{([^[{}]*)}")

def compile (string: str, key_pattern_dict: Dict[str, str] = {}) -> Pattern :
    string = _to_parseable(string)
    matches = std_findall(_GET_KEY_NAMES, string)
    for m in matches :
        p = key_pattern_dict.get(m, "(.*)")
        string = string.replace("{" + m + "}", f"(?P<{m}>{p})")
    return std_compile(string)

def _to_parseable (string: str) -> str :
    string = string.replace("(", r"\(").replace(")", r"\)")
    string = string.replace("[", r"\[").replace("]", r"\]")
    
    return string
    