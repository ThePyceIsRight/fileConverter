import gradio as gr
import cv2
import numpy as np

def blur_mask(data_dict):

    image = data_dict["image"]
    mask = data_dict["mask"]

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask_blur = cv2.GaussianBlur(mask_gray, (21, 21), 0)

    mask_bin = mask_blur / 255

    image_masked = image_gray * mask_bin

    image_masked = image_masked.astype(np.uint8)

    image_masked = cv2.cvtColor(image_masked, cv2.COLOR_GRAY2BGR)

    return image_masked


with gr.Blocks() as demo:
    image_input = gr.Image(tool="sketch", label="input image", value="C:/Users/lprice/Downloads/Oil-rig.jpg")

    image_output = gr.Image(label="output image")

    button = gr.Button("process")

    button.click(fn=blur_mask,
                 inputs=[image_input],
                 outputs=image_output)

demo.launch()