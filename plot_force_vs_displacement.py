import tools
import numpy as np
from matplotlib import pyplot as plt
from lasso.dyna import Binout, D3plot, ArrayType


# RUN_ID = '0015_SNS5_run1'
# RUN_ID = '0025_SNM5_run1'
# RUN_ID = '0035_SNL5_run1'

def main():
    # # make_plot('0015_SNS5_run2')
    # # make_plot('0025_SNM5_run2')
    # make_plot('0033_SNL3_run2')
    # # experiment_vs_simulation_plot()
    # combo_plot_SNS()
    # combo_plot_SNM()
    # combo_plot_SNL()
    # plot_run('0035_SNL5_run4')
    # plot_run('0015_SNS5_run4')
    # plot_run('0025_SNM5_run4')
    # plot_run('0035_SNL5_run5')
    make_plot('0016_SNS6_run2')
    make_plot('0026_SNM6_run2')
    make_plot('0036_SNL6_run2')
    # combo_plot_SNL()


def combo_plot_SNS():
    plt.figure()
    plot_experiment('experimental_data/9011_SNS_test1/SNSDisplacement1.csv', 'experimental_data/9011_SNS_test1/SNSForce1.csv', color='C0', label='Test 1')
    plot_experiment('experimental_data/9011_SNS_test1/SNSDisplacement1.csv', 'experimental_data/9011_SNS_test1/SNSForce1.csv', smoothed=True, color='C0', alpha=0.5)
     
    plot_experiment('experimental_data/9012_SNS_test2/SNSDisplacement2.csv', 'experimental_data/9012_SNS_test2/SNSForce2.csv', color='C1', label='Test 2')
    plot_experiment('experimental_data/9012_SNS_test2/SNSDisplacement2.csv', 'experimental_data/9012_SNS_test2/SNSForce2.csv', smoothed=True, color='C1', alpha=0.5)
     
    plot_experiment('experimental_data/9013_SNS_test3/SNSDisplacement3.csv', 'experimental_data/9013_SNS_test3/SNSForce3.csv', color='C2', label='Test 3')
    plot_experiment('experimental_data/9013_SNS_test3/SNSDisplacement3.csv', 'experimental_data/9013_SNS_test3/SNSForce3.csv', smoothed=True, color='C2', alpha=0.5)
    

    plot_run('0015_SNS5_run4', smoothed=False, color='C4', label='Simulation', alpha=0.5)
    plot_run('0015_SNS5_run4', smoothed=True, color='C4')

    plt.xlabel('Displacement (inch)')
    plt.ylabel('Force (lbf)')
    plt.legend()
    plt.grid()
    plt.savefig(f'meta_plots/SNS_force_vs_displacement-3.png')
    plt.show()

def combo_plot_SNM():
    plt.figure()
    plot_experiment('experimental_data/9021_SNM_test1/SNMDisplacement1.csv', 'experimental_data/9021_SNM_test1/SNMForce1.csv', color='C0', label='Test 1')
    plot_experiment('experimental_data/9021_SNM_test1/SNMDisplacement1.csv', 'experimental_data/9021_SNM_test1/SNMForce1.csv', smoothed=True, color='C0', alpha=0.5)
     
    plot_experiment('experimental_data/9022_SNM_test2/SNMDisplacement2.csv', 'experimental_data/9022_SNM_test2/SNMForce2.csv', color='C1', label='Test 2')
    plot_experiment('experimental_data/9022_SNM_test2/SNMDisplacement2.csv', 'experimental_data/9022_SNM_test2/SNMForce2.csv', smoothed=True, color='C1', alpha=0.5)
     
    plot_experiment('experimental_data/9023_SNM_test3/SNMDisplacement3.csv', 'experimental_data/9023_SNM_test3/SNMForce3.csv', color='C2', label='Test 3')
    plot_experiment('experimental_data/9023_SNM_test3/SNMDisplacement3.csv', 'experimental_data/9023_SNM_test3/SNMForce3.csv', smoothed=True, color='C2', alpha=0.5)
    
    plot_run('0025_SNM5_run4', smoothed=False, color='C4', label='Simulation', alpha=0.5)
    plot_run('0025_SNM5_run4', smoothed=True, color='C4')

    plt.xlabel('Displacement (inch)')
    plt.ylabel('Force (lbf)')
    plt.legend()
    plt.grid()
    plt.savefig(f'meta_plots/SNM_force_vs_displacement-3.png')
    plt.show()

