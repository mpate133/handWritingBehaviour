import wf_ml_training_trait_determining
import wf_ml_training
import wf_ml_prediction
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
import os
from wf_ml_prediction_getdatafrommodel import get_data_from_model
import pickle


'''
Input the image names from "data_original/for_testing" folder
for example:
Enter file name to predict or z to exit: 013-0.png
Enter file name to predict or z to exit: 013-1.png
Enter file name to predict or z to exit: 309-0.png

If error occurs while running the program after 1st time,
then try running the file again.
'''


def calculate_evaluation_metrics():

    x_emotional, y_emotional = get_data_from_model("emotional_stability_model_values")
    x_mental, y_mental = get_data_from_model("mental_energy_model_values")
    x_modesty, y_modesty = get_data_from_model("modesty_model_values")
    x_flexibility, y_flexibility = get_data_from_model("flexibility_model_values")
    x_discipline, y_discipline = get_data_from_model("discipline_model_values")
    x_concentration, y_concentration = get_data_from_model("concentration_power_model_values")
    x_communication, y_communication = get_data_from_model("communication_skill_model_values")
    x_social, y_social = get_data_from_model("social_isolation_model_values")

    os.chdir("evaluation")

    with open('summary.txt', 'w') as summary:
        summary.write("Used 80% of the data for training:\n")
        summary.write("Linear Model Accuracy and Precision Scores:\n")
        x_train, x_test, y_train, y_test = train_test_split(
            x_emotional, y_emotional, test_size=.20, random_state=8)

        emotional_stability_classifier = pickle.load(open('../models/emotional_stability_model', 'rb'))
        accuracy = accuracy_score(emotional_stability_classifier.predict(x_test), y_test)
        precision = precision_score(emotional_stability_classifier.predict(x_test), y_test, zero_division=0.0)
        summary.write(f"Emotional Stability Classifier:\n")
        summary.write(f"\tAccuracy: {accuracy * 100}%\n")
        summary.write(f"\tPrecision: {precision * 100}%\n")

        x_train, x_test, y_train, y_test = train_test_split(
            x_mental, y_mental, test_size=.20, random_state=16)
        mental_energy_classifier = pickle.load(open('../models/mental_energy_model', 'rb'))
        accuracy = accuracy_score(mental_energy_classifier.predict(x_test), y_test)
        precision = precision_score(mental_energy_classifier.predict(x_test), y_test, zero_division=0.0)
        summary.write(f"Mental Energy Classifier:\n")
        summary.write(f"\tAccuracy: {accuracy * 100}%\n")
        summary.write(f"\tPrecision: {precision * 100}%\n")

        x_train, x_test, y_train, y_test = train_test_split(
            x_modesty, y_modesty, test_size=.20, random_state=32)
        modesty_classifier = pickle.load(open('../models/modesty_model', 'rb'))
        accuracy = accuracy_score(modesty_classifier.predict(x_test), y_test)
        precision = precision_score(modesty_classifier.predict(x_test), y_test, zero_division=0.0)
        summary.write(f"Modesty Classifier:\n")
        summary.write(f"\tAccuracy: {accuracy * 100}%\n")
        summary.write(f"\tPrecision: {precision * 100}%\n")

        x_train, x_test, y_train, y_test = train_test_split(
            x_flexibility, y_flexibility, test_size=.20, random_state=64)
        flexibility_classifier = pickle.load(open('../models/flexibility_model', 'rb'))
        accuracy = accuracy_score(flexibility_classifier.predict(x_test), y_test)
        precision = precision_score(flexibility_classifier.predict(x_test), y_test, zero_division=0.0)
        summary.write(f"Flexibility Classifier:\n")
        summary.write(f"\tAccuracy: {accuracy * 100}%\n")
        summary.write(f"\tPrecision: {precision * 100}%\n")

        x_train, x_test, y_train, y_test = train_test_split(
            x_discipline, y_discipline, test_size=.20, random_state=42)
        discipline_classifier = pickle.load(open('../models/discipline_model', 'rb'))
        accuracy = accuracy_score(discipline_classifier.predict(x_test), y_test)
        precision = precision_score(discipline_classifier.predict(x_test), y_test, zero_division=0.0)
        summary.write(f"Discipline Classifier:\n")
        summary.write(f"\tAccuracy: {accuracy * 100}%\n")
        summary.write(f"\tPrecision: {precision * 100}%\n")

        x_train, x_test, y_train, y_test = train_test_split(
            x_concentration, y_concentration, test_size=.20, random_state=52)
        concentration_classifier = pickle.load(open('../models/concentration_power_model', 'rb'))
        accuracy = accuracy_score(concentration_classifier.predict(x_test), y_test)
        precision = precision_score(concentration_classifier.predict(x_test), y_test, zero_division=0.0)
        summary.write(f"Concentration Power Classifier:\n")
        summary.write(f"\tAccuracy: {accuracy * 100}%\n")
        summary.write(f"\tPrecision: {precision * 100}%\n")

        x_train, x_test, y_train, y_test = train_test_split(
            x_communication, y_communication, test_size=.20, random_state=21)
        communication_classifier = pickle.load(open('../models/communication_skill_model', 'rb'))
        accuracy = accuracy_score(communication_classifier.predict(x_test), y_test)
        precision = precision_score(communication_classifier.predict(x_test), y_test, zero_division=0.0)
        summary.write(f"Communication Skill Classifier:\n")
        summary.write(f"\tAccuracy: {accuracy * 100}%\n")
        summary.write(f"\tPrecision: {precision * 100}%\n")

        x_train, x_test, y_train, y_test = train_test_split(
            x_social, y_social, test_size=.20, random_state=73)
        social_isolation_classifier = pickle.load(open('../models/social_isolation_model', 'rb'))
        accuracy = accuracy_score(social_isolation_classifier.predict(x_test), y_test)
        precision = precision_score(social_isolation_classifier.predict(x_test), y_test, zero_division=0.0)
        summary.write(f"Social Isolation Classifier:\n")
        summary.write(f"\tAccuracy: {accuracy * 100}%\n")
        summary.write(f"\tPrecision: {precision * 100}%\n\n")

        print('', file=summary)
        print("evaluation/summary.txt file generated with all models' accuracy and precision.")

    os.chdir("..")


