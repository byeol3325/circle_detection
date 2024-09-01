import os
os.environ['PATH'] += os.pathsep + r"D:\opencv\build\x64\vc16\bin"
from pyAAMED import pyAAMED
import cv2

def list_image_files_in_directory(directory_path: str):
    """
    Gets a list of image files (.jpg, .jpeg, .png) from a specified directory.
    """
    # Extension list settings
    image_extensions = ['.jpg', '.jpeg', '.png']

    # Filter only image files from the list of files in the directory
    image_files = [f for f in os.listdir(directory_path)
                   if os.path.isfile(os.path.join(directory_path, f)) and
                   os.path.splitext(f)[1].lower() in image_extensions]

    return image_files

def create_folder_if_not_exists(folder_path: str):
    """
    Create a folder if it does not exist in that path
    :param folder_path: Path to the folder to be created
    :return:
    """
    # Create folder if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"folder '{folder_path}'is generated.")
    else:
        print(f"folder '{folder_path}' already exists .")
    return None


def draw_detected_ellipses(image, ellipses, output_path, file):
    """
    drawing the circles
    :param image:
    :param ellipses:
    :return:
    """
    for ellipse in ellipses:
        x, y, height, width, angle = ellipse[:5]
        center = (int(y), int(x))
        axes = (int(width / 2), int(height / 2))
        cv2.ellipse(image, center, axes, -angle, 0, 360, (0, 0, 255), 2)
    cv2.imwrite(output_path + file, image)
    return None

if __name__ == "__main__":
    print("=================================== START ===================================")
    path = "../circle_sample/"
    output_path = "../circle_samples_output/"
    files = list_image_files_in_directory(path) # load image files
    create_folder_if_not_exists(output_path) # create output path

    for i in range(len(files)):
        img_file = path + files[i]
        imgC = cv2.imread(img_file)

        scale_factor = 2 / 3
        h, w, _ = imgC.shape
        imgC = cv2.resize(imgC, (int(w * scale_factor), int(h * scale_factor)))
        imgG = cv2.cvtColor(imgC, cv2.COLOR_BGR2GRAY)

        aamed = pyAAMED(h, w) # must be larger than the width and height of the image being entered.
        aamed.setParameters(3.1415926 / 3, 3.0, 0.77)  # you can adjust hyper-parameters
        res = aamed.run_AAMED(imgG)  #
        draw_detected_ellipses(imgC, res, output_path, files[i])
        aamed.release()

        print(len(res), "circles detected in", files[i])

    print("==================================== END ====================================")
