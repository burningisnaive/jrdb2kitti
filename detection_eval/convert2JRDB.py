import os
import shutil
import multiprocessing as mp
import argparse
import tqdm

# this script is aimed at reorganizing the kitti labels to JRDB file structure

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-d',
                    '--JRDB_dir',
                    default='out_put_200_07/epnet_10_200_07/dt',
                    help='location to store files in JRDB file structure')
    ap.add_argument('-l',
                    '--label_dir',
                    default='/home/blli/epnet_modified/EPNet_Extend/tools/log/jrdb/extension_200_07/eval/epoch_10/test/test_mode/final_result/data',
                    help='directory of the file sequence')
    ap.add_argument('-f',
                    '--filelist',
                    default='/data2/blli/JRDB/KITTI/object/testing/filelist.txt',
                    help='filelist.txt generated while running convert_dataset_to_KITTI.py')
    return ap.parse_args()

def get_file_list(filelist):
    with open(filelist, 'r') as f:
        lines = f.readlines()
        print('total number of files is %d' %len(lines))
    return [line.strip().split(' ') for line in lines]

def copy_label_file_core(kitti_label_dir, file_idx, jrdb_label_dir, seq_frame):

    shutil.copy(os.path.join(kitti_label_dir, f'{file_idx:06d}.txt'),
                os.path.join(jrdb_label_dir, seq_frame[0], seq_frame[1]+'.txt')
                )
    '''
    print('copy file from %s to %s' %(
        os.path.join(kitti_label_dir, f'{file_idx:06d}.txt'),
        os.path.join(jrdb_label_dir, seq_frame[0], seq_frame[1]+'.txt')
        )
    )
    '''

def copy_label_file(kitti_label_dir, jrdb_label_dir, filelist_path):
    seq_frame_list = get_file_list(filelist_path)
    seq_set = set([seq for seq, frame in seq_frame_list])
    for seq in seq_set:
        if os.path.exists(os.path.join(jrdb_label_dir, seq)):
            pass
        else:
            os.makedirs(os.path.join(jrdb_label_dir, seq))
    
    for file_idx, seq_frame in tqdm.tqdm(enumerate(seq_frame_list)):
        copy_label_file_core(kitti_label_dir, file_idx, jrdb_label_dir, seq_frame)

    '''
    pool = mp.Pool(8)
    pool.starmap(
        copy_label_file_core,
        [(kitti_label_dir, file_idx, jrdb_label_dir, seq_frame)
         for file_idx, seq_frame in enumerate(seq_frame_list)]
    )
    '''

if __name__ == '__main__':
    args = parse_args()
    copy_label_file(args.label_dir, args.JRDB_dir, args.filelist)


