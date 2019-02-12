from collections import defaultdict


class State:
    def __init__(self, game):
        self.game = game
        self.event_listeners = defaultdict(list)

    def draw(self, screen):
        pass

    def update(self):
        pass

    def poll_events(self, events):
        pass

    def on(self, event_name, listener):
        self.event_listeners[event_name].append(listener)

    def emit(self, event_name):
        for listener in self.event_listeners[event_name]:
            listener()
