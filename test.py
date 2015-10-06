import random
import simpy
import itertools

RANDOM_SEED = 42
NUM_SERVER = 2  # Number of machines in the carwash
SIM_TIME = 200     # Simulation time in minutes
servidorFree = 1
number_of_clients = 0
fila = []
time_in_line = []
time_in_server = []
clients_in_server_1 = 0
clients_in_server_2 = 0
#list = [3,3,3,6,6, 12,12, 30, 22,44]
list = [4, 4, 4]
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
    global fila
    global time_in_line
    global servidorFree
    global time_in_server
    global clients_in_server_2
    global clients_in_server_1
    fila.append(len(cw.machine.queue))

    print('%s arrives at the server at %.2f.' % (name, env.now))
    process_in_line = env.now
    with cw.machine.request() as request:
        yield request

        if servidorFree:
            print("%s vou usar o servidor 1" % name)
            cw.serverTime = random.choice(servidor1)
            servidorFree = 0
            clients_in_server_1 += 1
        else:
            print("%s vou usar o servidor 2" % name)
            cw.serverTime = random.choice(servidor2)
            clients_in_server_2 += 1
            servidorFree = 1

        print('%s enters the server at %.2f.' % (name, env.now))
        
        process_out_line = env.now
        time_in_line.append(process_out_line - process_in_line)
        #Process being processed
        yield env.process(cw.do(name))
        process_out_server = env.now
        time_in_server.append(process_out_server - process_in_line)
        print('%s leaves the server at %.2f.' % (name, env.now))



def setup(env, nun_server):
    """Create a carwash, a number of initial cars and keep creating cars
    approx. every ``t_inter`` minutes."""
    # Create the environment
    ambiente = Server(env, nun_server)
    i = 0
    # Create more process while the simulation is running
    while True:
        yield env.timeout(random.choice(list))
        global number_of_clients
        number_of_clients += 1
        env.process(processo(env, 'process %d' % i, ambiente))
        i += 1

# Setup and start the simulation
random.seed(RANDOM_SEED)  # This helps reproducing the results
# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_SERVER))
# Execute!
env.run(until=SIM_TIME)


#------------Analise-----#
print("O numero final de processos: %i" % number_of_clients)
sun = 0
for x in fila:
    sun +=  x
avarage_of_process = sun/len(fila)
print("Numero Medio de Clientes na Fila: %i" % avarage_of_process)
sun = 0
for x in time_in_line:
    sun += x
avarage_time_in_line = sun/len(time_in_line)
print("Tempo Medio de um Cliente na Fila: %i" % avarage_time_in_line)

sun = 0
for x in time_in_server:
    sun += x
avarage_time_in_server = sun/len(time_in_server)
print("Tempo Medio no Sistema: %i" % avarage_time_in_server)

print clients_in_server_2
percent_server_1 = round(clients_in_server_1, 2)/round(number_of_clients, 2) * 100
percent_server_2 = round(clients_in_server_2, 2)/round(number_of_clients, 2) * 100

print("porcentagem de clientes no servidor 1: %f" % round(percent_server_1, 2))
print("porcentagem de clientes no servidor 2: %f" % round(percent_server_2, 2))
print "o restante dos clientes estavam na fila ao fim do processo"





