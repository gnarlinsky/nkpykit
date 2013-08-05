#!/usr/bin/env python

"""
Various useful decorators.
"""

from termcolor import colored
import inspect

class callinfo(object):
    """ Keep track of and print call information, including call counts and
    argument names and values.

    Some of the call counting code is based on the 'Alternate counting function
    calls' decorator at
    http://wiki.python.org/moin/PythonDecoratorLibrary#Counting_function_calls

    Note: one reason to use a class (rather than a function) decorator here is
    because we need to maintain state for the call counts. """

    # Keep track of the decorated/registered functions
    __instances = {}

    def __init__(self, func):
        """ Initialize, set num calls to zero """
        self.__func = func
        self.__numcalls = 0
        callinfo.__instances[func] = self

    def __call__(self, *args, **kwargs):
        """ Update call count; print call counts and argument names and values """

        #######################################################################
        # Update call count and build call info string
        #######################################################################
        self.__numcalls += 1
        call_info = "{0}(): call #{1}".format(self.__func.__name__,
                                              self.__numcalls)

        #######################################################################
        # Gather information for building call count and arg names/values info
        #######################################################################
        all_arg_names, _, _, default_arg_vals = inspect.getargspec(self.__func)

        # Determine number of required arguments by subtracting number of
        # keyword arguments from total argument count. Note: to determine the
        # number of keyword arguments, we won't count the number
        # of items in kwargs dict because it may be empty if no keyword
        # arugments were explicitly specified; so counting the number of
        # *default* arguments.
        try:  # in case default_arg_vals is actually None
            num_just_pos_args = len(all_arg_names) - len(default_arg_vals)
        except:
            num_just_pos_args = len(all_arg_names)

        # Create a dictionary of default arg values, because otherwise things
        # are going to get very confusing if only some keyword args were
        # specified (i.e. when building argument name/value information, may
        # need to refer to either default keyword argument values or explicitly
        # specified keyword argument values).
        just_keyword_arg_names = all_arg_names[num_just_pos_args:]
        karg_defaults_dict = {}
        for i in range(len(just_keyword_arg_names)):
            karg_name = just_keyword_arg_names[i]
            karg_default_val = default_arg_vals[i]
            karg_defaults_dict[karg_name] = karg_default_val

        #######################################################################
        # Build argument name/value info
        #######################################################################
        arg_info = ''
        # positional args
        just_pos_args = all_arg_names[:num_just_pos_args]
        for i in range(num_just_pos_args):
            arg_info = '{0}{1} = {2}, '.format(arg_info,
                                               just_pos_args[i],
                                               args[i])
        # keyword args
        for karg_name in just_keyword_arg_names:
            if karg_name in kwargs:
                arg_info = '{0}{1} = {2}, '.format(arg_info,
                                                   karg_name,
                                                   kwargs[karg_name])
            # no explicit keyword arguments passed in, so get the defaults
            else:
                arg_info = '{0}{1} = {2}, '.format(arg_info,
                                                   karg_name,
                                                   karg_defaults_dict[karg_name])

        #######################################################################
        # Print call count info and argument names with current values
        #######################################################################
        print colored(call_info, 'red'), colored('( {})'.format(arg_info), 'blue')

        #######################################################################
        # Return decorated function
        #######################################################################
        return self.__func(*args, **kwargs)

    def count(self):
        """ Return the number of times the particular function was called. """
        return callinfo.__instances[self.__func].__numcalls

    def reset_count(self):
       """ Reset the count number for this function to zero. """
       self.__numcalls = 0

    @staticmethod
    def all_counts():
        """ Return dict mapping each registered function to the number of times 
        it was called. """
        # create {function: # of calls} dict
        all_counts_dict = {}
        for func in callinfo.__instances:
            all_counts_dict[func.__name__] = callinfo.__instances[func].__numcalls
        return all_counts_dict

    @staticmethod
    def reset_all_counts():
        """ Reset counts for all registered functions to zero. """
        for func in callinfo.__instances:
            callinfo.__instances[func].__numcalls = 0

    @staticmethod
    def all_func():
        """ Return list of all registered/decorated functions. """
        return callinfo.__instances
