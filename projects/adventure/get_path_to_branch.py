def get_path_to_branch(g, start_room, next_room, exploration_table): 
  path = []
  
  exploration_table[start_room].remove(next_room)
  
  """
  Traverse until:
   1) Dead-End
   2) Loop Discovered
   3) Fork

#      012--011--002--009--010           #
#                 |                      #
#                 |                      #
#                001                     #
#                 |                      #
#                 |                      #
#      008--007--000--003--004           #
#                 |                      #
#                 |                      #
#                005                     #
#                 |                      #
#                 |                      #
#                006                     #
#                                        #

#                                        #
#      017       002       014           #
#       |         |         |            #
#       |         |         |            #
#      016--015--001--012--013           #
#                 |                      #
#                 |                      #
#      008--007--000--003--004           #
#       |         |                      #
#       |         |                      #
#      009       005                     #
#       |         |                      #
#       |         |                      #
#      010--011--006                     #
#                                        #
  """


  # Setup

  room_connections = g.get_neighbors(next_room)
  prev_room_id = start_room
  room_id = next_room

  # Traverse

  while True:

    if len(room_connections) == 2:
      room_connections.remove(prev_room_id) # remove the link to the previous room
      path.append(room_id)
      
      prev_room_id = room_id
      room_id = room_connections.pop()

      exploration_table[prev_room_id].remove(room_id)

      if room_id == start_room:
        path.append("LOOP")
        break

      room_connections = g.get_neighbors(room_id)

    elif len(room_connections) == 1:
      back_track_room = room_connections.pop()
      if prev_room_id != back_track_room: # verify
        raise Exception("Impossible")
      path.append(room_id)
      path.append("END")
      break

    else:
      path.append(room_id) # FORK
      break

  if len(path) == 0:
    1/0

  return path

