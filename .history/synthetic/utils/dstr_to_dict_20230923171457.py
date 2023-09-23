from typing import Tuple
from synthetic.dstrdict import DictElement

import re

def get_head_and_body (string: str) -> Tuple[DictElement, DictElement] :
    extract_head_and_body = re.compile(r"^<HEAD>(.*)</HEAD>(\s*)<START>(.*)<END>$")
    
    match = re.match(pattern=extract_head_and_body, string=string)
    
    if not match : raise ValueError("Invalid string! A string must be validated before using this function.")
    
    print(match)
    
    