# PyDySoFu - Python Dynamic Source Fuzzer

## Contributors

* Tom Wallis<br/>
  School of Computing Science, University of Glasgow<br/>
  GitHub ID: probablytom
  [twallisgm@googlemail.com](mailto:twallisgm@googlemail.com)

* Tim Storer<br/>
  School of Computing Science, University of Glasgow<br/>
  GitHub ID: twsswt
  [timothy.storer@glagow.ac.uk](mailto:timothy.storer@glagow.ac.uk)

## Overview

PyDySoFu is a library for performing source code fuzzing of Python programs at runtime. Fuzzing operations are
implemented in an extensible library of fuzzers.  The fuzzers can be applied to functions in in two ways:

* By constructing an Aspect Oriented Programming like advice dictionary, mapping function pointers to fuzzers
 (recommended).

* By decorating fuzzable operations with an <code>@fuzz</code> decorator, parameterised with the desired fuzzer.

The AOP approach is preferred because this separates concerns between the implementation of reference functions and the
specification of fuzzers, allowing many different fuzzings of the same program to be constructed.

Each fuzzing operator is a function that accepts the body of a work flow function (as a list of statements) and returns
a fuzzed list of statements.

## Available Fuzzers

The core library includes both atomic and composite fuzzers for building more complex behaviours:

* Identity
* Applying a fuzzer to a subset of function body steps using a filter.  Filters provided include:
 * Identity
 * Random selection
  * n last steps
  * Excluding control structures
  * Inverting a selection
* Removing steps
* Duplicating steps
* Shuffling steps
* Applying a sequence of fuzz operators
* Choosing a random fuzz operator to apply from a probability distribution.
* Applying a fuzz operator conditionally.
* Replacing the iterable of a foreach loop
* Replacing a condition expression
* Recursing into composite steps
* Swapping if blocks

A number of demonstrator fuzzers are also provided:

* Remove last step(s)
* Duplicate last step
* Remove random step


## Tutorial

###Basic usage

Consider the following Python class representing a collection of simple workflow descriptions defined in a separate
source file.

    class TutorialWorkflow(object):
        def __init__(self):
            self.environment = list()

        def an_activity(self):
            self.environment.append(1)
            self.environment.append(2)
            self.environment.append(3)

We can fuzz the workflow to have a randomly chosen removed line as follows.

    from fuzzi_moss import *
    from tutorial import TutorialWorkflow

    advice = {
        TutorialWorkflow.an_activity: remove_random_step
    }
    fuzz_clazz(ExampleWorkflow, advice)

The advice dictionary maps the function pointer to the remove_random_step fuzzer.  The fuzz_clazz operation then applies
this advice to the whole ExampleWorkflow class.

Now we can use the fuzzed class as normal.

    workflow = ExampleWorkflow()
    workflow.activity()
    print workflow.environment
    workflow.activity()
    print workflow.environment

Output:

Note that the fuzzer will be re-applied each time the fuzzed function is called meaning that in this case a different
step can be removed from the workflow on each invocation.
