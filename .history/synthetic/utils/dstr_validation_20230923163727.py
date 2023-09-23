import re

def str_has_head_body_structure (string: str) -> bool :
    list_str = re.split(pattern=r"[<>]gm", string=string)
    
    print(list_str)
    
    