import random
import simpy
import itertools

RANDOM_SEED = 42
NUM_SERVER = 2  # Number of machines in the server
SIM_TIME = 200  # Simulation time in minutes

#global variables
servidorFree = 1
number_of_clients = 0
line = []
time_in_line = []
time_in_server = []
clients_in_server_1 = 0
clients_in_server_2 = 0
avarage_time_to_create_server = []

#list of possible times between arrival of clients in the server
time_between_arrivals = [3] * 35 + [8] * 19 + [13] * 19 + [18] * 13 + [22] * 3 + [29] * 7 + [34] + [38] * 2 + [40]

#list of possible times of service of the machines in the server
servidor1 = [9.5] * 6 + [10] * 5 + [10.5] * 23 + [11] * 20 + [11.5] * 21 + [12] * 12 + [12.5] * 9 + [13] * 2 + [13.5]
servidor2 = [9.5] * 5 + [10] * 4 + [10.5] * 15 + [11] * 16 + [11.5] * 23 + [12] * 20 + [12.5] * 10 + [13] * 5 + [13.5] * 2


class Server(object):
    def __init__(self, env, num_servers):
        print "init"
        self.env = env
        self.machine = simpy.Resource(env, num_servers)
        self.serverTime = 1

    def do(self, process):
        yield self.env.timeout(self.serverTime)
        print("procss %s left." %process)


def service(env, name, server):
    #instance the global variables
    global line
    global time_in_line
    global servidorFree
    global time_in_server
    global clients_in_server_2
    global clients_in_server_1
    #add to the line one more service
    line.append(len(server.machine.queue))
    print('%s arrives at the server at %.2f.' % (name, env.now))

    #saves when the service arrived in the server
    process_in_line = env.now
    with server.machine.request() as request:
        yield request

        if servidorFree:
            print("%s vou usar o servidor 1" % name)
            server.serverTime = random.choice(servidor1)
            servidorFree = 0
            clients_in_server_1 += 1
        else:
            print("%s vou usar o servidor 2" % name)
            server.serverTime = random.choice(servidor2)
            clients_in_server_2 += 1
            servidorFree = 1

        print('%s enters the server at %.2f.' % (name, env.now))
        #saves when the service is processed by the server
        process_out_line = env.now
        #calculate how long the service waiter for being processed
        time_in_line.append(process_out_line - process_in_line)
        #Process being processed
        print('%s vai ficar %d segundos no servidor' % (name, server.serverTime))
        yield env.process(server.do(name))
        #saves when the service leaves the server
        process_out_server = env.now
        #calculate how long the service stayed in ther server
        time_in_server.append(process_out_server - process_in_line)
        print('%s leaves the server at %.2f.' % (name, env.now))



def setup(env, nun_server):
    """Create a server, a number of initial services and keep creating servies
    randomly based on list of time between arrivals."""
    # Create the environment
    global number_of_clients
    global avarage_time_to_create_server
    ambiente = Server(env, nun_server)
    i = 0
    # Create more process while the simulation is running
    while True:
        #time to create a new service
        time = random.choice(time_between_arrivals)
        avarage_time_to_create_server.append(time)
        print('Proximo servico sera criado daqui %d segundos' % time)
        yield env.timeout(time)
        number_of_clients += 1
        env.process(service(env, 'process %d' % i, ambiente))
        i += 1

# Setup and start the simulation
random.seed(RANDOM_SEED)  # This helps reproducing the results
# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_SERVER))
# Execute!
env.run(until=SIM_TIME)


#------------Analise-----#
print "------Analise--------"
#final number of services
print("O numero final de processos: %i" % number_of_clients)
sun = 0
for x in line:
    sun +=  x
avarage_of_process = sun/len(line)
#average number of services waiting in line
print("Numero Medio de Clientes na fila: %i" % avarage_of_process)
sun = 0
for x in time_in_line:
    sun += x
avarage_time_in_line = sun/len(time_in_line)
#average time of a service waiting in the line
print("Tempo Medio de um Cliente na Fila: %i" % avarage_time_in_line)

sun = 0
for x in time_in_server:
    sun += x
avarage_time_in_server = sun/len(time_in_server)
#average time of a service waiting in the server
print("Tempo Medio no Sistema: %i" % avarage_time_in_server)

sun = 0
for x in avarage_time_to_create_server:
    sun += x
avarage_time = sun/len(avarage_time_to_create_server)
#average time of a service waiting in the server
print("Tempo Medio para criar um processo: %i" % avarage_time)


percent_server_1 = round(clients_in_server_1, 2)/round(number_of_clients, 2) * 100
percent_server_2 = round(clients_in_server_2, 2)/round(number_of_clients, 2) * 100

#percentage of service that used server 1
print("porcentagem de clientes no servidor 1: %f" % round(percent_server_1, 2))
#percentage of service that used server 2
print("porcentagem de clientes no servidor 2: %f" % round(percent_server_2, 2))
print "o restante dos clientes estavam na fila ao fim do processo"
