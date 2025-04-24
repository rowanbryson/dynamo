import tools
from lasso.dyna import Binout, D3plot, ArrayType
import numpy as np
from matplotlib import pyplot as plt

# RUN_ID = '0005_basic_run3'

def main():
    # run_script('0015_SNS5_run2')
    # get_eps_tri_time('0015_SNS5_run2', [5, 6, 7, 8, 9])
    # get_eps_tri_time('0025_SNM5_run2', [1, 12, 11, 10, 9])
    # get_eps_tri_time('0035_SNL5_run2', [1, 12, 11, 10, 9])
    # plot_eps_tri_time_6()
    # plot_eps_tri_time_5()
    plot_eps_tri_time_5_with_johnson()

def plot_eps_tri_time_6():
    DISPLACEMENT_AT_FRACTURE_SNS5 = (0.0525 + 0.0425 + 0.0475) / 3
    DISPLACEMENT_AT_FRACTURE_SNM5 = (0.06 + 0.058 + 0.062) / 3
    DISPLACEMENT_AT_FRACTURE_SNL5 = (0.08 + 0.08 + 0.085) / 3

    TIME_AT_FRACTURE_SNS5 = (DISPLACEMENT_AT_FRACTURE_SNS5 / 0.1574804) * 100
    TIME_AT_FRACTURE_SNM5 = (DISPLACEMENT_AT_FRACTURE_SNM5 / 0.1574804) * 100
    TIME_AT_FRACTURE_SNL5 = (DISPLACEMENT_AT_FRACTURE_SNL5 / 0.1574804) * 100
    print(f'TIME AT FRACTURE: SNS: {TIME_AT_FRACTURE_SNS5}')
    print(f'TIME AT FRACTURE: SNM: {TIME_AT_FRACTURE_SNM5}')
    print(f'TIME AT FRACTURE: SNL: {TIME_AT_FRACTURE_SNL5}')


    EPS_AT_FRACTURE_TENSION_BAR_1 = 0.0745734993134432
    EPS_AT_FRACTURE_TENSION_BAR_2 = 0.0609865379304494
    EPS_AT_FRACTURE_TENSION_BAR_3 = 0.107108788997506
    EPS_AT_FRACTURE_TENSION_BAR_4 = 0.0397820620995518
    EPS_AT_FRACTURE_TENSION_BAR_5 = 0.066960232403737

    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_1 = 0.33
    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_2 = 0.33
    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_3 = 0.33
    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_4 = 0.33
    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_5 = 0.33

    EPS_TENSION = [EPS_AT_FRACTURE_TENSION_BAR_1, EPS_AT_FRACTURE_TENSION_BAR_2, EPS_AT_FRACTURE_TENSION_BAR_3, EPS_AT_FRACTURE_TENSION_BAR_4, EPS_AT_FRACTURE_TENSION_BAR_5]
    TRIAXIALITY_TENSION = [TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_1, TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_2, TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_3, TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_4, TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_5]

    eps_sns5, triaxiality_sns5, time_sns5 = get_eps_tri_time('0016_SNS6_run2', [5, 6, 7, 8, 9])
    eps_snm5, triaxiality_snm5, time_snm5 = get_eps_tri_time('0026_SNM6_run2', [1, 12, 11, 10, 9])
    eps_snl5, triaxiality_snl5, time_snl5 = get_eps_tri_time('0036_SNL6_run2', [1, 12, 11, 10, 9])

    eps_at_fracture_snl5, triaxiality_avg_before_fracture_snl5 = average_eps_tri(eps_snl5, triaxiality_snl5, time_snl5, TIME_AT_FRACTURE_SNL5)
    eps_at_fracture_snm5, triaxiality_avg_before_fracture_snm5 = average_eps_tri(eps_snm5, triaxiality_snm5, time_snm5, TIME_AT_FRACTURE_SNM5)
    eps_at_fracture_sns5, triaxiality_avg_before_fracture_sns5 = average_eps_tri(eps_sns5, triaxiality_sns5, time_sns5, TIME_AT_FRACTURE_SNS5)

    triaxialities = [triaxiality_avg_before_fracture_sns5, triaxiality_avg_before_fracture_snm5, triaxiality_avg_before_fracture_snl5]
    eps_at_fractures = [eps_at_fracture_sns5, eps_at_fracture_snm5, eps_at_fracture_snl5]
    print(f'Triaxiality avg before fracture: {triaxialities}')
    print(f'Eps at fracture: {eps_at_fractures}')

    plt.figure()
    plt.xlabel('Stress Triaxiality')
    plt.ylabel('Effective Plastic Strain')
    plt.plot([triaxiality_avg_before_fracture_sns5, triaxiality_avg_before_fracture_snm5, triaxiality_avg_before_fracture_snl5],
             [eps_at_fracture_sns5, eps_at_fracture_snm5, eps_at_fracture_snl5], 
             'x', label='Compression Testing')
    plt.text(triaxiality_avg_before_fracture_sns5, eps_at_fracture_sns5, f'SNS', fontsize=8, ha='right', va='bottom')
    plt.text(triaxiality_avg_before_fracture_snm5, eps_at_fracture_snm5, f'SNM', fontsize=8, ha='right', va='bottom')
    plt.text(triaxiality_avg_before_fracture_snl5, eps_at_fracture_snl5, f'SNL', fontsize=8, ha='right', va='bottom')

    plt.plot(TRIAXIALITY_TENSION,
             EPS_TENSION,
                'x', label='Tension Testing')
    plt.grid()
    plt.ylim(bottom=0)
    plt.legend()
    plt.tight_layout()
    plt.savefig('meta_plots/locus.png')
    plt.xlim(-1.5, 1.5)
    # plt.tight_layout()
    plt.savefig('meta_plots/locus_limited.png')
    plt.show()

