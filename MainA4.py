from collections import defaultdict
import itertools
import time


class Data(object): # ließt und speichert alle Daten der Stracke
    def __init__(self, name):
        file = open(name, "r")
        self.stations = []
        self.price = []
        line = 1
        for val in file.read().split():
            if line > 5 and line % 2 == 0:
                self.stations.append(int(val))
            elif line > 5 and line % 2 != 0:
                self.price.append(int(val))
            elif line == 1:
                self.v = int(val)  # Verbrauch
            elif line == 2:
                self.g = (int(val) / self.v) * 100  # Tankgröße
            elif line == 3:
                self.f = (int(val) / self.v) * 100  # anfängliche Tankfüllung
            elif line == 4:
                self.l = int(val)  # Länge bis zum Ziel
            else:
                self.z = int(val)  # Anzahl an Tankstellen
            line += 1
        self.stations.append(self.l)
        self.price.append(0)
        file.close()

    def r_in_f(self, r): # rechnet Reichweite/Entfernung in Liter um
        return (r / 100) * self.v


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v, w):
        self.graph[u].append((v, w))

    def find_shortest_path(self, min_stops):
        self.p = list(itertools.chain(*plan.copy()))
        stack = list(reversed(self.p.copy()))
        cost = {i: float("Inf") for i in self.p} # Kosten werden am Anfang alle auf Unendlich gesetzt
        min_cost = float("Inf")
        cost[d.l] = 0
        parent = {x: -1 for x in self.p}
        parent[d.l] = d.l

        while stack:
            i = stack.pop()
            for node, weight in self.graph[i]:
                # Bei Tankstellen die vom Start aus erreicht werden können ist die Kostenberechnung anders, wegen der
                if Graph.get_layer(plan, node) == min_stops: # anfänglichen Tankfüllung
                    if min_cost > (cost[i] + weight) - (d.r_in_f(d.f - node) * d.price[d.stations.index(node)]):
                        min_cost = (cost[i] + weight) - (d.r_in_f(d.f - node) * d.price[d.stations.index(node)])
                        cost[node] = min_cost
                        parent[node] = [parent[i], node]
                else:
                    # wenn die Kosten zu diesem Knoten niedriger sind
                    if cost[node] > cost[i] + weight:
                        cost[node] = cost[i] + weight
                        parent[node] = [parent[i], node] # Weg zu diesem Knoten wird gespeichert
        return parent, cost

    @staticmethod
    def get_layer(list, station): # Sucht heraus in welcher Schicht sich eine Tankstelle befindet
        for i in range(len(list)):
            if station in list[i]:
                return i


class Setup(object):
    @staticmethod
    def get_stations(r, gas):
        gas_stations = []
        for i, e in enumerate(gas):
            if e > r:  # wenn die Distanz der jetzigen Tankstelle größer ist als die Reichweite
                gas_stations.append(gas[i - 1])
                r = d.g + gas[i - 1]
                if r >= d.l:
                    gas_stations.append(gas[-1])
                    break
        r = d.l
        plan = []
        ix = len(gas_stations) - 1
        # erstellt Liste mit allen Tankstellen die zur Auswahl stehen und verteilt sie auf verschieden Schichten
        if len(gas_stations) < (len(gas) - 1): # Wird nur gemacht, wenn gas_stations nicht schon alle Tankstellen beinhaltet
            for i, e in enumerate(reversed(gas)):
                if e < r:
                    l = []
                    for j in range(gas.index(e) + 1, gas.index(gas_stations[ix]) + 1):
                        l.insert(ix, gas[j])
                    plan.append(l.copy())
                    ix -= 1 # Index der Tankstelle
                    r = gas[gas.index(e) + 1] - d.g
                    if r < 0 <= ix: # wenn der start der Strecke erreicht wird, wird das Programm abgebrochen
                        l = []
                        for k in range(1, gas.index(gas_stations[0]) + 1):
                            l.insert(0, gas[k])
                        plan.append(l.copy())
                        break
        else:
            for i in reversed(gas_stations):
                plan.append([i])
        return plan

    @staticmethod
    def create_graph(graph, plan): # erstellt den Graphen anhand von den vorher erstellten Schichten von Tankstellen
        for i in range(len(plan) - 1):
            for j in range(len(plan[i])):
                node1 = plan[i][j]
                for k in range(len(plan[i + 1])):
                    node2 = plan[i + 1][k]
                    if node2 >= (node1 - d.g): # Kante zwischen Zwei Tankstellen
                                               # wird nur erstellt wenn diese in Reichweite sind
                        graph.add_edge(node1, node2, (d.r_in_f(node1 - node2)) * d.price[d.stations.index(node2)])

print('Geben Sie die Nummer eines Beispiels ein:')
beispiel = input()

t1 = time.time()
filename = "fahrt" + str(beispiel) + ".txt"
d = Data(filename)
plan = Setup.get_stations(d.f, d.stations)

g = Graph()
Setup.create_graph(g, plan)

parent, cost = g.find_shortest_path(len(plan) - 1)
min_cost = float("Inf")
node = 0

for i in parent:
    if Graph.get_layer(plan, i) == (len(plan) - 1):
        if cost[i] < min_cost:
            min_cost = cost[i]
            node = i


def flatten(l):
    try:
        return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]
    except IndexError:
        return []

# Ausgabe
node = parent[node].pop()
result = flatten(parent[node])
result.append(node)
print('Beispiel: ' + str(beispiel))
print('Tankstelle | Getankte Liter')
fuel = []
result = result[::-1]
current = (d.r_in_f(d.f) - d.r_in_f(result[0]))
for i, e in enumerate(result[:-1]):
    # wenn die jetzige Tankstelle billiger ist als die nächste soll an der jetzigen Tankstelle vollgetankt werden
    if d.price[d.stations.index(e)] < d.price[d.stations.index(result[i + 1])]:
        fuel.append(d.r_in_f(d.g) - current)
        current = d.r_in_f(d.g) - d.r_in_f(result[i + 1] - e)
    else: # sonst wird so viel vollgetankt wie benötigt wird um zur nächsten zu kommen
        fuel.append(d.r_in_f(result[i + 1] - e) - current)
        current = 0

price = 0
for i, e in enumerate(fuel):
    print(str(result[i]) + " | " + str(round(e, 2)))
    price += e * d.price[d.stations.index(result[i])]
print('Gesamtpreis: ' + str(round(price) / 100) + ' €')
print('Anzahl der durchgeführten Tankstopps: ' + str(len(result) - 1))

t2 = time.time()
print("In " + str(round(t2-t1, 5)) + " Sekunden")
