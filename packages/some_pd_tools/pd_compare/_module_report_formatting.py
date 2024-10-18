import io
import pprint
import re
import textwrap


def fill(
    txt,
    initial_indent: str,
    subsequent_indent: str,
    width: int = 100,
    expand_tabs: bool = False,
    replace_whitespace: bool = False,
    drop_whitespace: bool = False,
) -> None:
    '''A wrapper for `textwrap.fill` with predefined options.'''
    return textwrap.fill(
        txt,
        initial_indent=initial_indent,
        subsequent_indent=subsequent_indent,
        width=width,
        expand_tabs=expand_tabs,
        replace_whitespace=replace_whitespace,
        drop_whitespace=drop_whitespace,
    )


def print_title(
    level: int,
    title: str,
    subtitle: str = None,
    file: io.StringIO = None,
) -> None:
    """Print a title for the report.

    Parameters
    ----------
    level : int
        Indentation level, 1 is the initial level.
    title : str
        The title.
    subtitle : str, optional
        A subtitle, by default None.
    file : io.StringIO, optional
        Same as in `print()`, by default None.
    """
    print('————————————————————', file=file)
    title_ii = f'{"#" * level} '
    title_si = f'{" " * level} '
    print(fill(title, initial_indent=title_ii, subsequent_indent=title_si), file=file)
    if subtitle is not None:
        sub_ii = f'{" " * level} '
        subtitle_si = f'{" " * level} '
        print(
            fill(f'({subtitle})', initial_indent=sub_ii, subsequent_indent=subtitle_si), file=file
        )


def return_result(result: str) -> None:
    '''Return the result string, useful to have the result always printed in the same way.'''
    return f'<<< {result} >>>'


def print_result(
    result: str,
    file: io.StringIO = None,
) -> None:
    """Print a result.

    Parameters
    ----------
    result : str
        The result's text.
    file : io.StringIO, optional
        Same as in `print()`, by default None.
    """
    print(
        fill(return_result(result=result), initial_indent='', subsequent_indent='    '),
        file=file,
    )


def print_event(
    level: int,
    event: str,
    file: io.StringIO = None,
) -> None:
    """Print an event.

    Parameters
    ----------
    level : int
        Indentation level, 1 is the initial level.
    event : str
        The event.
    file : io.StringIO, optional
        Same as in `print()`, by default None.
    """
    event_ii = f'{"  "*(level-1)}> '
    event_si = f'{"  "*(level-1)}  '
    print(
        fill(event, initial_indent=event_ii, subsequent_indent=event_si),
        file=file,
    )


def print_plain(
    level: int,
    txt: str,
    file: io.StringIO = None,
) -> None:
    """Print plain text with an indentation level.

    Parameters
    ----------
    level : int
        Indentation level, 1 is the initial level.
    txt : str
        The text.
    file : io.StringIO, optional
        Same as in `print()`, by default None.
    """
    level_str = '  ' * (level - 1)
    txt_ii = f'{level_str}  '
    txt_si = f'{level_str}  '
    print(fill(txt, initial_indent=txt_ii, subsequent_indent=txt_si), file=file)


def pprint_wrap(level: int, obj: object, stream: io.StringIO = None) -> None:
    """A `pprint.pprint()` wrapper to add indentation.

    Parameters
    ----------
    level : int
        Indentation level, 1 is the initial level.
    obj : object
        The object.
    stream : io.StringIO, optional
        Same as in `pprint.pprint()`, by default None.
    """
    level_str = f'{"  " * (level - 1)}  '
    _stream = io.StringIO()
    pprint.pprint(obj, indent=1, width=100 - len(level_str), compact=True, stream=_stream)
    to_print = level_str + _stream.getvalue()
    to_print = re.sub('\n(.+)', f'\n{level_str}\\1', to_print)
    print(to_print, end='', file=stream)
