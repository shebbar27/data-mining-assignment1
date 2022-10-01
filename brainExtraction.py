import cv2

valid_slice_coordinates = []

# verifify whether the boundary coordinates are valid and add them valid boundary coordinates
def validate_coordinates(x, y, w, h):
    # reject if width or height is less than 10 pixels
    if w < 10 or h < 10:
        return
    
    # reject if width or height is greater than 200 pixels
    if w > 200 or h > 200:
        return
    
    # assume first boundary coordinates as valid
    if valid_slice_coordinates.count == 0:
        valid_slice_coordinates.append((x, y, w, h))
        return

    # for each existing valid boundary coordinates check for overlap with new coordinates
    overlapped = False
    for coordinates in valid_slice_coordinates:
        x1 = coordinates[0]
        y1 = coordinates[1]
        x2 = coordinates[0] + coordinates[2]
        y2 = coordinates[1] + coordinates[3]

        # if there is an ovelap keep the larger boundary coordinates
        if x >= x1 and x <= x2 and y >= y1 and y <= y2:
            # print(f"overlapping found: {x1}, {y1}, {coordinates[2]}, {coordinates[3]}")
            if w * h > coordinates[2] * coordinates[3]:
                valid_slice_coordinates.remove(coordinates)
                # print(f"removed coordinates: {x1}, {y1}, {coordinates[2]}, {coordinates[3]}")
                break
            else:
                overlapped = True
        
        if x + w >= x1 and x + w <= x2 and y + h >= y1 and y + h <= y2:
            # print(f"overlapping found: {x1}, {y1}, {coordinates[2]}, {coordinates[3]}")
            if w * h > coordinates[2] * coordinates[3]:
                valid_slice_coordinates.remove(coordinates)
                # print(f"removed coordinates: {x1}, {y1}, {coordinates[2]}, {coordinates[3]}")
                break
            else:
                overlapped = True
        
        if x1 >= x and x1 <= x + w and y1 >= y and y1 <= y + h:
            # print(f"overlapping found: {x1}, {y1}, {coordinates[2]}, {coordinates[3]}")
            if w * h > coordinates[2] * coordinates[3]:
                valid_slice_coordinates.remove(coordinates)
                # print(f"removed coordinates: {x1}, {y1}, {coordinates[2]}, {coordinates[3]}")
                break
            else:
                overlapped = True

        if x2 >= x and x2 <= x + w and y2 >= y and y2 <= y + h:
            # print(f"overlapping found: {x1}, {y1}, {coordinates[2]}, {coordinates[3]}")
            if w * h > coordinates[2] * coordinates[3]:
                valid_slice_coordinates.remove(coordinates)
                # print(f"removed coordinates: {x1}, {y1}, {coordinates[2]}, {coordinates[3]}")
                break
            else:
                overlapped = True
            
    if not overlapped:
        valid_slice_coordinates.append((x, y, w, h))


# function to slice input fMRI image containing multipe brain images into individual images
def slice_brain_image(brain_image):
    BINARY_THRESHOLD = 65
    MAX_PIXEL_VALUE = 255
    OFFSET_PIXELS = 15

    brain_images = []
    gray_image = cv2.cvtColor(brain_image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, BINARY_THRESHOLD, MAX_PIXEL_VALUE, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        validate_coordinates(x, y, w, h)
            
    for coordinates in valid_slice_coordinates:
        x = coordinates[0]
        y = coordinates[1]
        w = coordinates[2]
        h = coordinates[3]
        cv2.rectangle(brain_image, (x, y), (x + w, y + h), (0, 0, 255), 1)
        slice = brain_image.copy()[y - OFFSET_PIXELS : y + h + OFFSET_PIXELS, x - OFFSET_PIXELS :  x + w + OFFSET_PIXELS]
        brain_images.append(slice)

    brain_images.append(brain_image)
    return brain_images


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