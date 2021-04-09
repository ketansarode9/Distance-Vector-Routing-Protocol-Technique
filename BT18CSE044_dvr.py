#Name - Ketan Sarode
#Roll no - BT18CSE044
import threading
import time
import math
import sys
from queue import Queue
import copy

def get_ord(name):
    return (ord(name) - 65)
def get_char(num):
    return chr(num + 65)

class router:
    def __init__(self, name):
        self.name = name
        self.id = get_ord(name)
        self.fwd = dict([(i, math.inf) for i in range(no_of_nodes)])
        self.fwd[self.id] = -1
        self.next_hop = [-1 for i in range(no_of_nodes)]
        self.neighbors = []
        self.updated = []

def Bellman_Ford(routers, i):
    temp_fwd = copy.deepcopy(routers[i].fwd)
    while not queueList[i].empty():
        next_fwd = queueList[i].get()
        received_from = -1

        for j in range(no_of_nodes):
            if next_fwd[j] == -1:
                received_from = j

        for j in range(no_of_nodes):
            if j != received_from:
                if temp_fwd[j] > routers[i].fwd[received_from] + next_fwd[j]:
                    temp_fwd[j] = routers[i].fwd[received_from] + next_fwd[j]
                    routers[i].next_hop[j] = received_from
                    
        for j in range(no_of_nodes):
            if routers[i].fwd[j] != temp_fwd[j]:
                routers[i].updated.append(j)
    routers[i].fwd = dict(temp_fwd)   

def Propagate(routers, i):
    for nei in routers[i].neighbors:
        queueList[nei].put(copy.deepcopy(routers[i].fwd))

    while True:
        if queueList[i].full():
            break

    Bellman_Ford(routers, i)
    queueList[i].queue.clear()

    time.sleep(2)

if __name__ == '__main__':
    inp = sys.argv[1]
    with open(inp, "r") as f:
        no_of_nodes = int(f.readline())
        nodes = f.readline().split()
        routers = [router(node) for node in nodes]
        
        line = f.readline()
        while line != "EOF":
            from_edge, to_edge, weight = line.split()
            routers[get_ord(from_edge)].fwd[get_ord(to_edge)] = int(weight)
            routers[get_ord(from_edge)].neighbors.append(get_ord(to_edge))
            routers[get_ord(from_edge)].next_hop[get_ord(to_edge)] = get_ord(to_edge)
            sorted(routers[get_ord(from_edge)].neighbors)

            routers[get_ord(to_edge)].fwd[get_ord(from_edge)] = int(weight)
            routers[get_ord(to_edge)].neighbors.append(get_ord(from_edge))
            routers[get_ord(to_edge)].next_hop[get_ord(from_edge)] = get_ord(from_edge)
            sorted(routers[get_ord(to_edge)].neighbors)
            line = f.readline()
    queueList = [Queue(maxsize = len(routers[i].neighbors)) for i in range(no_of_nodes)]


    print("\nInitialised input:")
    print_str = ""
    for i in range(no_of_nodes):
        print_str += f"\nRouting table of router {routers[i].name}:"
        for key, item in routers[i].fwd.items():
            if key != i:
                print_str += "\n" + str(get_char(key)) + " -- " + str(item)
    print(print_str)
    for k in range(4):
        for i in range(no_of_nodes):
            thread = threading.Thread(target = Propagate, args = (routers, i))
            thread.start()
        thread.join()
        print("==================================================")
        print("                  Iteration " + str(k + 1))
        print("==================================================")

        print_str = ""
        for i in range(no_of_nodes):
            print_str += f"\nRouting table of router {routers[i].name} with next hop:"
            for key, item in routers[i].fwd.items():
                if key != i:
                    print_str += "\n"
                    if key in routers[i].updated:
                        print_str += "  *"
                    print_str += "\t" + str(get_char(key)) + " -- " + str(item)
                    print_str += " -- " + str(get_char(routers[i].next_hop[key]))
            routers[i].updated.clear()
        print(print_str + "\n\n")