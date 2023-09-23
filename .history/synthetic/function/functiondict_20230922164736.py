from typing import Dict, Optional

class FunctionDict ():
    dict: Dict[str, str]
    input_tag: str = "input"
    output_tag: str = "output"
    
    def __init__ (self, dict: Dict[str, str],
        input_tag: str = "input", output_tag: str = "output"
    ) -> None :
        self.dict = dict

        
        if not self.input_tag in dict.keys() and not self.output_tag in dict.keys():
            raise ValueError("Need to include the input or output tag in the FunctionDict")