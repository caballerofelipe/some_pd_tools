import io
import pprint
import re
import textwrap
from contextlib import redirect_stdout
from typing import Callable


def _sorted(obj):
    if isinstance(obj, dict):
        return sorted(obj.items(), key=lambda item: str(item[0]))
    if isinstance(obj, set) or isinstance(obj, list):
        return sorted(obj, key=lambda item: str(item))


def _fill(
    txt,
    initial_indent,
    subsequent_indent,
    width=100,
    expand_tabs=False,
    replace_whitespace=False,
    drop_whitespace=False,
):
    return textwrap.fill(
        txt,
        initial_indent=initial_indent,
        subsequent_indent=subsequent_indent,
        width=width,
        expand_tabs=expand_tabs,
        replace_whitespace=replace_whitespace,
        drop_whitespace=drop_whitespace,
    )


def _return_print_title(level: int, title: str, subtitle: str = None) -> None:
    to_return = '————————————————————' + '\n'
    title_ii = f'{"#" * level} '
    title_si = f'{" " * level} '
    to_return += _fill(title, initial_indent=title_ii, subsequent_indent=title_si) + '\n'
    if subtitle is not None:
        sub_ii = f'{" " * level} '
        subtitle_si = f'{" " * level} '
        to_return += (
            _fill(f'({subtitle})', initial_indent=sub_ii, subsequent_indent=subtitle_si) + '\n'
        )
    return to_return


def _return_print_result(result: str) -> None:
    return _fill(f'<<< {result} >>>', initial_indent='', subsequent_indent='    ') + '\n'


def _return_print_event(level: int, event: str) -> None:
    event_ii = f'{"  "*(level-1)}> '
    event_si = f'{"  "*(level-1)}  '
    return _fill(event, initial_indent=event_ii, subsequent_indent=event_si) + '\n'


def _return_print_plain(level: int, txt: str) -> None:
    level_str = '  ' * (level - 1)
    txt_ii = f'{level_str}  '
    txt_si = f'{level_str}  '
    return _fill(txt, initial_indent=txt_ii, subsequent_indent=txt_si) + '\n'


def _return_pprint(level: int, obj: object) -> None:
    level_str = f'{"  " * (level - 1)}  '
    _stream = io.StringIO()
    pprint.pprint(obj, indent=1, width=100 - len(level_str), compact=True, stream=_stream)
    to_print = level_str + _stream.getvalue()
    to_print = re.sub('\n.+', f'\n{level_str}', to_print)
    return to_print

def _fn_ret_and_output(fn: Callable, *args, **kwargs):
    stream = io.StringIO()
    with redirect_stdout(stream):
        returned = fn(*args, **kwargs)
    return returned, stream.getvalue()