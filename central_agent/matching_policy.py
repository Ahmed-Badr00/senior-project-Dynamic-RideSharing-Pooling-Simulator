import numpy as np
from simulator.simulator import Simulator
from dummy_agent.agent import Dummy_Agent
from dispatch import DispatchPolicy
from matching import MatchingPolicy
from novelties import status_codes
from config.settings import ENTERING_TIME_BUFFER
from logger import sim_logger

class Experiment(object):
    def __init__(self, start_time, timestep):
        print("Initializing Experiment...")
        self.simulator = Simulator(start_time, timestep)
        self.dispatch_policy = DispatchPolicy()
        self.matching_policy = MatchingPolicy()
        self.agent = Dummy_Agent(self.dispatch_policy, self.matching_policy)
        self.last_vehicle_id = 1
        self.vehicle_queue = []

    def reset(self, start_time=None, timestep=None):
        self.simulator.reset(start_time, timestep)

    def populate_vehicles(self, vehicle_locations):
        n_vehicles = len(vehicle_locations)
        vehicle_ids = range(self.last_vehicle_id, self.last_vehicle_id + n_vehicles)
        self.last_vehicle_id += n_vehicles

        t = self.simulator.get_current_time()
        entering_time = np.random.uniform(t, t + ENTERING_TIME_BUFFER, n_vehicles).tolist()
        q = sorted(zip(entering_time, vehicle_ids, vehicle_locations))
        self.vehicle_queue = q

    def enter_market(self):
        t = self.simulator.get_current_time()
        while self.vehicle_queue:
            t_enter, vehicle_id, location = self.vehicle_queue[0]
            if t >= t_enter:
                self.vehicle_queue.pop(0)
                self.simulator.populate_vehicle(vehicle_id, location)
            else:
                break

    def step(self, verbose=False):
        self.enter_market()
        self.simulator.step()
        vehicles = self.simulator.get_vehicles_state()
        requests = self.simulator.get_new_requests()
        
        current_time = self.simulator.get_current_time()
        
        # Get dispatch commands
        d_commands = self.agent.get_dispatch_commands(current_time, vehicles)

        # Get matching commands
        m_commands = self.matching_policy.match(current_time, vehicles, requests)

        self.simulator.match_vehicles(m_commands, self.agent, self.agent)
        self.simulator.dispatch_vehicles(d_commands)

        net_v = vehicles[vehicles.status != status_codes.V_OFF_DUTY]
        if len(m_commands) > 0:
            average_wt = np.mean([command['duration'] for command in m_commands]).astype(int)
        else:
            average_wt = 0
            
        summary = "{:d}, {:d}, {:d}, {:d}, {:d}, {:d}, {:d}".format(
            current_time, len(net_v), len(net_v[net_v.status == status_codes.V_OCCUPIED]),
            len(requests), len(m_commands), len(d_commands), average_wt
        )
        sim_logger.log_summary(summary)

        if verbose:
            print("summary: ({})".format(summary), flush=True)

    def dry_run(self, n_steps):
        print("Starting dry run for {} steps.".format(n_steps))
        for step in range(n_steps):
            print("Step {}...".format(step + 1))
            self.step(verbose=True)

if __name__ == "__main__":
    experiment = Experiment(start_time=0, timestep=1)
    experiment.dry_run(n_steps=5)
