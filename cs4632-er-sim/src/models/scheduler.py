import simpy

class StaffScheduler:
    def __init__(self, env, default_capacity, schedule):
        self.env = env
        self.schedule = schedule
        self.current_capacity = default_capacity

        # initialize with default capacity, not 0
        self.resource = simpy.Resource(env, capacity=default_capacity)

        env.process(self.run_schedule())

    def run_schedule(self):
        for start, end, cap in self.schedule:
            yield self.env.timeout(start - self.env.now)
            # replace resource with new capacity
            self.resource = simpy.Resource(self.env, capacity=cap)
            self.current_capacity = cap
