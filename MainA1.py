from collections import defaultdict
import time
import copy


class Data(object):
    def __init__(self, name):
        file = open(name, "r")
        line = 1
        # 0: grün, 1: gelb, 2: orange, 3: rot, 4: rosa, 5: türkis, 6: blau
        self.graphF = Graph()
        counter = 0
        for val in file.read().split():
            if val == 'gruen':
                val = 0
            elif val == 'gelb':
                val = 1
            elif val == 'orange':
                val = 2
            elif val == 'tuerkis':
                val = 3
            elif val == 'blau':
                val = 4
            elif val == 'rot':
                val = 5
            elif val == 'rosa':
                val = 6

            if line == 1:
                self.f = int(val)  # Anzahl der benötigten unterschiedlichen Farben
            elif line == 2:
                self.w = int(val)  # Anzahl der Kundenwünsche
            elif line > 2 and counter == 0:
                node1 = val
                counter += 1
            elif line > 2 and counter == 1:
                node2 = val
                counter += 1
            else:
                self.graphF.add_edge(node1, node2, int(val))
                counter = 0
            line += 1
        file.close()

        # Erstellen des Blumenbeets
        self.graphB = Graph()
        print('    P0    ')
        print('  P1  P2  ')
        print('P3  P4  P5')
        print('  P6  P7  ')
        print('    P8    ')
        self.graphB.add_edge(0, 1, 1)
        self.graphB.add_edge(0, 2, 1)
        self.graphB.add_edge(1, 2, 1)
        self.graphB.add_edge(1, 3, 1)
        self.graphB.add_edge(1, 4, 1)
        self.graphB.add_edge(2, 4, 1)
        self.graphB.add_edge(2, 5, 1)
        self.graphB.add_edge(3, 4, 1)
        self.graphB.add_edge(3, 6, 1)
        self.graphB.add_edge(4, 5, 1)
        self.graphB.add_edge(4, 6, 1)
        self.graphB.add_edge(4, 7, 1)
        self.graphB.add_edge(5, 7, 1)
        self.graphB.add_edge(6, 8, 1)
        self.graphB.add_edge(6, 7, 1)
        self.graphB.add_edge(7, 8, 1)


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v, w):
        if v != -1:
            self.graph[u].append((v, w))
            if v not in self.graph or u not in self.graph[v]:
                self.graph[v].append((u, w))
        else:
            self.graph[u].append((-1, -1))
            self.remove(-1)

    def duplicate_node(self, vertecies):
        graphD = copy.deepcopy(self.graph)
        counter = 1
        for j in vertecies:
            for node, weight in graphD[j]:
                graphD[j+(10*counter)].append((node, weight))
                graphD[node].append(((j+(10*counter)), weight))
            counter += 1
        return graphD

    def get_graph(self):
        return self.graph

    def remove_all(self, vertex):
        if vertex in self.graph:
            del self.graph[vertex]

        for i in self.graph:
            for node, weight in self.graph[i]:
                if node == vertex:
                    self.graph[i].remove((node, weight))

    def remove(self, vertex):
        if vertex in self.graph:
            del self.graph[vertex]


class Node:
    def __init__(self, tuple, points, parent=None):
        self.data = tuple
        self.points = points
        self.parent = parent

    def get_parent(self):
        return self.parent

    def get_data(self):
        return self.data

    def get_points(self):
        return self.points