def plot_eps_tri_time_5():
    DISPLACEMENT_AT_FRACTURE_SNS5 = (0.0525 + 0.0425 + 0.0475) / 3
    DISPLACEMENT_AT_FRACTURE_SNM5 = (0.06 + 0.058 + 0.062) / 3
    DISPLACEMENT_AT_FRACTURE_SNL5 = (0.08 + 0.08 + 0.085) / 3

    TIME_AT_FRACTURE_SNS5 = (DISPLACEMENT_AT_FRACTURE_SNS5 / 0.1574804) * 100
    TIME_AT_FRACTURE_SNM5 = (DISPLACEMENT_AT_FRACTURE_SNM5 / 0.1574804) * 100
    TIME_AT_FRACTURE_SNL5 = (DISPLACEMENT_AT_FRACTURE_SNL5 / 0.1574804) * 100
    print(f'TIME AT FRACTURE: SNS: {TIME_AT_FRACTURE_SNS5}')
    print(f'TIME AT FRACTURE: SNM: {TIME_AT_FRACTURE_SNM5}')
    print(f'TIME AT FRACTURE: SNL: {TIME_AT_FRACTURE_SNL5}')


    EPS_AT_FRACTURE_TENSION_BAR_1 = 0.0745734993134432
    EPS_AT_FRACTURE_TENSION_BAR_2 = 0.0609865379304494
    EPS_AT_FRACTURE_TENSION_BAR_3 = 0.107108788997506
    EPS_AT_FRACTURE_TENSION_BAR_4 = 0.0397820620995518
    EPS_AT_FRACTURE_TENSION_BAR_5 = 0.066960232403737

    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_1 = 0.33
    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_2 = 0.33
    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_3 = 0.33
    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_4 = 0.33
    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_5 = 0.33

    EPS_TENSION = [EPS_AT_FRACTURE_TENSION_BAR_1, EPS_AT_FRACTURE_TENSION_BAR_2, EPS_AT_FRACTURE_TENSION_BAR_3, EPS_AT_FRACTURE_TENSION_BAR_4, EPS_AT_FRACTURE_TENSION_BAR_5]
    TRIAXIALITY_TENSION = [TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_1, TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_2, TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_3, TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_4, TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_5]

    eps_sns5, triaxiality_sns5, time_sns5 = get_eps_tri_time('0015_SNS5_run4', [5, 6, 7, 8, 9])
    eps_snm5, triaxiality_snm5, time_snm5 = get_eps_tri_time('0025_SNM5_run4', [1, 12, 11, 10, 9])
    eps_snl5, triaxiality_snl5, time_snl5 = get_eps_tri_time('0035_SNL5_run4', [1, 12, 11, 10, 9])

    eps_at_fracture_snl5, triaxiality_avg_before_fracture_snl5 = average_eps_tri(eps_snl5, triaxiality_snl5, time_snl5, TIME_AT_FRACTURE_SNL5)
    eps_at_fracture_snm5, triaxiality_avg_before_fracture_snm5 = average_eps_tri(eps_snm5, triaxiality_snm5, time_snm5, TIME_AT_FRACTURE_SNM5)
    eps_at_fracture_sns5, triaxiality_avg_before_fracture_sns5 = average_eps_tri(eps_sns5, triaxiality_sns5, time_sns5, TIME_AT_FRACTURE_SNS5)

    triaxialities = [triaxiality_avg_before_fracture_sns5, triaxiality_avg_before_fracture_snm5, triaxiality_avg_before_fracture_snl5]
    eps_at_fractures = [eps_at_fracture_sns5, eps_at_fracture_snm5, eps_at_fracture_snl5]
    print(f'Triaxiality avg before fracture: {triaxialities}')
    print(f'Eps at fracture: {eps_at_fractures}')

    plt.figure()
    plt.xlabel('Stress Triaxiality')
    plt.ylabel('Effective Plastic Strain')
    plt.plot([triaxiality_avg_before_fracture_sns5, triaxiality_avg_before_fracture_snm5, triaxiality_avg_before_fracture_snl5],
             [eps_at_fracture_sns5, eps_at_fracture_snm5, eps_at_fracture_snl5], 
             'x', label='Compression Testing')
    plt.text(triaxiality_avg_before_fracture_sns5, eps_at_fracture_sns5, f'SNS', fontsize=8, ha='right', va='bottom')
    plt.text(triaxiality_avg_before_fracture_snm5, eps_at_fracture_snm5, f'SNM', fontsize=8, ha='right', va='bottom')
    plt.text(triaxiality_avg_before_fracture_snl5, eps_at_fracture_snl5, f'SNL', fontsize=8, ha='right', va='bottom')

    plt.plot(TRIAXIALITY_TENSION,
             EPS_TENSION,
                'x', label='Tension Testing')
    plt.grid()
    plt.ylim(bottom=0)
    plt.legend()
    plt.tight_layout()
    plt.savefig('meta_plots/locus5.png')
    plt.xlim(-1.5, 1.5)
    # plt.tight_layout()
    plt.savefig('meta_plots/locus5_limited.png')
    plt.show()

