import cv2
import numpy
import multiprocessing as mp
from PIL import Image, ImageSequence
import rembg

vid_path = "C:/Users/lprice/OneDrive - Range Resources/Desktop/Delete/20231211_162102000_iOS.mp4"


def cv_to_PIL(cv_im):
    # Convert the color space (if needed)
    img = cv2.cvtColor(cv_im, cv2.COLOR_BGR2RGB)

    # Create a PIL image from the numpy array
    return Image.fromarray(img)


def get_vid_frames(vid_path: str) -> [numpy.ndarray]:
    # Open the video file
    vid_cap = cv2.VideoCapture(vid_path)
    success, image = vid_cap.read()
    count = 0
    frames = []  # Initialize an empty list to store frames

    while success:
        frames.append(image)  # Add each frame to the list
        success, image = vid_cap.read()
        count += 1

    vid_cap.release()

    if len(frames) > 0:
        print(f'{len(frames)} captured from video')
    else:
        print("No frames captured from the video.")

    return frames


def edit_images(frame, q, counter: mp, lock, frame_count):
    rem_frame = rembg.remove(frame)
    q.put(rem_frame)
    # Increment the counter after processing
    with lock:
        completion = counter.value/frame_count
        print(f"bg removed - img no. {counter.value} - percent complete: {completion:.2%}")
        counter.value += 1


def mult_process(frames):
    # use multiprocessing to process images concurrently
    p = mp.Pool(4)
    # manager = mp.Manager()
    q = mp.Manager().Queue()
    counter = mp.Manager().Value('i', 0)
    lock = mp.Manager().Lock()

    for frame in frames:
        p.apply_async(edit_images, args=(frame, q, counter, lock, len(frames)))

    p.close()
    p.join()

    edited_frames = []
    while not q.empty():
        edited_frame = q.get()
        edited_frames.append(edited_frame)

    return edited_frames


def main(my_path: str):
    print(f"number of cpus: {mp.cpu_count()}")

    # get frames from video
    frames = get_vid_frames(my_path)

    # convert cv2 to PIL
    pil_frames = []
    for frame in frames:
        pil_frames.append(cv_to_PIL(frame))

    print(f"no. frames: {len(pil_frames)}")

    # pass frames to multiprocessing for quicker editing
    edited_frames = mult_process(pil_frames)

    print("multiprocessing of image complete")

    # Save the edited frames as a GIF file
    if len(edited_frames) > 0:
        edited_frames[0].save('edited.gif',
                              save_all=True,
                              append_images=edited_frames[1:],
                              duration=20,
                              disposal=2,
                              loop=0)

    print("Done!")


if __name__ == '__main__':
    main(vid_path)
