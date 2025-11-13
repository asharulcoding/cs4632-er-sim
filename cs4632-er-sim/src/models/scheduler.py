import simpy

class StaffScheduler:
    def __init__(self, env, default_capacity, schedule):
        self.env = env
        self.schedule = schedule
        self.current_capacity = max(1, default_capacity)

        # initialize with safe default capacity
        self.resource = simpy.Resource(env, capacity=self.current_capacity)

        env.process(self.run_schedule())

    def run_schedule(self):
        for start, end, cap in self.schedule:
            if start > 0:  # skip the initial setup at time 0
                # Wait until the scheduled change time
                yield self.env.timeout(start - self.env.now)

                # Prevent SimPy from ever getting cap = 0
                safe_cap = max(1, cap)

                print(f"[Scheduler] At time {self.env.now}, capacity set to {safe_cap}")

                # Update the resource with safe capacity
                self.resource = simpy.Resource(self.env, capacity=safe_cap)
                self.current_capacity = safe_cap
