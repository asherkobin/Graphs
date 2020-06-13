room_graph = test_cross_double = {
  0: [(3, 5), {'n': 1, 's': 5, 'e': 3, 'w': 7}],
  1: [(3, 6), {'s': 0, 'n': 2}],
  2: [(3, 7), {'s': 1, 'e': 9, 'w': 11}],
  3: [(4, 5), {'w': 0, 'e': 4}],
  4: [(5, 5), {'w': 3}],
  5: [(3, 4), {'n': 0, 's': 6}],
  6: [(3, 3), {'n': 5}],
  7: [(2, 5), {'w': 8, 'e': 0}],
  8: [(1, 5), {'e': 7}],
  9: [(4, 7), {'w': 2, 'e': 10}],
 10: [(5, 7), {'w': 9}],
 11: [(2, 7), {'e': 2, 'w': 12}],
 12: [(1, 7), {'e': 11}]
}

room_graph = test_look_fork = {
  0: [(3, 5), {'n': 1, 's': 5, 'e': 3, 'w': 7}],
  1: [(3, 6), {'s': 0, 'n': 2, 'e': 12, 'w': 15}],
  2: [(3, 7), {'s': 1}],
  3: [(4, 5), {'w': 0, 'e': 4}],
  4: [(5, 5), {'w': 3}],
  5: [(3, 4), {'n': 0, 's': 6}],
  6: [(3, 3), {'n': 5, 'w': 11}],
  7: [(2, 5), {'w': 8, 'e': 0}],
  8: [(1, 5), {'e': 7}, {'s': 9}],
  9: [(1, 4), {'n': 8, 's': 10}],
  10: [(1, 3), {'n': 9, 'e': 11}],
  11: [(2, 3), {'w': 10, 'e': 6}],
  12: [(4, 6), {'w': 1, 'e': 13}],
  13: [(5, 6), {'w': 12, 'n': 14}],
  14: [(5, 7), {'s': 13}],
  15: [(2, 6), {'e': 1, 'w': 16}],
  16: [(1, 6), {'n': 17, 'e': 15}],
  17: [(1, 7), {'s': 16}]
}

from helpers import build_graph, build_ordinal_map, convert_path_to_moves, build_exploration_table, backtrack
from get_path_to_branch import get_path_to_branch
from explore_path import explore_path

def get_path(room_graph):
  g = build_graph(room_graph)
  g.freeze()
  exploration_table = build_exploration_table(g.vertices)
  ordinal_map = build_ordinal_map(room_graph)
  num_rooms = len(g)
  visited_rooms = set()
  start_room_id = 0
  final_path = [start_room_id]
  visited_rooms = set([start_room_id])
  
  for next_room_id in g.get_neighbors(start_room_id):

    if len(final_path) > 1:
      last_room = final_path[-1]
      if start_room_id != last_room:
        # walk back to start_room
        #BFS lastroom -> start_room_id
        path_back = backtrack(last_room, start_room_id, g)
        first_room_id = path_back.pop(0)
        if first_room_id != last_room:
          raise Exception("Serious Error")
        final_path.extend(path_back)

    path_to_branch = get_path_to_branch(g, start_room_id, next_room_id, exploration_table)

    if len(path_to_branch) == 0:
      raise Exception("Impossible")
    
    elif path_to_branch[-1] in visited_rooms:
      # rejoined
      # if all room connections are visited:
      #   backtrack until found room with unvisited connection (BFS)
      # else pick a path to explore
      1/0
    
    elif path_to_branch[-1] == "LOOP":
      path_to_branch.remove("LOOP")
      for room_id in path_to_branch:
        visited_rooms.add(room_id)
      final_path.extend(path_to_branch)
      final_path.append(start_room_id)
    
    elif path_to_branch[-1] == "END":
      path_to_branch.remove("END")
      for room_id in path_to_branch:
        visited_rooms.add(room_id)
      
      final_path.extend(path_to_branch) # path to END
      
      # return path
      path_to_branch = [start_room_id] + path_to_branch
      # mark return path explored
      for idx, room_id in enumerate(path_to_branch):
        if idx == len(path_to_branch) - 1: 
          break
        next_room_id = path_to_branch[idx + 1]
        exploration_table[next_room_id].remove(room_id)
        
      path_to_branch.reverse()
      path_to_start = path_to_branch[1:]
      final_path.extend(path_to_start) # return path
    
    else:
      final_path.extend(path_to_branch)
      unexplored_room = path_to_branch[-1]
      prev_room = path_to_branch[-2]

      ns = g.get_neighbors(unexplored_room)
      ns.remove(prev_room)
      
      for room_id in ns:
        explore_path(unexplored_room, room_id, g, exploration_table, visited_rooms, final_path)

      if len(exploration_table[unexplored_room]) == 0:
        1/0
      
      # a = 3 + 3
      # for remaining_unexplored_room in exploration_table[unexplored_room]:
      #   explore_path(unexplored_room, remaining_unexplored_room, g, exploration_table, visited_rooms, final_path)

    if len(visited_rooms) == num_rooms: # DONE
      break

  move_list = convert_path_to_moves(final_path, ordinal_map)
  
  return move_list

get_path(room_graph)