from typing import List

class DictElement () :
    id: str
    content: str

    children: List["DictElement"] = []

    def __init__ (self, id: str, content: str, children: List["DictElement"] = []) -> None :
        self.id = id
        self.content = content
        self.children = children

class FunctionCall (DictElement) :
    name: str
    input: str
    output: str
    
    def __init__(self, name: str, input: str, output:str, id: str, content: str, children: List[DictElement] = []) -> None:
        super().__init__(id, content, children)
        self.name = name
        self.input = input
        self.output = output
class DynamicStringDict () :
    head: DictElement
    body: DictElement
    
    def __init__(self, head: DictElement, body: DictElement) -> None:
        self.head = head
        self.body = body

