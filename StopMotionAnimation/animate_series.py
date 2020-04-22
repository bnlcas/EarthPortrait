import argparse
import numpy as np
import os
from moviepy.editor import ImageSequenceClip
from moviepy.video.fx.all import rotate
from skimage.io import imread
from skimage import color

#Compress Color Space?
def CompressColor(im, compression_factor = 1.5):
    im = 255 * np.arctan(compression_factor * im / 255)
    im = im.astype(np.uint8)
    return im

def WarpHSV(im, sat_comp = 2.0, value_comp = 0.8):
    im_hsv = color.rgb2hsv(im)
    im_hsv[:,:,1] = np.arctan(sat_comp * im_hsv[:,:,1])
    im_hsv[:,:,2] = value_comp * im_hsv[:,:,2]
    im_hsv = np.minimum(im_hsv,np.ones(np.shape(im_hsv)))
    im_rgb = 255 * color.hsv2rgb(im_hsv)
    return im_rgb.astype(np.uint8)

def CompressHSV(im, sat_comp = 0.7, value_comp = 0.7):
    im_hsv = color.rgb2hsv(im)
    im_hsv[:,:,1] = sat_comp * im_hsv[:,:,1]
    im_hsv[:,:,2] = value_comp * im_hsv[:,:,2]
    im_hsv = np.minimum(im_hsv,np.ones(np.shape(im_hsv)))
    im_rgb = 255 * color.hsv2rgb(im_hsv)
    return im_rgb.astype(np.uint8)

parser = argparse.ArgumentParser(
    description='Combine Raw Images into an animated Gif')
parser.add_argument('--n_colors', dest="n_colors", default=128, type=int)
parser.add_argument('--dir', dest="image_dir", type=str, default='EarthImages_Color4')
parser.add_argument('--fps', dest="out_fps", default=15, type=int)
parser.add_argument('--rescale', dest="rescale", default=0.1, type=float)
parser.add_argument('--compression', dest="compression_factor", default=1.3, type=float)
parser.add_argument('--out_file', dest='out_file', default = 'earth_rotate.gif', type = str)
args = parser.parse_args()

# Parameters:
root_dir = '/Users/benjaminlucas/Projects/EarthPortrait/StopMotionAnimation/'
image_dir = args.image_dir
out_file = args.out_file
n_colors = args.n_colors
out_fps = args.out_fps
rescale = args.rescale
compression_factor = args.compression_factor
rotate_angle = 0
modify_images = False

image_dir = root_dir + os.path.sep + image_dir

image_files = os.listdir(image_dir)
image_files = [f for f in image_files if f.split('.')[1] == 'JPG']
image_files = sorted(image_files, key=lambda x: int(x.split('.')[0].split('_')[1]))
image_files = [image_dir + os.path.sep + f for f in image_files]

if modify_images:
    images = []
    for f in image_files:
        im = imread(f)
        images.append(im)
        #images.append(CompressColor(im, compression_factor))
        #images.append(WarpHSV(im))
    clip = ImageSequenceClip(images, fps=out_fps)
else:
    clip = ImageSequenceClip(image_files, fps=out_fps)

clip_small = clip.resize(rescale)
if(rotate_angle != 0):
    clip_small = clip_small.fx(rotate, rotate_angle)
(w, h) = clip_small.size
clip_cropped = clip_small.crop( x_center=w//2 , width=h)
clip_cropped.write_gif(out_file, program='ffmpeg')
os.system('gifsicle -O3 --colors ' + str(n_colors) + ' ' +
        out_file + ' > ' + out_file.split('.')[0] + '_opt.gif')
