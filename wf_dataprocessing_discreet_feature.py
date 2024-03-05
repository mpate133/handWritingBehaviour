import os
import wf_dataprocessing_feature_calculation as calculate


def run():
    os.chdir("data_processed")
    if os.path.isfile('discreet_features_list'):
        print("Found: discreet_features_list file exists")

    elif os.path.isfile("extracted_features_list"):
        with open("extracted_features_list", "r") as extracted_features_list, open("discreet_features_list", "a") as discreet_features_list:
            for extracted_line in extracted_features_list:
                factor_value = extracted_line.split()

                extracted_baseline_angle = float(factor_value[0])
                extracted_top_margin = float(factor_value[1])
                extracted_letter_size = float(factor_value[2])
                extracted_line_spacing = float(factor_value[3])
                extracted_word_spacing = float(factor_value[4])
                extracted_pen_pressure = float(factor_value[5])
                extracted_slant_angle = float(factor_value[6])
                image_name = factor_value[7]

                baseline_angle, comment = calculate.calculate_angle_of_line_base(
                    extracted_baseline_angle)
                top_margin, comment = calculate.calculate_top_margin(
                    extracted_top_margin)
                letter_size, comment = calculate.calculate_letter_size(
                    extracted_letter_size)
                line_spacing, comment = calculate.calculate_line_spacing(
                    extracted_line_spacing)
                word_spacing, comment = calculate.calculate_word_spacing(
                    extracted_word_spacing)
                pen_pressure, comment = calculate.calculate_pen_pressure(
                    extracted_pen_pressure)
                slant_angle, comment = calculate.calculate_slant_angle(
                    extracted_slant_angle)

                discreet_features_list.write("%s\t" % str(baseline_angle))
                discreet_features_list.write("%s\t" % str(top_margin))
                discreet_features_list.write("%s\t" % str(letter_size))
                discreet_features_list.write("%s\t" % str(line_spacing))
                discreet_features_list.write("%s\t" % str(word_spacing))
                discreet_features_list.write("%s\t" % str(pen_pressure))
                discreet_features_list.write("%s\t" % str(slant_angle))
                discreet_features_list.write("%s\t" % str(image_name))
                print('', file=discreet_features_list)
        print("Discreet Features created successfully!")

    else:
        print("Attention: extracted_features_list file not found.")

    os.chdir('..')
    return
