import os


def calculate_emotional_stability(baseline_angle, slant_angle):
    # 1 = stable, 0 = not stable
    if slant_angle == 0 or slant_angle == 4 or slant_angle == 6 or baseline_angle == 0:
        return 0
    else:
        return 1


def calculate_mental_energy(size_of_letter, pen_pressure):
    # 1 = high or average, 0 = low
    if (pen_pressure == 0 or pen_pressure == 2) or (size_of_letter == 1 or size_of_letter == 2):
        return 1
    else:
        return 0


def calculate_modesty(top_margin, size_of_letter):
    # 1 = observed, 0 = not observed (not necessarily the opposite)
    if top_margin == 0 or size_of_letter == 1:
        return 1
    else:
        return 0


def calculate_flexibility(spacing_bw_lines, spacing_bw_words):
    # 1 = harmonious, 0 = non harmonious
    if spacing_bw_lines == 2 and spacing_bw_words == 2:
        return 1
    else:
        return 0


def calculate_discipline(top_margin, slant_angle):
    # 1 = observed, 0 = not observed (not necessarily the opposite)
    if top_margin == 1 and slant_angle == 6:
        return 1
    else:
        return 0


def calculate_concentration_power(size_of_letter, spacing_bw_lines):
    # 1 = observed, 0 = not observed (not necessarily the opposite)
    if size_of_letter == 0 and spacing_bw_lines == 1:
        return 1
    else:
        return 0


def calculate_communicativeness(size_of_letter, spacing_bw_words):
    # 1 = observed, 0 = not observed (not necessarily the opposite)
    if size_of_letter == 1 and spacing_bw_words == 0:
        return 1
    else:
        return 0


def calculate_social_isolation(spacing_bw_lines, spacing_bw_words):
    # 1 = observed, 0 = not observed (not necessarily the opposite)
    if spacing_bw_words == 0 or spacing_bw_lines == 0:
        return 1
    else:
        return 0


def run():
    os.chdir("data_processed")
    if os.path.isfile("trait_measure_list"):
        print("trait_measure_list already exists.")

    elif os.path.isfile("discreet_features_list"):
        print("Discreet_features_list found.")
        with open("discreet_features_list", "r") as discreet_features_list, open("trait_measure_list", "a") as trait_measure_list:
            for line in discreet_features_list:
                data = line.split()

                baseline_angle = float(data[0])
                top_margin = float(data[1])
                size_of_letter = float(data[2])
                spacing_bw_lines = float(data[3])
                spacing_bw_words = float(data[4])
                pen_pressure = float(data[5])
                slant_angle = float(data[6])
                image_names = data[7]

                emotional_stability = calculate_emotional_stability(baseline_angle, slant_angle)
                mental_energy = calculate_mental_energy(size_of_letter, pen_pressure)
                modesty = calculate_modesty(top_margin, size_of_letter)
                flexibility = calculate_flexibility(spacing_bw_lines, spacing_bw_words)
                discipline = calculate_discipline(top_margin, slant_angle)
                concentration_power = calculate_concentration_power(size_of_letter, spacing_bw_lines)
                communicativeness = calculate_communicativeness(size_of_letter, spacing_bw_words)
                social_isolation = calculate_social_isolation(spacing_bw_lines, spacing_bw_words)

                trait_measure_list.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % (str(baseline_angle), str(top_margin), str(
                    size_of_letter), str(spacing_bw_lines), str(spacing_bw_words), str(pen_pressure), str(slant_angle)))
                trait_measure_list.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % (str(emotional_stability), str(mental_energy), str(
                    modesty), str(flexibility), str(discipline), str(concentration_power), str(communicativeness), str(social_isolation)))
                trait_measure_list.write("%s" % str(image_names))
                print('', file=trait_measure_list)
        print("Done!")

    else:
        print("Error: feature_list file not found.")

    os.chdir("..")
