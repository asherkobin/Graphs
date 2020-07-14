from ast import literal_eval
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

  # at the worse, keep going until there are every path has been explored
  
  while len(rooms_with_unexpored_paths) > 0 or room_id == start_room_id:
    path = stack.pop()
    room_id = path[0]

    unexplored_adjacent_rooms_set = exploration_table[room_id]
    num_unexplored_rooms = len(unexplored_adjacent_rooms_set)

    if num_unexplored_rooms == 0: # aka DEAD-END
      if room_id in rooms_with_unexpored_paths:
        raise Exception("Unexpected")
      previous_room_with_unexpored_paths = rooms_with_unexpored_paths[-1]
      backtrack_path = backtrack(room_id, previous_room_with_unexpored_paths, room_graph)
      # ?? mother_path.extend(backtrack_path)
      room_id = previous_room_with_unexpored_paths
    else:
      # pick a random unexplored adjacent room to visit
      next_room_id = 4#random.choice(tuple(unexplored_adjacent_rooms_set))
      # mark explored (remove from exploration table)
      unexplored_adjacent_rooms_set.remove(next_room_id)
      # mark explored the way back
      unexplored_adjacent_rooms_set_next_room = exploration_table[next_room_id]
      unexplored_adjacent_rooms_set_next_room.remove(room_id)
      # mark room as unexplored if there remains any
      if len(unexplored_adjacent_rooms_set) != 0:
        rooms_with_unexpored_paths.append(room_id)
      # save path
      path_copy = [next_room_id, *path]
      stack.append(path_copy)
      # ?? mother_path

      room_id = next_room_id

  return mother_path

map_file = "projects/adventure/maps/main_maze.txt"
room_direction_graph = literal_eval(open(map_file, "r").read())

explore_graph(room_direction_graph)