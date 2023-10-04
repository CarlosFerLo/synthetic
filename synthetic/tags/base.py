from typing import Optional

from synthetic.validators import ValidatorSet

class Tag () :
    name: str
    validator_set: ValidatorSet
    def __init__(self, name: str, validator_set: Optional[ValidatorSet] = None) -> None :
        self.name = name
        if validator_set: self.validator_set = validator_set
        else : self.validator_set = ValidatorSet(validators=[])