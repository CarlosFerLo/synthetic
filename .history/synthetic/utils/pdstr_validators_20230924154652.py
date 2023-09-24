from typing import List, Callable

import re

def str_has_partial_head_body_structure (string: str) -> bool :
    extract_tags = re.compile(r"<([^<>]*)>", flags=re.M)
    tags = ["HEAD", "/HEAD", "START", "END"]
    
    match = re.search(pattern=extract_tags, string=string)
    
    if not match: return False
        
    for tag, idx in enumerate(match.groups()) :
        if tag != tags[idx] : return False
        
    return True


PDSTR_VALIDATORS: List[Callable[[str], str]] = [
    str_has_partial_head_body_structure
]