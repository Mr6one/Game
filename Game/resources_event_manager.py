from resources_events import ResourceEvent


class ResourcesEventManager:
    def __init__(self):
        self.listeners = dict()
        for event in ResourceEvent:
            self.listeners[event] = list()

    def subscribe(self, event_type, new_listener):
        self.listeners[event_type].append(new_listener)

    def unsubscribe(self, event_type, del_listener):
        self.listeners[event_type].remove(del_listener)

    def notify(self, event_type, value):
        for listener in self.listeners[event_type]:
            listener.update(value)
