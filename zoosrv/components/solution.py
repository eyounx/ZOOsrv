"""
This module contains the class Solution.

Author:
    Yu-Ren Liu
"""

from zoosrv.components.zoo_global import pos_inf, neg_inf, nan, gl
from zoosrv.components.tool_function import ToolFunction


class Solution:
    """
    A solution encapsulates a solution vector with attached properties, including dimension information, objective value,
and attachment
    """
    def __init__(self, x=[], value=nan, resample_value=None, attach=None, post_attach=None, is_in_possible_solution=False):
        """
        Initialization.

        :param x: a list
        :param value: objective value
        :param resample_value: reevaluated value
        :param attach: attached structure
        :param post_attach:
        :param is_in_possible_solution:
        """
        self.__x = x
        self.__value = value
        self.__resample_value = resample_value
        self.__attach = attach
        self.__post_attach = post_attach
        self.__is_in_possible_solution = is_in_possible_solution
        return

    @property
    def is_in_possible_solution(self):
        return self.__is_in_possible_solution

    @is_in_possible_solution.setter
    def is_in_possible_solution(self, value):
        self.__is_in_possible_solution = value

    def deep_copy(self):
        """
        Deep copy this solution. Note that the attachment is not deeply copied
        :return: a new solution
        """

        x = []
        for x_i in self.__x:
            x.append(x_i)
        value = self.__value
        attach = self.__attach
        resample_value = self.__resample_value
        post_attach = self.__post_attach
        return Solution(x, value, resample_value, attach, post_attach, self.is_in_possible_solution)

    def is_equal(self, sol):
        """
        Check if two solutions equal

        :param sol: another solution
        :return: True or False
        """
        sol_x = sol.get_x()
        sol_value = sol.get_value()
        if sol_value != nan and self.__value != nan:
            if abs(self.__value - sol_value) > gl.precision:
                return False
        if len(self.__x) != len(sol_x):
            return False
        for i in range(len(self.__x)):
            if abs(self.__x[i] - sol_x[i]) > gl.precision:
                return False
        return True

    def exist_equal(self, sol_set):
        """
        Check if exists another solution in sol_set the same as this one

        :param sol_set: solution set
        :return: True or False
        """
        for sol in sol_set:
            if self.is_equal(self, sol):
                return True
        return False

    def set_x_index(self, index, x):
        self.__x[index] = x
        return

    def set_x(self, x):
        self.__x = x
        return

    def set_value(self, value):
        self.__value = value
        return

    def set_attach(self, attach):
        self.__attach = attach
        return

    def set_post_attach(self, attach):
        self.__post_attach = attach
        return

    def set_resample_value(self, resample_value):
        self.__resample_value = resample_value

    def get_resample_value(self):
        return self.__resample_value

    def get_post_attach(self):
        return self.__post_attach

    def get_x_index(self, index):
        return self.__x[index]

    def get_x(self):
        return self.__x

    def get_value(self):
        return self.__value

    def get_attach(self):
        return self.__attach

    def print_solution(self):
        ToolFunction.log('x: ' + repr(self.__x))
        ToolFunction.log('value: ' + repr(self.__value))

    @staticmethod
    def deep_copy_set(sol_set):
        """
        Deep copy an solution set

        :param sol_set: solution set
        :return: copied solution set
        """
        result_set = []
        for sol in sol_set:
            result_set.append(sol.deep_copy())
        return result_set

    @staticmethod
    def print_solution_set(sol_set):
        """
        Print the value of each solution in an solution set.

        :param sol_set: solution set
        :return: no return
        """
        for sol in sol_set:
            ToolFunction.log('value: %f' % (sol.get_value()))
        return

    @staticmethod
    def find_maximum(sol_set):
        """
        Find the solution having maximum value from the solution set

        :param sol_set: solution set
        :return: solution, index
        """
        maxi = neg_inf
        max_index = 0
        for i in range(len(sol_set)):
            if sol_set[i].get_value() > maxi:
                maxi = sol_set[i].get_value()
                max_index = i
        return sol_set[max_index], max_index

    @staticmethod
    def find_minimum(sol_set):
        """
        Find the solution having minimum value from the solution set

        :param sol_set: solution set
        :return: solution, index
        """
        mini = pos_inf
        mini_index = 0
        for i in range(len(sol_set)):
            if sol_set[i].get_value() < mini:
                mini = sol_set[i].get_value()
                mini_index = i
        return mini, mini_index
