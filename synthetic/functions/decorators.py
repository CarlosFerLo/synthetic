from .base import Function, FunctionCallable

def function (name: str, description: str) :
    def inner (func: FunctionCallable) :
        return Function(
            name=name,
            description=description,
            func=func
    )
    return inner


