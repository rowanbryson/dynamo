import tools
import numpy as np
from matplotlib import pyplot as plt
from lasso.dyna import Binout, D3plot, ArrayType

# RUN_ID = '0015_SNS5_run1'
# RUN_ID = '0025_SNM5_run1'
# RUN_ID = '0035_SNL5_run1'

def main():
    # make_plot('0015_SNS5_run2')
    # make_plot('0025_SNM5_run2')
    # make_plot('0035_SNL5_run2')
    experiment_vs_simulation_plot()


def experiment_vs_simulation_plot():
    RUN_ID = '0025_SNM5_run1'
    disp_exp = np.genfromtxt('experimental_data/9011_SNS_test1/SNSDisplacement1.csv', skip_header=23)
    disp_exp_time = disp_exp[:, 0]
    disp_exp_displacement = disp_exp[:, 1]

    force_exp = np.genfromtxt('experimental_data/9011_SNS_test1/SNSForce1.csv', skip_header=7, delimiter=',')
    force_exp_time = force_exp[:, 1].astype(float)
    force_exp_force = force_exp[:, 2].astype(float)

    # find first time where disp_exp is greater than 0.5
    disp_index = np.where(disp_exp_displacement > 0.00001)[0][0]
    disp_exp_time_offset = disp_exp_time[disp_index]
    disp_exp_time_modified = disp_exp_time[disp_index:] - disp_exp_time_offset
    disp_exp_displacement_modified = disp_exp_displacement[disp_index:]

    force_index = np.where(force_exp_force > 0.00001)[0][0]
    force_exp_time_offset = force_exp_time[force_index]
    force_exp_time_modified = force_exp_time[force_index:] - force_exp_time_offset
    force_exp_force_modified = force_exp_force[force_index:]


    def displacement_calibration_volts_to_inch(volts):
        pass

    plt.subplot(2, 1, 1)
    plt.plot(disp_exp_time_modified, disp_exp_displacement_modified, label='Experimental Data', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Displacement (mm)')
    plt.title('Displacement vs Time')
    plt.grid()
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(force_exp_time_modified, force_exp_force_modified, label='Experimental Data', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Force vs Time')
    plt.grid()
    plt.show()

    # # interpolate the experimental data to match the simulation data
    # plot_time = np.linspace()


    # plt.figure()
    # plt.plot(disp_exp_time, disp_exp_displacement, label='Experimental Data', color='red')
    # plt.show()
    

    # binout = Binout(f'run_sets/{RUN_ID}/binout*')
    # d3plot = D3plot(f'run_sets/{RUN_ID}/d3plot')

    # reference_node_index = tools.extract.find_face_node_index(binout)
    # reference_node_displacement = binout.read('nodout', 'z_displacement')[:, reference_node_index]

    # node_ids = binout.read('nodout', 'ids')

    # specimen_displacement = -reference_node_displacement * 2
    # specimen_load = -binout.read('bndout', 'velocity', 'nodes', 'z_total') * 4

    # time = binout.read('bndout', 'velocity', 'nodes', 'time')

    # # convert m to inches
    # specimen_displacement = specimen_displacement * 39.3701
    # # convert N to lbf
    # specimen_load = specimen_load * 0.224809


    # plt.figure()
    # plt.plot(specimen_displacement, specimen_load)
    # plt.xlabel('Displacement (inch)')
    # plt.ylabel('Force (lbf)')
    # # plt.title('Force vs Displacement')
    # plt.grid()
    # # plt.show()
    # plt.savefig(f'summaries/{RUN_ID}/force_vs_displacement.png')

def make_plot(RUN_ID):
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


    plt.figure()
    plt.plot(specimen_displacement, specimen_load)
    plt.xlabel('Displacement (inch)')
    plt.ylabel('Force (lbf)')
    # plt.title('Force vs Displacement')
    plt.grid()
    # plt.show()
    plt.savefig(f'summaries/{RUN_ID}/force_vs_displacement.png')

if __name__ == '__main__':
    main()
    # make_plot('0015_SNS4_run2')
    # make_plot('0025_SNM4_run2')
    # make_plot('0035_SNL4_run2')
    # make_plot('0015_SNS4_run1')
    # make_plot('0025_SNM4_run1')
    # make_plot('0035_SNL4_run1')
