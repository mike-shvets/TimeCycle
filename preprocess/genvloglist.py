import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('data_folder', help='Path to dataset root folder.')
args = parser.parse_args()

src = os.path.join(args.data_folder, 'manifest.txt')
outlist = os.path.join(args.data_folder, 'vlog_frames_12fps.txt')
foldername = os.path.join(args.data_folder, 'vlog_frames_12fps/')

file = open(src, 'r')
fout = open(outlist, 'w')

for line in file:
    line = line[:-1]
    fname = foldername + line
    fnms  = len(os.listdir(fname))

    outstr = fname + ' ' + str(fnms) + '\n'
    fout.write(outstr)


file.close()
fout.close()