class Tree:

    def __init__(self, source):
        self.tree = defaultdict(list)
        s = Node(source, 0, 0)
        self.tree[s] = []
        self.root = s

    def get_source(self):
        return self.root

    def get_tree(self, d=False):
        if d:
            t = defaultdict(list)
            for i in self.tree:
                for j in self.tree[i]:
                    t[i.get_data()].append(j.get_data())
            return t
        else:
            return self.tree

    def add_child(self, parent, child, points):
        c = Node(child, points, parent)
        self.tree[parent].append(c)

    def remove_child(self, child, parent):
        self.tree[parent].remove(child)

    def get_children(self, parent, d=False):
        children = []
        if d:
            for i in self.tree:
                if i == parent:
                    for child in self.tree[i]:
                        children.append(child.get_data())
        else:
            for i in self.tree:
                if i == parent:
                    for child in self.tree[i]:
                        children.append(child)
        return children

    def get_parents(self, parent):
        if parent.get_data() == self.root.get_data(): # An der Wurzel angekommen
            return [parent.get_data()]
        else: # Sonst Liste den nächsten parent hinzufügen
            return [parent.get_data()] + self.get_parents(parent.get_parent())

    def get_max_points(self):
        max_points = 0
        node = 0
        for i in self.tree.keys():
            if i.get_points() > max_points:
                max_points = i.get_points()
                node = i
            for j in self.tree[i]:
                if j.get_points() > max_points:
                    max_points = j.get_points()
                    node = j
        return max_points, self.get_parents(node)


