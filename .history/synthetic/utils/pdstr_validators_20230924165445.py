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

def str_has_no_non_space_characters_between_head_and_start_tags (string: str) -> bool :
    match_only_head = re.compile(r"</HEAD>(\s*)$")
    match_both_head_and_body = re.compile(r"</HEAD>(\s*)<START>")
        
    if match_only_head.match(string) :
        return True
    if match_both_head_and_body.match(string) :
        return True
    
    if not r"</HEAD>".match(string):
        return True
    
    return False
            


PDSTR_VALIDATORS: List[Callable[[str], str]] = [
    str_has_partial_head_body_structure,
    str_has_no_non_space_characters_between_head_and_start_tags
]