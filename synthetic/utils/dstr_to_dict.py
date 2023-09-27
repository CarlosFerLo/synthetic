from typing import Tuple, List
from synthetic.dstrdict import DictElement, FunctionCall

import re

def get_function_calls (string: str) -> List[FunctionCall] :
    extract_function_call = re.compile(r"\[(.*)\((.*)\)->(.*)\]")
    matches = extract_function_call.findall(string)
    
    function_calls = []
    for idx, match in enumerate(matches) :
        name, input, output = match
        call = FunctionCall(
            name=name,
            input=input,
            output=output,
            id=f"fcall-{idx}",
            content=f"[{name}({input})->{output}]"
        )
    
        function_calls += [call]
        
    return function_calls

def get_head_and_body (string: str) -> Tuple[DictElement, DictElement] :
    extract_head_and_body = re.compile(r"^<HEAD>(?P<head>(.|\n)*)<\/HEAD>([\s\n]*)<START>(?P<body>(.|\n)*)<END>$")
    string = string.strip()
    match = re.search(pattern=extract_head_and_body, string=string)
    
    if not match : raise ValueError("Invalid string! A string must be validated before using this function.")

    head = DictElement(
        id = "head",
        content = match.group("head")
    )
    
    function_calls = get_function_calls(match.group("body"))
    body = DictElement (
        id = "body",
        content = match.group("body"),
        children=function_calls
    )
    
    return head, body