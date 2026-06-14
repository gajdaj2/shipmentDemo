from typing import Any, Callable


def fence(func):
    def wrapper(*args):
        print("This is a fence")
        func(*args)
        print("This is the end of the fence")

    return wrapper


@fence
def log(string: str = "This is a log message"):
    print(string)


routes: dict[str, Callable[[Any], Any]] = {}


def route(path: str):
    def decorator(func: Callable[[Any], Any]):
        routes[path] = func
        return func

    return decorator


log("Hej to jest test")
