import pandas as pd

# Linhas:
# Azul -> 1 
# Amarela -> 2
# Vermelha -> 3
# Verde -> 4

# O problema será representado como grafo, utilizando um dicionário;
# cada entrada do dicionário representa uma estação, armazenando uma lista
# de tuplas, que por sua vez representa as 'arestas' que podem ser tomadas,
# sendo uma aresta uma tupla (destino, linha, distancia)
map_graph = {
    'E1': [('E2', 1, 10)],
    'E2': [('E3', 1, 8.5), ('E9', 2, 10), ('E10', 2, 3.5)],
    'E3': [('E4', 1, 6.3), ('E9', 3, 9.4), ('E13', 3, 18.7)],
    'E4': [('E5', 1, 13), ('E8', 4, 15.3), ('E13', 4, 12.8)],
    'E5': [('E6', 1, 3), ('E7', 2, 2.4), ('E8', 2, 30)],
    'E6': [],
    'E7': [],
    'E8': [('E9', 2, 9.6), ('E12', 4, 6.4)],
    'E9': [('E11', 3, 12.2)],
    'E10': [],
    'E11': [],
    'E12': [],
    'E13': [('E14', 4, 5.1)],
    'E14': [],
}

for node, lst in map_graph.items():
  for (end, line, cost) in lst:
    if node not in map(lambda it: it[0], map_graph[end]):
      map_graph[end].append((node, line, cost))


data = pd.read_csv('h_table.csv')

h_table = {key: [] for key in map_graph}

for node in map_graph:
  for destination, dist in data[['Destination', node]].values:
    if not pd.isna(dist):
      h_table[node].append((destination, dist))
      h_table[destination].append((node, dist))

for node in h_table:
  h_table[node].append((node, 0.0))

def h(state, final_destination):
  return [i for i in h_table[state] if i[0] == final_destination][0][1]

for node in map_graph:
  map_graph[node] = list(map(
      lambda destination: (destination[0], destination[1], destination[2]/0.5)
      , map_graph[node]
  ))

for node in h_table:
  h_table[node] = list(map(
      lambda destination: (destination[0], float(destination[1].replace(",", ".") if type(destination[1]) == str else destination[1])/0.5)
      , h_table[node]
  ))

def a_star(current_node, destination, line=0, cost=0.0, solution=[]):
  if line == 0 and cost == 0.0:
    solution = []
  if len(solution) == 0:
    solution.append((current_node, 0, 0.0))

  if current_node == destination:
    return solution

  possible_next_steps = [edge for edge in map_graph[current_node] if edge[0] not in map(lambda it: it[0], solution) and edge[0] != current_node]
  next_steps = sorted(
      list(map(
          # edge = (node, line, cost)
          lambda edge: (*edge, cost + edge[2] + h(edge[0], destination) + (0.0 if edge[1] == line else 4.0))
          , possible_next_steps
      )), key= lambda it: it[3]
      , reverse= False
  )

  next_step, next_line, step_cost, estimated_cost = next_steps[0]
  next_cost = cost + step_cost
  solution.append((next_step, next_line, next_cost))
  return a_star(next_step, destination, line=next_line, cost=next_cost, solution=solution)

solution = a_star('E7', 'E13')

print()