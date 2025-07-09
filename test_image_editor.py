import pytest
from image_editor import *


@pytest.mark.parametrize("img, expected", [
    # Case 1
    ([[[1, 2]]], [[[1]], [[2]]]),
    # Case 2
    ([[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
      [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
      [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
      [[1, 2, 3], [1, 2, 3], [1, 2, 3]]],
     [[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
      [[2, 2, 2], [2, 2, 2], [2, 2, 2], [2, 2, 2]],
      [[3, 3, 3], [3, 3, 3], [3, 3, 3], [3, 3, 3]]]),
    # Case 3
    ([[[1, 22, 23], [1, 1, 1]],
      [[0, 0, 0], [1, 1, 1]]],
     [[[1, 1], [0, 1]],
      [[22, 1], [0, 1]],
      [[23, 1], [0, 1]]]),
    # Case 4
    ([[[1, 2, 3]]], [[[1]], [[2]], [[3]]]),
])
def test_separate_channels(img, expected):
    assert separate_channels(img) == expected


@pytest.mark.parametrize("channels, expected", [
    # Case 1
    ([[[1]], [[2]]], [[[1, 2]]]),
    # Case 2
    ([[[1, 2], [3, 4]]], [[[1], [2]], [[3], [4]]]),
    # Case 3
    ([[[1, 4], [7, 10]],
      [[2, 5], [8, 11]],
      [[3, 6], [9, 12]]],
     [[[1, 2, 3], [4, 5, 6]],
      [[7, 8, 9], [10, 11, 12]]]
     )
])
def test_combine_channels(channels, expected):
    assert combine_channels(channels) == expected


@pytest.mark.parametrize("img, expected", [
    # Case 1
    ([[[200, 0, 14], [15, 6, 50]]], [[61, 14]]),
    # Case 2
    ([[[1, 2, 3]]], [[2]]),
    # Case 3
    ([[[1, 2, 3], [4, 5, 6]],
      [[7, 8, 9], [10, 11, 12]]],
     [[2, 5], [8, 11]]),
    # Case 4
    ([[[100, 180, 240]]], [[163]])

])
def test_RGB2grayscale(img, expected):
    assert RGB2grayscale(img) == expected


@pytest.mark.parametrize("size, expected", [
    # Case 1
    (3, [[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9]]),
    # Case 2
    (5, [[1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25], [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25],
         [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25],
         [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25], [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25]])
])
def test_blur_kernel(size, expected):
    assert blur_kernel(size) == expected


@pytest.mark.parametrize("image, kernel, expected", [
    # Case 1
    ([[10, 20, 30, 40, 50],
      [8, 16, 24, 32, 40],
      [6, 12, 18, 24, 30],
      [4, 8, 12, 16, 20]], blur_kernel(5), [[12, 20, 26, 34, 44],
                                            [11, 17, 22, 27, 34],
                                            [10, 16, 20, 24, 29],
                                            [7, 11, 16, 18, 21]]),
    # Case 2
    ([[-10, 20, 30, 40, 50],
      [8, 16, 24, 32, 40],
      [6, 12, 18, 24, 30],
      [4, 8, 12, 16, 20]], blur_kernel(3), [[0, 16, 28, 37, 46],
                                            [8, 14, 24, 32, 37],
                                            [8, 12, 18, 24, 28],
                                            [6, 9, 14, 19, 21]]),
    # Case 3
    ([[1000, 20, 30, 40, 50],
      [8, 16, 24, 32, 40],
      [6, 12, 18, 24, 30],
      [4, 8, 12, 16, 20]], blur_kernel(5), [[255, 60, 66, 34, 44],
                                            [50, 57, 61, 27, 34],
                                            [49, 55, 60, 24, 29],
                                            [7, 11, 16, 18, 21]])
])
def test_apply_kernel(image, kernel, expected):
    assert apply_kernel(image, kernel) == expected


@pytest.mark.parametrize("image, y, x, expected", [
    # Case 1
    ([[0, 64], [128, 255]], 0, 0, 0),
    # Case 2
    ([[0, 64], [128, 255]], 1, 1, 255),
    # Case 3
    ([[0, 64], [128, 255]], 0.5, 0.5, 112),
    # Case 4
    ([[0, 64], [128, 255]], 0.5, 1, 160),
    # Case 5
    ([[15, 30, 45, 60, 75],
      [90, 105, 120, 135, 150],
      [165, 180, 195, 210, 225]], 4 / 5, 8 / 3, 115)
    # Case 6
])
def test_bilinear_interpolation(image, y, x, expected):
    assert bilinear_interpolation(image, y, x) == expected


@pytest.mark.parametrize('image, new_height, new_width, expected', [
    # Case 1
    ([[0, 64], [128, 255]], 3, 3, [[0, 32, 64],
                                   [64, 112, 160],
                                   [128, 192, 255]]),
    # Case 2
    ([[0, 64], [128, 255]], 2, 2, [[0, 64], [128, 255]])
])
def test_resize(image, new_height, new_width, expected):
    assert resize(image, new_height, new_width) == expected


@pytest.mark.parametrize("image, direction, expected", [
    # Case 1
    ([[1, 2, 3], [4, 5, 6]], 'R', [[4, 1],
                                   [5, 2],
                                   [6, 3]]),
    # Case 2
    ([[1, 2, 3], [4, 5, 6]], 'L', [[3, 6],
                                   [2, 5],
                                   [1, 4]]),
    # Case 3
    ([[[1, 2, 3], [4, 5, 6]], [[0, 5, 9], [255, 200, 7]]], 'L', [[[4, 5, 6],
                                                                  [255, 200, 7]],
                                                                 [[1, 2, 3],
                                                                  [0, 5, 9]]])
])
def test_rotate_90(image, direction, expected):
    assert rotate_90(image, direction) == expected


@pytest.mark.parametrize("image, blur_size, block_size, c, expected", [
    # Case 1
    ([[200, 50, 200]], 3, 3, 10, [[255, 0, 255]]),
    # Case 2
    ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 3, 3, 0, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
])
def test_get_edges(image, blur_size, block_size, c, expected):
    assert get_edges(image, blur_size, block_size, c) == expected


@pytest.mark.parametrize("image, N, expected", [
    # Case 1
    ([[0, 50, 100], [150, 200, 250]], 8,  [[0, 36, 109], [146, 219, 255]])
])
def test_quantize(image, N, expected):
    assert quantize(image, N) == expected


@pytest.mark.parametrize("image, N, expected", [
    # Case 1
    ([[[0, 50, 100], [150, 200, 250]]], 8, [[[0, 36, 109], [146, 219, 255]]])
])
def test_quantize_colored_image(image, N, expected):
    assert quantize_colored_image(image, N) == expected
