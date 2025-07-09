#################################################################
# FILE : image_editor.py
# WRITER : your_name , your_login , your_id
# EXERCISE : intro2cs ex5 2022-2023
# DESCRIPTION: A simple program that...
# STUDENTS I DISCUSSED THE EXERCISE WITH: Bugs Bunny, b_bunny.
#								 	      Daffy Duck, duck_daffy.
# WEB PAGES I USED: www.looneytunes.com/lola_bunny
# NOTES: ...
#################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
import copy
from sys import argv

import ex5_helper
from ex5_helper import *

from typing import Optional
import math

NUM_ARGUMENTS = 8
LEGAL_FORMAT = ".png"
ERROR_NUM_ARGUMENTS = "Usage: python3 cartoonify.py <image_src> <cartoon_dest> <max_im_size> " \
                      "<blur_size> <th_block_size> <th_c> <quant_num_shades>"
ERROR_FORMAT = "The image files are not in the .png format!"
ALL_OPTIONS = "choose the option you would like to implement " \
              "1." \
              "2." \
              "3." \
              "4." \
              "5." \
              "6." \
              "7." \
              "8."

##############################################################################
#                                  Functions                                 #
##############################################################################


def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    seprated_image = []
    if not image:
        return image
    for chl in range(len(image[0][0])):
        tmp_arr = []
        for rows in range(len(image)):
            row_arr = []
            for cols in range(len(image[rows])):
                row_arr.append(image[rows][cols][chl])
            tmp_arr.append(row_arr)
        seprated_image.append(tmp_arr)

    return seprated_image


def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    new_lst = []
    for row in range(len(channels[0])):
        new_row = []
        for col in range(len(channels[0][0])):
            new_col = []
            for chl in range(len(channels)):
                new_col.append(channels[chl][row][col])
            new_row.append(new_col)
        new_lst.append(new_row)
    return new_lst


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    new_image = []
    for row in range(len(colored_image)):
        new_row = []
        for column in range(len(colored_image[row])):
            new_column = colored_image[row][column][0] * 0.299 + colored_image[row][column][1] * 0.587 + \
                         colored_image[row][column][2] * 0.114
            new_row.append(round(new_column))
        new_image.append(new_row)
    return new_image


def blur_kernel(size: int) -> Kernel:
    matrix = []
    for row in range(size):
        new_row = []
        for column in range(size):
            new_row.append(float(1) / float(size ** 2))
        matrix.append(new_row)
    return matrix


def calc_pixel(image, kernel, row, col):
    new_pixel = 0
    for i, row_index in enumerate(range(-int(len(kernel) / 2), int(len(kernel) / 2) + 1)):
        for j, col_index in enumerate(range(-int(len(kernel) / 2), int(len(kernel) / 2) + 1)):
            if row_index + row >= len(image) or row_index + row < 0 \
                    or col_index + col >= len(image[0]) or col_index + col < 0:
                new_pixel += image[row][col] * kernel[i][j]
            else:
                new_pixel += image[row + row_index][col + col_index] * kernel[i][j]
    if new_pixel > 255:
        new_pixel = 255
    if new_pixel < 0:
        new_pixel = 0
    return round(new_pixel)


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    new_image = copy.deepcopy(image)
    for row in range(len(image)):
        for col in range(len(image[0])):
            new_image[row][col] = calc_pixel(image, kernel, row, col)
    return new_image


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    y_floor = max(math.floor(y), 0)
    y_ceil = min(math.ceil(y), len(image) - 1)
    x_floor = max(math.floor(x), 0)
    x_ceil = min(math.ceil(x), len(image[0]) - 1)
    a = image[y_floor][x_floor]
    b = image[y_ceil][x_floor]
    c = image[y_floor][x_ceil]
    d = image[y_ceil][x_ceil]
    delta_x = abs(x - x_floor)
    delta_y = abs(y - y_floor)
    return round(a * (1 - delta_x) * (1 - delta_y) +
                 b * delta_y * (1 - delta_x) + c * delta_x * (1 - delta_y) +
                 d * delta_x * delta_y)


def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    matrix = []
    for row in range(new_height):
        new_row = []
        for column in range(new_width):
            row_index = row * (int(len(image)-1) / (new_height-1))
            column_index = column * (int(len(image[0])-1) / (new_width-1))
            new_row.append(bilinear_interpolation(image, row_index, column_index))
        matrix.append(new_row)
    return matrix

