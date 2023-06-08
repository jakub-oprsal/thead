from textwrap import indent as textwrap_indent
import re
import codecs


def indent(lines):
    return textwrap_indent(lines, "  ")


def render_command(command, a, b="", end="\n"):
    atr = f"[{b}]" if b != "" else ""
    return f"\\{command}{atr}{{{a}}}{end}"


def render_env(envname, content):
    return (
        render_command("begin", envname)
        + f"{indent(content)}\n"
        + render_command("end", envname)
    )


def join_and(strs):
    list_strs = list(strs)
    if len(list_strs) == 1:
        return list_strs[0]
    elif len(list_strs) == 2:
        return " and ".join(list_strs)
    else:
        return ", and ".join((", ".join(list_strs[:-1]), list_strs[-1]))


def short_name(name):
    names = name.split(" ")
    initials = ".".join(map(lambda x: x[0], names[:-1]))
    return initials + ". " + names[-1]


def include(filename, end="", soft=False):
    if soft is False:
        if not re.match(r".*\.[a-zA-Z0-9]+", filename):
            filename += ".tex"
        with codecs.open(filename, encoding="utf-8") as file:
            return file.read().strip() + "\n" + end
    elif soft is True:
        return f"\\input{{{filename}}}\n" + end
    else:
        raise ValueError("The argument `soft` is neither True nor False!")
