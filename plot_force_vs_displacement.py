import tools
import numpy as np
from matplotlib import pyplot as plt
from lasso.dyna import Binout, D3plot, ArrayType

RUN_ID = '0005_basic_run3'
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
plt.title('Force vs Displacement')
plt.grid()
# plt.show()
plt.savefig(f'summaries/{RUN_ID}/force_vs_displacement.png')