def combo_plot_SNL():
    plt.figure()
    plot_experiment('experimental_data/9031_SNL_test1/SNLDisplacement1.csv', 'experimental_data/9031_SNL_test1/SNLForce1.csv', color='C0', label='Test 1')
    plot_experiment('experimental_data/9031_SNL_test1/SNLDisplacement1.csv', 'experimental_data/9031_SNL_test1/SNLForce1.csv', smoothed=True, color='C0', alpha=0.5)
     
    plot_experiment('experimental_data/9032_SNL_test2/SNLDisplacement2.csv', 'experimental_data/9032_SNL_test2/SNLForce2.csv', color='C1', label='Test 2')
    plot_experiment('experimental_data/9032_SNL_test2/SNLDisplacement2.csv', 'experimental_data/9032_SNL_test2/SNLForce2.csv', smoothed=True, color='C1', alpha=0.5)
     
    plot_experiment('experimental_data/9033_SNL_test3/SNLDisplacement3.csv', 'experimental_data/9033_SNL_test3/SNLForce3.csv', color='C2', label='Test 3')
    plot_experiment('experimental_data/9033_SNL_test3/SNLDisplacement3.csv', 'experimental_data/9033_SNL_test3/SNLForce3.csv', smoothed=True, color='C2', alpha=0.5)
    
    plot_run('0035_SNL5_run5', smoothed=False, color='C4', label='Simulation', alpha=0.5)
    plot_run('0035_SNL5_run5', smoothed=True, color='C4')

    plt.xlabel('Displacement (inch)')
    plt.ylabel('Force (lbf)')
    plt.legend()
    plt.grid()
    plt.savefig(f'meta_plots/SNL_force_vs_displacement-3.png')
    plt.show()

def plot_experiment(filepath_disp, filepath_force, smoothed=False, **kwargs):
    INITIAL_FORCE = 15
    INITIAL_DISP = 0.16
    BUFFER = 20
    PRE_TIME = 30  # seconds before 0 to show
    N_INTERPOLATE = 100  # number of points to interpolate to
    N_SMOOTH_KERNEL = 10


    def displacement_calibration_volts_to_inch(volts):
            return volts * 0.518713

    disp_exp = np.genfromtxt(filepath_disp, skip_header=23)
    disp_exp_time = disp_exp[:, 0]
    disp_exp_volts = disp_exp[:, 1]

    force_exp = np.genfromtxt(filepath_force, skip_header=7, delimiter=',')
    force_exp_time = force_exp[:, 1].astype(float)
    force_exp_force = force_exp[:, 2].astype(float)

    # find first index of disp_exp_displacement where disp_exp_displacement is greater than 0.16
    initial_disp_index = np.argmax(disp_exp_volts > INITIAL_DISP) - 5
    disp_exp_displacement_modified = displacement_calibration_volts_to_inch(disp_exp[:, 1] - disp_exp[initial_disp_index, 1])
    disp_exp_time_modified = disp_exp_time[:] - disp_exp_time[initial_disp_index]

    initial_force_index = np.argmax(force_exp_force > INITIAL_FORCE) - 5
    force_exp_force_modified = force_exp[:, 2].astype(float) - force_exp_force[initial_force_index]
    force_exp_time_modified = force_exp_time[:] - force_exp_time[initial_force_index]
    print(initial_disp_index)

    plot_time = np.linspace(-PRE_TIME, disp_exp_time_modified[-1], N_INTERPOLATE)
    # interpolate the experimental data to match the simulation data
    plot_displacement = np.interp(plot_time, disp_exp_time_modified, disp_exp_displacement_modified)
    plot_force = np.interp(plot_time, force_exp_time_modified, force_exp_force_modified)

    # apply a time average to the data using a kernel
    kernel = np.ones(N_SMOOTH_KERNEL) / N_SMOOTH_KERNEL
    plot_displacement_smoothed = np.convolve(plot_displacement, kernel, mode='valid')
    plot_force_smoothed = np.convolve(plot_force, kernel, mode='valid')


    plt.figure(1)
    if smoothed:
        plt.plot(plot_displacement, plot_force, **kwargs)
    else:
        plt.plot(plot_displacement_smoothed, plot_force_smoothed, **kwargs)
    # plt.xlabel('Displacement (inches)')
    # plt.ylabel('Force (lbf)')
    # plt.title('Force vs Displacement')
    # plt.grid()

    # plt.legend()
    # plt.savefig(f'meta_plots/force_vs_displacement.png')
    # plt.show()


    # plt.figure(2)
    # plt.subplot(2, 1, 1)
    # plt.plot(disp_exp_time_modified, disp_exp_displacement_modified, label='Experimental Data', color='red')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Displacement (mm)')
    # plt.title('Displacement vs Time')
    # plt.grid()
    # plt.legend()
    # plt.subplot(2, 1, 2)
    # plt.plot(force_exp_time_modified, force_exp_force_modified, label='Experimental Data', color='red')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Force (N)')
    # plt.title('Force vs Time')
    # plt.grid()
    # plt.show()

    # interpolate the experimental data to match the simulation data
    # plot_time = np.linspace()


    # plt.figure()
    # plt.plot(disp_exp_time, disp_exp_displacement, label='Experimental Data', color='red')
    # plt.show()
    

