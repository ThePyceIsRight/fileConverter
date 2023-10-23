from PIL import Image
from pillow_heif import register_heif_opener
import os
import base64
import csv
import time
import io

register_heif_opener()


def image_to_image(folder_path: str, img_ext: list[str], delete_files: bool = False):
    """
    Converts all images in a folder to the specified image type

    :param folder_path: path to the folder containing images to convert
    :param img_ext: list of extensions that you want to convert to base64
    :param delete_files: set to True to delete converted files
    """

    # Remove periods if any
    i = 0
    for extension in img_ext:
        img_ext[i] = extension.replace(".", "")
        i = i + 1

    # Assign csv path to store base64 encodings
    base64_list_path = f"{folder_path}/base64_list.csv"

    print(f"{folder_path}/n{img_ext}")

    # Create new csv if already exists
    if os.path.exists(base64_list_path):
        os.remove(base64_list_path)
        with open(base64_list_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['filename', 'base64'])
    else:
        with open(base64_list_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['filename', 'base64'])

    # Loop through all files in the directory
    for filename in os.listdir(folder_path):

        for extension in img_ext:

            # Check if the file is an image
            if filename.endswith(extension):
                # Delay
                time.sleep(0.01)

                image_path = f"{folder_path}/{filename}"

                new_height = 100

                image = Image.open(image_path)
                width, height = image.size
                new_width = int(width * new_height / height)
                resized_image = image.resize((new_width, new_height))

                with io.BytesIO() as buffer:
                    resized_image.save(buffer, format="png")
                    encoded_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
                # Open image and convert to base64 string
                # with open(image_path, "rb") as image_file:
                #     encoded_string = base64.b64encode(image_file.read())

                # Write base64 to csv list file
                with open(base64_list_path, 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([os.path.splitext(os.path.basename(filename))[0], encoded_string])

                # Delete file if option selected
                if delete_files:
                    os.remove(image_path)


if __name__ == '__main__':
    image_to_image(
        "C:/Users/lprice/OneDrive - Range Resources/Documents/Personal Working Files/Bots/Bot Dashboard/Bot Images",
        ['.jpg', 'jpeg', '.png'])
