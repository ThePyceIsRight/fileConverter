import sys
from PIL import Image
import os
import tempfile
import shutil
from rembg import remove
import glob
import contextlib
import requests
from io import BytesIO


def remove_img_bg(img_file, output_path):
    output = remove(img_file)
    output.save(output_path)
    print(f"Background removed, output saved to:    \"{output_path}\"")


def imgs_to_video(framesDir):
    # https://stackoverflow.com/a/57751793/17312223
    fp_in = f"{framesDir}/frame-*.png"  # Will return all file paths obeying regex to a list var
    fp_out = f"{framesDir}/modified.gif"

    # use exit stack to automatically close opened images
    with contextlib.ExitStack() as stack:
        # lazily load images
        imgs = (stack.enter_context(Image.open(f))
                for f in sorted(glob.glob(fp_in)))

        # extract  first image from iterator
        img = next(imgs)

        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
        img.save(fp=fp_out, format='GIF', disposal=2, append_images=imgs,
                 save_all=True, duration=100, loop=0)


def gif_to_imgs(imgDir,gif_url):
    framesDir = f"{imgDir}/gif_frames"

    # Delete frames folder if exists
    if (os.path.exists(framesDir)):
        tmp = tempfile.mktemp(dir=os.path.dirname(framesDir))
        shutil.move(framesDir, tmp)  # "Move" to temporary folder
        shutil.rmtree(tmp)  # Delete

    os.mkdir(framesDir)

    # Check if local GIF exists in path
    for filename in os.listdir(imgDir):
        if filename.lower().endswith(".gif"):
            im2 = Image.open(f"{imgDir}/{filename}")
            break
        else:
            im2 = False

    # If URL given, use that, otherwise, use local GIF
    if (gif_url != ""):
        response = requests.get(gif_url)
        im = Image.open(BytesIO(response.content))
    elif im2:
        im = im2
    else:
        print("no URL given and no local GIF file detected - please try again")
        sys.exit(1)

    print("Number of frames: " + str(im.n_frames))

    for i in range(0, im.n_frames):
        # Create sort-friendly numerical suffix for GIF frames
        numSuffix = str(i)
        while (len(numSuffix) < 4):
            numSuffix = f"0{numSuffix}"

        # Remove background from the frame
        im.seek(i)  # Iterate to specific frame
        duration = im.info['duration']/1000  # Get frame duration
        output_path = f"{framesDir}/frame-{numSuffix}-{duration}.png"  # Set output path
        remove_img_bg(im, output_path)  # Remove background

    imgs_to_video(framesDir)
