from lasso.dyna import Binout, ArrayType
import numpy as np

def extract_gauge_edge_nodes_ids(d3plot):
    """
    Find the nodes at the edge of the gauge section
    """
    # get the node ids and coordinates
    node_ids = d3plot.arrays[ArrayType.node_ids]
    node_coordinates = d3plot.arrays[ArrayType.node_coordinates]

    # find the nodes in the gauge section
    gauge_z = 0
    gauge_nodemask = (node_coordinates[:, 2] == gauge_z)

    gauge_ids = node_ids[gauge_nodemask]
    gauge_node_coordinates = node_coordinates[gauge_nodemask]

    gauge_radii = np.sqrt(gauge_node_coordinates[:, 0]**2 + gauge_node_coordinates[:, 1]**2)
    gauge_edge_radius = np.max(gauge_radii)

    gauge_edge_node_ids = gauge_ids[np.isclose(gauge_radii, gauge_edge_radius, atol=gauge_edge_radius*0.1)]
    return gauge_edge_node_ids

def extract_stress_tensor(binout):
    sig_xx = binout.read('eloutdet', 'sig_xx')
    sig_yy = binout.read('eloutdet', 'sig_yy')
    sig_zz = binout.read('eloutdet', 'sig_zz')
    sig_xy = binout.read('eloutdet', 'sig_xy')
    sig_xz = binout.read('eloutdet', 'sig_xz')
    sig_yz = binout.read('eloutdet', 'sig_yz')
    stress_tensor = np.zeros((sig_xx.shape[0], 6))
    stress_tensor[:, 0] = sig_xx[:, 0]
    stress_tensor[:, 1] = sig_yy[:, 0]
    stress_tensor[:, 2] = sig_zz[:, 0]
    stress_tensor[:, 3] = sig_xy[:, 0]
    stress_tensor[:, 4] = sig_xz[:, 0]
    stress_tensor[:, 5] = sig_yz[:, 0]
    
    return stress_tensor

def extract_specimen_displacement(binout):
    displacement = binout.read('nodout', 'z_displacement')
    face_node_index = find_face_node_index(binout)
    # extract the z displacement of the face node
    face_node_displacement = -displacement[:, face_node_index]
    return face_node_displacement

def find_face_node_index(binout):
    # find node coords
    ids = binout.read('nodout', 'ids')
    node_coords = binout.read('nodout', 'z_coordinate')[0]
    # find id associate with max z coordinate
    max_z = np.max(node_coords)
    max_z_index = np.where(node_coords == max_z)[0][0]
    return max_z_index


if __name__ == '__main__':
    run_id = '0002_basic_run1'
    binout = Binout(f'run_sets/{run_id}/binout*')
    # extract_specimen_displacement(binout)
    print(find_face_node_index(binout))
    print(extract_specimen_displacement(binout))