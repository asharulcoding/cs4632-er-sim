import simpy

class LabImaging:
    def __init__(self, env, capacity):
        self.env = env
        self.resource = simpy.Resource(env, capacity=capacity)

    def process(self, env, rng):
        """Simulate lab/imaging work with random turnaround time."""
        # Assume average 30 min turnaround, exponential distribution
        yield env.timeout(rng.exponential(30))
