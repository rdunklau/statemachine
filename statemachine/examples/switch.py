from .. import  StateMachine, Event, Transition
from itertools import cycle

class SwitchEvent(Event):
    pass

class Switch():

    __metaclass__ = StateMachine

    def __init__(self, state):
        self.states = cycle([True, False])
        self.state = state


    @Transition(froms=[True, False], input=SwitchEvent)
    def switch(self, input=SwitchEvent()):
        self.state = self.states.next()


    def __call__(self):
        self.feed(SwitchEvent())


class Lamp():

    __metaclass__ = StateMachine

    def __init__(self, *switches):
        self.switches = switches
        for switch in switches:
            switch.watchers.append(self.on_state_change)

    @property
    def state(self):
        return all(switch.state == self.switches[0].state
                for switch in self.switches)


    def on_state_change(self, switch=None, old_state=None):
        print "The lamp is %s" % ("On" if self.state else "Off")

if __name__ == '__main__':
    switch1 = Switch(True)
    switch2 = Switch(False)
    lamp = Lamp(switch1, switch2)
    switch1()
    switch2()
    switch2()
    switch1()
    switch1()
