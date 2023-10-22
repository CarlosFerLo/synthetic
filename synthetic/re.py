from typing import Dict, List

from re import *
from re import compile as _compile, findall as _findall, RegexFlag, search as _search

_GET_KEY_NAMES = _compile(r"{([^[{}]*)}")

def compile (string: str, key_pattern_dict: Dict[str, str] = {}, flags: int | RegexFlag = 0) -> Pattern :
    string = _to_parseable(string)
    matches = _findall(_GET_KEY_NAMES, string)
    for m in matches :
        p = key_pattern_dict.get(m, "(.*)")
        string = string.replace("{" + m + "}", f"(?P<{m}>{p})")
    return _compile(string, flags=flags)

def findall(pattern: bytes | Pattern[bytes], string: str, flags: int | RegexFlag = 0) -> List[Dict[str, str]]:
    compiled_pattern = _compile(pattern, flags=flags) if isinstance(pattern, bytes) else pattern
    matches = []
    while string:
        match = _search(compiled_pattern, string)
        if match:
            match_dict = match.groupdict()
            match_dict["match"] = match.group()
            
            matches.append(match_dict)
            string = string[match.end():]
        else:
            break
    return matches    
    
def _to_parseable (string: str) -> str :
    string = string.replace("(", r"\(").replace(")", r"\)")
    string = string.replace("[", r"\[").replace("]", r"\]")
    
    return string
