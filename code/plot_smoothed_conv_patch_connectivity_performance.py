from __future__ import division

import matplotlib.pyplot as plt
import cPickle as p
import numpy as np
import os


performance_dir = '../performance/conv_patch_connectivity_performance/'

if not os.path.isdir(performance_dir + 'performance_plots_smoothed/'):
    os.makedirs(performance_dir + 'performance_plots_smoothed/')

def window(size):
    return np.ones(size) / float(size)

print '\n'
print '\n'.join([ str(idx + 1) + ' | ' + file_name for idx, file_name in enumerate(sorted(os.listdir(performance_dir))) if '.p' in file_name ])
print '\n'

to_plot = raw_input('Enter the index of the file from above which you\'d like to plot: ')
file_name = sorted([ file_name for file_name in os.listdir(performance_dir) if '.p' in file_name ])[int(to_plot) - 1]

# get pickled performances dictionary (voting mechanism, performance recordings over training)
_, performances = p.load(open(performance_dir + file_name, 'rb'))

print '\n'

performance_plots = []
for voting_mechanism in sorted(performances.keys()):
    if voting_mechanism in [ 'all', 'most_spiked', 'top_percent', 'spatial_clusters' ]:
        performance_plots.append(plt.plot(np.convolve(performances[voting_mechanism], window(15), 'same'), label=voting_mechanism)[0])

plt.legend(handles=performance_plots)

fig = plt.gcf()
fig.set_size_inches(16, 12)

plt.xlabel('Iteration number (1 through ' + str(len(performances[performances.keys()[0]]) * 100) + ')')
plt.xticks([ x for x in xrange(0, len(performances[performances.keys()[0]]) + 25, 25) ], [ x * 100 for x in xrange(0, len(performances[performances.keys()[0]]) + 25, 25) ])
plt.ylabel('Classification accuracy (out of 100%)')

title_strs = file_name[:file_name.index('weight') - 1].split('_')

conv_size = int(file_name.split('_')[1])
conv_stride = int(file_name.split('_')[2])
conv_features = int(file_name.split('_')[3])
lattice_structure = file_name[-7:-6]
if 'no_weight_sharing' in file_name:
    weight_sharing = 'no_weight_sharing'
else:
    weight_sharing = 'weight_sharing'

plt.title(str(conv_size) + 'x' + str(conv_size) + ' convolutions, stride ' + str(conv_stride) + ', ' + str(conv_features) + \
                        ' convolution patches, ' + ' '.join(weight_sharing.split('_')) + ', ' + str(lattice_structure) + '-lattice')
plt.tight_layout()

plt.savefig(performance_dir + 'performance_plots_smoothed/' + file_name[:file_name.index('.')])
plt.show()

print '\n'
