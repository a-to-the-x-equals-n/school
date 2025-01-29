from typing import Callable, TypeVar, Any
import threading


''' CUSTOM DEBUG TOOL FROM MY OWN LIL' LIBRARY OF HELPERS '''

__COLORS = {
        (_DEBUG := "red"): "\033[91m",
        (_HEADING := "green"): "\033[92m",
        (_UPDATE :="blue"): "\033[94m",
        (_RESET := "reset"): "\033[0m"
    }



# thread-local storage to track nested debug states
bugs = _debug_stack = threading.local()
F = TypeVar('F', bound = Callable) # generic function type




def debug(*, enabled: bool = False) -> Callable[[F], F]:
    import functools
    ''' Decorator that enables or disables debug prints inside the wrapped function. '''

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            if not hasattr(_debug_stack, 'state'):
                _debug_stack.nest = [] # init debug state if missing

            _debug_stack.nest.append(enabled) # push current function's debug flag

            if enabled:
                print(f'\n{__COLORS.get(_HEADING)}[START] {__COLORS[_RESET]}')
                print(f'{__COLORS.get(_DEBUG)}[DEBUG] {__COLORS["reset"]}' + 
                      f'{__COLORS.get(_UPDATE)}Calling "{func.__name__}"...{__COLORS.get(_RESET)}')
            
            try:
                result = func(*args, **kwargs)  # call actual function so behavior is as intended
            finally:
                _debug_stack.nest.pop()
            
            if enabled:
                print(f'{__COLORS.get(_DEBUG)}[DEBUG] {__COLORS[_RESET]}' + 
                      f'{__COLORS.get(_UPDATE)}Function "{func.__name__}" exited...{__COLORS.get(_RESET)}')
                print(f'{__COLORS.get(_HEADING)}[END] {__COLORS[_RESET]}\n')         
            
            return result  # make sure the function still behaves as intended
        return wrapper # return wrapped function
    return decorator  # returns the decorator
