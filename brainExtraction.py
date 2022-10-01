import cv2

# function to slice input fMRI image containing multipe brain images into individual images
def slice_brain_image(brain_image):
    return [brain_image, brain_image, brain_image, brain_image, brain_image]

# function to draw boundary on brain image
def draw_brain_boundary(brain_image, boundary_color, boundary_thickness):
    BINARY_THRESHOLD = 65
    MAX_PIXEL_VALUE = 255
    CONTOUR_INDEX = -1

    gray_image = cv2.cvtColor(brain_image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, BINARY_THRESHOLD, MAX_PIXEL_VALUE, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    brain_boundary_image = cv2.drawContours(brain_image, contours, CONTOUR_INDEX, boundary_color, boundary_thickness)
    return brain_boundary_image