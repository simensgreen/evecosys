from dataclasses import dataclass


@dataclass(frozen=True)
class System:
    """
    System representation
    """
    func: callable
    query: tuple

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)


class EventPool:
    """
    A place where events accumulate
    """
    def __init__(self):
        self.__counter = 0
        # stores type of component and set of associated events
        # Example:
        # {Type: {1, 2, 3}, WindowSize: {2}, Position: {3}, KeyPress: {1}}
        # if I want to get a set of events with a set of components,
        # I just need to get the intersection of the corresponding sets
        self.components = dict()
        # stores dict of events and components with their values
        # {1: {Type: Type(something), KeyPress: KeyPress(32)}, 2: ...}
        self.pool = dict()

    def add(self, *components):
        event_id = self.next_id
        self.pool[event_id] = {type(component): component for component in components}
        for component in components:
            component_type = type(component)
            if component_type in self.components:
                self.components[component_type].add(event_id)
            else:
                self.components[component_type] = {event_id}

    def request(self, query):
        events = set(self.pool.keys())
        for _, component in query:
            events.intersection_update(self.components.get(component, set()))
        if events:
            return {key: tuple(self.pool[event][component] for event in sorted(events)) for key, component in query}
        else:
            return {}

    @property
    def next_id(self):
        tmp = self.__counter
        self.__counter += 1
        return tmp


class EventServer:
    """
    The class that manages the call of systems, the accumulation of events
    """
    def __init__(self):
        self.systems = []
        self.event_pool = EventPool()
        self.next_event_pool = EventPool()

    def register_system(self, system, **query):
        self.systems.append(System(system, tuple(query.items())))

    def tick(self):
        self.process_events()
        # after processing events drop current pool (lost relevance)
        self.event_pool = self.next_event_pool
        # pool update for future events
        self.next_event_pool = EventPool()

    def process_events(self):
        for system in self.systems:
            response = self.event_pool.request(system.query)
            # system call only if there are events that satisfy the system request
            if response:
                system(**response)

    def spawn(self, *components):
        """Adds an event to the execution queue (will be processed in the next tick)"""
        self.next_event_pool.add(*components)
