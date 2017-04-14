# File name: config.py
# Author: Nupur Garg
# Date created: 4/13/2017
# Python Version: 3.5


from src.globals import *


class Config(object):

    def __init__(self):
        # Numerics for generating suggestions.
        self.min_diff_complexity_between_slices = None
        self.max_dist_between_grouped_linenos = None
        self.max_diff_ref_and_live_var_block = None

        # Numerics for validing suggestions.
        self.min_lines_in_suggestion = None
        self.min_variables_parameter_in_suggestion = None
        self.max_variables_parameter_in_suggestion = None
        self.max_variables_return_in_suggestion = None
        self.min_lines_func_not_in_suggestion = None
