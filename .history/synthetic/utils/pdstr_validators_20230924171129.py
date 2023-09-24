from typing import List, Callable

import re

def str_has_partial_head_body_structure (string: str) -> bool :
    extract_tags = re.compile(r"<([^<>]*)>", flags=re.M)
    tags = ["HEAD", "/HEAD", "START", "END"]
    
    match = re.search(pattern=extract_tags, string=string)
    
    if not match: return False
        
    for idx, tag in enumerate(match.groups()) :
        if tag != tags[idx] : return False
        
    return True

def str_has_no_nonwhite_characters_between_head_and_body (string: str) -> bool :
    ends_head_and_non_whitespace = re.compile(r"</HEAD>(.*)")
    
    match = ends_head_and_non_whitespace.search(string)
    
    if match and re.find(r"\S", match.group()) and not re.find(r"<START>", match.group()):
        return False
    
    return True

PDSTR_VALIDATORS: List[Callable[[str], str]] = [
    str_has_partial_head_body_structure,
    str_has_no_nonwhite_characters_between_head_and_body
]