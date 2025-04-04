import pandas as pd
from matplotlib import pyplot as plt
from lasso.dyna import Binout, D3plot, ArrayType
import numpy as np
import tools.extract as extract
import tools.dyna_tools as dyna_tools

def find_summary(binout, d3plot):
    element_ids = d3plot.arrays[ArrayType.element_solid_ids]
    # interest_element_ids = extract.extract_gauge_edge_nodes_ids(d3plot)  # this should be the element ids of the gauge section
    interest_element_ids = np.array([81, 67, 47, 53, 45, 61])
    interest_mask = np.isin(element_ids, interest_element_ids)  # this can be used to slice for the data of interest
    # eventually, this should be automated to grab ids of the edge of gauge section

    stress = binout.read('eloutdet')

    return {
        'bin_time': binout.read('bndout', 'velocity', 'nodes', 'time'),
        'force': dyna_tools.find_specimen_load(binout),
        'displacement': extract.extract_specimen_displacement(binout),
        'd3_time': d3plot.arrays[ArrayType.global_timesteps],
        'effective_plastic_strain': d3plot.arrays[ArrayType.element_solid_effective_plastic_strain][:, interest_mask, 0],
        'triaxiality': dyna_tools.find_triaxiality(d3plot)[:, interest_mask, 0],
        'interest_element_ids': interest_element_ids,
    }

def summary_to_df(summary):
    headers = ['bin_time', 'force', 'displacement', 'd3_time', *[f'eps_element_{eid}' for eid in summary['interest_element_ids']], *[f'triaxiality_{eid}' for eid in summary['interest_element_ids']]]
    data = {
        'bin_time': summary['bin_time'],
        'force': summary['force'],
        'displacement': summary['displacement'],
        'd3_time': summary['d3_time'],
    }
    print(headers)
    for i, eid in enumerate(summary['interest_element_ids']):
        data[f'eps_element_{eid}'] = summary['effective_plastic_strain'][:, i]
        data[f'triaxiality_{eid}'] = summary['triaxiality'][:, i]
    print(data)
    df = pd.DataFrame()
    for key in headers:
        new_col = pd.Series(data[key])
        df[key] = new_col
    return df

def plot_force_vs_displacement(summary):
    plt.figure()
    plt.plot(summary['displacement'], summary['force'])
    plt.xlabel('Displacement (m)')
    plt.ylabel('Force (N)')
    plt.title('Force vs Displacement')
    plt.grid()

def plot_eps_triaxiality(summary):
    plt.figure()
    for i, eid in enumerate(summary['interest_element_ids']):
        plt.plot(summary['triaxiality'][:, i], summary['effective_plastic_strain'][:, i], label=f'Element {eid}')
    plt.xlabel('Triaxiality')
    plt.ylabel('Effective Plastic Strain')
    plt.title('Triaxiality vs Effective Plastic Strain @ Gauge Edge')
    plt.legend()
    plt.grid()

def process_run(run_id):
    # make the directories if they don't exist
    import os
    os.makedirs(f'summaries/{run_id}', exist_ok=True)


    binout = Binout(f'run_sets/{run_id}/binout*')
    d3plot = D3plot(f'run_sets/{run_id}/d3plot')
    summary = find_summary(binout, d3plot)
    df = summary_to_df(summary)
    df.to_csv(f'summaries/{run_id}/summary.csv')
    print(f'Summary saved to summaries/{run_id}/summary.csv')
    plot_force_vs_displacement(summary)
    plt.savefig(f'summaries/{run_id}/force_vs_displacement.png')
    plot_eps_triaxiality(summary)
    plt.savefig(f'summaries/{run_id}/triaxiality_vs_eps.png')

if __name__ == '__main__':
    # get the summary
    run_id = '0002_basic_run1'
    # binout = Binout(f'run_sets/{run_id}/binout*')
    # d3plot = D3plot(f'run_sets/{run_id}/d3plot')
    # summary = find_summary(binout, d3plot)
    # print(summary)
    # plot_eps_triaxiality(summary)

    process_run(run_id)