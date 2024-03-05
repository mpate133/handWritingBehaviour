import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pickle


def run():
    os.chdir("data_processed")
    x_baseline_angle = []
    x_top_margin = []
    x_letter_size = []
    x_line_spacing = []
    x_word_spacing = []
    x_pen_pressure = []
    x_slant_angle = []
    y_emotional = []
    y_mental = []
    y_modesty = []
    y_flexibility = []
    y_discipline = []
    y_concentration = []
    y_communication = []
    y_social = []
    image_names = []

    if os.path.isfile("trait_measure_list"):
        print("Note: trait_measure_list found.")
        # =================================================================
        with open("trait_measure_list", "r") as labels:
            for line in labels:
                content = line.split()

                baseline_angle = float(content[0])
                x_baseline_angle.append(baseline_angle)

                top_margin = float(content[1])
                x_top_margin.append(top_margin)

                letter_size = float(content[2])
                x_letter_size.append(letter_size)

                line_spacing = float(content[3])
                x_line_spacing.append(line_spacing)

                word_spacing = float(content[4])
                x_word_spacing.append(word_spacing)

                pen_pressure = float(content[5])
                x_pen_pressure.append(pen_pressure)

                slant_angle = float(content[6])
                x_slant_angle.append(slant_angle)

                emotional_stability = float(content[7])
                y_emotional.append(emotional_stability)

                mental_energy = float(content[8])
                y_mental.append(mental_energy)

                modesty = float(content[9])
                y_modesty.append(modesty)

                flexibility = float(content[10])
                y_flexibility.append(flexibility)

                discipline = float(content[11])
                y_discipline.append(discipline)

                concentration = float(content[12])
                y_concentration.append(concentration)

                communication = float(content[13])
                y_communication.append(communication)

                social_isolation = float(content[14])
                y_social.append(social_isolation)

                image_name = content[15]
                image_names.append(image_name)
        # ===============================================================

        # emotional stability
        x_emotional = []
        for a, b in zip(x_baseline_angle, x_slant_angle):
            x_emotional.append([a, b])

        # mental energy or will power
        x_mental = []
        for a, b in zip(x_letter_size, x_pen_pressure):
            x_mental.append([a, b])

        # modesty
        x_modesty = []
        for a, b in zip(x_letter_size, x_top_margin):
            x_modesty.append([a, b])

        # personal harmony and flexibility
        x_flexibility = []
        for a, b in zip(x_line_spacing, x_word_spacing):
            x_flexibility.append([a, b])

        # lack of discipline
        x_discipline = []
        for a, b in zip(x_slant_angle, x_top_margin):
            x_discipline.append([a, b])

        # poor concentration
        x_concentration = []
        for a, b in zip(x_letter_size, x_line_spacing):
            x_concentration.append([a, b])

        # non communicativeness
        x_communication = []
        for a, b in zip(x_letter_size, x_word_spacing):
            x_communication.append([a, b])

        # social isolation
        x_social = []
        for a, b in zip(x_line_spacing, x_word_spacing):
            x_social.append([a, b])

        os.chdir("../models")
        x_train, x_test, y_train, y_test = train_test_split(
            x_emotional, y_emotional, test_size=.20, random_state=8)
        emotional_stability_classifier = SVC(kernel='linear')
        emotional_stability_classifier.fit(x_train, y_train)
        pickle.dump(emotional_stability_classifier, open('emotional_stability_model', 'wb'))

        x_train, x_test, y_train, y_test = train_test_split(
            x_mental, y_mental, test_size=.20, random_state=16)
        mental_energy_classifier = SVC(kernel='sigmoid')
        mental_energy_classifier.fit(x_train, y_train)
        pickle.dump(mental_energy_classifier, open('mental_energy_model', 'wb'))


        x_train, x_test, y_train, y_test = train_test_split(
            x_modesty, y_modesty, test_size=.20, random_state=32)
        modesty_classifier = SVC(kernel='sigmoid', degree=4)
        modesty_classifier.fit(x_train, y_train)
        pickle.dump(modesty_classifier, open('modesty_model', 'wb'))


        x_train, x_test, y_train, y_test = train_test_split(
            x_flexibility, y_flexibility, test_size=.20, random_state=64)
        flexibility_classifier = SVC(kernel='linear')
        flexibility_classifier.fit(x_train, y_train)
        pickle.dump(flexibility_classifier, open('flexibility_model', 'wb'))


        x_train, x_test, y_train, y_test = train_test_split(
            x_discipline, y_discipline, test_size=.20, random_state=42)
        discipline_classifier = SVC(kernel='linear')
        discipline_classifier.fit(x_train, y_train)
        pickle.dump(discipline_classifier, open('discipline_model', 'wb'))


        x_train, x_test, y_train, y_test = train_test_split(
            x_concentration, y_concentration, test_size=.20, random_state=52)
        concentration_classifier = SVC(kernel='linear')
        concentration_classifier.fit(x_train, y_train)
        pickle.dump(concentration_classifier, open('concentration_power_model', 'wb'))


        x_train, x_test, y_train, y_test = train_test_split(
            x_communication, y_communication, test_size=.20, random_state=21)
        communication_classifier = SVC(kernel='linear')
        communication_classifier.fit(x_train, y_train)
        pickle.dump(communication_classifier, open('communication_skill_model', 'wb'))

        x_train, x_test, y_train, y_test = train_test_split(
            x_social, y_social, test_size=.20, random_state=73)
        social_isolation_classifier = SVC(kernel='sigmoid')
        social_isolation_classifier.fit(x_train, y_train)
        pickle.dump(social_isolation_classifier, open('social_isolation_model', 'wb'))

        os.chdir("..")
        os.chdir("data_processed")

        with open("emotional_stability_model_values", "w") as emotional_stability_model:
            for i in range(len(x_emotional)):
                emotional_stability_model.write(f"{x_emotional[i]}${y_emotional[i]}${image_names[i]}")
                print('', file=emotional_stability_model)

        with open("mental_energy_model_values", "w") as mental_energy_model:
            for i in range(len(x_mental)):
                mental_energy_model.write(f"{x_mental[i]}${y_mental[i]}${image_names[i]}")
                print('', file=mental_energy_model)

        with open("modesty_model_values", "w") as modesty_model:
            for i in range(len(x_modesty)):
                modesty_model.write(f"{x_modesty[i]}${y_modesty[i]}${image_names[i]}")
                print('', file=modesty_model)

        with open("flexibility_model_values", "w") as flexibility_model:
            for i in range(len(x_flexibility)):
                flexibility_model.write(f"{x_flexibility[i]}${y_flexibility[i]}${image_names[i]}")
                print('', file=flexibility_model)

        with open("discipline_model_values", "w") as discipline_model:
            for i in range(len(x_discipline)):
                discipline_model.write(f"{x_discipline[i]}${y_discipline[i]}${image_names[i]}")
                print('', file=discipline_model)

        with open("concentration_power_model_values", "w") as concentration_power_model:
            for i in range(len(x_concentration)):
                concentration_power_model.write(f"{x_concentration[i]}${y_concentration[i]}${image_names[i]}")
                print('', file=concentration_power_model)

        with open("communication_skill_model_values", "w") as communication_skill_model:
            for i in range(len(x_communication)):
                communication_skill_model.write(f"{x_communication[i]}${y_communication[i]}${image_names[i]}")
                print('', file=communication_skill_model)

        with open("social_isolation_model_values", "w") as social_isolation_model:
            for i in range(len(x_social)):
                social_isolation_model.write(f"{x_social[i]}${y_social[i]}${image_names[i]}")
                print('', file=social_isolation_model)

    else:
        print("Run wf_ml_evaluation.py file to create trait_measure_list.")

    os.chdir("..")
    return
