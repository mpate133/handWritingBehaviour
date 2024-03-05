import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

middle_point = 6000
approx_image_middle = 15000
min_word_height = 20


def capture_horizontal_lines(image):
    (height, width) = image.shape[:2]
    image_rows = []
    for i in range(height):
        one_row = image[i:i + 1, 0:width]
        image_rows.append(np.sum(one_row))
    return image_rows


def capture_vertical_lines(image):
    (height, width) = image.shape[:2]
    image_cols = []
    for i in range(width):
        one_col = image[0:height, i:i + 1]
        image_cols.append(np.sum(one_col))
    return image_cols


def bilateral_filter(image, d):
    image = cv2.bilateralFilter(image, d, 50, 50)
    return image


def measure_pen_pressure(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = image.shape[:]
    inverted_image = invert_image(image, h, w)
    filtered_image = bilateral_filter(inverted_image, 3)
    _, threshold = cv2.threshold(filtered_image, 100, 255, cv2.THRESH_TOZERO)
    total_pressure = 0
    px_cnt = 0
    for x in range(h):
        for y in range(w):
            if threshold[x][y] > 0:
                total_pressure += threshold[x][y]
                px_cnt += 1

    average_intensity = float(total_pressure) / px_cnt
    return average_intensity


def invert_image(image, h, w):
    inverted = image
    for x in range(h):
        for y in range(w):
            inverted[x][y] = 255 - image[x][y]
    return inverted


def threshold_inverted_binary(image, min_value):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(image, min_value, 255, cv2.THRESH_BINARY_INV)
    return image


def dilate(image, size):
    kernel = np.ones(size, np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    return image


def measure_baseline_angle(image):
    sum_of_angles = 0.0
    number_of_contour = 0
    filtered_image = bilateral_filter(image, 3)
    threshold_image = threshold_inverted_binary(filtered_image, 120)
    dilated_image = dilate(threshold_image, (5, 100))
    contours, _ = cv2.findContours(dilated_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i, contour in enumerate(contours):
        x, y, width, height = cv2.boundingRect(contour)
        if height > width or height < min_word_height:
            continue

        region_of_interest = image[y:y + height, x:x + width]
        if width < image.shape[1] / 2:
            region_of_interest = 255
            image[y:y + height, x:x + width] = region_of_interest
            continue
        contour_rectangle = cv2.minAreaRect(contour)
        center, angle = contour_rectangle[0], contour_rectangle[2]
        if angle < -45.0:
            angle += 90.0
        rotated_matrix = cv2.getRotationMatrix2D(((x + width) / 2, (y + height) / 2), angle, 1)
        contour_image = cv2.warpAffine(region_of_interest, rotated_matrix, (width, height),
                                       borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
        image[y:y + height, x:x + width] = contour_image
        sum_of_angles = sum_of_angles + angle
        number_of_contour += 1

    if number_of_contour == 0:
        avg_angle = sum_of_angles
    else:
        avg_angle = sum_of_angles / number_of_contour

    return image, avg_angle


def measure_letter_size(image):
    filtered_image = bilateral_filter(image, 5)
    threshold_image = threshold_inverted_binary(filtered_image, 160)
    horizontal_lines = capture_horizontal_lines(threshold_image)
    top_margin_count = 0
    for line_sum in horizontal_lines:
        if line_sum <= 255:
            top_margin_count += 1
        else:
            break

    line_top = 0
    line_bottom = 0
    space_top = 0
    space_bottom = 0
    index_count = 0
    set_line_top = True
    set_space_top = True
    include_next_space = True
    line_spaces = []
    line_indices = []

    for i, line_sum in enumerate(horizontal_lines):
        if line_sum == 0:
            if space_top:
                space_top = index_count
                set_space_top = False
            index_count += 1
            space_bottom = index_count
            if i < len(horizontal_lines) - 1:
                if horizontal_lines[i + 1] == 0:
                    continue
            if include_next_space:
                line_spaces.append(space_bottom - space_top)
            else:
                if len(line_spaces) == 0:
                    previous = 0
                else:
                    previous = line_spaces.pop()
                line_spaces.append(previous + space_bottom - line_top)
            set_space_top = True

        if line_sum > 0:
            if set_line_top:
                line_top = index_count
                set_line_top = False
            index_count += 1
            line_bottom = index_count
            if i < len(horizontal_lines) - 1:
                if horizontal_lines[i + 1] > 0:
                    continue

                if line_bottom - line_top < 20:
                    include_next_space = False
                    set_line_top = True
                    continue
            include_next_space = True
            line_indices.append([line_top, line_bottom])
            set_line_top = True

    extracted_lines = []
    for i, line_index in enumerate(line_indices):
        start_point = line_index[0]
        start_list = []
        going_up = True
        going_down = False
        line_segment = horizontal_lines[int(line_index[0]):int(line_index[1])]

        for j, segment_sum in enumerate(line_segment):
            if going_up:
                if segment_sum < middle_point:
                    start_point += 1
                    continue
                start_list.append(start_point)
                going_up = False
                going_down = True
            if going_down:
                if segment_sum > middle_point:
                    start_point += 1
                    continue
                start_list.append(start_point)
                going_down = False
                going_up = True

        if len(start_list) < 2:
            continue

        line_top = line_index[0]
        for x in range(1, len(start_list) - 1, 2):
            line_middle = (start_list[x] + start_list[x + 1]) / 2
            line_bottom = line_middle
            if line_bottom - line_top < 20:
                continue
            extracted_lines.append([line_top, line_bottom])
            line_top = line_bottom
        if line_index[1] - line_top < 20:
            continue
        extracted_lines.append([line_top, line_index[1]])

    space_row_count = 0
    midzone_row_count = 0
    midline_count = 0
    counted = False

    for i, line in enumerate(extracted_lines):
        line_segment = horizontal_lines[int(line[0]):int(line[1])]
        for j, sum in enumerate(line_segment):
            if sum < approx_image_middle:
                space_row_count += 1
            else:
                midzone_row_count += 1
                counted = True

        if counted:
            midline_count += 1
            counted = False

    if midline_count == 0:
        midline_count = 1

    total_space_rows = space_row_count + np.sum(line_spaces[1:-1])
    average_line_spacing = float(
        total_space_rows) / midline_count
    avg_letter_size = float(midzone_row_count) / midline_count
    letter_size = avg_letter_size
    if avg_letter_size == 0:
        avg_letter_size = 1

    line_spacing = average_line_spacing / avg_letter_size
    top_margin = float(top_margin_count) / avg_letter_size

    return extracted_lines, letter_size, line_spacing, top_margin


def measure_spacing_between_words(image, extracted_line, letter_size):
    filtered_image = bilateral_filter(image, 5)
    threshold_image = threshold_inverted_binary(filtered_image, 180)
    width = threshold_image.shape[1]
    word_spaces = []
    word_cords = []

    for i, line in enumerate(extracted_line):
        extract = threshold_image[int(line[0]):int(line[1]), 0:width]
        vertical_lines = capture_vertical_lines(extract)

        start_of_word = 0
        start_of_space = 0
        ind_cnt = 0
        set_word_start = True
        set_space_start = True
        spaces = []

        for j, sum in enumerate(vertical_lines):
            if sum == 0:
                if set_space_start:
                    start_of_space = ind_cnt
                    set_space_start = False
                ind_cnt += 1
                end_of_space = ind_cnt
                if j < len(vertical_lines) - 1:
                    if vertical_lines[j + 1] == 0:
                        continue

                if (end_of_space - start_of_space) > int(letter_size / 2):
                    spaces.append(end_of_space - start_of_space)

                set_space_start = True

            if sum > 0:
                if set_word_start:
                    start_of_word = ind_cnt
                    set_word_start = False
                ind_cnt += 1
                end_of_word = ind_cnt
                if j < len(vertical_lines) - 1:
                    if vertical_lines[j + 1] > 0:
                        continue

                count = 0
                for k in range(int(line[1]) - int(line[0])):
                    row = threshold_image[int(line[0] + k):int(line[0] + k + 1),
                          start_of_word:end_of_word]  # y1:y2, x1:x2
                    if np.sum(row):
                        count += 1
                if count > int(letter_size / 2):
                    word_cords.append([line[0], line[1], start_of_word, end_of_word])

                set_word_start = True

        word_spaces.extend(spaces[1:-1])

    col_spaces = np.sum(word_spaces)
    sp_cnt = len(word_spaces)
    if sp_cnt == 0:
        sp_cnt = 1
    avg_spacing = float(col_spaces) / sp_cnt
    if letter_size == 0.0:
        word_spacing = avg_spacing
    else:
        word_spacing = avg_spacing / letter_size

    return word_cords, word_spacing


def measure_angle_of_slant(img, words):
    theta = [-0.785398, -0.523599, -0.261799, -0.0872665,
             0.01, 0.0872665, 0.261799, 0.523599, 0.785398]

    s_function = [0.0] * 9
    count_ = [0] * 9

    filtered_image = bilateral_filter(img, 5)
    threshold_image = threshold_inverted_binary(filtered_image, 180)

    for i, angle in enumerate(theta):
        s_temp = 0.0
        count = 0

        for j, word in enumerate(words):
            original = threshold_image[int(word[0]):int(word[1]), int(word[2]):int(word[3])]  # y1:y2, x1:x2

            height = int(word[1]) - int(word[0])
            width = int(word[3]) - int(word[2])

            shift = (math.tan(angle) * height) / 2

            pad_length = abs(int(shift))

            blank_image = np.zeros((int(height), int(width + pad_length * 2), 3), np.uint8)
            new_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
            new_image[:, pad_length:width + pad_length] = original

            (height, width) = new_image.shape[:2]
            x1 = width / 2
            y1 = 0
            x2 = width / 4
            y2 = height
            x3 = 3 * width / 4
            y3 = height

            pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3]])
            pts2 = np.float32([[x1 + shift, y1], [x2 - shift, y2], [x3 - shift, y3]])
            M = cv2.getAffineTransform(pts1, pts2)
            deslanted = cv2.warpAffine(new_image, M, (width, height))

            vp = capture_vertical_lines(deslanted)

            for k, sum in enumerate(vp):
                if sum == 0:
                    continue

                num_fgpixel = sum / 255

                if num_fgpixel < int(height / 3):
                    continue

                column = deslanted[0:height, k:k + 1]
                column = column.flatten()

                for l, pixel in enumerate(column):
                    if pixel == 0:
                        continue
                    break

                for m, pixel in enumerate(column[::-1]):
                    if pixel == 0:
                        continue
                    break

                delta_y = height - (l + m)

                h_sq = (float(num_fgpixel) / delta_y) ** 2

                h_wted = (h_sq * num_fgpixel) / height
                s_temp += h_wted

                count += 1

        s_function[i] = s_temp
        count_[i] = count

    max_value = 0.0
    max_index = 4
    for index, value in enumerate(s_function):
        if value > max_value:
            max_value = value
            max_index = index

    if max_index == 0:
        angle = 45
    elif max_index == 1:
        angle = 30
    elif max_index == 2:
        angle = 15
    elif max_index == 3:
        angle = 5
    elif max_index == 5:
        angle = -5
    elif max_index == 6:
        angle = -15
    elif max_index == 7:
        angle = -30
    elif max_index == 8:
        angle = -45
    elif max_index == 4:
        if s_function[3] == 0.0:
            p = s_function[4]
            q = s_function[4]
        else:
            p = s_function[4] / s_function[3]
            q = s_function[4] / s_function[5]

        if (p <= 1.2 and q <= 1.2) or (p > 1.4 and q > 1.4):
            angle = 0
        elif (p <= 1.2 and q - p > 0.4) or (q <= 1.2 and p - q > 0.4):
            angle = 0
        else:
            max_index = 9
            angle = 180

    return angle


def extract(image_name, for_testing):
    if for_testing:
        image = cv2.imread('../data_original/for_testing/' + image_name)
    else:
        image = cv2.imread('../data_original/' + image_name)
    pressure_of_pen = measure_pen_pressure(image)
    straight_image, angle_of_line_base = measure_baseline_angle(image)
    extracted_line, size_of_letter, spacing_of_line, margin_from_top = measure_letter_size(straight_image)
    coordinates_of_word, spacing_between_words = measure_spacing_between_words(straight_image, extracted_line,
                                                                               size_of_letter)
    angle_of_slant = measure_angle_of_slant(straight_image, coordinates_of_word)

    margin_from_top = round(margin_from_top, 2)
    angle_of_line_base = round(angle_of_line_base, 2)
    spacing_between_words = round(spacing_between_words, 2)
    angle_of_slant = round(angle_of_slant, 2)
    pressure_of_pen = round(pressure_of_pen, 2)
    size_of_letter = round(size_of_letter, 2)
    spacing_of_line = round(spacing_of_line, 2)

    return [angle_of_line_base, margin_from_top, size_of_letter, spacing_of_line, spacing_between_words,
            pressure_of_pen, angle_of_slant]
