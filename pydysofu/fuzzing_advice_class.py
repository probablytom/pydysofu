'''
A class used to represent fuzzing advice that pydysofu can consume.
@author probablytom
'''
from core_fuzzers import identity


def do_nothing(args):
    '''
    For clarity with the callbacks, because 'pass' doesn't go into a lambda.
    '''
    pass


class FuzzingAdvice:
    '''
    A class to represent the advice given to pydysofu
    '''

    def __init__(self, fuzzer_dict, callback_dict):
        '''
        Construct a FuzzingAdvice.
        '''
        self.fuzzer_dict = fuzzer_dict
        self.callback_dict = callback_dict

        # Specify defaults
        self.default_fuzzer = identity
        self.default_callback = do_nothing

    def get_callback(self, func_id):
        '''
        Get the callback to be run after a given function.
        '''
        return self.callback_dict.get(func_id, self.default_fuzzer)

    def get_fuzzer(self, func_id):
        '''
        Returns a dictionary representing the fuzzing that'll take place.
        '''
        return self.fuzzer_dict.get(func_id, self.default_callback)

    def set_default_callback(self, new_default):
        '''
        Sets a new default callback to be run on any function.
        '''
        self.default_callback = new_default

    def set_default_fuzzing_behaviour(self, new_default):
        '''
        Sets a new default fuzzing behaviour to apply.
        '''
        self.default_fuzzer = new_default


# Advice representing the identity for both callbacks and for fuzzing.
identity_advice = FuzzingAdvice(fuzzer_dict={}, callback_dict={})
