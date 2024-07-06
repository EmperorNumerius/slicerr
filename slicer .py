import numpy as np

def load_stl(file_path):
    vertices = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip().startswith('vertex'):
                vertices.append(list(map(float, line.strip().split()[1:])))
    return np.array(vertices)

def slice_model(vertices, layer_height):
    layers = []
    z_min, z_max = vertices[:, 2].min(), vertices[:, 2].max()
    current_height = z_min
    while current_height <= z_max:
        layer = vertices[(vertices[:, 2] >= current_height) & (vertices[:, 2] < current_height + layer_height)]
        layers.append(layer)
        current_height += layer_height
    return layers

def generate_paths(layers):
    paths = []
    for layer in layers:
        path = []
        for i in range(len(layer)):
            path.append((layer[i][0], layer[i][1], layer[i][2]))
        paths.append(path)
    return paths

def generate_gcode(paths):
    gcode = []
    gcode.append("G21 ; Set units to millimeters\n")
    gcode.append("G90 ; Use absolute positioning\n")
    gcode.append("M82 ; Use absolute distances for extrusion\n")
    for path in paths:
        gcode.append("G0 Z{}\n".format(path[0][2]))
        for point in path:
            gcode.append("G1 X{} Y{}\n".format(point[0], point[1]))
    return gcode

def main():
    file_path = input("Enter the path to the STL file: ")
    vertices = load_stl(file_path)
    layer_height = 0.2
    layers = slice_model(vertices, layer_height)
    paths = generate_paths(layers)
    gcode = generate_gcode(paths)

    output_file = file_path.replace('.stl', '.gcode')
    with open(output_file, 'w') as f:
        f.write('\n'.join(gcode))
    print(f"G-code has been written to {output_file}")

if __name__ == "__main__":
    main()
