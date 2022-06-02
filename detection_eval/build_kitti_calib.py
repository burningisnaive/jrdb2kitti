import os
import numpy as np
import tqdm

'''
To project a point from Velodyne coordinates into the left color image,
you can use this formula: x = P2 * R0_rect * Tr_velo_to_cam * y
For the right color image: x = P3 * R0_rect * Tr_velo_to_cam * y

Note: All matrices are stored row-major, i.e., the first values correspond
to the first row. R0_rect contains a 3x3 matrix which you need to extend to
a 4x4 matrix by adding a 1 as the bottom-right element and 0's elsewhere.
Tr_xxx is a 3x4 matrix (R|t), which you need to extend to a 4x4 matrix 
in the same way!
'''
'''
P0: 7.070493000000e+02 0.000000000000e+00 6.040814000000e+02 0.000000000000e+00 0.000000000000e+00 7.070493000000e+02 1.805066000000e+02 0.000000000000e+00 0.000000000000e+00 0.000000000000e+00 1.000000000000e+00 0.000000000000e+00
P1: 7.070493000000e+02 0.000000000000e+00 6.040814000000e+02 -3.797842000000e+02 0.000000000000e+00 7.070493000000e+02 1.805066000000e+02 0.000000000000e+00 0.000000000000e+00 0.000000000000e+00 1.000000000000e+00 0.000000000000e+00
P2: 7.070493000000e+02 0.000000000000e+00 6.040814000000e+02 4.575831000000e+01 0.000000000000e+00 7.070493000000e+02 1.805066000000e+02 -3.454157000000e-01 0.000000000000e+00 0.000000000000e+00 1.000000000000e+00 4.981016000000e-03
P3: 7.070493000000e+02 0.000000000000e+00 6.040814000000e+02 -3.341081000000e+02 0.000000000000e+00 7.070493000000e+02 1.805066000000e+02 2.330660000000e+00 0.000000000000e+00 0.000000000000e+00 1.000000000000e+00 3.201153000000e-03
R0_rect: 9.999128000000e-01 1.009263000000e-02 -8.511932000000e-03 -1.012729000000e-02 9.999406000000e-01 -4.037671000000e-03 8.470675000000e-03 4.123522000000e-03 9.999556000000e-01
Tr_velo_to_cam: 6.927964000000e-03 -9.999722000000e-01 -2.757829000000e-03 -2.457729000000e-02 -1.162982000000e-03 2.749836000000e-03 -9.999955000000e-01 -6.127237000000e-02 9.999753000000e-01 6.931141000000e-03 -1.143899000000e-03 -3.321029000000e-01
Tr_imu_to_velo: 9.999976000000e-01 7.553071000000e-04 -2.035826000000e-03 -8.086759000000e-01 -7.854027000000e-04 9.998898000000e-01 -1.482298000000e-02 3.195559000000e-01 2.024406000000e-03 1.482454000000e-02 9.998881000000e-01 -7.997231000000e-01
'''
import argparse

parser = argparse.ArgumentParser('description=Show the usage')
parser.add_argument('-o',
                    '--output_dir',
                    default='/data2/blli/JRDB/KITTI/object/testing',
                    help='location to store the calib folder')
parser.add_argument('-n',
                    '--num_calib',
                    type=int,
                    default=27661,
                    help='number of calib files')
args = parser.parse_args()

# training: 27947, testing: 27661

# P matrix, they are all false and meaningless for cylindrical images
# fake data
P0 = np.array([-1, 0, -1, 0, -1, -1, 0, 0, 1, 0, 1, 0])
P1 = np.array([-1, 0, -1, 0, -1, -1, 0, 0, 1, 0, 1, 0])
P2 = np.array([-1, 0, -1, 0, -1, -1, 0, 0, 1, 0, 1, 0])
P3 = np.array([-1, 0, -1, 0, -1, -1, 0, 0, 1, 0, 1, 0])

# R0_rect is just identical matrix, meaningful                      
R0_rect = np.array([1, 0, 0, 0, 1, 0, 0, 0, 1])
# this marix is correct and meaningful !
Tr_velo_to_cam = np.array([[0, -1, 0, 0],
                           [0, 0, -1, 0],
                           [1, 0,  0, 0]]).reshape(-1)
# meaningless
Tr_imu_to_velo = Tr_velo_to_cam      

def build_line(name, values):
    line = [name+':']
    for value in values:
        line.append( f'{value:.12e}')
    return ' '.join(line)+'\n'

lines = []
lines.append(build_line('P0', P0))
lines.append(build_line('P1', P1))
lines.append(build_line('P2', P2))
lines.append(build_line('P3', P3))
lines.append(build_line('R0_rect', R0_rect))
lines.append(build_line('Tr_velo_to_cam', Tr_velo_to_cam))
lines.append(build_line('Tr_imu_to_velo', Tr_imu_to_velo))
OUT_CALIB_PATH = 'calib'
output_dir = args.output_dir

for file_idx in tqdm.tqdm(range(args.num_calib)):
    if file_idx%100 == 1:
        # print(file_idx)
        pass
    calib_out = os.path.join(output_dir, OUT_CALIB_PATH, f'{file_idx:06d}.txt')
    with open(calib_out, 'w') as f:
        f.writelines(lines)


 
