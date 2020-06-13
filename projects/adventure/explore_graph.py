from graph import Graph
from helpers import build_graph, backtrack, build_exploration_table
import random

# DFS then BFS for backtrack

def explore_graph(room_direction_graph):
  mother_path = []
  start_room_id = 0
  room_id = start_room_id
  room_graph = build_graph(room_direction_graph)
  exploration_table = build_exploration_table(room_graph.vertices)
  stack = []
  rooms_with_unexpored_paths = []
  
  room_graph.freeze() # help detect corruption
  
  stack.append([start_room_id])

  # keep going until dead-end

  #rooms_with_unexplored_connections = []
  
  while rooms_with_unexpored_paths > 0:
    path = stack.pop()
    room_id = path[0]

    unexplored_adjacent_rooms_set = exploration_table[room_id]
    num_unexplored_rooms = len(unexplored_adjacent_rooms_set)

    if num_unexplored_rooms == 0: # aka DEAD-END
      previous_room_with_unexpored_paths = rooms_with_unexpored_paths[-1]
      backtrack_path = backtrack(room_id, previous_room_with_unexpored_paths, room_graph)
      # ?? mother_path.extend(backtrack_path)
      room_id = previous_room_with_unexpored_paths
    else:
      # pick a random unexplored adjacent room to visit
      next_room_id = random.randint(0, num_unexplored_rooms - 1)
      # mark explored (remove from exploration table)
      unexplored_adjacent_rooms_set.remove(next_room_id)
      # mark room as unexplored if there remains any
      if len(unexplored_adjacent_rooms_set) != 0:
        rooms_with_unexpored_paths.append(room_id)
      # save path
      path_copy = [next_room_id, *path]
      stack.append(path_copy)
      # ?? mother_path

      room_id = next_room_id

  return mother_path