import tools.outputs as outputs
import tools.dyna_tools as dyna_tools

input_ids = ['0010_SNS', '0020_SNM', '0030_SNL']  # corresponds to a folder containing a set of input files
run_ids = input_ids  # corresponds to a folder containing a set of output files

if __name__ == '__main__':
    # dyna_tools.run_lsdyna(input_id, run_id)
    # for input_id, run_id in zip(input_ids, run_ids):
    #     dyna_tools.run_lsdyna(input_id, run_id)

    # for input_id, run_id in zip(input_ids, run_ids):
    #     # process
    #     outputs.process_run(run_id)

    # dyna_tools.run_lsdyna('0015_SNS5', '0015_SNS5_run2')
    # dyna_tools.run_lsdyna('0025_SNM5', '0025_SNM5_run2')
    # dyna_tools.run_lsdyna('0035_SNL5', '0035_SNL5_run2')
    dyna_tools.run_lsdyna('0010_SNS', '0010_SNS_run3')


    # outputs.process_run('0015_SNS5_run2')
    # outputs.process_run('0025_SNM5_run2')
    # outputs.process_run('0035_SNL5_run2')
    # outputs.process_run('0015_SNS4_run2')