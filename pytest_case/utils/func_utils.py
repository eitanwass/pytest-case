from typing import Any, Callable, Dict, Tuple


def get_func_param_names(func: Callable[..., Any]) -> Tuple[str, ...]:
    """
    Extracts the names of positional parameters from the given function.

    :param func: A callable to analyze.
    :return: A tuple of strings where each string is the name of a positional parameter.
    """
    func_code = func.__code__
    func_arg_count = func_code.co_argcount
    return func_code.co_varnames[:func_arg_count]


def get_func_optional_params(func: Callable[..., Any]) -> Dict[str, Any]:
    """
    Extracts optional parameters from the given function.

    :param func: A callable to analyze.
    :return: A dictionary where the keys are the names of optional parameters and the values are their default values.
    """
    func_params = get_func_param_names(func)
    return dict(
        reversed(
            list(
                zip(
                    reversed(func_params),
                    reversed(func.__defaults__ or [])
                )
            )
        )
    )
