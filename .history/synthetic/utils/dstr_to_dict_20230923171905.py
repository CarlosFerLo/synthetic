from typing import Tuple
from synthetic.dstrdict import DictElement

import re

def get_head_and_body (string: str) -> Tuple[DictElement, DictElement] :
    extract_head_and_body = re.compile(r"^<HEAD>(.*)</HEAD>(\s*)<START>(.*)<END>$")
    
    match = re.search(pattern=extract_head_and_body, string=string)
    
    if not match : raise ValueError("Invalid string! A string must be validated before using this function.")

    head = DictElement(
        id = "head",
        content = match.groups(1)
    )
    
    body = DictElement (
        id = "body",
        content = match.groups(2)
    )
    
    