# def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
#     orig_height = len(image)
#     orig_width = len(image[0])
#     height_ratio = (orig_height-1) / (new_height-1)
#     width_ratio = (orig_width-1) / (new_width-1)
#     print ("ratio", height_ratio, width_ratio)
#     # Create the new image mat
#     #new_image = []
#     # for i in range(new_height):
#     #     new_row=[]
#     #     for j in range (new_width):
#     #         new_row.append(0)
#     #     new_image.append(new_row)
#     #print (new_image)
#     # The values in the edges
#     # new_image[0][0] = image[0][0]
#     # new_image[0][new_width-1] = image[0][len(image[0])-1]
#     # new_image[new_height-1][0] = image[len(image)-1][0]
#     # new_image[new_height-1][new_width-1] = image[len(image)-1][len(image[0])-1]
#     #print(new_image)
#     # The values in the rest of the image
#     new_image=[]
#     for i in range(new_height):
#         new_row = []
#         for j in range(new_width):
#             # if (i == 0 and j == 0) or (i == 0 and j == new_width-1) or (i == new_height-1 and j == 0) or (i == new_height-1) and (j == new_width-1):
#             #     if i < len(image) and j < len(image[0]):
#             #         new_row.append(image[i][j])
#             #     else:
#             #         new_row.append(0)
#             print ("j,i:", j,i)
#             y = height_ratio * i
#             x = width_ratio * j
#             print (y,x)
#             new = bilinear_interpolation(image, y, x)
#             new_row.append(new)
#             # if i == 0:
#             #     new_row.append(image[0][len(image[0])-1])
#             # if i == new_height - 1:
#             #     new_row.append(image[len(image) - 1][len(image[0])- 1])
#         new_image.append(new_row)
#         # Changing the edges:
#     new_image[0][0]=image[0][0]
#     new_image[len(new_image)-1][0] = image[len(image)-1][0]
#     new_image[0][len(new_image[0])-1] = image[0][len(image[0])-1]
#     new_image[len(new_image)-1][len(new_image[0])-1] = image[len(image)-1][len(image[0])-1]
#     return new_image


def scale_down_colored_image(image, max_size):
    if len(image) <= max_size and len(image[0]) <= max_size:
        return
    else:
        channels = separate_channels(image)
        new_channels = []
        for channel in channels:
            new_channels.append(resize(channel, max_size, max_size))
        return combine_channels(new_channels)


# print (resize([[15, 30, 45, 60, 75], [90, 105, 120, 135, 190], [165 ,180 ,195, 210,225]], 6, 7))
def invert_rows(matrix):
    new_matrix = []
    for row in matrix:
        new_matrix.append(row[::-1])
    return new_matrix


def transpose(matrix):
    if not matrix:
        return matrix
    new_matrix = [[] for i in range(len(matrix[0]))]
    for col in range(len(matrix[0])):
        for row in range(len(matrix)):
            new_matrix[col].append(matrix[row][col])
    return new_matrix


def rotate_90(image: Image, direction: str) -> Image:
    if direction == 'L':
        return transpose(invert_rows(image))
    return invert_rows(transpose(image))


def cal_threshold(blurred_image, row_start, col_start, row_end, col_end):
    cur_sum_px = 0
    num_px = 0
    for i in range(max(row_start - row_end, 0), min(row_start + row_end + 1, len(blurred_image))):
        for j in range(max(col_start - row_end, 0), min(col_start + row_end + 1,
                                                        len(blurred_image[0]))):
            cur_sum_px += blurred_image[i][j]
            num_px += 1
    return float(cur_sum_px) / float(num_px) - col_end



