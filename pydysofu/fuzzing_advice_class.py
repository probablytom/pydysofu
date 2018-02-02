'''
A class used to represent fuzzing advice that pydysofu can consume.
@author probablytom
'''
from core_fuzzers import identity
from abc import ABCMeta, abstractmethod

# def do_nothing(args):
#     '''
#     For clarity with the callbacks, because 'pass' doesn't go into a lambda.
#     '''
#     pass


class Advice(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        self.fuzzing_advice = self.fuzzer(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.fuzzing_advice(*args, **kwargs)

    @abstractmethod
    def fuzzer(self, *args, **kwargs):
        pass


class FeedbackAdvice(metaclass=Advice):
    @abstractmethod
    def fuzzer(self, *args, **kwargs):
        super(FeedbackAdvice, self).fuzzer(*args, **kwargs)

    @abstractmethod
    def callback(self, result):
        pass


def advice(advice_func):
    '''
    Decorator that makes a callable Advice instance from a traditional-style
    advice function
    '''

    class AutomaticallyGeneratedAdvice(Advice):
        def fuzzer(self, *args, **kwargs):
            advice_func(*args, **kwargs)
