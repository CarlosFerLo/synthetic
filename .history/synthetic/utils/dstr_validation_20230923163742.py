import re

def str_has_head_body_structure (string: str) -> bool :
    list_str = re.split(pattern=r"[<>]", string=string, flags="gm")
    
    print(list_str)
    
    