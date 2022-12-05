import numpy as np
import pandas as pd
import cv2

def printarray(a):
    for i in range(5):
        for k in a:
            for n in k:
                print(n)

def binary(img_array):
    for y in range(len(img_array)):
        for x in range(len(img_array[0])):
            if img_array[y][x] > 127:
                img_array[y][x] = 255
            else:
                img_array[y][x] = 0

def kernel_count(kernel):
    kernel_rows = len(kernel)
    kernel_cols = len(kernel[0])

    count = 0

    for y in range(kernel_rows):
        for x in range(kernel_cols):
            if (kernel[y][x]) == 0:
                count = count + 1
    return count


def thinning2(img_array, smoothness = 0):
    img_rows = len(img_array)
    img_cols = len(img_array[0])

    new_img = [[255] * img_cols] * img_rows
    new_img = np.array(new_img)
    pixel_tup = []

    # image kernel
    kernel = [[0, 0],
              [0, 0]]

    kernel_rows = len(kernel)
    kernel_cols = len(kernel[0])

    kernel_row_half_length = kernel_rows // 2
    kernel_cols_half_length = kernel_cols // 2

    kernel_cnt = kernel_count(kernel)

    # begin looping through image (range is minus 1 because the kernel is 3 in length)
    print("applying filter...")
    for y in range(img_rows - kernel_rows):
        for x in range(img_cols - kernel_cols):

            # keep track of original position of x and y so I can go back to them, because I am going to move them when ->
            # looping through kernel
            original_y = y
            original_x = x

            # keep track of number of matches to kernel
            track = 0

            # begin looping through kernel

            for ky in range(kernel_rows):
                # print("ky")
                for kx in range(kernel_cols):
                    if kernel[ky][kx] == img_array[y][x]:
                        track = track + 1
                    # print("kx")
                    # print((x, y))
                    x = x + 1
                x = original_x
                y = y + 1

            # set x and y back to original values before going through kernel
            if y != original_y:
                y = original_y

            if x != original_x:
                x = original_x

            # if kernel fits draw a black square in the middle
            if track >= kernel_cnt - smoothness:
                pixel_tup.append((x + kernel_cols_half_length, y + kernel_row_half_length))

            track = 0

    for i in pixel_tup:
        x = i[0]
        y = i[1]

        new_img[y][x] = 0

    return new_img

def thinning(img_array):
    img_rows = len(img_array)
    img_cols = len(img_array[0])

    new_img = [[255]*img_cols]*img_rows
    new_img = np.array(new_img)
    pixel_tup = []

    # image kernel
    kernel = [[1, 0, 1],
              [0, 0, 0],
              [1, 0, 1]]

    kernel_rows = len(kernel)
    kernel_cols = len(kernel[0])

    kernel_row_half_length = kernel_rows // 2
    kernel_cols_half_length = kernel_cols // 2

    kernel_cnt = kernel_count(kernel)

    # begin looping through image (range is minus 1 because the kernel is 3 in length)
    print("applying filter...")
    for y in range(img_rows - kernel_rows):
        for x in range(img_cols - kernel_cols):

            # keep track of original position of x and y so I can go back to them, because I am going to move them when ->
            # looping through kernel
            original_y = y
            original_x = x

            # keep track of number of matches to kernel
            track = 0

            # begin looping through kernel
            for ky in range(kernel_rows):
                # print("ky")
                for kx in range(kernel_cols):
                    if kernel[ky][kx] == img_array[y][x]:
                        track = track + 1
                    # print("kx")
                    #print((x, y))
                    x = x + 1
                x = original_x
                y = y + 1

            # set x and y back to original values before going through kernel
            if y != original_y:
                y = original_y

            if x != original_x:
                x = original_x

            # if kernel fits draw a black square in the middle
            if track == kernel_cnt:

                pixel_tup.append((x + kernel_cols_half_length, y + kernel_row_half_length))

            track = 0

    for i in pixel_tup:
        x = i[0]
        y = i[1]

        new_img[y][x] = 0

    return new_img



img = cv2.imread("100.png",0)
print("loaded image")

print("processing image...")
binary(img)
print("image processed")
print("saving processed image...")
cv2.imwrite("processed.png",img)
print("processed image created")

print("thinning image...")

img = thinning2(img, smoothness = 1)

print("image thinned")

print("creating final new image...")
cv2.imwrite("thinned_img.png",img)
print("final new image created")


