from functools import wraps
import types
import logging

class InvalidTransition(Exception):
    pass

class Event(object):
    pass


class State(object):

    def __init__(self):
        pass

class Transition(object):

    def __init__(self, froms, input=None):
        self.froms = froms
        self.input = input

    def __call__(self, fun):
        @wraps(fun)
        def wrapper(state_machine, event):
            if not isinstance(event, self.input):
                raise InvalidTransition("This transition needs an %s, got %s"\
                        % (self.input, event))
            state = state_machine.state
            if not state in self.froms:
                raise InvalidTransition(
                        "This transition cannot happen from the state %s"
                            % state)
            return fun(state_machine, event)
        wrapper._transition = self
        return wrapper

class StateMachine(type):

    transitions = {}

    def __new__(metacls, name, bases, dct):
        transitions = dct.setdefault('transitions', {})
        for slot in dct.values():
            if type(slot) is types.FunctionType and hasattr(slot, "_transition"):
                transitions[slot._transition] = slot
        state_property = dct.setdefault("state", metacls.__dict__['state'])
        for attr in ('getter', 'setter'):
            if not hasattr(state_property, attr):
                state_property = metcls.state.__dict__[attr]
        dct['feed'] = metacls.__dict__['feed']
        dct['watchers'] = metacls.__dict__['watchers']
        instance = super(StateMachine, metacls).__new__(metacls, name, bases, dct)
        instance._state = None
        old_init = instance.__init__
        def new_init(self, *args, **kwargs):
            self._watchers = []
            old_init(self, *args, **kwargs)
        instance.__init__ = new_init
        return instance

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        assert value is not None , "Can't set the state to value None"
        old_value = self._state
        self._state = value
        for watcher in self.watchers:
            watcher(self, **dict(old_state=old_value))

    @property
    def watchers(self):
        return self._watchers

    @watchers.setter
    def watchers(self, value):
        self._watchers = value

    def feed(self, event):
        to_call = None
        for transition, fun in self.transitions.items():
            if self.state in transition.froms\
                    and isinstance(event, transition.input):
                if to_call is not None:
                    raise InvalidTransition("Multiple matching transition from %s with %s" % (self.state, event))
                to_call = fun
        if to_call is None:
            raise InvalidTransition("Cannot find a matching transition from %s with %s" % (self.state, event))
        to_call(self, event)
