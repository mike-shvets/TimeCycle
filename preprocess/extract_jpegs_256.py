import argparse
import os
import subprocess

from joblib import delayed
from joblib import Parallel


parser = argparse.ArgumentParser()
parser.add_argument('data_folder', help='Path to dataset root folder.')
parser.add_argument('njobs', type=int, default=10, nargs='?', help='Number of parallel jobs.')
args = parser.parse_args()

file_src = os.path.join(args.data_folder, 'manifest.txt')
folder_path = os.path.join(args.data_folder, 'vlog_256')
output_path = os.path.join(args.data_folder, 'vlog_frames_12fps')

file_list = []

f = open(file_src, 'r')
for line in f:
    line = line[:-1]
    file_list.append(line)
f.close()


def download_clip(inname, outname):

    status = False
    inname = '"%s"' % inname
    outname = '"%s"' % outname
    command = "ffmpeg  -loglevel panic -i {} -q:v 1 -vf fps=12 {}/%06d.jpg".format( inname, outname)
    # ffmpeg  -loglevel panic -i /scratch/xiaolonw/kinetics/data/train/making_tea/DImSF2kwc5g_000083_000093.mp4 -q:v 1 -vf fps=12 /nfs.yoda/xiaolonw/kinetics/jpg_outs/%06d.jpg
    try:
        output = subprocess.check_output(command, shell=True,
                                         stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        return status, err.output

    # Check if the video was successfully saved.
    status = os.path.exists(outname)
    return status, 'Downloaded'


def download_clip_wrapper(row):
    """Wrapper for parallel processing purposes."""

    videoname = row

    inname = folder_path  + '/' + videoname + '/clip.mp4'
    assert os.path.exists(inname), '{} does not exist.'.format(inname)
    outname = output_path + '/' +videoname

    if os.path.isdir(outname) is False:
        try:
            os.makedirs( outname, 0755 )
        except:
            print(outname)

    downloaded, log = download_clip(inname, outname)
    return downloaded


# def main(input_csv, output_dir, trim_format='%06d', num_jobs=24, tmp_dir='/tmp/kinetics'):

# if __name__ == '__main__':

status_lst = Parallel(n_jobs=args.njobs)(delayed(download_clip_wrapper)(row) for row in file_list)

