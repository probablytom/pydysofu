'''
Utility functions which can be imported by all other modules
without incurring circular import errors
'''

import inspect
import ast

_reference_syntax_trees = dict()


def get_reference_syntax_tree(func):
    if func not in _reference_syntax_trees:
        func_source_lines = inspect.getsourcelines(func)[0]

        global_indentation = len(func_source_lines[0]) - len(func_source_lines[0].strip())
        for i in range(len(func_source_lines)):
            func_source_lines[i] = func_source_lines[i][global_indentation - 1:]

        func_source = ''.join(func_source_lines)
        _reference_syntax_trees[func] = ast.parse(func_source)

    return _reference_syntax_trees[func]

