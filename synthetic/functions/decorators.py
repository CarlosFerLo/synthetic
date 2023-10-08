from .base import Function, FunctionCall

def function (name: str, description: str) :
    def inner (func: FunctionCall) :
        return Function(
            name=name,
            description=description,
            func=func
    )
    return inner


