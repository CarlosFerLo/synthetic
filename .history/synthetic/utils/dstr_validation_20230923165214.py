import re
from typing import List, Callable

def str_has_head_body_structure (string: str) -> bool :
    split_by_tag = re.compile(r"[<>]", flags=re.M)
    list_str = re.split(pattern=split_by_tag, string=string)
    
    print(list_str)
    
    if len(list_str) < 7 : return False
    
    return (list_str[1] == "HEAD" and 
            list_str[3] == "/HEAD" and
           
            list_str[5] == "START" and
            list_str[6] == "END" ) 

VALIDATORS: List[Callable[[str], bool]] = [
    str_has_head_body_structure
]
