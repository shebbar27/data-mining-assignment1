import cv2

# utiltiy function to check whether given two rectangles overlap with each other 
def is_overlapping(rect1, rect2):
    dx = min(rect1[2], rect2[2]) - max(rect1[0], rect2[0])
    dy = min(rect1[3], rect2[3]) - max(rect1[1], rect2[1])

    if dx > 0 and dy > 0:
        return True
    return False


# verifify whether the boundary coordinates are valid and add them valid boundary coordinates
def validate_coordinates(x, y, w, h, valid_slice_coordinates, invalid_slice_coordinates, offset_pixels):
    MIN_DIMENSION = 10
    MAX_DIMENSION = 250
    # reject if width or height is less than 10 pixels
    if w < MIN_DIMENSION or h < MIN_DIMENSION:
        return
    
    # reject if width or height is greater than 200 pixels
    if w > MAX_DIMENSION or h > MAX_DIMENSION:
        return
    
    # assume first boundary coordinates as valid
    if len(valid_slice_coordinates) == 0:
        valid_slice_coordinates.add((x, y, w, h))
        return

    is_valid = True
    # for each existing valid boundary coordinates check for overlap with new coordinates
    for x1, y1, w1, h1 in valid_slice_coordinates:
        if is_overlapping([x - offset_pixels, y - offset_pixels, x + w + offset_pixels, y + h + offset_pixels], [x1, y1, x1 + w1, y1 + h1]):
            if w * h > w1 * h1:
                invalid_slice_coordinates.add((x1, y1, w1, h1))
            else:
                is_valid = False
                    
    if is_valid:
        valid_slice_coordinates.add((x, y, w, h))


# function to slice input fMRI image containing multipe brain images into individual images
def slice_brain_image(brain_image):
    BINARY_THRESHOLD = 65
    MAX_PIXEL_VALUE = 255
    OFFSET_PIXELS = 15

    brain_images = []
    valid_slice_coordinates = set()
    invalid_slice_coordinates = set()
    gray_image = cv2.cvtColor(brain_image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, BINARY_THRESHOLD, MAX_PIXEL_VALUE, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        validate_coordinates(x, y, w, h, valid_slice_coordinates, invalid_slice_coordinates, OFFSET_PIXELS)

    for coordinate in invalid_slice_coordinates:
        valid_slice_coordinates.discard(coordinate)

    for x, y, w, h in valid_slice_coordinates:
        # cv2.rectangle(brain_image, (x - OFFSET_PIXELS, y - OFFSET_PIXELS), (x + w + OFFSET_PIXELS, y + h + OFFSET_PIXELS), (0, 0, 255), 1)
        slice = brain_image.copy()[y - OFFSET_PIXELS : y + h + OFFSET_PIXELS, x - OFFSET_PIXELS :  x + w + OFFSET_PIXELS]
        brain_images.append(slice)

    # brain_images.append(brain_image)
    return brain_images


# function to draw boundary on brain image
def draw_brain_boundary(brain_image, boundary_color, boundary_thickness):
    BINARY_THRESHOLD = 65
    MAX_PIXEL_VALUE = 255
    CONTOUR_INDEX = -1

    gray_image = cv2.cvtColor(brain_image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, BINARY_THRESHOLD, MAX_PIXEL_VALUE, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    brain_boundary_image = cv2.drawContours(brain_image, contours, CONTOUR_INDEX, boundary_color, boundary_thickness)
    return brain_boundary_image