class StateMachine:
    def __init__(self, start_state):
        self.current_state = start_state
        self.current_state.enter()
        pass

    def update(self):
        next_stage = self.current_state.exit()
        if next_stage:
            self.current_state = next_stage
        self.current_state.enter()
        pass

    def draw(self):
        self.current_state.draw()
        pass
