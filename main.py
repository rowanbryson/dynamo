from lasso.dyna import D3plot, ArrayType
import dyna_tools
from loguru import logger

def try_find_face_position_z():
    run_id = '0001_basic_run1'
    # grab data from the d3plot (LS-DYNA output file)
    d3plot = D3plot(f'run_sets/{run_id}/d3plot')

    node_ids = d3plot.arrays[ArrayType.node_ids]
    node_coordinates = d3plot.arrays[ArrayType.node_coordinates]
    face_nodemask = dyna_tools.find_nodes(node_ids, node_coordinates, 0.0254, 0.0254)
    node_displacement = d3plot.arrays[ArrayType.node_displacement]

    print(node_displacement.shape)

    specimen_displacement = dyna_tools.find_specimen_displacement(face_nodemask, node_displacement)
    print(specimen_displacement)

def try_find_nodes():
    run_id = '0001_basic_run1'
    # grab data from the d3plot (LS-DYNA output file)
    d3plot = D3plot(f'run_sets/{run_id}/d3plot')

    node_ids = d3plot.arrays[ArrayType.node_ids]
    node_coordinates = d3plot.arrays[ArrayType.node_coordinates]

    print(node_ids.shape)
    print(node_coordinates.shape)

    nodes = dyna_tools.find_nodes(node_ids, node_coordinates, 0.0254, 0.0254)
    print(nodes)    
    print(nodes.shape)

    # print(max(node_coordinates[:, 2]))

def try_find_specimen_displacement():
    run_id = '0001_basic_run1'
    # grab data from the d3plot (LS-DYNA output file)
    d3plot = D3plot(f'run_sets/{run_id}/d3plot')

    node_ids = d3plot.arrays[ArrayType.node_ids]
    node_coordinates = d3plot.arrays[ArrayType.node_coordinates]

    face_nodemask = dyna_tools.find_nodes(node_ids, node_coordinates, 0.0254, 0.0254)
    node_displacement = d3plot.arrays[ArrayType.node_displacement]

    face_position = dyna_tools.find_face_position_z(face_nodemask, node_displacement)
    specimen_displacement = dyna_tools.find_specimen_displacement(face_position, scale_factor=2)
    
    print(specimen_displacement.shape)
    print(specimen_displacement)

def try_find_specimen_load():
    run_id = '0001_basic_run1'
    # grab data from the d3plot (LS-DYNA output file)
    d3plot = D3plot(f'run_sets/{run_id}/d3plot')

    print(d3plot.arrays.keys())

    node_ids = d3plot.arrays[ArrayType.node_ids]
    node_coordinates = d3plot.arrays[ArrayType.node_coordinates]
    node_residual_forces = d3plot.arrays[ArrayType.node_residual_forces]

    face_nodemask = dyna_tools.find_nodes(node_ids, node_coordinates, 0.0254, 0.0254)

    specimen_load = dyna_tools.find_specimen_load(face_nodemask, node_residual_forces)
    
    print(specimen_load.shape)
    print(specimen_load)


def try_stuff():
    run_id = '0001_basic_run1'
    # grab data from the d3plot (LS-DYNA output file)
    d3plot = D3plot(f'run_sets/{run_id}/d3plot')

    print(d3plot.arrays.keys())

if __name__ == '__main__':
    # try_find_nodes()
    # try_find_specimen_load()
    try_stuff()