import json
import cv2
import numpy as np
import os
from joblib import Parallel, delayed
import argparse
import multiprocessing
#read image and detected bounding box, output the image with bounding box

def TifFile(jsonfile):
    jsonfile = jsonfile.split('.')[0]
    book, p, _ = jsonfile.split('_')
    p = p[0] + str(int(p[1:]))
    return book + '_' + p + '.tif'

def main(jsonfile,jsondir,imgdir,outputdir):
    print("processing ", jsonfile)

    file=os.path.join(jsondir,jsonfile)
    scale = 4
    #import pdb;pdb.set_trace()
    img = cv2.imread(os.path.join(imgdir, TifFile(jsonfile)))
    img = cv2.pyrDown(cv2.pyrDown(img))

    with open(file) as rectjson:
        rect = json.load(rectjson)
    box = cv2.boxPoints(tuple(rect))
    box = np.int0(box/scale)
    cv2.drawContours(img, [box], 0, (0,0,255), 2)
    #import pdb;pdb.set_trace()
    cv2.imwrite(os.path.join(outputdir,jsonfile.split('.')[0]+'.png'),img)

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    parser = argparse.ArgumentParser(description='Page Detection')
    parser.add_argument('--jsondir', type=str)
    parser.add_argument('--imgdir', type=str)
    parser.add_argument('--outputdir', type=str)
    args = parser.parse_args()

    #create output file
    if not os.path.isdir(args.outputdir):
        os.mkdir(args.outputdir)
        print('creating directory ' + args.outputdir)

    clean_names = lambda x: [i for i in x if i[0] != '.']
    rowRects = os.listdir(args.jsondir)
    rowRects = sorted(clean_names(rowRects))
    jsondir=[args.jsondir] * len(rowRects)
    imgdir=[args.imgdir] * len(rowRects)
    outputdir=[args.outputdir] * len(rowRects)

    Parallel(n_jobs=2)(map(delayed(main), rowRects, jsondir, imgdir, outputdir))
    #Parallel(n_jobs=multiprocessing.cpu_count())(map(delayed(main), rowRects,jsondir,imgdir,outputdir))
