import wf_dataprocessing_feature_calculation as calculate
import wf_dataprocessing_feature_extraction as extraction
import os
import pickle

trait_dict = {
    "emotional_stability" : {
        0: 'Not Stable',
        1: 'Stable'
    },
    "mental_energy": {
        0: 'Low',
        1: 'Average or Above'
    },
    "modesty": {
        0: 'Not observed (Not necessarily immodest)',
        1: 'Observed'
    },
    "flexibility": {
        0: 'Not harmonious',
        1: 'Harmonious'
    },
    "discipline": {
        0: 'Observed',
        1: 'Not Observed'
    },
    "concentration_power": {
        0: 'Average or Above',
        1: 'Poor Concentration'
    },
    "communication_skill": {
        0: 'Average or Above',
        1: 'Poor Communication'
    },
    "social_isolation": {
        0: 'Not observed',
        1: 'Observed'
    }
}


def run():
    print("Input the image names from {data_original/for_testing} folder")
    print("for example: Enter file name to predict or z to exit: 013-0.png\n")

    while True:
        file_name = input("Enter file name to predict or z to exit: ")
        if file_name == 'z':
            break
        os.chdir('data_original/for_testing')
        if not os.path.isfile(file_name):
            print("Enter valid image name from 6 available images in for_testing folder.\n")
            os.chdir('../..')
            continue
        os.chdir('..')
        extracted_features = extraction.extract(file_name, 1)
        os.chdir('..')
        baseline_angle = extracted_features[0]
        discreet_baseline_angle, comment = calculate.calculate_angle_of_line_base(
            baseline_angle)
        print("Baseline Angle: " + comment)

        extracted_top_margin = extracted_features[1]
        discreet_top_margin, comment = calculate.calculate_top_margin(extracted_top_margin)
        print("Top Margin: " + comment)

        extracted_letter_size = extracted_features[2]
        discreet_letter_size, comment = calculate.calculate_letter_size(
            extracted_letter_size)
        print("Size of Letter: " + comment)

        extracted_line_spacing = extracted_features[3]
        discreet_line_spacing, comment = calculate.calculate_line_spacing(
            extracted_line_spacing)
        print("Spacing betweeen Lines: " + comment)

        extracted_word_spacing = extracted_features[4]
        discreet_word_spacing, comment = calculate.calculate_word_spacing(
            extracted_word_spacing)
        print("Spacing between Words: " + comment)

        extracted_pen_pressure = extracted_features[5]
        discreet_pen_pressure, comment = calculate.calculate_pen_pressure(
            extracted_pen_pressure)
        print("Pen Pressure: " + comment)

        extracted_slant_angle = extracted_features[6]
        discreet_slant_angle, comment = calculate.calculate_slant_angle(
            extracted_slant_angle)
        print("Slant: " + comment)

        emotional_stability_classifier = pickle.load(open('models/emotional_stability_model', 'rb'))
        print("\nEmotional Stability: ", trait_dict["emotional_stability"][int(emotional_stability_classifier.predict(
            [[discreet_baseline_angle, discreet_slant_angle]]))])
        mental_energy_classifier = pickle.load(open('models/mental_energy_model', 'rb'))
        print("Mental Energy or Will Power: ",
              trait_dict["modesty"][int(mental_energy_classifier.predict([[discreet_letter_size, discreet_pen_pressure]]))])
        modesty_classifier = pickle.load(open('models/modesty_model', 'rb'))
        print("Modesty: ", trait_dict["modesty"][int(modesty_classifier.predict([[discreet_letter_size, discreet_top_margin]]))])
        flexibility_classifier = pickle.load(open('models/flexibility_model', 'rb'))
        print("Personal Harmony and Flexibility: ",
              trait_dict["flexibility"][int(flexibility_classifier.predict([[discreet_line_spacing, discreet_word_spacing]]))])
        discipline_classifier = pickle.load(open('models/discipline_model', 'rb'))
        print("Discipline: ", trait_dict["discipline"][int(discipline_classifier.predict(
            [[discreet_slant_angle, discreet_top_margin]]))])
        concentration_classifier = pickle.load(open('models/concentration_power_model', 'rb'))
        print("Concentration Power: ", trait_dict["concentration_power"][int(concentration_classifier.predict(
            [[discreet_letter_size, discreet_line_spacing]]))])
        communication_classifier = pickle.load(open('models/communication_skill_model', 'rb'))
        print("Communicativeness: ", trait_dict["communication_skill"][int(communication_classifier.predict(
            [[discreet_letter_size, discreet_word_spacing]]))])
        social_isolation_classifier = pickle.load(open('models/social_isolation_model', 'rb'))
        print("Social Isolation: ", trait_dict["social_isolation"][int(social_isolation_classifier.predict(
            [[discreet_line_spacing, discreet_word_spacing]]))])
        print("---------------------------------------------------")

    return
