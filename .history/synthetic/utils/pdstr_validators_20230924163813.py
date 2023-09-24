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
    contains_head_end = re.compile(r"</HEAD>")
    contains_start_tag = re.compile(r"<START>")
    
    match_head_end = contains_head_end.search(string)
    match_start_tag = contains_start_tag.search(string)
    
    if not match_head_end :
        return True
    else :
        if not match_start_tag :
            if string.split().endswith("</HEAD>") :
                return True
            else :
                return False
        else :
            contains_white_space_between_head_and_body = re.compile(r"</HEAD>(\w*)<START>")
            if contains_white_space_between_head_and_body.match(string) :
                return True
            else :
                return False
            


PDSTR_VALIDATORS: List[Callable[[str], str]] = [
    str_has_partial_head_body_structure
]