from graph import Graph

def build_graph(room_graph):
  g = Graph()

  for v in room_graph:
    if not g.has_vertex(v):
      g.add_vertex(v)
    ns = [room_id for room_id in room_graph[v][1].values()]
    for n in ns:
      if not g.has_vertex(n):
        g.add_vertex(n)
      g.add_edge(v, n)

  return g

def build_ordinal_map(room_graph):
  ordinal_map = {}

  for room_id in room_graph:
    moves = room_graph[room_id][1]
    for move in moves:
      connected_room_id = moves[move]
      ordinal_map[(room_id, connected_room_id)] = move

  return ordinal_map

def convert_path_to_moves(path, ordinal_map):
  moves = []
  path_len = len(path)
  
  for idx, room_id in enumerate(path):
    if idx == path_len - 1: # do not look beyond next element
      break
    next_room_id = path[idx + 1]
    moves.append(ordinal_map[(room_id, next_room_id)])

  return moves

def build_exploration_table(graph_table):
  exploration_table = {}

  for key in graph_table:
    exploration_table[key] = graph_table[key].copy()

  return exploration_table

def backtrack(src_id, dst_id, g): # BFS
  queue = []
  visited = set()

  queue.append([src_id])
  
  while len(queue) > 0:
    path = queue.pop(0)
    cur_id = path[-1]

    if cur_id not in visited:
      visited.add(cur_id)

      if cur_id == dst_id:
        return path

      for n_id in g.get_neighbors(cur_id):
        path_copy = path.copy()
        path_copy.append(n_id)
        queue.append(path_copy)

  raise Exception("Backtrack Failed")
