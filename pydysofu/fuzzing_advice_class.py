'''
A class used to represent fuzzing advice that pydysofu can consume.
@author probablytom
'''
from core_fuzzers import identity
from abc import ABCMeta, abstractmethod


class Advice(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        self.fuzzing_advice = self.fuzzer(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        '''
        Implemented so the class instance is `callable()` and can be
        executed as if it was a traditional-style fuzzer.
        '''
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
            return advice_func(*args, **kwargs)

    return AutomaticallyGeneratedAdvice() ## A (callable!) instance of the class
