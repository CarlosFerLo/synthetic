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
    find_head_end = re.compile(r"</HEAD>")
    find_start_tag = re.compile(r"<START>")
    
    has_head_end = find_head_end.match(string)
    has_start_tag = find_start_tag.match(string)
    
    if has_head_end and has_start_tag :
        find_intermediate_content_is_white_space = re.compile("</HEAD>(\s*)<START>")
        has_intermediate_content_is_white_space: bool = find_intermediate_content_is_white_space.match(string)
        
        return has_intermediate_content_is_white_space 
    
    if has_head_end and not has_start_tag :
        find_ending_white_space = re.compile("</HEAD>(\s*)$")
        has_ending_white_space: bool = find_ending_white_space.match(string)
        
        return has_ending_white_space
    
    return True

PDSTR_VALIDATORS: List[Callable[[str], str]] = [
    str_has_partial_head_body_structure,
    str_has_no_nonwhite_characters_between_head_and_body
]