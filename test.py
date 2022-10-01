import brainExtraction
import cv2
import os
import shutil


INPUT_DIR = 'testPatient/'
SLICES_OUTPUT_DIR = 'Slices/'
BOUNDARIES_OUTPUT_DIR = 'Boundaries/'
IMAGE_EXTENSION = '.png'
BOUNDARY_COLOR = (0, 0, 255)
BOUNDARY_THICKNESS = 1


# utility function to remove file extension form file name
def remove_file_extension(file_name):
    return os.path.splitext(file_name)[0]


# utility function to join directory path with file name
def join_path(dir, filename):
    return os.path.join(dir, filename)


# utlity function to clear all contents of output directory
def init_output_dirs(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)
    os.makedirs(folder)


# utility function to read all the input images form the testPatient directory
def read_input_data():
    images = []
    for file_name in os.listdir(INPUT_DIR):
        if(file_name.endswith("_thresh.png")):
            brain_image = cv2.imread(join_path(INPUT_DIR, file_name))
            images.append((file_name, brain_image))
    return images


def main():
    # initialize Slices output directory
    init_output_dirs(SLICES_OUTPUT_DIR)
    
    # read all the required input images from 'testPatient' input directory
    images = read_input_data()
    
    # extract slices from each input image and store the slices in the Slices output directory
    for file_name, image in images:
        slices_dir = join_path(SLICES_OUTPUT_DIR, remove_file_extension(file_name))
        os.makedirs(slices_dir, exist_ok = True)
        slices = brainExtraction.slice_brain_image(image)
        index = 1
        for slice in slices:
            cv2.imwrite(join_path(slices_dir, str(index) + IMAGE_EXTENSION), slice)
            index += 1

    # initialise Boundaries output directory
    init_output_dirs(BOUNDARIES_OUTPUT_DIR)

    # get list of all sub directories under Slices folder    
    slice_dirs = [dir for dir in os.listdir(SLICES_OUTPUT_DIR) if os.path.isdir(join_path(SLICES_OUTPUT_DIR, dir))]

    # for each sub directory under Slices directory read all the slice image files and 
    # draw boundaries on them and write the output images to Boundaries directory
    for slice_dir in slice_dirs:
        source_path = join_path(SLICES_OUTPUT_DIR, slice_dir)
        sub_directory = join_path(BOUNDARIES_OUTPUT_DIR, slice_dir)
        os.makedirs(sub_directory, exist_ok = True)
        for file_name in os.listdir(source_path):
            brain_image = cv2.imread(join_path(source_path, file_name))
            boundary_image = brainExtraction.draw_brain_boundary(brain_image, BOUNDARY_COLOR, BOUNDARY_THICKNESS)
            cv2.imwrite(join_path(sub_directory, file_name), boundary_image)

if __name__ == '__main__':
    main()
