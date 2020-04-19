import argparse
import os
from moviepy.editor import ImageSequenceClip
from moviepy.video.fx.all import rotate

parser = argparse.ArgumentParser(
    description='Combine Raw Images into an animated Gif')
parser.add_argument('--n_colors', dest="n_colors", default=128, type=int)
parser.add_argument('--dir', dest="image_dir", type=str, default='EarthImages_Color2')
parser.add_argument('--fps', dest="out_fps", default=10, type=int)
parser.add_argument('--rescale', dest="rescale", default=0.1, type=float)
parser.add_argument('--out_file', dest='out_file', default = 'earth_rotate.gif', type = str)
args = parser.parse_args()

# Parameters:
root_dir = '/Users/benjaminlucas/Projects/EarthPortrait/StopMotionAnimation/'
image_dir = args.image_dir
out_file = args.out_file
n_colors = args.n_colors
out_fps = args.out_fps
rescale = args.rescale

image_dir = root_dir + os.path.sep + image_dir

image_files = os.listdir(image_dir)
image_files = [f for f in image_files if f.split('.')[1] == 'JPG']
image_files = sorted(image_files, key=lambda x: int(x.split('.')[0].split('_')[1]))
image_files = [image_dir + os.path.sep + f for f in image_files]


clip = ImageSequenceClip(image_files, fps=out_fps)
clip_small = clip.resize(rescale)
clip_rotated = clip_small.fx(rotate, 270)
clip_rotated.write_gif(out_file)
os.system('gifsicle -O3 --colors ' + str(n_colors) + ' ' +
        out_file + ' > ' + out_file.split('.')[0] + '_opt.gif')
