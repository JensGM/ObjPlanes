#!/usr/bin/env python3
import argparse
import itertools
import numpy as np


def remap(a, in_min, in_max, tar_min, tar_max):
    return np.interp(
        float(a),
        [float(in_min), float(in_max)],
        [float(tar_min), float(tar_max)])


def save_mesh(filename, vertices, indices, normals, uvs):
    with open(filename, 'w') as f:
        print('# Vertices', end='\n\n', file=f)
        for x, y, z in vertices:
            print('v {} {} {}'.format(x, y, z), file=f)
        print(file=f)

        print('# Texture coordinates', end='\n\n', file=f)
        for u, v in uvs:
            print('vt {} {}'.format(u, v), file=f)
        print(file=f)

        print('# Normals', end='\n\n', file=f)
        for x, y, z in normals:
            print('vn {} {} {}'.format(x, y, z), file=f)
        print(file=f)

        print('# Indices', end='\n\n', file=f)
        for i0, i1, i2 in indices:
            print('f {0}/{0}/{0} {1}/{1}/{1} {2}/{2}/{2}'.format(
                  i0 + 1, i1 + 1, i2 + 1), file=f)
        print(file=f)


def main(args):
    n_x = args.n_x
    n_y = args.n_y
    n_vertices = n_x * n_y
    sizex = args.size_x
    sizey = args.size_y

    vertices = []
    indices = []
    normals = [(0.0, 0.0, 1.0)] * n_vertices
    uvs = []

    for x, y in itertools.product(range(n_x), range(n_y)):
        vertex = (
            remap(x, 0, n_x - 1, -sizex * 0.5, sizex * 0.5),
            remap(y, 0, n_y - 1, -sizey * 0.5, sizey * 0.5),
            0.0)
        vertices.append(vertex)

    for x, y in itertools.product(range(n_x), range(n_y)):
        texture_coordinate = (
            remap(x, 0, n_x - 1, 0.0, 1.0),
            remap(y, 0, n_y - 1, 0.0, 1.0))
        uvs.append(texture_coordinate)

    for x, y in itertools.product(range(n_x - 1), range(n_y - 1)):
        i0 = (x + 0) * n_y + (y + 0)
        i1 = (x + 1) * n_y + (y + 0)
        i2 = (x + 1) * n_y + (y + 1)
        i3 = (x + 0) * n_y + (y + 1)
        indices.append((i0, i1, i3))
        indices.append((i1, i2, i3))

    save_mesh(args.dest_file, vertices, indices, normals, uvs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate plane mesh')
    parser.add_argument('n_x', type=int)
    parser.add_argument('n_y', type=int)
    parser.add_argument('dest_file', type=str)
    parser.add_argument('--size-x', type=float, default=100.0)
    parser.add_argument('--size-y', type=float, default=100.0)
    main(parser.parse_args())
