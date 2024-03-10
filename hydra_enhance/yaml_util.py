from dataclasses import dataclass, field
import warnings
import re


@dataclass
class LineInfo:
    if_comment: bool
    num_space: int
    key: str
    val: str


def parse_line(line: str):
    # regex pattern

    # TODO, refine the regex pattern
    # standard pattern: ␣␣key␣:␣!!type␣␣value␣#comment
    # ignore type hint: ␣␣key␣:␣value␣#comment
    # yaml tag is not welcome, check this one:
    # https://stackoverflow.com/questions/63672774/yaml-constructor-constructorerror-could-not-determine-a-constructor-for-the-tag
    # list item like: ␣␣-␣item␣ #comment is not considered since it's not possible for initialize a class
    # and it will be regarded as a comment line
    # TODO, limitation: key value in two lines is not considered
    #       e.g.:
    #         key:
    #           value
    pattern_comment = r'(^[ ]*#)|(^\s*$)'  # old pattern: r'^[ ]*#'
    # pattern_parse = r'^([ ]*)?(\S+?)[ ]*:[ ]+(\S+)?[ ]*(#.*)?$'
    pattern_parse = r'^([ ]*)?(\S+?)[ ]*:([ ]+\S+)?[ ]*(#.*)?$'
    pattern_list_item = r'^[ ]*-[ ]+\S+.*$'
    # groups: space?, key, value?, comment?
    # r'^([ ]*)([^:]+?)\s*:\s+([^#]+?)(?:\s*#.*)?$'  # r'^(?![ ]*#)([ ]*)(.+?):(.*)$'
    """
    note some strange yaml configuration, e.g, this is still valid but very strange
    t_list:  #!!seq
      -2
      -1
      - 3 !! sfdd
    """

    match_comment = re.search(pattern_comment, line)
    match_parse = re.search(pattern_parse, line)
    match_list_item = re.search(pattern_list_item, line)
    if match_comment or match_list_item:
        # return True, None, None, None
        if_comment, num_space, key, val = True, None, None, None
    elif match_parse:
        _i_space = match_parse.group(1)
        _i_num_space = len(_i_space)
        _i_key = match_parse.group(2)
        _i_val = match_parse.group(3)

        if _i_val:  # TODO, too verbose, improve the regex pattern try this one r"(?:\s+([^\s].{1,})|\s*)"
            val_pattern = r"[ ]+(\S*)?"
            match_val = re.search(val_pattern, _i_val)
            if match_val:
                _i_val = match_val.group(1)
            else:
                _i_val = ""
        if_comment, num_space, key, val = False, _i_num_space, _i_key, _i_val
    else:
        warnings.warn(f'unknown line format: {line}')
        # return True, None, None, None
        if_comment, num_space, key, val = True, None, None, None
    return LineInfo(if_comment, num_space, key, val)