import tools
from lasso.dyna import Binout, D3plot, ArrayType
import numpy as np

RUN_ID = '0005_basic_run3'

def run_script(run_id):
    binout = Binout(f'run_sets/{run_id}/binout*')
    d3plot = D3plot(f'run_sets/{run_id}/d3plot')

    gauge_edge_node_ids = tools.extract.extract_gauge_edge_nodes_ids(d3plot)
    nodavg_ids = binout.read('eloutdet', 'nodavg', 'ids')[0]
    idx = np.isin(nodavg_ids, gauge_edge_node_ids)

    sig_xx = binout.read('eloutdet', 'nodavg', 'lower_sig_xx')[:, idx]
    sig_yy = binout.read('eloutdet', 'nodavg', 'lower_sig_yy')[:, idx]
    sig_zz = binout.read('eloutdet', 'nodavg', 'lower_sig_zz')[:, idx]
    sig_xy = binout.read('eloutdet', 'nodavg', 'lower_sig_xy')[:, idx]
    sig_xz = binout.read('eloutdet', 'nodavg', 'lower_sig_zx')[:, idx]
    sig_yz = binout.read('eloutdet', 'nodavg', 'lower_sig_yz')[:, idx]

    eps_xx = binout.read('eloutdet', 'nodavg', 'lower_eps_xx')[:, idx]
    eps_yy = binout.read('eloutdet', 'nodavg', 'lower_eps_yy')[:, idx]
    eps_zz = binout.read('eloutdet', 'nodavg', 'lower_eps_zz')[:, idx]
    eps_xy = binout.read('eloutdet', 'nodavg', 'lower_eps_xy')[:, idx]
    eps_xz = binout.read('eloutdet', 'nodavg', 'lower_eps_zx')[:, idx]
    eps_yz = binout.read('eloutdet', 'nodavg', 'lower_eps_yz')[:, idx]

    sig_tensor = np.zeros((sig_xx.shape[0], sig_xx.shape[1], 6))
    sig_tensor[:, :, 0] = sig_xx
    sig_tensor[:, :, 1] = sig_yy
    sig_tensor[:, :, 2] = sig_zz
    sig_tensor[:, :, 3] = sig_xy
    sig_tensor[:, :, 4] = sig_xz
    sig_tensor[:, :, 5] = sig_yz

    eps_tensor = np.zeros((eps_xx.shape[0], eps_xx.shape[1], 6))
    eps_tensor[:, :, 0] = eps_xx
    eps_tensor[:, :, 1] = eps_yy
    eps_tensor[:, :, 2] = eps_zz
    eps_tensor[:, :, 3] = eps_xy
    eps_tensor[:, :, 4] = eps_xz
    eps_tensor[:, :, 5] = eps_yz

    sig_hydrostatic_pressure = 1/3 * (sig_tensor[:, :, 0] + sig_tensor[:, :, 1] + sig_tensor[:, :, 2])
    sig_deviator = np.zeros((sig_tensor.shape[0], sig_tensor.shape[1], 6))
    sig_deviator[:, :, 0] = sig_tensor[:, :, 0] - sig_hydrostatic_pressure
    sig_deviator[:, :, 1] = sig_tensor[:, :, 1] - sig_hydrostatic_pressure
    sig_deviator[:, :, 2] = sig_tensor[:, :, 2] - sig_hydrostatic_pressure
    sig_deviator[:, :, 3] = sig_tensor[:, :, 3]
    sig_deviator[:, :, 4] = sig_tensor[:, :, 4]
    sig_deviator[:, :, 5] = sig_tensor[:, :, 5]

    eps_hydrostatic_pressure = 1/3 * (eps_tensor[:, :, 0] + eps_tensor[:, :, 1] + eps_tensor[:, :, 2])
    eps_deviator = np.zeros((eps_hydrostatic_pressure.shape[0], eps_hydrostatic_pressure.shape[1], 6))
    eps_deviator[:, :, 0] = eps_tensor[:, :, 0] - eps_hydrostatic_pressure
    eps_deviator[:, :, 1] = eps_tensor[:, :, 1] - eps_hydrostatic_pressure
    eps_deviator[:, :, 2] = eps_tensor[:, :, 2] - eps_hydrostatic_pressure
    eps_deviator[:, :, 3] = eps_tensor[:, :, 3]
    eps_deviator[:, :, 4] = eps_tensor[:, :, 4]
    eps_deviator[:, :, 5] = eps_tensor[:, :, 5]

    sig_J2 = 0.5 * (sig_deviator[:, :, 0]**2 + sig_deviator[:, :, 1]**2 + sig_deviator[:, :, 2]**2 + 2 * (sig_deviator[:, :, 3]**2 + sig_deviator[:, :, 4]**2 + sig_deviator[:, :, 5]**2))
    sig_vm = np.sqrt(3/2 * 2 * sig_J2)
    triaxiality = sig_hydrostatic_pressure / sig_vm

    eps_J2 = 0.5 * (eps_deviator[:, :, 0]**2 + eps_deviator[:, :, 1]**2 + eps_deviator[:, :, 2]**2 + 2 * (eps_deviator[:, :, 3]**2 + eps_deviator[:, :, 4]**2 + eps_deviator[:, :, 5]**2))
    eps = np.sqrt(2/3 * 2 * eps_J2)


    avg_triaxiality = np.mean(triaxiality, axis=1)
    avg_sig_vm = np.mean(sig_vm, axis=1)
    avg_eps = np.mean(eps, axis=1)

    from matplotlib import pyplot as plt
    plt.figure()
    for i in range(gauge_edge_node_ids.shape[0]):
        plt.plot(triaxiality[:, i], eps[:, i], label=f'Element {gauge_edge_node_ids[i]}', alpha=0.5)
    plt.plot(avg_triaxiality, avg_eps, label='Average', color='black', linewidth=2)
    plt.xlabel('Triaxiality')
    plt.ylabel('Effective Plastic Strain')
    plt.title('Triaxiality vs Effective Plastic Strain @ Gauge Edge')
    plt.legend()
    plt.grid()
    # plt.show()
    plt.savefig(f'summaries/{run_id}/triaxiality_vs_eps.png')

    plt.figure()
    for i in range(gauge_edge_node_ids.shape[0]):
        plt.plot(eps[:, i], sig_vm[:, i], label=f'Element {gauge_edge_node_ids[i]}', alpha=0.5)
    plt.plot(avg_eps, avg_sig_vm, label='Average', color='black', linewidth=2)
    plt.xlabel('Effective Plastic Strain')
    plt.ylabel('Von Mises Stress')
    plt.title('Von Mises Stress vs Effective Plastic Strain @ Gauge Edge')
    plt.legend()
    plt.grid()
    # plt.show()
    plt.savefig(f'summaries/{run_id}/eps_vs_vm.png')

    time = binout.read('bndout', 'velocity', 'nodes', 'time')

    # triaxiality and effective plastic strain vs time
    plt.figure()
    for i in range(gauge_edge_node_ids.shape[0]):
        plt.plot(time, triaxiality[:, i], label=f'Element {gauge_edge_node_ids[i]}', alpha=0.5)
    plt.plot(time, avg_triaxiality, label='Average', color='black', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Triaxiality')
    plt.title('Triaxiality vs Time @ Gauge Edge')
    plt.legend()
    plt.grid()
    # plt.show()

    plt.savefig(f'summaries/{run_id}/triaxiality_vs_time.png')

    # effective plastic strain vs time
    plt.figure()
    for i in range(gauge_edge_node_ids.shape[0]):
        plt.plot(time, eps[:, i], label=f'Node {gauge_edge_node_ids[i]}', alpha=0.5)
    plt.plot(time, avg_eps, label='Average', color='black', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Effective Plastic Strain')
    plt.title('Effective Plastic Strain vs Time @ Gauge Edge')
    plt.legend()
    plt.grid()
    # plt.show()
    plt.savefig(f'summaries/{run_id}/eps_vs_time.png')

if __name__ == '__main__':
    run_script(RUN_ID)
