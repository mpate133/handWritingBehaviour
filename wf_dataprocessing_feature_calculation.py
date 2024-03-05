def calculate_angle_of_line_base(angle_of_line_base):
    comment = ""
    if angle_of_line_base >= 0.2:
        baseline_angle = 0
        comment = "DESCENDING"
    elif angle_of_line_base <= -0.3:
        baseline_angle = 1
        comment = "ASCENDING"
    else:
        baseline_angle = 2
        comment = "STRAIGHT"

    return baseline_angle, comment


def calculate_top_margin(margin_from_top):
    comment = ""
    if margin_from_top >= 1.7:
        top_margin = 0
        comment = "MEDIUM OR BIGGER"
    else:
        top_margin = 1
        comment = "NARROW"

    return top_margin, comment


def calculate_letter_size(size_of_letter):
    comment = ""
    if size_of_letter >= 18.0:
        letter_size = 0
        comment = "BIG"
    elif size_of_letter < 13.0:
        letter_size = 1
        comment = "SMALL"
    else:
        letter_size = 2
        comment = "MEDIUM"

    return letter_size, comment


def calculate_line_spacing(spacing_of_line):
    comment = ""
    if spacing_of_line >= 3.5:
        line_spacing = 0
        comment = "BIG"
    elif spacing_of_line < 2.0:
        line_spacing = 1
        comment = "SMALL"
    else:
        line_spacing = 2
        comment = "MEDIUM"

    return line_spacing, comment


def calculate_word_spacing(spacing_between_words):
    comment = ""
    if spacing_between_words > 2.0:
        word_spacing = 0
        comment = "BIG"
    elif spacing_between_words < 1.2:
        word_spacing = 1
        comment = "SMALL"
    else:
        word_spacing = 2
        comment = "MEDIUM"

    return word_spacing, comment


def calculate_pen_pressure(pressure_of_pen):
    comment = ""
    if pressure_of_pen > 180.0:
        pen_pressure = 0
        comment = "HEAVY"
    elif pressure_of_pen < 151.0:
        pen_pressure = 1
        comment = "LIGHT"
    else:
        pen_pressure = 2
        comment = "MEDIUM"

    return pen_pressure, comment


def calculate_slant_angle(angle_of_slant):
    comment = ""
    if angle_of_slant == -45.0 or angle_of_slant == -30.0:
        slant_angle = 0
        comment = "EXTREMELY RECLINED"
    elif angle_of_slant == -15.0 or angle_of_slant == -5.0:
        slant_angle = 1
        comment = "A LITTLE OR MODERATELY RECLINED"
    elif angle_of_slant == 5.0 or angle_of_slant == 15.0:
        slant_angle = 2
        comment = "A LITTLE INCLINED"
    elif angle_of_slant == 30.0:
        slant_angle = 3
        comment = "MODERATELY INCLINED"
    elif angle_of_slant == 45.0:
        slant_angle = 4
        comment = "EXTREMELY INCLINED"
    elif angle_of_slant == 0.0:
        slant_angle = 5
        comment = "STRAIGHT"
    else:
        slant_angle = 6
        comment = "IRREGULAR"

    return slant_angle, comment