class Solve:

    def __init__(self, graph, flower_bed): # Im Graph graph sind die Blumen gespeichert, in flower_bed das Hochbeet
        self.graph = graph
        self.flower_bed = flower_bed

    @staticmethod
    def order(graph):  # orndnet Blumen nach Punktzahl
        ordered = defaultdict()
        for i in graph:
            counter = 0
            for n, weight in graph[i]:
                counter += weight
            ordered[i] = counter
        return list(reversed(sorted(ordered.items(), key=lambda kv: kv[1]))) # Sortiert die Liste

    def solve(self):
        global_best = 0
        best_arrangement = 0

        order = self.order(self.graph)
        iterations = [0] * (9 - d.f)
        for i in range(d.f, len(d.graphF.get_graph())):
            d.graphF.remove_all(order[-1][0])
            order.pop()
        order = self.order(self.graph)

        for i in range((len(order) - 1) * (9 - d.f)):
            currents = []
            for j in iterations:
                currents.append(order[j][0])

            self.graph = d.graphF.duplicate_node(currents)

            if global_best >= self.get_points_graph(self.graph):
                return global_best, best_arrangement

            edges_f = defaultdict()
            for j in self.graph: # erstellt dictionary mit Anzahl an Verbindungen von jeder Blume
                counter = 0
                for x in self.graph[j]:
                    counter += 1
                edges_f[j] = counter
            edges_b = defaultdict()
            for j in flower_bed: # erstellt dictionary mit Anzahl an Verbindungen von jedem Platz im Blumenbeet
                counter = 0
                for x in flower_bed[j]:
                    counter += 1
                edges_b[j] = counter

            start = defaultdict()
            for fx in edges_f:
                f = fx - (fx//10)*10 # Duplizierte Blumen werden in eine normale Farbe zurück umgewandelt.
                                     # Bsp: 25 - (25//10) * 10 = 5
                for b in edges_b:
                    if f in start:
                        if abs(edges_f[f]-edges_b[b]) < start[f][1]:
                            start[f] = (b, abs(edges_f[f]-edges_b[b]))
                    else:
                        start[f] = (b, abs(edges_f[f]-edges_b[b]))
            # einsetzen
            for j in start:
                root = (j, start[j][0])
                tree = Tree(root) # Ursprung des Baums wird gesetzt
                parents = [[tree.get_source()]]
                cancel = False
                while not cancel: # cancel ist True wenn alle Blumen oder Plätze aufgebraucht sind
                    next_parents = []
                    for parent in parents[-1]:
                        children_f = []
                        children_b = []

                        # Bisher eingesetzte Knoten bestimmen
                        if parent.get_data() != root:
                            source = tree.get_parents(parent)
                        else:
                            source = [root]
                        # Nachfolger bestimmen
                        for s in source:
                            for f, weigth in self.graph[s[0]]:
                                for b, wb in self.flower_bed[s[1]]:
                                # überprüfen ob die Blume oder der Platz noch kein Nachfolger ist und ob er schon
                                # mal gesetzt wurde
                                    if f not in children_f:
                                        children_f.append(f)
                                    if b not in children_b:
                                        children_b.append(b)
                                    for sf, sb in source:
                                        if sf == f:
                                            children_f.remove(f)
                                        if sb == b:
                                            children_b.remove(b)
                        best_points = 0
                        if children_f != [] and children_b != []:
                            # Durch alle möglichen Nachfolger iterieren und dem Baum hinzufügen
                            for f in children_f:
                                for b in children_b:
                                    if (f, b) not in tree.get_children(parent, True):
                                        points = self.get_points_node((f, b), source)
                                        if points == best_points: # neuen Knoten dem Baum hinzufügen
                                            tree.add_child(parent, (f, b), points + parent.get_points())
                                        elif points > best_points: # vorherige Löschen und neuen Knoten hinzufügen
                                            best_points = points
                                            for child in tree.get_tree()[parent]:
                                                tree.remove_child(child, parent)
                                            tree.add_child(parent, (f, b), points + parent.get_points())
                            next_parents.append(tree.get_children(parent))
                    if next_parents == []:
                        points = tree.get_max_points()[0]
                        if tree.get_max_points()[0] > global_best:
                            global_best = points
                            best_arrangement = tree.get_max_points()[1]
                        cancel = True
                    parents = copy.deepcopy(next_parents)

            self.get_next_indices(iterations)
        return global_best, best_arrangement

    def get_points_node(self, tuple, parents):  # gibt Punkzahl eines hinzugefügten Knoten zurück
        total = 0
        for i in parents:
            for nf, wf in self.graph[i[0]]:
                for nb, wb in self.flower_bed[i[1]]:
                    if tuple == (nf, nb):
                        total += wf
        return total

    @staticmethod
    def get_points_graph(graph):  # gibt Gesamtpunkzahl eines Graphen zurück
        total = 0
        edges_f = []
        for i in graph:
            for node, weight in graph[i]:
                if (node, i) not in edges_f:
                    total += weight
                    edges_f.append((i, node))
        return total

    @staticmethod
    def get_next_indices(list):  # gibt die Kombination von Indexen zurück
        same = 0
        for i in range(len(list) - 1):
            if list[i + 1] != list[i]:
                list[i + 1] += 1
                return list
            elif list[i] == list[i + 1]:
                same += 1
                if same == len(list) - 1:
                    list[0] += 1
                    return list

    def fill_in(self, arrangement):
        used_flowers = []
        used_places = []
        for f, b in arrangement:  # Füllt die leeren Plätze mit Blumen auf
            used_flowers.append(f)
            used_places.append(b)
        for f in range(7): # Iteration durch alle Farben
            for b in range(9): # Iteration durch alle Plätze
                if f not in used_flowers and b not in used_places: # Wenn die Blume und der Platz noch nicht verwendet
                    # wurden
                    used_flowers.append(f)
                    used_places.append(b)
                    arrangement.append((f, b))
                    if len(arrangement) == 9: # Wenn alle Plätze voll sind
                        return arrangement

print('Geben Sie die Nummer eines Beispiels ein:')
beispiel = input()
time1 = time.time()
filename = "blumen" + str(beispiel) + ".txt"
d = Data(filename)

flowers = d.graphF.get_graph()
flower_bed = d.graphB.get_graph()

s = Solve(flowers, flower_bed)
points, arrangement = s.solve()

# Wenn das Blumenbeet nicht ganz gefüllt ist wird es mit den restlichen Blumen aufgefüllt
if len(arrangement) < 9:
    arrangement = s.fill_in(arrangement)

print('Beispiel: ' + str(beispiel))
print('Ergebnis:')
# Nach reihenfolge der Plätze im Hochbeet sortieren (mit Timsort)
arrangement.sort(key=lambda tup: tup[1])
for f, b in arrangement:
    val = f - (f//10)*10
    if val == 0:
        val = 'gruen'
    elif val == 1:
        val = 'gelb'
    elif val == 2:
        val = 'orange'
    elif val == 3:
        val = 'tuerkis'
    elif val == 4:
        val = 'blau'
    elif val == 5:
        val = 'rot'
    elif val == 6:
        val = 'rosa'
    print('P' + str(b) + ': ' + val)

print('Bewertung: ' + str(points))
time2 = time.time()
print('In ' + str(round((time2 - time1), 5)) + ' Sekunden')
