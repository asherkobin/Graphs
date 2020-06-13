from get_path_to_branch import get_path_to_branch

def explore_path(start_room, next_room, g, exploration_table, visited_rooms, final_path):
  start_room_id = start_room
  next_room_id = next_room

  print(f"{start_room} to {next_room}")
  
  path_to_branch = get_path_to_branch(g, start_room_id, next_room_id, exploration_table)

  if len(path_to_branch) == 0:
    raise Exception("Impossible")
  
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
    for room_id in g.get_neighbors(next_room_id):
      if next_room_id in exploration_table[room_id]:
        explore_path(room_id, next_room_id, g, exploration_table, visited_rooms, final_path)
      
  if len(visited_rooms) == len(g): # DONE
    return