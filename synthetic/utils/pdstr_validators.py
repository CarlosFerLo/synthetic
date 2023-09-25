from typing import List, Callable

import re

def str_has_partial_head_body_structure (string: str) -> bool :
    extract_tags = re.compile(r"<([^<>]*)>", flags=re.M)
    tags = ["HEAD", "/HEAD", "START", "END"]
    
    match = re.findall(pattern=extract_tags, string=string)
    
    if not match and string != "": return False
        
    for idx, tag in enumerate(match) :
        if tag != tags[idx] : return False
        
    return True

def str_has_no_nonwhite_characters_between_head_and_body (string: str) -> bool :
    head_end_tag = re.compile(r"</HEAD>")
    if head_end_tag.search(string) :
        start_tag = re.compile(r"<START>")
        if start_tag.search(string) :
            head_end_start_content = re.compile(r"</HEAD>(\s*)<START>", flags=re.M)
            return head_end_start_content.search(string)
        else :
            head_and_whitespace_at_the_end = re.compile(r"</HEAD>(\s*)$", flags=re.M)
            return head_and_whitespace_at_the_end.search(string) 
   
    return True

def str_has_no_function_calls_in_the_head (string: str) -> bool :
    has_head_start = re.compile(r"<HEAD>")
    if has_head_start.search(string) :
        has_head_end = re.compile(r"</HEAD>")
        
        if has_head_end.search(string) :
            head_content_extractor = re.compile(r"<HEAD>(.*)</HEAD>")
            content = head_content_extractor.findall(string=string)[0]
        else :
            content = re.split(pattern=has_head_start, string=string)[-1]
    
        has_function_call = re.compile(r"\[(\S*)\((.*)\)->(.*)\]")
        
        return not has_function_call.search(content)
    
    return True

def str_has_no_partial_function_calls_on_head (string: str)-> bool:
    has_head_start = re.compile(r"<HEAD>")
    if has_head_start.search(string) :
        has_head_end = re.compile(r"</HEAD>")
        if has_head_end.search(string) :
            return True
        else :            
            has_partial_function_call = re.compile(r"\[(\S*)\((.*)\)")
            return not has_partial_function_call.search(string)
    return True

PDSTR_VALIDATORS: List[Callable[[str], str]] = [
    str_has_partial_head_body_structure,
    str_has_no_nonwhite_characters_between_head_and_body,
    str_has_no_function_calls_in_the_head,
    str_has_no_partial_function_calls_on_head
]