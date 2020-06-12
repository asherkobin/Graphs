from ast import literal_eval

#map_file = "projects/adventure/maps/test_line.txt"
# map_file = "projects/adventure/maps/test_loop_simple.txt"
# map_file = "projects/adventure/maps/test_cross.txt"
map_file = "projects/adventure/maps/test_loop.txt"
# map_file = "projects/adventure/maps/test_loop_fork.txt"
# map_file = "projects/adventure/maps/main_maze.txt"

room_graph = literal_eval(open(map_file, "r").read())

class Graph:
  def __init__(self):
      self.vertices = {}

  def add_vertex(self, vertex_id):
    if vertex_id not in self.vertices:
      self.vertices[vertex_id] = set()
    else:
      raise KeyError("Vertex already exists")

  def has_vertex(self, vertex_id):
    return vertex_id in self.vertices

  def add_edge(self, v1, v2):
    if v1 not in self.vertices:
      raise KeyError(f"Vertex not found: {v1}")

    if v2 not in self.vertices:
      raise KeyError(f"Vertex not found: {v2}")

    if v2 in self.vertices[v1]:
      raise KeyError("Edge already exists")

    self.vertices[v1].add(v2)

  def get_neighbors(self, vertex_id):
    if vertex_id not in self.vertices:
      raise KeyError("Vertex not found")

    return self.vertices[vertex_id]

  def __len__(self):
    return len(self.vertices)

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
  """
  FROM
  1: [(3, 6), {'s': 0, 'n': 2}]
  2: [(3, 7), {'s': 1, 'n': 3}]
  TO
  (1, 0): "s"
  (1, 2): "n"
  (2, 1): "s"
  (2, 3): "n"
  """

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

def get_path_to_branch(g, start_room, next_room): 
  path = []
  
  """
  Traverse until:
   1) Dead-End
   2) Loop Discovered
   3) Fork
  """

  # Setup

  room_connections = g.get_neighbors(next_room)
  prev_room_id = start_room
  room_id = next_room

  # Traverse

  while len(room_connections) == 2:
    room_connections.remove(prev_room_id) # remove the link to the previous room
    path.append(room_id)
    
    prev_room_id = room_id
    room_id = room_connections.pop()

    if room_id == start_room:
      path.append("LOOP")
      return path

    room_connections = g.get_neighbors(room_id)

  if len(room_connections) == 1:
    back_track_room = room_connections.pop()
    if prev_room_id != back_track_room: # verify
      raise Exception("Impossible")
    path.append(room_id)
    path.append("END")

  if len(path) == 0:
    path.append(next_room)

  return path

def create_path(room_graph):
  g = build_graph(room_graph)
  ordinal_map = build_ordinal_map(room_graph)
  num_rooms = len(g)
  visited_rooms = {}
  start_room_id = 0
  final_path = [start_room_id]
  
  for next_room_id in g.get_neighbors(start_room_id):

    path_to_branch = get_path_to_branch(g, start_room_id, next_room_id)

    # TEMP TEST
    # if str(type(path_to_branch[-1])) == "<class 'str'>":
    #   move_list = convert_path_to_moves(path_to_branch[:-1], ordinal_map)
    # else:
    #   move_list = convert_path_to_moves(path_to_branch, ordinal_map)
    # END TEMP TEST

    if len(path_to_branch) == 0:
      raise Exception("Impossible")
    elif path_to_branch[-1] in visited_rooms:
      # rejoined
      # if all room connections are visited:
      #   backtrack until found room with unvisited connection (BFS)
      # else pick a path to explore
      pass
    elif path_to_branch[-1] is "LOOP":
      path_to_branch.remove("LOOP")
      final_path.extend(path_to_branch)
      final_path.append(start_room_id)
      continue
      
    elif path_to_branch[-1] is "END":
      path_to_branch.remove("END")
      final_path.extend(path_to_branch)
      path_to_branch.reverse()
      final_path.extend(path_to_branch[1:] + [start_room_id])
      continue

    else:
      pass # make decision

  move_list = convert_path_to_moves(final_path, ordinal_map)
  
  return move_list

"""

0: [(3, 5), {'n': 1}]
1: [(3, 6), {'s': 0, 'n': 2}]
2: [(3, 7), {'s': 1, 'n': 3}]
3: [(3, 8), {'s': 2}]

"""

#create_path(room_graph)