def experiment_vs_simulation_plot():
    def displacement_calibration_volts_to_inch(volts):
        return volts * 0.518713

    RUN_ID = '0025_SNM5_run1'
    disp_exp = np.genfromtxt('experimental_data/9011_SNS_test1/SNSDisplacement1.csv', skip_header=23)
    disp_exp_time = disp_exp[:, 0]
    disp_exp_volts = disp_exp[:, 1]

    force_exp = np.genfromtxt('experimental_data/9011_SNS_test1/SNSForce1.csv', skip_header=7, delimiter=',')
    force_exp_time = force_exp[:, 1].astype(float)
    force_exp_force = force_exp[:, 2].astype(float)

    initial_force = 3

    # find first index of disp_exo_displacement where disp_exp_displacement is greater than 0.16
    initial_disp = 0.16
    initial_disp_index = np.argmax(disp_exp_volts > initial_disp) - 5
    disp_exp_displacement_modified = displacement_calibration_volts_to_inch(disp_exp[initial_disp_index:, 1] - disp_exp[initial_disp_index, 1])
    disp_exp_time_modified = disp_exp_time[initial_disp_index:] - disp_exp_time[initial_disp_index]

    initial_force_index = np.argmax(force_exp_force > initial_force) - 5
    force_exp_force_modified = force_exp[initial_force_index:, 2].astype(float) - force_exp_force[initial_force_index]
    force_exp_time_modified = force_exp_time[initial_force_index:] - force_exp_time[initial_force_index]
    print(initial_disp_index)

    plot_time = np.linspace(0, disp_exp_time_modified[-1], 100)
    # interpolate the experimental data to match the simulation data
    plot_displacement = np.interp(plot_time, disp_exp_time_modified, disp_exp_displacement_modified)
    plot_force = np.interp(plot_time, force_exp_time_modified, force_exp_force_modified)

    # apply a time average to the data using a kernel
    kernel = np.ones(8) / 8
    plot_displacement_smoothed = np.convolve(plot_displacement, kernel, mode='valid')
    plot_force_smoothed = np.convolve(plot_force, kernel, mode='valid')




    plt.figure(1)
    plt.plot(plot_displacement, plot_force, label='Unsmoothed')
    plt.plot(plot_displacement_smoothed, plot_force_smoothed, label='Smoothed')
    plt.xlabel('Displacement (inches)')
    plt.ylabel('Force (lbf)')
    plt.title('Force vs Displacement')
    plt.grid()

    plt.legend()
    # plt.savefig(f'meta_plots/force_vs_displacement.png')
    # plt.show()



    



    # plt.figure(2)
    # plt.subplot(2, 1, 1)
    # plt.plot(disp_exp_time_modified, disp_exp_displacement_modified, label='Experimental Data', color='red')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Displacement (mm)')
    # plt.title('Displacement vs Time')
    # plt.grid()
    # plt.legend()
    # plt.subplot(2, 1, 2)
    # plt.plot(force_exp_time_modified, force_exp_force_modified, label='Experimental Data', color='red')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Force (N)')
    # plt.title('Force vs Time')
    # plt.grid()
    # plt.show()

    # interpolate the experimental data to match the simulation data
    # plot_time = np.linspace()


    # plt.figure()
    # plt.plot(disp_exp_time, disp_exp_displacement, label='Experimental Data', color='red')
    # plt.show()
    

    binout = Binout(f'run_sets/{RUN_ID}/binout*')
    d3plot = D3plot(f'run_sets/{RUN_ID}/d3plot')

    reference_node_index = tools.extract.find_face_node_index(binout)
    reference_node_displacement = binout.read('nodout', 'z_displacement')[:, reference_node_index]

    node_ids = binout.read('nodout', 'ids')

    specimen_displacement = -reference_node_displacement * 2
    specimen_load = -binout.read('bndout', 'velocity', 'nodes', 'z_total') * 4

    time = binout.read('bndout', 'velocity', 'nodes', 'time')

    # convert m to inches
    specimen_displacement = specimen_displacement * 39.3701
    # convert N to lbf
    specimen_load = specimen_load * 0.224809


    plt.figure(1)
    plt.plot(specimen_displacement, specimen_load, label='simulation')
    # plt.xlabel('Displacement (inch)')
    # plt.ylabel('Force (lbf)')
    # plt.title('Force vs Displacement')
    plt.grid()
    # plt.show()
    plt.savefig(f'summaries/{RUN_ID}/force_vs_displacement.png')
    plt.show()