def plot_eps_tri_time_5_with_johnson():
    DISPLACEMENT_AT_FRACTURE_SNS5 = (0.0525 + 0.0425 + 0.0475) / 3
    DISPLACEMENT_AT_FRACTURE_SNM5 = (0.06 + 0.058 + 0.062) / 3
    DISPLACEMENT_AT_FRACTURE_SNL5 = (0.08 + 0.08 + 0.085) / 3

    TIME_AT_FRACTURE_SNS5 = (DISPLACEMENT_AT_FRACTURE_SNS5 / 0.1574804) * 100
    TIME_AT_FRACTURE_SNM5 = (DISPLACEMENT_AT_FRACTURE_SNM5 / 0.1574804) * 100
    TIME_AT_FRACTURE_SNL5 = (DISPLACEMENT_AT_FRACTURE_SNL5 / 0.1574804) * 100
    print(f'TIME AT FRACTURE: SNS: {TIME_AT_FRACTURE_SNS5}')
    print(f'TIME AT FRACTURE: SNM: {TIME_AT_FRACTURE_SNM5}')
    print(f'TIME AT FRACTURE: SNL: {TIME_AT_FRACTURE_SNL5}')


    EPS_AT_FRACTURE_TENSION_BAR_1 = 0.0745734993134432
    EPS_AT_FRACTURE_TENSION_BAR_2 = 0.0609865379304494
    EPS_AT_FRACTURE_TENSION_BAR_3 = 0.107108788997506
    EPS_AT_FRACTURE_TENSION_BAR_4 = 0.0397820620995518
    EPS_AT_FRACTURE_TENSION_BAR_5 = 0.066960232403737

    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_1 = 0.33
    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_2 = 0.33
    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_3 = 0.33
    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_4 = 0.33
    TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_5 = 0.33

    EPS_TENSION = [EPS_AT_FRACTURE_TENSION_BAR_1, EPS_AT_FRACTURE_TENSION_BAR_2, EPS_AT_FRACTURE_TENSION_BAR_3, EPS_AT_FRACTURE_TENSION_BAR_4, EPS_AT_FRACTURE_TENSION_BAR_5]
    TRIAXIALITY_TENSION = [TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_1, TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_2, TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_3, TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_4, TRIAXIALITY_AVG_BEFORE_FRACTURE_TENSION_BAR_5]

    eps_sns5, triaxiality_sns5, time_sns5 = get_eps_tri_time('0015_SNS5_run4', [5, 6, 7, 8, 9])
    eps_snm5, triaxiality_snm5, time_snm5 = get_eps_tri_time('0025_SNM5_run4', [1, 12, 11, 10, 9])
    eps_snl5, triaxiality_snl5, time_snl5 = get_eps_tri_time('0035_SNL5_run4', [1, 12, 11, 10, 9])

    eps_at_fracture_snl5, triaxiality_avg_before_fracture_snl5 = average_eps_tri(eps_snl5, triaxiality_snl5, time_snl5, TIME_AT_FRACTURE_SNL5)
    eps_at_fracture_snm5, triaxiality_avg_before_fracture_snm5 = average_eps_tri(eps_snm5, triaxiality_snm5, time_snm5, TIME_AT_FRACTURE_SNM5)
    eps_at_fracture_sns5, triaxiality_avg_before_fracture_sns5 = average_eps_tri(eps_sns5, triaxiality_sns5, time_sns5, TIME_AT_FRACTURE_SNS5)

    triaxialities = [triaxiality_avg_before_fracture_sns5, triaxiality_avg_before_fracture_snm5, triaxiality_avg_before_fracture_snl5]
    eps_at_fractures = [eps_at_fracture_sns5, eps_at_fracture_snm5, eps_at_fracture_snl5]
    print(f'Triaxiality avg before fracture: {triaxialities}')
    print(f'Eps at fracture: {eps_at_fractures}')

    plt.figure()
    plt.xlabel('Stress Triaxiality')
    plt.ylabel('Effective Plastic Strain')
    plt.plot([triaxiality_avg_before_fracture_sns5, triaxiality_avg_before_fracture_snm5, triaxiality_avg_before_fracture_snl5],
             [eps_at_fracture_sns5, eps_at_fracture_snm5, eps_at_fracture_snl5], 
             'x', label='Compression Testing')
    plt.text(triaxiality_avg_before_fracture_sns5, eps_at_fracture_sns5, f'SNS', fontsize=8, ha='right', va='bottom')
    plt.text(triaxiality_avg_before_fracture_snm5, eps_at_fracture_snm5, f'SNM', fontsize=8, ha='right', va='bottom')
    plt.text(triaxiality_avg_before_fracture_snl5, eps_at_fracture_snl5, f'SNL', fontsize=8, ha='right', va='bottom')

    plt.plot(TRIAXIALITY_TENSION,
             EPS_TENSION,
                'x', label='Tension Testing')

    johnson_triax_axis = np.linspace(-1, 1, 100)
    D1, D2, D3 = 77.46e-3, 34.48e-3, 4.164
    johnson_eps_axis = D1 + D2 * np.exp(-D3 * johnson_triax_axis)

    plt.plot(johnson_triax_axis, johnson_eps_axis, linestyle=':', label='Johnson-Cooke Fracture Model')

    plt.grid()
    plt.ylim(bottom=0)
    plt.legend()
    plt.tight_layout()
    plt.savefig('meta_plots/locus5_with_johnson.png')
    plt.xlim(-1.1, 1)
    plt.ylim(top=0.5)
    # plt.tight_layout()
    plt.savefig('meta_plots/locus5_limited_with_johnson.png')
    plt.show()

