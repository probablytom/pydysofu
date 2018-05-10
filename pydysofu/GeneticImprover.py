from .fuzz_weaver import IncrementalImprover, identity, fuzz_function, get_reference_syntax_tree, copy_func
from .fuzz_weaver import record_generated_syntax_tree
from random import randint
from copy import deepcopy
import inspect


def choose_new_ranks(variant_1_rank, variant_2_rank, already_spliced):
    if already_spliced:
        variant_1_rank += 1

        if variant_1_rank == variant_2_rank:
            variant_1_rank = 1
            variant_2_rank += 1

    return variant_1_rank, variant_2_rank, not already_spliced


class GeneticImprover(IncrementalImprover):

    def __init__(self, variants_per_round, iterations_per_variant, success_metric_function, fuzzing_advice={}):
        super(GeneticImprover, self).__init__(variants_per_round,
                                              iterations_per_variant,
                                              success_metric_function,
                                              fuzzing_advice)

    @property
    def variants_to_splice(self):
        return self.variants_per_round / 2

    @property
    def variants_to_generate_through_fuzzing(self):
        return self.variants_per_round / 2 + self.variants_per_round % 2

    def construct_new_round(self, attribute, context):
        '''
        Constructs a new round of variants.
        :param attribute: The variant to base the next round of variants on.
        :param context: The context passed to the fuzzer
        '''

        current_round = {}

        # Some variables we may use later when splicing.
        # These are the rankings of two variants we'll splice together, by their previous success metric.
        variant_1_to_splice = 1
        variant_2_to_splice = 2
        already_spliced_pair = False

        # Iterate through a new round, and construct new variants to go in it.
        # If this is our *first* variant, add the unaltered target; sometimes original is best!
        # If not, add the best variant from the previous round.
        for i in range(self.variants_per_round):
            if i is 0:
                if self.invocation_count is 0:
                    current_round[attribute] = []
                else:
                    best_attr = self.best_attribute_in_last_round[0]
                    best_attr_copy = copy_func(best_attr)

                    new_advice = {best_attr_copy: self.fuzzing_advice.get(best_attr, identity)}
                    self.give_advice(new_advice)
                    current_round[best_attr] = []

                    relevant_syntax_tree = get_reference_syntax_tree(best_attr)
                    record_generated_syntax_tree(best_attr_copy, relevant_syntax_tree)

            # We're not adding the unaltered target, so generate and add a variant.
            else:

                # What kind of variant do we need to add?
                # If we have a history of past mutants, make by splicing previous ones.
                # Add some fuzzed variants either way.
                if len(self.variants) != 0 and i < self.variants_to_splice and False: # TODO: remove debug `False`!!!!!!!!!!!!!!!!!!!!!!!!!

                    # Splice two previous variants to make a new one.
                    variant_function_1 = self.nth_best_attribute_in_last_round(variant_1_to_splice)[0]
                    variant_function_2 = self.nth_best_attribute_in_last_round(variant_2_to_splice)[0]
                    variant_1_tree = get_reference_syntax_tree(variant_function_1)
                    variant_2_tree = get_reference_syntax_tree(variant_function_2)

                    new_variant_tree = deepcopy(variant_1_tree)
                    new_variant_tree.body[0].body = self.splice(variant_1_tree.body[0].body,
                                                                variant_2_tree.body[0].body)
                    variant_code = compile(new_variant_tree, '<spliced tree>', 'exec')

                    # A shell we'll inject new code into
                    if variant_function_1 != attribute:
                        variant = copy_func(variant_function_1)
                    else:
                        variant = copy_func(variant_function_2)

                    variant.func_code = variant_code.co_consts[0]
                    record_generated_syntax_tree(variant, new_variant_tree)

                    # We'll say this variant inherits its more successful ancestor's fuzzer.
                    # Shouldn't make a difference as they should all have used the same fuzzer, as of the current
                    # implementation.
                    fuzzer = self.fuzzing_advice.get(variant_function_1)
                    if inspect.ismethod(variant_function_1):
                        fuzzer = getattr(variant_function_1.im_class, variant_function_1.func_name)

                    self.give_advice({variant: fuzzer})

                    # We might need new variants to generate a splice from next time, rather than constantly
                    # choosing the same ones. Splice a pair twice, but then move on.

                    variant_1_to_splice, variant_2_to_splice, already_spliced_pair =\
                        choose_new_ranks(variant_1_to_splice, variant_2_to_splice, already_spliced_pair)

                    current_round[variant] = []

                else:

                    # Create a new variant via fuzzing!
                    # Ensure that advice key is unbound method for instance methods.
                    if inspect.ismethod(attribute):
                        reference_function = attribute.im_func
                        advice_key = getattr(attribute.im_class, attribute.func_name)
                    else:
                        reference_function, advice_key = attribute, attribute

                    fuzzer = self.fuzzing_advice.get(advice_key, identity)
                    variant = fuzz_function(reference_function, fuzzer, context)
                    get_reference_syntax_tree(variant)
                    self.give_advice({variant: fuzzer})
                    current_round[variant] = []

        self.variants.append(current_round)

    def splice(self, variant_1_steps, variant_2_steps):

        # Don't choose a point to splice that's longer than one tree
        splice_point_1 = randint(0, len(variant_1_steps))
        splice_point_2 = randint(0, len(variant_2_steps) - 1)

        return variant_1_steps[:splice_point_1] + variant_2_steps[splice_point_2:]
