import outputs
import dyna_tools

if __name__ == '__main__':
    input_id = '0002_basic'  # corresponds to a folder containing a set of input files
    run_id = '0002_basic_run1'

    # dyna_tools.run_lsdyna(input_id, run_id)
    outputs.process_run(run_id)