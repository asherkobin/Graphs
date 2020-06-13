from ast import literal_eval
from graph import Graph
from helpers import build_graph, backtrack, build_exploration_table
import random

def is_exploration_complete(exploration_table):
  item_count = 0
  for room_id in exploration_table:
    for _ in exploration_table[room_id]:
      item_count += 1
  return item_count == 0

# DFS then BFS for backtrack

def explore_graph(room_direction_graph):
  mother_path = []
  start_room_id = 0
  room_id = start_room_id
  room_graph = build_graph(room_direction_graph)
  exploration_table = build_exploration_table(room_graph.vertices)
  stack = []
  rooms_with_unexpored_paths = []
  
  stack.append([start_room_id])

  # at the worse, keep going until there are every path has been explored
  t = [4, 8, 3, 1]

  starting_room_paths = {}
  starting_room_paths[4] = []
  starting_room_paths[8] = []
  starting_room_paths[3] = []
  starting_room_paths[1] = []

  while not is_exploration_complete(exploration_table):
    path = stack.pop()
    room_id = path[0]

    unexplored_adjacent_rooms_set = exploration_table[room_id]
    num_unexplored_rooms = len(unexplored_adjacent_rooms_set)



    a = 100
    while a != 0:
      a -= 1

    if a != 0:
      1/0





    if num_unexplored_rooms == 0: # aka DEAD-END
      if room_id in rooms_with_unexpored_paths:
        rooms_with_unexpored_paths.remove(room_id)
      previous_room_with_unexpored_paths = rooms_with_unexpored_paths[-1]
      backtrack_path = backtrack(room_id, previous_room_with_unexpored_paths, room_graph)
      backtrack_path.reverse()
      path = backtrack_path[:-1] + path


      if path[0] == start_room_id and path[-1] == start_room_id:
        # path is complete
        starting_room_paths[path[1]] = path
      else:
        stack.append(path)
      stack.append([previous_room_with_unexpored_paths])

    else:
      # pick a random unexplored adjacent room to visit
      # next_room_id = random.choice(tuple(unexplored_adjacent_rooms_set))
      
      if room_id == 0:
        next_room_id = t[0]
        t.remove(next_room_id)
      else:
        next_room_id = random.choice(tuple(unexplored_adjacent_rooms_set))
      
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

      room_id = next_room_id

  # TODO: stich togeother the stack

  return mother_path

map_file = "projects/adventure/maps/main_maze.txt"
room_direction_graph = literal_eval(open(map_file, "r").read())

explore_graph(room_direction_graph)