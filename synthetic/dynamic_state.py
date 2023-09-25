import re
from enum import Enum

Location = Enum("Location", ["HEAD", "BODY", "START", "MIDDLE", "END"])

head_start = re.compile(r"<HEAD>")
head_end = re.compile(r"</HEAD>")
body_start = re.compile(r"<START>")
body_end = re.compile(r"<END>")
class DynamicState () :
    location: Location
    
    def __init__(self, string: str) -> None:
        self._set_location(string)
        
    def update (self, string: str) -> None:
        if body_end.search(string) :
            self.location = Location.END
        elif body_start.search(string) :
            self.location = Location.BODY
        elif head_end.search(string) :
            self.location = Location.MIDDLE
        elif head_start.search(string) :
            self.location = Location.HEAD
        
        
    def _set_location(self, string:str) -> None:
        if not head_start.search(string) :
            self.location = Location.START
        elif not head_end.search(string) :
            self.location = Location.HEAD
        elif not body_start.search(string) :
            self.location = Location.MIDDLE
        elif not body_end.search(string):
            self.location = Location.BODY
        else :
            self.location = Location.END
        
