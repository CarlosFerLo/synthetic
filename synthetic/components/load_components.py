from typing import List, Type, Optional

from .base import Component
from .function_description import FunctionDescriptions
from .funation_call_description import FunctionCallDescription

import synthetic
import synthetic.re as re
from synthetic.errors import LoadComponentsError

_BASE_COMPONENTS = {
    "FunctionDescriptions": FunctionDescriptions,
    "FunctionCallDescription": FunctionCallDescription
}
 
def load_components (string: Optional[str] = None, names: Optional[List[str]] = None) -> List[Type[Component]] :
    if string is not None and names is not None :
        raise LoadComponentsError("Too Many Arguments. You can only specify either a string or a list of names.")
    if string is None and names is None :
        raise LoadComponentsError("Need to specify either a string or a list of names.")
    
    if string is not None :
        components = []
        for comp in _BASE_COMPONENTS.values() :
            sign = comp.signature()
            if re.search(sign, string) :
                components.append(comp)
    else :
        components = []
        for name in names :
            try :
                comp: Type[Component] = _BASE_COMPONENTS.get(name)
            except KeyError :
                raise LoadComponentsError(f"Invalid name '{name}'.")
            components.append(comp)
    
    return components