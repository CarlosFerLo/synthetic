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
    if string.find("</HEAD>") :
        if string.find("<START>") :
            intermediate_str_extractor = re.compile(r"</HEAD>(\s*)<START>")
            if intermediate_str_extractor.match(string) :
                return True
            else: 
                return False
        else :
            string = string.strip()
            if string.endswith("</HEAD>") :
                return True
            else :
                return False
        
            


PDSTR_VALIDATORS: List[Callable[[str], str]] = [
    str_has_partial_head_body_structure,
    str_has_no_non_space_characters_between_head_and_start_tags
]