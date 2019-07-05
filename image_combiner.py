#!/usr/bin/python3

import argparse
import os
import logging
import numpy as np
import PIL.Image

def get_args():
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f1", "--folderone", required=False, default='./left', help="First image folder. default is './left'")
    ap.add_argument("-f2", "--foldertwo", required=False, default='./right', help="Second image folder. default is './right'")
    ap.add_argument("-ie", "--imageext", required=False, default='jpg', help="Image extension name. default is 'jpg'.")
    ap.add_argument("-o", "--outputfolder", required=False, default='./output', help="Output folder. default is ./output")
    ap.add_argument("-v","--verbose", help="increase output verbosity", action="store_true")

    args = vars(ap.parse_args())
    return args

# Get files from a folder that match the extension
def get_images(folder, ext):
    files = []
    for f in os.listdir(folder):
        if f.endswith(ext):
            files.append(PIL.Image.open(os.path.join(folder,f)))
    
    logging.debug("Found %s files on %s" % (len(files), folder))
    return files

# Main function
def main():

    # just set the parameters to variables
    args = get_args()
    if args['verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    image_ext = args['imageext']
    f1 = args['folderone']
    f2 = args['foldertwo']
    output_folder = args['outputfolder']

    left_images = get_images(folder=f1, ext=image_ext)
    right_images = get_images(folder=f2, ext=image_ext)
    
    
    # create a video made of 1 image with  soundtrack made of 1 music
    for left, right in zip(left_images, right_images):
        min_shape = min(left.size, right.size)
        a = []
        a.append(np.asarray(left.resize(min_shape)))
        a.append(np.asarray(right.resize(min_shape)))
        img_comb = np.hstack(np.asarray(a))
        img_comb = PIL.Image.fromarray( img_comb)
        img_comb.save(os.path.join(
            output_folder,
            os.path.basename(left.filename).split(".")[0] + 
            "_" + 
            os.path.basename(right.filename).split(".")[0]+
            "." +
            image_ext
        ))
        logging.debug("Image %s created" % img_comb)
if __name__=="__main__":
    main()
    