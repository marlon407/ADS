import random
import simpy
import itertools

list = [3,3,3,6,6, 12,12, 30, 22,44]
servidor1 = [12, 12, 11, 11, 10.8, 10, 12.2, 13]
servidor2 = [12, 12.2, 13,13.5, 11,2, 10.8, 10]

def processo(name, env):
    """A car arrives at the gas station for refueling.

    It requests one of the gas station's fuel pumps and tries to get the
    desired amount of gas from it. If the stations reservoir is
    depleted, the car has to wait for the tank truck to arrive.

    """
    print('%s arriving at the server at %.1f' % (name, env.now))
    yield env.timeout(random.choice(servidor1))
    print('%s leaving at the server at %.1f' % (name, env.now))

def process_generator(env):
    """Generate new cars that arrive at the gas station."""
    for i in itertools.count():
        yield env.timeout(random.choice(list))
        print('print')
        env.process(processo('Car %d' % i, env))

# Create environment and start processes
env = simpy.Environment()
env.process(process_generator(env))

# Execute!
env.run(until=100)