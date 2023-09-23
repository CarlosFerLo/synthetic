class DictElement () :
    id: str
    content: str

    def __init__ (self, id: str, content: str) -> None :
        self.id = id
        self.content = content

class DynamicStringDict () :
    head: DictElement
    body: DictElement
    
    def __init__(self, head: DictElement, body: DictElement) -> None:
        self.head = head
        self.body = body
