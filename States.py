from Control import Control

class States(Control):
    def __init__(self):
        Control.__init__(self)
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
