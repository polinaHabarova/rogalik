from random import randint, choice
def generation_dungeon_grid(rows, cols, room_count):
    grid = [[None for i in range(cols)] for k in range(rows)]
    start_x = randint(0, cols - 1)
    start_y = randint(0, rows -1)
    grid[start_y][start_x]  = 'S'
    start = (start_x, start_y)
    current = start
    room_list = [start]
    while len(room_list) < room_count:
        x, y = current
        neighbours = []
        for dx, dy in [(1,0),(0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] is None:
                neighbours.append((nx,ny))
        if neighbours:
            next_cell = choice(neighbours)
            grid[next_cell[1]][next_cell[0]] = '*'
            room_list.append(next_cell)
            current = next_cell
        else:
            possible_rooms = []
            for rx, ry in room_list:
                for dx, dy in [(1,0),(0, 1), (-1, 0), (0, -1)]:
                    nx, ny = rx + dx, ry + dy
                    if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] is None:
                        possible_rooms.append((nx, ny))
            if possible_rooms:
                current = choice(possible_rooms)
            else:
                break
    end_x, end_y = room_list[-1]
    grid[end_y][end_x] = "E"
    return grid
grid = generation_dungeon_grid(10, 10, 10)

for row in grid:
    print(' '.join(cell if cell is not None else ' ' for cell in row))
