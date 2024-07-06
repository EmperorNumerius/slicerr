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
