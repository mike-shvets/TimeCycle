import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('data_folder', help='Path to dataset root folder.')
args = parser.parse_args()

outlist = os.path.join(args.data_folder, 'davis/DAVIS/vallist.txt')
imgfolder = os.path.join(args.data_folder, 'davis/DAVIS/JPEGImages/480p/')
lblfolder = os.path.join(args.data_folder, 'davis/DAVIS/Annotations/480p/')

jpglist = []

valpath = os.path.join(args.data_folder, 'davis/DAVIS/ImageSets/2017/val.txt')
f1 = open(valpath, 'r')
for line in f1:
    line = line[:-1]
    jpglist.append(line)
f1.close()


f = open(outlist, 'w')

for i in range(len(jpglist)):

    fname = jpglist[i]
    fnameim = imgfolder + fname + '/'
    fnamelbl= lblfolder + fname + '/'

    print(len(os.listdir(fnameim)) )

    if len(os.listdir(fnameim)) > 20:

        f.write(fnameim + ' ' + fnamelbl + '\n')


f.close()