def alternative_models():
    x_modesty, y_modesty = get_data_from_model("modesty_model_values")
    os.chdir("evaluation")
    with open('summary.txt', 'a') as summary:
        summary.write("Alternative Models:\n")

        x_train, x_test, y_train, y_test = train_test_split(
            x_modesty, y_modesty, test_size=.20, random_state=32)

        alt_rbf = SVC(kernel='rbf')
        alt_rbf.fit(x_train, y_train)
        summary.write("Gaussian Kernel Radial Basis Function for Modesty:\n")
        accuracy = accuracy_score(alt_rbf.predict(x_test), y_test)
        precision = precision_score(alt_rbf.predict(x_test), y_test, zero_division=0.0)
        summary.write(f"\tAccuracy: {accuracy * 100}%\n")
        summary.write(f"\tPrecision: {precision * 100}%\n")

        alt_sigmoid = SVC(kernel='sigmoid')
        alt_sigmoid.fit(x_train, y_train)
        summary.write("Sigmoid Kernel for Modesty:\n")
        accuracy = accuracy_score(alt_sigmoid.predict(x_test), y_test)
        precision = precision_score(alt_sigmoid.predict(x_test), y_test, zero_division=0.0)
        summary.write(f"\tAccuracy: {accuracy * 100}%\n")
        summary.write(f"\tPrecision: {precision * 100}%\n")

        alt_poly = SVC(kernel='poly')
        alt_poly.fit(x_train, y_train)
        summary.write("Polynomial Kernel for Modesty:\n")
        accuracy = accuracy_score(alt_poly.predict(x_test), y_test)
        precision = precision_score(alt_poly.predict(x_test), y_test, zero_division=0.0)
        summary.write(f"\tAccuracy: {accuracy * 100}%\n")
        summary.write(f"\tPrecision: {precision * 100}%\n")
        print('', file=summary)
        print("evaluation/summary.txt file updated with alternative models' evaluation metrics.\n")

    os.chdir("..")


wf_ml_training_trait_determining.run()
wf_ml_training.run()
calculate_evaluation_metrics()
alternative_models()
wf_ml_prediction.run()
