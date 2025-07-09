#################################################################
# FILE : image_editor.py
# WRITER : noa haba, noa_haba , 316034453
# EXERCISE : intro2cs ex5 2022-2023
# DESCRIPTION: A simple program - cartoonify
# STUDENTS I DISCUSSED THE EXERCISE WITH: Bugs Bunny, b_bunny.
#								 	      Daffy Duck, duck_daffy.
# WEB PAGES I USED: www.looneytunes.com/lola_bunny
# NOTES: ...
#################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
from ex5_helper import *
import sys
from math import floor, ceil

##############################################################################
#                                  Functions                                 #
##############################################################################


# Variables that are more convenient to work with later
RED_COEFFICIENT = 0.299
GREEN_COEFFICIENT = 0.587
BLUE_COEFFICIENT = 0.114
RED_INDEX = 0
GREEN_INDEX = 1
BLUE_INDEX = 2
MAX_PIXEL_VALUE = 255
MIN_PIXEL_VALUE = 0
ROTATE_RIGHT = "R"
ROTATE_LEFT = "L"
MAX_SHADES = 256


def make_pixel_in_borders(pixel_value):
    """An auxiliary function for determining the boundaries of the pixel,
     for use other functions later in the program"""
    pixel_value = min(pixel_value, MAX_PIXEL_VALUE)
    pixel_value = max(pixel_value, MIN_PIXEL_VALUE)
    return pixel_value


def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    """
    separate channels
    :param image: 3D list
    :return: A list of 2D images each represents single color channel.
    """
    outer_matrix = []
    for channel in range(len(image[0][0])):
        channel_matrix = []
        for row in range(len(image)):
            row_matrix = []
            for col in range(len(image[0])):
                row_matrix.append(image[row][col][channel])
            channel_matrix.append(row_matrix)
        outer_matrix.append(channel_matrix)
    return outer_matrix


def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    """
    does the opposite of the previous function,
    :param channels: Gets a channels-long list of 2D images consisting
    of individual color channels
    :return: One color image that measures .rows × columns × channels
    """
    outer_matrix = []
    for row in range(len(channels[0])):
        row_matrix = []
        for col in range(len(channels[0][0])):
            channel_matrix = []
            for channel in range(len(channels)):
                channel_matrix.append(channels[channel][row][col])
            row_matrix.append(channel_matrix)
        outer_matrix.append(row_matrix)
    return outer_matrix


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    """
    A color image (red, green, blue) becomes a black and white image
    :param colored_image: 3D list
    :return: 2D list
    """
    outer_matrix = []
    for row in range(len(colored_image)):
        row_matrix = []
        for col in range(len(colored_image[0])):
            sum_by_formula = \
                round(colored_image[row][col][RED_INDEX] * RED_COEFFICIENT +
                      colored_image[row][col][
                          GREEN_INDEX] * GREEN_COEFFICIENT +
                      colored_image[row][col][BLUE_INDEX] * BLUE_COEFFICIENT)
            sum_by_formula = make_pixel_in_borders(sum_by_formula)
            row_matrix.append(sum_by_formula)
        outer_matrix.append(row_matrix)
    return outer_matrix


def blur_kernel(size: int) -> Kernel:
    """Blur an image using a kernel"""
    outer_matrix = []
    for row in range(size):
        row_matrix = []
        for col in range(size):
            row_matrix.append(float(1) / float(size ** 2))
        outer_matrix.append(row_matrix)
    return outer_matrix


def check_borders(image, row, col):
    """check borders of image to calculate a pixel later in the program"""
    return len(image) > row >= 0 and len(image[row]) > col >= 0


