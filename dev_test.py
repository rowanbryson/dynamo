from lasso.dyna import D3plot, ArrayType, Binout
import dyna_tools
import outputs
from loguru import logger

from rich import print

RUN_ID = '0002_basic_run1'

def try_find_face_position_z():
    run_id = '0002_basic_run1'
    # grab data from the d3plot (LS-DYNA output file)
    d3plot = D3plot(f'run_sets/{run_id}/d3plot')

    node_ids = d3plot.arrays[ArrayType.node_ids]
    node_coordinates = d3plot.arrays[ArrayType.node_coordinates]
    face_nodemask = dyna_tools._find_nodes(node_ids, node_coordinates, 0.0254, 0.0254)
    node_displacement = d3plot.arrays[ArrayType.node_displacement]

    print(node_displacement.shape)

    specimen_displacement = dyna_tools.find_specimen_displacement(face_nodemask, node_displacement)
    print(specimen_displacement)

def try_find_nodes():
    run_id = '0002_basic_run1'
    # grab data from the d3plot (LS-DYNA output file)
    d3plot = D3plot(f'run_sets/{run_id}/d3plot')

    node_ids = d3plot.arrays[ArrayType.node_ids]
    node_coordinates = d3plot.arrays[ArrayType.node_coordinates]

    print(node_ids.shape)
    print(node_coordinates.shape)

    nodes = dyna_tools._find_nodes(node_ids, node_coordinates, 0.0254, 0.0254)
    print(nodes)    
    print(nodes.shape)

    # print(max(node_coordinates[:, 2]))

def try_find_specimen_displacement():
    run_id = '0002_basic_run1'
    # grab data from the d3plot (LS-DYNA output file)
    d3plot = D3plot(f'run_sets/{run_id}/d3plot')

    binout = Binout(f'run_sets/{run_id}/binout*')
    dyna_tools.find_specimen_displacement(binout)

    # node_ids = d3plot.arrays[ArrayType.node_ids]
    # node_coordinates = d3plot.arrays[ArrayType.node_coordinates]

    # face_nodemask = dyna_tools._find_nodes(node_ids, node_coordinates, 0.0254, 0.0254)
    # node_displacement = d3plot.arrays[ArrayType.node_displacement]

    # face_position = dyna_tools._find_face_position_z(face_nodemask, node_displacement)
    # specimen_displacement = dyna_tools.find_specimen_displacement(face_position, scale_factor=2)
    
    # print(specimen_displacement.shape)
    # print(specimen_displacement)

def try_find_specimen_load():
    run_id = '0002_basic_run1'
    # grab data from the d3plot (LS-DYNA output file)
    # d3plot = D3plot(f'run_sets/{run_id}/d3plot')
    binout = Binout(f'run_sets/{run_id}/binout*')
    print(dyna_tools.find_specimen_load(binout))

    # print(d3plot.arrays.keys())

    # node_ids = d3plot.arrays[ArrayType.node_ids]
    # node_coordinates = d3plot.arrays[ArrayType.node_coordinates]
    # node_residual_forces = d3plot.arrays[ArrayType.node_residual_forces]

    # face_nodemask = dyna_tools.find_nodes(node_ids, node_coordinates, 0.0254, 0.0254)

    # specimen_load = dyna_tools.find_specimen_load(face_nodemask, node_residual_forces)
    
    # print(specimen_load.shape)
    # print(specimen_load)


def try_stuff():
    run_id = '0002_basic_run1'
    # grab data from the d3plot (LS-DYNA output file)
    d3plot = D3plot(f'run_sets/{run_id}/d3plot')


    print(d3plot.arrays.keys())


def try_binout():
    from lasso.dyna import Binout, ArrayType
    run_id = '0002_basic_run1'
    # grab data from the binout (LS-DYNA output file)
    binout = Binout(f'run_sets/{run_id}/binout*')
    d3plot = D3plot(f'run_sets/{run_id}/d3plot')

    bin_time = binout.read('bndout', 'velocity', 'nodes', 'time')
    d3_time = d3plot.arrays[ArrayType.global_timesteps]
    print(bin_time)
    print(d3_time)

    print(binout.read())

def try_find_effective_plastic_strain():
    d3plot = D3plot(f'run_sets/{RUN_ID}/d3plot')
    print(d3plot.arrays[ArrayType.element_solid_effective_plastic_strain].shape)

    eps = dyna_tools.find_interest_effective_plastic_strain(d3plot)

    print(eps.shape)

def try_find_edge_nodes():
    d3plot = D3plot(f'run_sets/{RUN_ID}/d3plot')
    gauge_edge_nodes_ids = dyna_tools._find_gauge_edge_nodes_ids(d3plot)
    print(gauge_edge_nodes_ids.shape)
    print(gauge_edge_nodes_ids)

def try_find_summary():
    d3plot = D3plot(f'run_sets/{RUN_ID}/d3plot')
    binout = Binout(f'run_sets/{RUN_ID}/binout*')
    summary = dyna_tools.find_summary(binout, d3plot)
    print(summary)

def try_save_summary():
    d3plot = D3plot(f'run_sets/{RUN_ID}/d3plot')
    binout = Binout(f'run_sets/{RUN_ID}/binout*')
    summary = outputs.find_summary(binout, d3plot)
    print(summary)
    outputs.save_summary(summary, f'run_sets/{RUN_ID}/summary.csv')
    print('Summary saved to run_sets/{RUN_ID}/summary.csv')

def try_plot_summary():
    from matplotlib import pyplot as plt
    d3plot = D3plot(f'run_sets/{RUN_ID}/d3plot')
    binout = Binout(f'run_sets/{RUN_ID}/binout*')
    summary = outputs.find_summary(binout, d3plot)
    outputs.plot_force_vs_displacement(summary)
    plt.show()

# def try_find_specimen_displacement():
#     binout = Binout(f'run_sets/{RUN_ID}/binout*')
#     d3plot = D3plot(f'run_sets/{RUN_ID}/d3plot')
#     specimen_displacement = dyna_tools.find_specimen_displacement(binout, d3plot)
#     print(specimen_displacement.shape)
#     print(specimen_displacement)

if __name__ == '__main__':
    # try_find_nodes()
    # try_find_specimen_load()
    # try_stuff()
    # try_binout()
    # try_find_specimen_load()
    # try_find_specimen_displacement()
    # dyna_tools.run_lsdyna('0002_basic', '0002_basic_run1')
    # try_find_effective_plastic_strain()
    # try_find_edge_nodes()
    # try_find_summary()
    # try_find_specimen_displacement()
    try_save_summary()
    # try_plot_summary()