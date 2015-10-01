"""
Carwash example.

Covers:

- Waiting for other processes
- Resources: Resource

Scenario:
  A carwash has a limited number of washing machines and defines
  a washing processes that takes some (random) time.

  Car processes arrive at the carwash at a random time. If one washing
  machine is available, they start the washing process and wait for it
  to finish. If not, they wait until they an use one.

"""
import random
import simpy
import itertools

RANDOM_SEED = 42
NUM_SERVER = 2  # Number of machines in the carwash
SIM_TIME = 200     # Simulation time in minutes
servidorFree = 1
list = [3,3,3,6,6, 12,12, 30, 22,44]
#list = [4, 4, 4]
servidor1 = [12, 12, 11, 11, 10.8, 10, 12.2, 13]
servidor2 = [12, 12.2, 13,13.5, 11,2, 10.8, 10]


class Server(object):
    def __init__(self, env, num_servers):
        self.env = env
        self.machine = simpy.Resource(env, num_servers)
        self.serverTime = 1

    def do(self, process):
        yield self.env.timeout(self.serverTime)
        print("procss %s left." %process)


def processo(env, name, cw):
    """The car process (each car has a ``name``) arrives at the carwash
    (``cw``) and requests a cleaning machine.

    It then starts the washing process, waits for it to finish and
    leaves to never come back ...

    """
    print('%s arrives at the server at %.2f.' % (name, env.now))
    with cw.machine.request() as request:
        yield request
        global servidorFree

        if servidorFree:
            print("%s vou usar o servidor 1" % name)
            cw.serverTime = random.choice(servidor1)
            servidorFree = 0
        else:
            print("%s vou usar o servidor 2" % name)
            cw.serverTime = random.choice(servidor2)
            servidorFree = 1



        print('%s enters the server at %.2f.' % (name, env.now))
        yield env.process(cw.do(name))
        print('%s leaves the server at %.2f.' % (name, env.now))


def setup(env, nun_server):
    """Create a carwash, a number of initial cars and keep creating cars
    approx. every ``t_inter`` minutes."""
    # Create the environment
    ambiente = Server(env, nun_server)
    i = 0
    # Create more cars while the simulation is running
    servidor0Free = 1
    while True:
        yield env.timeout(random.choice(list))
        env.process(processo(env, 'process %d' % i, ambiente))
        i += 1

    
    


# Setup and start the simulation
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_SERVER))

# Execute!
env.run(until=SIM_TIME)
