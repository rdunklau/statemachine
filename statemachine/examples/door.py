from statemachine import StateMachine, Transition, State, Event, InvalidTransition

class Opened(State):
    pass

class Closed(State):
    pass

class CloseEvent(Event):
    pass

class OpenEvent(Event):
    pass


class Door(object):

    states = [Opened, Closed]

    __metaclass__ = StateMachine

    def __init__(self, initialstate):
        self.state = initialstate

    @Transition(froms=[Opened], input=CloseEvent)
    def close(self, closeEvent):
        self.state = Closed


    @Transition(froms=[Closed], input=OpenEvent)
    def open(self, openEvent):
        self.state = Opened

if __name__ == '__main__':
    door = Door(Opened)
    door.close(CloseEvent())
    door.open(OpenEvent())
    try:
        door.open(OpenEvent())
    except InvalidTransition:
        print "Can't open an opened door!"
    try:
        door.close(OpenEvent())
    except InvalidTransition:
        print "Can't close a door by opening it!"
    door.feed(CloseEvent())
    try:
        door.feed(CloseEvent())
    except InvalidTransition:
        print "Can't close a closed door!"