def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    blurred_image = apply_kernel(image, blur_kernel(blur_size))
    new_lst = []
    for row in range(len(image)):
        new_row = []
        for col in range(len(image[0])):
            if blurred_image[row][col] > cal_threshold(blurred_image, row, col, block_size // 2, c):
                new_row.append(255)
            else:
                new_row.append(0)
        new_lst.append(new_row)
    return new_lst


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    qimg = []
    for row in range(len(image)):
        new_row = []
        for col in range(len(image[row])):
            new_value = round(math.floor(image[row][col] * (
                    float(N) / float(256))) * (float(255) / float(N - 1)))
            new_row.append(new_value)
        qimg.append(new_row)
    return qimg


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    channels = separate_channels(image)
    quantized_channels = []
    for channel in channels:
        quantized_channels.append(quantize(channel, N))
    return combine_channels(quantized_channels)


def add_mask_helper(image1, image2, mask):
    new_image = []
    for row in range(len(mask)):
        new_row = []
        for col in range(len(mask[row])):
            new_value = round(image1[row][col] * mask[row][col] +
                              image2[row][col] * (1 - mask[row][col]))
            new_row.append(new_value)
        new_image.append(row)
    return new_image


def add_mask(image1, image2, mask):
    channels1 = separate_channels(image1)
    channels2 = separate_channels(image2)
    masked_channels = []
    for i in range(len(channels1)):
        masked_channels.append(add_mask_helper(channels1[i], channels2[i], mask))
    return combine_channels(masked_channels)


def get_mask_from_edges(edges):
    mask = []
    for row in range(len(edges)):
        new_row = []
        for col in range(len(edges[row])):
            new_row.append(round(float(edges[row][col]) / float(255)))
        mask.append(new_row)
    return mask


def check_cla():
    if len(argv) != NUM_ARGUMENTS:
        print(ERROR_NUM_ARGUMENTS)
        return False
    return True


if __name__ == '__main__':
    check_cla()
    image = load_image(argv[1])
    while True:
            user_input = input(ALL_OPTIONS)
            if not (user_input.isnumeric() and int(user_input) <= 8 and int(user_input) > 0):
                print("not correct")
            elif int(user_input) == 1:
                if not isinstance(image[0][0], list):
                    print('Image is already grayscale. Please provide an RGB image.')
                    continue
                else:
                    image = RGB2grayscale(image)
            elif int(user_input) == 2:
                kernel_size = int(input("please choose kernel size "))
                if not isinstance(kernel_size, int) or kernel_size % 2 == 0:
                    print("wrong kernel ")
                    continue
                elif isinstance(image[0][0], list):
                    image = separate_channels(image)
                    for i in range(len(image)):
                        image[i] = apply_kernel(image[i], blur_kernel(kernel_size))
                    image = combine_channels(image)
                else:
                    image = apply_kernel(image, blur_kernel(kernel_size))
            elif int(user_input) == 3:
                row_col = (input("please choose row, col and dont forget the ',' "))  # need to add exceptions
                row_col = row_col.split(',')
                if len(row_col) != 2 or int(row_col[1]) <= 1 or int(row_col[0]) <= 1:
                    continue
                else:
                    row, col = int(row_col[0]), int(row_col[1])
                    if isinstance(image[0][0], list):
                        image = separate_channels(image)
                        for i in range(len(image)):
                            image[i] = resize(image[i], row, col)
                        image = combine_channels(image)
                    else:
                        image = resize(image, row, col)
            elif int(user_input) == 4:
                RorL = input("Choose R or L ")
                if RorL != 'L' and RorL != 'R':
                    continue
                if RorL == 'L':
                    image = rotate_90(image, 'L')
                else:
                    image = rotate_90(image, 'R')
            elif int(user_input) == 5:
                ch_input = input("please choose Blur_size, Block_size, c ")
                ch_input = ch_input.split(',')
                if len(ch_input) != 3 or not ch_input[0].isnumeric() or not ch_input[1].isnumeric() \
                    or int(ch_input[0]) < 0 or int(ch_input[1]) < 0 or float(ch_input[2]) < 0\
                        or int(ch_input[0]) % 2 == 0 or int(ch_input[1]) % 2 == 0:
                    continue
                blur_size, block_size, c = int(ch_input[0]), int(ch_input[1]), float(ch_input[2])
                if isinstance(image[0][0], list):
                    image = RGB2grayscale(image)
                image = get_edges(image, blur_size, block_size, c)
            elif int(user_input) == 6:
                N_q = input("pliz choose N for ququqnatation ")
                if not N_q.isnumeric() or int(N_q) < 2:
                    print("Invalid N value. Please choose a number >= 2")
                    continue
                elif isinstance(image[0][0], list):
                    image = quantize_colored_image(image, int(N_q))
                else:
                    image = quantize(image, int(N_q))
            elif int(user_input) == 7:
                ex5_helper.show_image(image)
                continue
            elif int(user_input) == 8:
                user_input = input("where to save the image ")
                save_image(image, user_input)
                break


