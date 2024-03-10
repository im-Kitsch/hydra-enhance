import difflib
import os
import argparse
import glob
import re
import warnings
from dataclasses import dataclass, field
import inspect

from .yaml_util import parse_line
from .hydra_locate import _locate


class YamlStatistical:
    def __init__(self, original_lines: list):
        self.original_lines = original_lines
        self.statistical = []
        self.cls_target_indexes = []
        for idx, _line in enumerate(original_lines):
            _line = parse_line(_line)
            self.statistical.append(_line)
            if _line.key == '_target_':
                self.cls_target_indexes.append(idx)
        return

    # TODO, delete old attribute line maybe in the future
    def search_friend_keys(self, line_idx):
        current_level = self.statistical[line_idx].num_space

        keys, indexes = [], []
        for i in range(line_idx-1, -1, -1):
            _line_info = self.statistical[i]
            if not _line_info.if_comment and (_line_info.num_space == current_level):
                keys.append(_line_info.key)
                indexes.append(i)
            elif not _line_info.if_comment and (_line_info.num_space < current_level):
                break

        for i in range(line_idx+1, len(self.original_lines)):
            _line_info = self.statistical[i]
            if not _line_info.if_comment and (_line_info.num_space == current_level):
                keys.append(_line_info.key)
                indexes.append(i)
            elif not _line_info.if_comment and (_line_info.num_space < current_level):
                break
        return indexes, keys


# ignore comment line
# TODO, if_hide_default is not implemented yet
def populate_file(file_path: str, if_hide_default: bool):
    assert file_path.endswith('.yaml')
    with open(file_path, 'r') as f:
        lines = f.readlines()

    yaml_stat = YamlStatistical(lines)
    to_delete_indexes = []
    to_append_indexes = []
    to_append_lines = []
    for _i in yaml_stat.cls_target_indexes:
        _line_info = yaml_stat.statistical[_i]
        if not _line_info.if_comment and _line_info.key == '_target_':
            # FIXME, here if key is initialized as "xx.xxx" will cause problem since " is not  removed
            signature = inspect.signature(_locate(_line_info.val))
            indexes, friend_keys = yaml_stat.search_friend_keys(line_idx=_i)

            _i_append_lines = []

            for _i_ind, _i_key in zip(indexes, friend_keys):
                if _i_key in signature.parameters:
                    pass
                else:
                    if _i_key not in ['_args_', '_convert_', '_partial_', '_recursive_']:
                        to_delete_indexes.append(_i_ind)

            for _i_key, _i_val in signature.parameters.items():
                if (_i_key in friend_keys) or (_i_key == "kwargs"):  # kwargs will not be considered
                    pass
                else:
                    default_val = _i_val.default if _i_val.default != inspect.Parameter.empty else "???"
                    if _i_key == "args":
                        if default_val == "???":
                            default_val = "[]"
                        _i_append_lines.append(f'{_line_info.num_space * " "}_args_: {default_val}\n')
                    else:
                        _i_append_lines.append(f'{_line_info.num_space * " "}{_i_key}: {default_val}\n')

            to_append_indexes.append(_i)
            to_append_lines.append(_i_append_lines)

    new_lines = []
    for _i, _line in enumerate(lines):
        if _i in to_delete_indexes:
            pass
        else:
            new_lines.append(_line)
            if _i in to_append_indexes:
                new_lines.extend(to_append_lines[to_append_indexes.index(_i)])

    # compare the new_lines with the original lines
    diff = difflib.unified_diff(lines, new_lines, fromfile='original', tofile='new')
    print('difference between original and new file')
    print("".join(diff))
    user_input = input("Do you want to proceed? (y/n): ")
    if user_input.lower() == 'y':
        # overwrite the file
        with open(file_path, 'w') as f:
            f.writelines(new_lines)
    else:
        # no change
        pass

    return

    # n_lines = len(lines)
    # new_file = []
    # for i in range(n_lines):
    #     if_comment, num_space, key, val = yaml_stat.statistical[i]
    #     if not if_comment and key == '_target_':
    #         # TODO, add support for delete old parameter that is not used anymore and support **kwargs *args
    #         #       add support for _partial_
    #         keys, _ = yaml_stat.search_friend_keys(line_idx=i)
    #
    #         target_callable = _locate(val)
    #         signature = inspect.signature(target_callable)
    #
    #         for _i_key in keys:
    #             if _i_key == '_target_':
    #                 continue
    #             elif _i_key in signature.parameters:
    #                 new_file.append(f'{num_space * " "}{_i_key}: {signature.parameters[_i_key].default}\n')
    #
    #     else:
    #         new_file.append(lines[i])



# def auto_populate(path: str, if_hide_default: bool):
#     # justify is path is file path or directory path
#     if os.path.isfile(path):
#         _populate_file(path, if_hide_default=if_hide_default)
#     elif os.path.isdir(path):
#         # yaml_files = glob.glob('**/*.yaml', recursive=True)
#         # for f_path in yaml_files:
#         #     _populate_file(f_path, if_hide_default=if_hide_default)
#         pass
#
#     return



