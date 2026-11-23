from heapq import heappop, heappush
import math
from itertools import count

def validate_graph(graph, start, goals):
    """String IDs; nonnegative integer weights."""
    for node in graph:
        if not isinstance(node, str):
            raise ValueError("Use string node IDs")
    if start not in graph: #or goal not in graph:
        raise ValueError("Unknown start or goal")

    #validate goal list
    if not isinstance(goals, (list, tuple, set)):
        raise ValueError("Goals must be a list")
    if not goals:
        raise ValueError("Goal list cannot be empty")
    for goal in goals:
        if goal not in graph:
            raise ValueError(f"Unknown goal: {goal}")

    for roads in graph.values():
        for neighbor, weight in roads:
            if neighbor not in graph:
                raise ValueError("Unknown endpoint")
            if not isinstance(weight, (int, float)) or weight < 0:
                raise ValueError(
                    "Nonnegative integers required"
                )

def rebuild_path(previous, goal):
    path = [goal]
    while path[-1] in previous:
        path.append(previous[path[-1]])
    path.reverse()
    return path

def shortest_path(graph, start, goals):
    """Return (cost, path), or (infinity, [])."""
    validate_graph(graph, start, goals)
    goals = set(goals)

    distances = {node: math.inf for node in graph}
    distances[start] = 0
    previous = {}
    pending = [(0, start)]

    while pending:
        cost, node = heappop(pending)
        if cost != distances[node]:
            continue
        if node in goals:
            path = rebuild_path(previous, node)
            return cost, path, node

        for neighbor, weight in graph[node]:
            candidate = cost + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = node
                offer = (candidate, neighbor)
                heappush(pending, offer)

    return math.inf, []

A = (0, 39.5)
B = (35, 39.5)
C = (69, 39.5)
D = (69, 125)
E = (69, 154)
F = (69, 199)
Fg1 = (69, 231)
Fg2 = (123, 303)
G = (123, 322)
Gh1 = (123, 411)
H = (78.5, 411)
I = (-53.98, 388.76)
J = (37.5, 322)
K = (0, 284.5)
L = (0, 154)
M = (0, 93.5)
N = (-74.5, 93.5)
O = (-74.5, 165)
P = (-74.5, 238)
Q = (-21.34, 291.16)
R = (-37.5, 322)
R1 = (102.5, 125)
R2 = (78.5, 378.5)
R3 = (-86.98, 388.76)
R4 = (-129, 238)
R5 = (-74.5, 5.5)
RP = (-135.5, 322)
S = (-25.74, 349.27)
ST = (0, 0)
W1 = (35, 71)
W2 = (101.5, 199)
W3 = (134.5, 322)
W4 = (-46, 165)
W5 = (-126.5, 93.5)
WP = (108.5, 39.5)
# The shared delivery map.
def dist (p1, p2):
    return abs(math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2))

GRAPH = {
    "ST": [("A", dist(ST, A))],
    "A": [("ST", dist(A, ST)), ("B", dist(A, B)), ("M", dist(A, M))],
    "B": [("A", dist(B, A)), ("C", dist(B, C)), ("W1", dist(B, W1))],
    "C": [("B", dist(C, B)), ("D", dist(C, D)), ("WP", dist(C, WP))],
    "D": [("C", dist(D, C)), ("E", dist(D, E)), ("R1", dist(D, R1))],
    "E": [("D", dist(E, D)), ("F", dist(E, F)), ("L", dist(E, L))],
    "F": [("E", dist(F, E)), ("Fg1", dist(F, Fg1)), ("W2", dist(F, W2))],
    "Fg1": [("F", dist(Fg1, F)), ("Fg2", dist(Fg1, Fg2))],
    "Fg2": [("Fg1", dist(Fg2, Fg1)), ("G", dist(Fg2, G))],
    "G": [("Fg2", dist(G, Fg2)), ("J", dist(G, J)), ("Gh1", dist(G, Gh1)), ("W3", dist(G, W3))],
    "Gh1": [("G", dist(Gh1, G)), ("H", dist(Gh1, H))],
    "H": [("Gh1", dist(H, Gh1)), ("R2", dist(H, R2)), ("I", dist(H, I))],
    "R2": [("H", dist(R2, H))],
    "I": [("H", dist(I, H)), ("R3", dist(I, R3)), ("S", dist(I, S))],
    "R3": [("I", dist(R3, I))],
    "S": [("I", dist(S, I)), ("R", dist(S, R)), ("J", dist(S, J))],
    "R": [("S", dist(R, S)), ("Q", dist(R, Q)), ("RP", dist(R, RP))],
    "RP": [("R", dist(RP, R))],
    "J": [("S", dist(J, S)), ("K", dist(J, K)), ("G", dist(J, G))],
    "K": [("J", dist(K, J)), ("Q", dist(K, Q)), ("L", dist(K, L))],
    "Q": [("K", dist(Q, K)), ("R", dist(Q, R)), ("P", dist(Q, P))],
    "P": [("Q", dist(P, Q)), ("R4", dist(P, R4)), ("O", dist(P, O))],
    "R4": [("P", dist(R4, P))],
    "O": [("P", dist(O, P)), ("N", dist(O, N)), ("W4", dist(O, W4))],
    "W4": [("O", dist(W4, O))],
    "N": [("O", dist(N, O)), ("M", dist(N, M)), ("W5", dist(N, W5)), ("R5", dist(N, R5))],
    "W5": [("N", dist(W5, N))],
    "R5": [("N", dist(R5, N))],
    "M": [("N", dist(M, N)), ("A", dist(M, A)), ("L", dist(M, L))],
    "L": [("M", dist(L, M)), ("K", dist(L, K)), ("E", dist(L, E))],
    "W1": [("B", dist(W1, B))],
    "W2": [("F", dist(W2, F))],
    "W3": [("G", dist(W3, G))],
    "R1": [("D", dist(R1, D))],
    "WP": [("C", dist(WP, C))]
}

if __name__ == "__main__":
    #initial drive
    print("ST")
    cost, route, goal = shortest_path(GRAPH, "ST", ["RP", "WP"])
    print(cost, route, goal)

    endWP = ["W1", "W2", "W3", "W4", "W5"]
    endRP = ["R1", "R2", "R3", "R4", "R5"]
    endDeliver = ["WP", "RP"]
    removedWP = False
    removedRP = False
    countWP = 0
    countRP = 0

    while True:
        if goal == "WP":
            start = "WP"
            end = endWP
            countWP += 1
        elif goal == "RP":
            start = "RP"
            end = endRP
            countRP += 1

        elif goal in endWP:
            start = goal
            endWP.remove(goal)
            end = endDeliver
        elif goal in endRP:
            start = goal
            endRP.remove(goal)
            end = endDeliver

        if countWP == 5 and not removedWP:
            endDeliver.remove("WP")
            removedWP = True
        elif countRP == 5 and not removedRP:
            endDeliver.remove("RP")
            removedRP = True

        if not endWP and not endRP:
            break

        cost, route, goal = shortest_path(GRAPH, start, end)
        print(goal)