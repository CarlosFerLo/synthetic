from typing import List, Callable

import re

def str_has_partial_head_body_structure (string: str) -> bool :
    extract_tags = re.compile(r"<([^<>]*)>", flags=re.M)
    tags = ["HEAD", "/HEAD", "START", "END"]
    
    match = re.findall(pattern=extract_tags, string=string)
    
    if not match: return False
        
    for idx, tag in enumerate(match) :
        if tag != tags[idx] : return False
        
    return True

def str_has_no_nonwhite_characters_between_head_and_body (string: str) -> bool :
    head_end_tag = re.compile(r"</HEAD>")
    if head_end_tag.find(string) :
        start_tag = re.compile(r"<START>")
        if start_tag.search(string) :
            head_end_start_content = re.compile(r"</HEAD>(\s*)<START>", flags=re.M)
            return head_end_start_content.search(string)
        else :
            head_and_whitespace_at_the_end = re.compile(r"</HEAD>(\s*)$", flags=re.M)
            return head_and_whitespace_at_the_end.search(string) 
   
    return True

PDSTR_VALIDATORS: List[Callable[[str], str]] = [
    str_has_partial_head_body_structure,
    str_has_no_nonwhite_characters_between_head_and_body
]