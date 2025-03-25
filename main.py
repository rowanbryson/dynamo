import sys
import os
import subprocess
import shutil
from loguru import logger
import numpy as np


SOLVER = "C:\Program Files\LS-DYNA Suite R14 Student\lsdyna\ls-dyna_smp_d_R14.1.1s_1-gef50e1efb1_winx64_ifort190.exe"
MEMORY = '20m'
NCPU = '4'

PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_SETS_DIR = 'input_sets'
OUTPUT_SETS_DIR = 'run_sets'
MAIN_FILE_NAME = "MAIN_Bar_6061-T651_Compression.key"


def run_lsdyna(input_id, run_id):
    # check if the the run_id exists in the runs directory
    # if it does, return an error
    # if it does not, create a directory for the run_id
    run_dirpath = os.path.join(PATH, OUTPUT_SETS_DIR, run_id)
    input_dirpath = os.path.join(PATH, INPUT_SETS_DIR, input_id)


    if os.path.exists(run_dirpath):
        logger.warning(f"Run directory {run_dirpath} already exists")
        keep_going = input("Do you want to continue? (y/n)")

        if keep_going.lower() != 'y':
            logger.info("Exiting program")
            sys.exit(0)


    # copy the input files to the results directory
    copy_files(input_id, run_id)

    # Create a directory for the runnning the simulation
    os.makedirs(run_dirpath, exist_ok=True)

    # copy the input files to the results directory
    copy_files(input_id, run_id)

    # Run LS-DYNA and print the output to the console
    args = [SOLVER, "i=" + MAIN_FILE_NAME, "memory=" + MEMORY, "ncpu=" + NCPU]


    logger.info(f"Running LS-DYNA at wd {run_dirpath} with the following arguments: {args}")
    subprocess.run(args, cwd=run_dirpath)


def copy_files(input_id, run_id):
    input_dirpath = os.path.join(PATH, INPUT_SETS_DIR, input_id)
    run_dirpath = os.path.join(PATH, OUTPUT_SETS_DIR, run_id)

    # check if the the run_id exists in the runs directory, if it does not, create a directory for the run_id
    logger.info(f"Copying files from {input_dirpath} to {run_dirpath}")
    logger.debug(f"Checking if {run_dirpath} exists")
    if not os.path.exists(run_dirpath):
        os.makedirs(run_dirpath, exist_ok=True)

    logger.debug(f"Copying files from {input_dirpath} to {run_dirpath}")
    # copy files within the input file directory to the results directory, if they are not already there
    for file in os.listdir(input_dirpath):
        if not os.path.exists(os.path.join(run_dirpath, file)):
            logger.info(f"Copying {file} to {run_dirpath}")
            shutil.copy(os.path.join(input_dirpath, file), run_dirpath)
        else:
            logger.info(f"{file} already exists in {run_dirpath}")

from lasso.dyna import D3plot, ArrayType, FilterType
from matplotlib import pyplot as plt

def plot_element(run_id, element_id):

    # grab data from the d3plot (LS-DYNA output file)
    d3plot = D3plot(f'run_sets/{run_id}/d3plot')

    element_ids = d3plot.arrays[ArrayType.element_solid_ids]
    eps = d3plot.arrays[ArrayType.element_solid_effective_plastic_strain]
    stress = d3plot.arrays[ArrayType.element_solid_stress]
    time = d3plot.arrays[ArrayType.global_timesteps]

    # compute the triaxiality
    triaxiality = compute_triaxiality(stress)

    # get the index of the element id we are interested in
    idx = np.where(element_ids == element_id)[0][0]

    plt.figure(figsize=(15, 5))
    plt.suptitle(f"Element {element_id} Data")
    plt.subplot(1, 3, 1)
    plt.title('Effective Plastic Strain vs Time')
    plt.scatter(time[time >= 0], eps[:, idx, 0][time >= 0])
    plt.xlabel('Time (s)')
    plt.ylabel('Effective Plastic Strain')
    plt.subplot(1, 3, 2)
    plt.title('Stress Triaxiality vs Time')
    plt.scatter(time[time >= 0], triaxiality[:, idx, 0][time >= 0])
    plt.xlabel('Time (s)')
    plt.ylabel('Stress Triaxiality')
    plt.subplot(1, 3, 3)
    plt.title('Effective Plastic Strain vs Stress Triaxiality')
    plt.scatter(eps[:, idx, 0][time >= 0], triaxiality[:, idx, 0][time >= 0])
    plt.xlabel('Effective Plastic Strain')
    plt.ylabel('Stress Triaxiality')
    plt.tight_layout()


def compute_triaxiality(stress: np.ndarray):
    """
    Calculate the triaxiality of the stress tensor
    """
    I1 = stress[..., 0] + stress[..., 1] + stress[..., 2]
    J2 = 0.5 * ((stress[..., 0] - stress[..., 1])**2 + (stress[..., 1] - stress[..., 2])**2 + (stress[..., 2] - stress[..., 0])**2 + 6 * (stress[..., 3]**2 + stress[..., 4]**2 + stress[..., 5]**2))
    triaxiality = I1 / (3 * np.sqrt(2) * np.sqrt(J2))
    return triaxiality

if __name__ == "__main__":
    input_id = '0001_basic' # corresponds to a folder containing a set of input files 
    # the input_sets folder contains many input folders, each with a unique input_id

    run_id = '0001_basic_run1' # corresponds to a folder containing the results of the simulation
    # picking an unused run_id will create a new folder in the run_sets directory to store the results of the simulation

    # run the simulation
    # run_lsdyna(input_id, run_id)

    # plot the data for element 81
    element_id = 81
    plot_element(run_id, element_id)
    plt.show()

