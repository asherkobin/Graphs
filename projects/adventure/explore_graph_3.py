from ast import literal_eval
from graph import Graph
from helpers import build_graph, backtrack, build_exploration_table, convert_path_to_moves, build_ordinal_map
import random

def is_exploration_complete(exploration_table):
  item_count = 0
  for room_id in exploration_table:
    for _ in exploration_table[room_id]:
      item_count += 1
  return item_count == 0

# DFS then BFS for backtrack

def explore_graph(room_direction_table, starting_room = 0):
  start_room_id = starting_room
  room_id = start_room_id
  room_graph = build_graph(room_direction_table)
  exploration_table = build_exploration_table(room_graph.vertices)
  stack = []
  rooms_with_unexpored_paths = []
  
  stack.append([start_room_id])

  while not is_exploration_complete(exploration_table):
    path = stack.pop()
    room_id = path[0]

    unexplored_adjacent_rooms_set = exploration_table[room_id]
    num_unexplored_rooms = len(unexplored_adjacent_rooms_set)

    if num_unexplored_rooms == 0: # aka DEAD-END
      if room_id in rooms_with_unexpored_paths:
        rooms_with_unexpored_paths.remove(room_id)
      previous_room_with_unexpored_paths = rooms_with_unexpored_paths[-1]
      backtrack_path = backtrack(room_id, previous_room_with_unexpored_paths, room_graph)
      backtrack_path.reverse()
      path = backtrack_path[:-1] + path

      stack.append(path)
      stack.append([previous_room_with_unexpored_paths])

    else:
      # pick a random unexplored adjacent room to visit
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

  # stitch togeother the paths from the stack ("dequeue" the stack)

  completed_path = [start_room_id]
  
  while len(stack) > 0:
    next_segment = stack.pop(0)[:-1]
    next_segment.reverse()

    completed_path.extend(next_segment)

  num_moves = len(completed_path)
  if num_moves < 960:
    raise Exception("Found Path for Stretch!")

  ordinal_map = build_ordinal_map(room_direction_table)

  move_list = convert_path_to_moves(completed_path, ordinal_map)

  return move_list