def average_eps_tri(eps, triaxiality, time, time_at_fracture):
    # Calculate the average of eps and triaxiality over time
    avg_eps = np.nanmean(eps)
    avg_triaxiality = np.nanmean(triaxiality)

    # Find the index of the time of fracture
    idx = np.argmin(np.abs(time - time_at_fracture))
    print(idx)

    print(f'time: {time[idx]}')

    eps_at_fracture = eps[idx]
    triaxiality_before_fracture = triaxiality[:idx]
    triaxiality_at_fracture = triaxiality[idx]

    triaxiality_avg_before_fracture = np.nanmean(triaxiality_before_fracture[1:], axis=0)
    print(triaxiality_before_fracture)
    print(triaxiality_avg_before_fracture)
    # mean and ignore nan values

    # print(triaxiality_avg_before_fracture)

    # plt.figure()
    # plt.plot(triaxiality_before_fracture, eps[:idx], 'x', label='Compression Testing')
    # plt.xlabel('Stress Triaxiality')
    # plt.ylabel('Effective Plastic Strain')
    # plt.title('Compression Testing')
    # plt.grid()
    # plt.legend()
    # plt.ylim(bottom=0)
    # plt.show()

    return eps_at_fracture, triaxiality_avg_before_fracture
    # return eps_at_fracture, triaxiality_at_fracture


def get_eps_tri_time(run_id, gauge_edge_node_ids=None):
    binout = Binout(f'run_sets/{run_id}/binout*')
    d3plot = D3plot(f'run_sets/{run_id}/d3plot')

    if gauge_edge_node_ids is None:
        gauge_edge_node_ids = tools.extract.extract_gauge_edge_nodes_ids(d3plot)
        print(gauge_edge_node_ids.shape)
    else:
        gauge_edge_node_ids = np.array(gauge_edge_node_ids)

    print(f'Gauge edge node ids: {gauge_edge_node_ids}')
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


    avg_triaxiality = np.nanmean(triaxiality, axis=1)
    avg_sig_vm = np.nanmean(sig_vm, axis=1)
    avg_eps = np.nanmean(eps, axis=1)


    time = binout.read('bndout', 'velocity', 'nodes', 'time')
    print(avg_triaxiality)
    return avg_eps, avg_triaxiality, time



if __name__ == '__main__':
    # run_script(RUN_ID)
    main()
