import simpy

class StaffScheduler:
    def __init__(self, env, default_capacity, schedule):
        self.env = env
        self.schedule = schedule
        self.current_capacity = default_capacity

        # initialize with default capacity
        self.resource = simpy.Resource(env, capacity=default_capacity)

        env.process(self.run_schedule())

    def run_schedule(self):
        for start, end, cap in self.schedule:
            if start > 0:  # skip the initial setup at time 0
                yield self.env.timeout(start - self.env.now)
                print(f"[Scheduler] At time {self.env.now}, capacity set to {cap}")
                self.resource = simpy.Resource(self.env, capacity=cap)
                self.current_capacity = cap