def apply_kernel_helper1(image, row_center, col_center, size):
    """Identify the pixel (image[row][col] with the central entry in the
    kernel matrix"""
    new_matrix = []
    for row in range(row_center - (size // 2), row_center + (size // 2) + 1):
        row_matrix = []
        for col in range(col_center - (size // 2),
                         col_center + (size // 2) + 1):
            if check_borders(image, row, col):
                row_matrix.append(image[row][col])
            else:
                row_matrix.append(image[row_center][col_center])
        new_matrix.append(row_matrix)
    return new_matrix


def apply_kernel_helper2(centralized_matrix, kernel):
    """Sum up the values of the pixel's neighbors including the pixel
    itself multiplied by their corresponding entry in the kernel
    The pixel itself (multiple their corresponding entry in the kernel)"""
    sum_matrix = 0
    for row in range(len(kernel)):
        for col in range(len(kernel)):
            sum_matrix += (centralized_matrix[row][col] * kernel[row][col])
    return sum_matrix


def apply_kernel(image: SingleChannelImage,
                 kernel: Kernel) -> SingleChannelImage:
    """
    Getting an image the same size as the original by calculating a kernel
    :param image: An image with a single color channel 2D list
    :param kernel: 2D list
    :return: Image is the same size as the original image
    """
    new_matrix = []
    for row in range(len(image)):
        row_matrix = []
        for col in range(len(image[0])):
            centralized_matrix = apply_kernel_helper1(image, row, col,
                                                      len(kernel))
            new_element = apply_kernel_helper2(centralized_matrix, kernel)
            row_matrix.append(make_pixel_in_borders(round(new_element)))
        new_matrix.append(row_matrix)
    return new_matrix


def bilinear_interpolation(image: SingleChannelImage, y: float,
                           x: float) -> int:
    """
    Bilinear interpolation for image
    :param image: 2D list
    :param y: Coordinates of the width of the image
    :param x: Coordinates of the length of the image
    :return: The pixel value is an integer between 0 and 255 according to
    the specific calculation
    """
    delta_x = x - floor(x)
    delta_y = y - floor(y)
    a = image[floor(y)][floor(x)]
    b = image[ceil(y)][floor(x)]
    c = image[floor(y)][ceil(x)]
    d = image[ceil(y)][ceil(x)]
    new_value = (a * (1 - delta_x) * (1 - delta_y)) + \
                (b * delta_y * (1 - delta_x)) + \
                (c * delta_x * (1 - delta_y)) + \
                (d * delta_x * delta_y)
    return make_pixel_in_borders(round(new_value))


def map_corners(image, new_height, new_width, row, col):
    """Corners will be mapped to corners."""
    if row == 0 and col == 0:
        return image[0][0]
    elif row == new_height - 1 and col == 0:
        return image[len(image) - 1][0]
    elif row == 0 and col == new_width - 1:
        return image[0][len(image[0]) - 1]
    elif row == new_height - 1 and col == new_width - 1:
        return image[len(image) - 1][len(image[0]) - 1]
    return None


def resize(image: SingleChannelImage, new_height: int,
           new_width: int) -> SingleChannelImage:
    """
    A new image with a new size so that the value of each pixel in the
    returned image is calculated according to its relative position in the
    source image
    :param image: 2D list
    :param new_height: Integer
    :param new_width: Integer
    :return: New size image (new height * new width)
    """
    new_matrix = []
    for row in range(new_height):
        row_matrix = []
        for col in range(new_width):
            corner_element = map_corners(image, new_height, new_width, row,
                                         col)
            if corner_element:
                row_matrix.append(corner_element)
            else:
                y_higher = row * (float(len(image) - 1)) / (
                        float(new_height) - 1)
                x_higher = col * (float(len(image[0]) - 1)) / (
                        float(new_width) - 1)
                new_value = bilinear_interpolation(image, y_higher,
                                                   x_higher)
                row_matrix.append(new_value)
        new_matrix.append(row_matrix)
    return new_matrix


def get_new_proportions(image, max_size):
    """get new proportions"""
    if len(image) >= len(image[0]):  # if height is bigger or equal to width
        new_height = max_size
        new_width = floor(float(max_size * len(image[0])) / float(len(image)))
    else:
        new_width = max_size
        new_height = floor(float(max_size * len(image)) / float(len(image[0])))
    return new_height, new_width


def transpose(image):
    """Auxiliary function to transpose of lists (image)"""
    new_matrix = []
    for col in range(len(image[0])):
        row_matrix = []
        for row in range(len(image)):
            row_matrix.append(image[row][col])
        new_matrix.append(row_matrix)
    return new_matrix


def invert_rows(image):
    """Auxiliary function to invert rows in lists"""
    new_matrix = []
    for row in image:
        new_matrix.append(row[::-1])
    return new_matrix


def rotate_90_helper(image, direction):
    """What does the function do if you rotate it 90 degrees
    left and right"""
    if direction == ROTATE_RIGHT:
        return invert_rows(transpose(image))
    if direction == ROTATE_LEFT:
        return transpose(invert_rows(image))


def rotate_90(image: Image, direction: str) -> Image:
    """Rotate image by 90 degrees (right or left)"""
    if not isinstance(image[0][0], List):
        return rotate_90_helper(image, direction)
    channels = separate_channels(image)
    new_channels = []
    for channel in channels:
        new_channels.append(rotate_90_helper(channel, direction))
    return combine_channels(new_channels)


def calculate_threshold(blurred_image, row, col, r, c):
    """Formula of threshold"""
    sum_pixels = 0
    num_pixels = 0
    for i in range(max(row - r, 0), min(row + r + 1, len(blurred_image))):
        for j in range(max(col - r, 0), min(col + r + 1,
                                            len(blurred_image[0]))):
            sum_pixels += blurred_image[i][j]
            num_pixels += 1
    return float(sum_pixels) / float(num_pixels) - c


def get_edges(image: SingleChannelImage, blur_size: int, block_size: int,
              c: float) -> SingleChannelImage:
    """
    Black and white image (2D list) turn to a new image,
    with the same dimensions, which consists of only two values
    (black and white) where black pixels mark boundaries in the image.
    """
    blurred_image = apply_kernel(image, blur_kernel(blur_size))
    new_matrix = []
    for row in range(len(image)):
        row_matrix = []
        for col in range(len(image[0])):
            if blurred_image[row][col] < calculate_threshold(
                    blurred_image, row, col, block_size // 2, c):
                row_matrix.append(MIN_PIXEL_VALUE)
            else:
                row_matrix.append(MAX_PIXEL_VALUE)
        new_matrix.append(row_matrix)
    return new_matrix


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    """An image with a single color channel becomes an image with identical
    dimensions, in which the values of The pixels are calculated
    according to a formula"""
    new_matrix = []
    for row in range(len(image)):
        row_matrix = []
        for col in range(len(image[0])):
            new_element = round(
                floor(image[row][col] * (float(N) / float(MAX_SHADES))) *
                (float(MAX_SHADES - 1) / float(N - 1)))
            row_matrix.append(make_pixel_in_borders(new_element))
        new_matrix.append(row_matrix)
    return new_matrix


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    """quantize colored image"""
    channels = separate_channels(image)
    new_channels = []
    for channel in channels:
        new_channels.append(quantize(channel, N))
    return combine_channels(new_channels)


def resize_colored_image(image, new_height, new_width):
    """resize colored image"""
    channels = separate_channels(image)
    new_channels = []
    for channel in channels:
        new_channels.append(resize(channel, new_height, new_width))
        image = combine_channels(new_channels)
    return image


def apply_kernel_colored_image(image, kernel_size):
    """apply kernel colored image"""
    channels = separate_channels(image)
    new_channels = []
    for channel in channels:
        new_channels.append(apply_kernel(channel, kernel_size))
        image = combine_channels(new_channels)
    return image


def actions():
    options = ["There are several options for image editing: ",
               "1. Convert a color image to a grayscale image.",
               "2. Blurring the image.",
               "3. Resize the image.",
               "4. Rotate the image by 90 degrees.",
               "5. Creating the contour image (edges) of the original image.",
               "6. Quantizing the image.",
               "7. Showing the picture.",
               "8. Exit the program and save the image.\n"]
    for i in range(len(options)):
        print(options[i])


def is_grayscale(image):
    """
    check if image is an Empty image,
    Get the dimensions of the image,
    Check if all pixels have the same value across channels,
    Check if pixel is a list or tuple,
    Check if Pixel has more than one value, or it's not an integer
    """
    if len(image) == 0:
        return False
    height = len(image)
    width = len(image[0])
    for i in range(height):
        for j in range(width):
            pixel = image[i][j]
            if isinstance(pixel, (list, tuple)):
                if len(pixel) != 1 or not isinstance(pixel[0], int):
                    return False
            elif not isinstance(pixel, int):
                return False
    return True


def main():
    """Executing the function will bring a colored image which is
    the illustrated version of the original image and save the image"""
    if len(sys.argv) != 2:
        print("Invalid number of arguments!")
        return

    image = load_image(sys.argv[1])

    while True:
        actions()
        choice = input(
            "Enter the number of the operation you want to perform: ")

        if choice == "1":
            if is_grayscale(image):
                print("The image is already grayscale.\n")
            else:
                image = RGB2grayscale(image)

        elif choice == "2":
            kernel_size = input(
                "Enter the kernel size for blurring "
                "(must be an odd positive integer): ")
            if not kernel_size.isdigit():
                print("Invalid kernel size.\n")
                continue
            kernel_size = int(kernel_size)
            if kernel_size % 2 == 0 or kernel_size < 1:
                print("Invalid kernel size.\n")
            else:
                kernel_size = blur_kernel(kernel_size)
                if is_grayscale(image):
                    image = apply_kernel(image, kernel_size)
                else:
                    image = apply_kernel_colored_image(image, kernel_size)

        elif choice == "3":
            new_size_user = input(
                "Enter the size of the image in the format 'height,width': ")
            if not new_size_user.isdigit():
                print("Invalid image size.\n")
                continue
            new_size_split = new_size_user.split(",")
            new_size_split = [int(num) for num in new_size_split]
            if len(new_size_split) != 2:
                print("Invalid image size.\n")
                continue
            new_height, new_width = new_size_split[0], new_size_split[1]
            if new_height < 1 or new_width < 1:
                print("Invalid image size.\n")
                continue
            if is_grayscale(image):
                image = resize(image, new_height, new_width)
            else:
                image = resize_colored_image(image, new_height, new_width)

        elif choice == "4":
            direction = input("Enter the direction of rotation: R or L: ")
            if direction not in ['R', 'L']:
                print("Invalid rotation direction.\n")
            else:
                image = rotate_90(image, direction)

        elif choice == "5":
            values_input = input(
                "Select 3 comma separated values: blur_size, block_size, c: ")
            values_input_split = values_input.split(",")
            if len(values_input_split) != 3:
                print("Invalid input.\n")
                continue
            else:
                for num in values_input_split:
                    if type(num) == float:
                        print("Invalid input.\n")
                        continue
            values_input_split = [int(num) for num in values_input_split]
            blur_size, block_size, c = values_input_split[0], \
                values_input_split[1], values_input_split[2]
            if (blur_size is None) or (
                    block_size is None) or (c is None) or (not (
                    blur_size % 2 == 1 and blur_size > 0 and
                    block_size % 2 == 1 and block_size > 0 and c >= 0)):
                print("Invalid input.\n")
            else:
                if is_grayscale(image):
                    image = get_edges(image, blur_size, block_size, c)
                else:
                    gray_image = RGB2grayscale(image)
                    image = get_edges(gray_image, blur_size, block_size, c)

        elif choice == "6":
            N_input = input(
                "Enter the number of tones to quantize each color channel to"
                "(must be a positive integer greater than 1): ")
            if not N_input.isdigit():
                print("Invalid number of tones.\n")
            else:
                N_input = int(N_input)
                if N_input < 2:
                    print("Invalid number of tones.\n")
                    continue
                if is_grayscale(image):
                    image = quantize(image, N_input)
                else:
                    image = quantize_colored_image(image, N_input)

        elif choice == "7":
            show_image(image)

        elif choice == "8":
            save_path = input("Enter a path to save the image: ")
            save_image(image, save_path)
            return

        else:
            print("Invalid choice. Please select a number between 1 and 8.\n")


if __name__ == '__main__':
    main()
