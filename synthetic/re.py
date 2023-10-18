from typing import Dict

from re import *
from re import compile as std_compile, findall as std_findall

_GET_KEY_NAMES = std_compile(r"{(\S*)}")

def compile (string: str, key_pattern_dict: Dict[str, str] = {}) -> Pattern :
    matches = std_findall(_GET_KEY_NAMES, string)
    for m in matches :
        p = key_pattern_dict.get(m, "(.*)")
        string = string.replace("{" + m + "}", f"(?P<{m}>{p})")
    return std_compile(string)