def plot_run(RUN_ID, smoothed=False, **kwargs):
    binout = Binout(f'run_sets/{RUN_ID}/binout*')
    d3plot = D3plot(f'run_sets/{RUN_ID}/d3plot')

    reference_node_index = tools.extract.find_face_node_index(binout)
    reference_node_displacement = binout.read('nodout', 'z_displacement')[:, reference_node_index]

    node_ids = binout.read('nodout', 'ids')

    specimen_displacement = -reference_node_displacement * 2
    specimen_load = -binout.read('bndout', 'velocity', 'nodes', 'z_total') * 4

    time = binout.read('bndout', 'velocity', 'nodes', 'time')

    # convert m to inches
    specimen_displacement = specimen_displacement * 39.3701
    # convert N to lbf
    specimen_load = specimen_load * 0.224809

    # apply a time average to the data using a kernel
    kernel = np.ones(4) / 4
    plot_displacement_smoothed = np.convolve(specimen_displacement, kernel, mode='valid')
    plot_force_smoothed = np.convolve(specimen_load, kernel, mode='valid')

    # plt.figure()
    if smoothed is True:
        plt.plot(plot_displacement_smoothed, plot_force_smoothed, **kwargs)
    else:
        plt.plot(specimen_displacement, specimen_load, **kwargs)




def make_plot(RUN_ID):
    binout = Binout(f'run_sets/{RUN_ID}/binout*')
    d3plot = D3plot(f'run_sets/{RUN_ID}/d3plot')

    reference_node_index = tools.extract.find_face_node_index(binout)
    print(reference_node_index)
    reference_node_displacement = binout.read('nodout', 'z_displacement')[:, reference_node_index]

    node_ids = binout.read('nodout', 'ids')

    specimen_displacement = -reference_node_displacement * 2
    specimen_load = -binout.read('bndout', 'velocity', 'nodes', 'z_total') * 4

    time = binout.read('bndout', 'velocity', 'nodes', 'time')

    # convert m to inches
    specimen_displacement = specimen_displacement * 39.3701
    # convert N to lbf
    specimen_load = specimen_load * 0.224809


    plt.figure()
    plt.plot(specimen_displacement, specimen_load)
    print('specimen load:', specimen_load)
    print('specimen disp:', specimen_displacement)
    plt.xlabel('Displacement (inch)')
    plt.ylabel('Force (lbf)')
    # plt.title('Force vs Displacement')
    plt.grid()
    # plt.show()
    plt.savefig(f'summaries/{RUN_ID}/force_vs_displacement.png')

    plt.figure()
    plt.plot(time, specimen_displacement)
    plt.xlabel('Time (s)')
    plt.ylabel('Displacement (inch)')
    plt.title('Displacement vs Time')
    plt.grid()
    plt.savefig(f'summaries/{RUN_ID}/displacement_vs_time.png') 

if __name__ == '__main__':
    main()
    # make_plot('0015_SNS4_run2')
    # make_plot('0025_SNM4_run2')
    # make_plot('0035_SNL4_run2')
    # make_plot('0015_SNS4_run1')
    # make_plot('0025_SNM4_run1')
    # make_plot('0035_SNL4_run1')
