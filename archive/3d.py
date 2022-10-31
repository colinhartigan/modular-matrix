led_map = [  # draw from top left as (0,0)
    [0, 31, 32, 63, 64, 95, 96, 127, 128, 159, 160, 191, 192, 223, 224, 255],
    [1, 30, 33, 62, 65, 94, 97, 126, 129, 158, 161, 190, 193, 222, 225, 254],
    [2, 29, 34, 61, 66, 93, 98, 125, 130, 157, 162, 189, 194, 221, 226, 253],
    [3, 28, 35, 60, 67, 92, 99, 124, 131, 156, 163, 188, 195, 220, 227, 252],
    [4, 27, 36, 59, 68, 91, 100, 123, 132, 155, 164, 187, 196, 219, 228, 251],
    [5, 26, 37, 58, 69, 90, 101, 122, 133, 154, 165, 186, 197, 218, 229, 250],
    [6, 25, 38, 57, 70, 89, 102, 121, 134, 153, 166, 185, 198, 217, 230, 249],
    [7, 24, 39, 56, 71, 88, 103, 120, 135, 152, 167, 184, 199, 216, 231, 248],
    [8, 23, 40, 55, 72, 87, 104, 119, 136, 151, 168, 183, 200, 215, 232, 247],
    [9, 22, 41, 54, 73, 86, 105, 118, 137, 150, 169, 182, 201, 214, 233, 246],
    [10, 21, 42, 53, 74, 85, 106, 117, 138, 149, 170, 181, 202, 213, 234, 245],
    [11, 20, 43, 52, 75, 84, 107, 116, 139, 148, 171, 180, 203, 212, 235, 244],
    [12, 19, 44, 51, 76, 83, 108, 115, 140, 147, 172, 179, 204, 211, 236, 243],
    [13, 18, 45, 50, 77, 82, 109, 114, 141, 146, 173, 178, 205, 210, 237, 242],
    [14, 17, 46, 49, 78, 81, 110, 113, 142, 145, 174, 177, 206, 209, 238, 241],
    [15, 16, 47, 48, 79, 80, 111, 112, 143, 144, 175, 176, 207, 208, 239, 240],
]
def get_led(x, y): return led_map[y][x]

scale = 31
vertex_table = [
    [scale, scale, scale],
    [scale, -scale, scale],
    [-scale, -scale, scale],
    [-scale, scale, scale],
    [scale, scale, -scale],
    [scale, -scale, -scale],
    [-scale, -scale, -scale],
    [-scale, scale, -scale],
]
edge_table = [
    [0, 1], [1, 2], [2, 3], [3, 0],
    [4, 5], [5, 6], [6, 7], [7, 4],
    [0, 4], [1, 5], [2, 6], [3, 7],
]
focal_length = 100


def project_vertex(vertex, focal_length):
    x, y, z = vertex
    x_projected = (x * focal_length) / (z + focal_length + 256)
    y_projected = (y * focal_length) / (z + focal_length + 256)

    return [x_projected, y_projected]


def plot_line(p1, p2):
    print(p1, p2)
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    print(dx, dy)
    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)

    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1

    for i in range(0, int(steps)):
        try:
            np[get_led(int(x)+8, int(y)+8)] = (5, 5, 5)
        except:
            pass
        x += x_inc
        y += y_inc


def rotate_x(vertex, angle):
    x, y, z = vertex
    y_rotated = y * math.cos(angle) - z * math.sin(angle)
    z_rotated = y * math.sin(angle) + z * math.cos(angle)
    return [x, y_rotated, z_rotated]


def rotate_y(vertex, angle):
    x, y, z = vertex
    x_rotated = x * math.cos(angle) - z * math.sin(angle)
    z_rotated = x * math.sin(angle) + z * math.cos(angle)
    return [x_rotated, y, z_rotated]


def rotate_z(vertex, angle):
    x, y, z = vertex
    x_rotated = x * math.cos(angle) - y * math.sin(angle)
    y_rotated = x * math.sin(angle) + y * math.cos(angle)
    return [x_rotated, y_rotated, z]


for i in range(1, 360):
    np.fill((0, 0, 0))
    #rotated = [rotate_z(rotate_y(rotate_x(vertex, math.radians(i)),math.radians(i)), math.radians(i)) for vertex in vertex_table]
    rotated = [rotate_y(vertex, math.radians(i)) for vertex in vertex_table]
    projected = [project_vertex(vertex, focal_length) for vertex in rotated]
    print(projected)
    for edge in edge_table:
        p1 = projected[edge[0]]
        p2 = projected[edge[1]]
        plot_line(p1, p2)
    np.write()
    await asyncio.sleep(.05)
