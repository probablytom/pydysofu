'''
A class used to represent fuzzing advice that pydysofu can consume.
@author probablytom
'''
from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass


class Advice:
    ''' A class which operates like a callable
    fuzzer from pydysofu. It can have internally held state (because it's just
    an object!) The fuzzer method represents the behaviour the advice
    represents.
    TODO: extend this out to a full aspect oriented modelling
    framework. (Right now it's tied into fuzzing a bit...)
    '''

    def __call__(self, *args, **kwargs):
        '''
        Boilerplate to run the fuzzer like it an instance of this class
        *actually is just this function*.

        Implemented so the class instance is `callable()` and can be
        executed as if it was a traditional-style fuzzer.
        '''
        self.fuzzer(*args, **kwargs)

    def fuzzer(self, *args, **kwargs):
        '''
        The fuzzer function to implement by subclasses of this fuzzer class.
        '''
        pass


class FeedbackAdvice:
    '''
    Sometimes, like in the case of genetic algorithms, we need to implement
    advice which has both fuzzing capabilities and a callback to catch the
    result of the fuzzing!
    FeedbackAdvice is a class to implement this.
    '''

    def fuzzer(self, *args, **kwargs):
        '''
        Fuzzers like the regular Advice class has (because this subclasses it)
        '''
        super(FeedbackAdvice, self).fuzzer(self, *args, **kwargs)

    def callback(self, result):
        '''
        The callback that'll be fed the result of the fuzzed function.
        '''
        pass


class CallbackAdvice:
    def fuzzer(self, steps, context):
        '''
        The associated fuzzer is just the identity.
        '''
        return steps

    def callback(self, result):
        '''
        This still needs to be implemented by the subclass!
        '''
        pass

    def __call__(self, *args, **kwargs):
        '''
        Instead of running the identity fuzzer when in instance of this
        is treated as a function, run the callback instead.
        TODO: is this really the behaviour we want?
        '''
        self.callback(*args, **kwargs)


def advice(advice_func):
    '''
    Decorator that makes a callable Advice instance from a traditional-style
    advice function
    '''

    class AutomaticallyGeneratedAdvice(Advice):
        def fuzzer(self, *args, **kwargs):
            return advice_func(*args, **kwargs)

    return AutomaticallyGeneratedAdvice()  # A (callable) instance of the class
