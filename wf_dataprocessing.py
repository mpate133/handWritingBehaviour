import os
import wf_dataprocessing_feature_extraction as extraction


def run():
    os.chdir("data_original")

    # images = []
    images = [f for f in os.listdir('.') if os.path.isfile(f)]
    # for entity in os.listdir('.'):
    #     if os.path.isfile(entity):
    #         images.append(entity)

    os.chdir("../data_processed")
    image_names = []
    if os.path.isfile("extracted_features_list"):
        print("Found: extracted_features_list already exists.")
        with open("extracted_features_list", "r") as extracted_features_list:
            for line in extracted_features_list:
                content = line.split()
                image_names.append(content[-1])

    with open("extracted_features_list", "a") as extracted_features_list:
        ind = len(image_names)
        for image in images:
            if image in image_names:
                continue
            features = extraction.extract(image)
            features.append(image)
            for i in features:
                extracted_features_list.write("%s\t" % i)
            print('', file=extracted_features_list)
            ind += 1
            progress = round((ind * 100) / len(images), 3)
            print(str(ind) + ' ' + image + ' ' + str(progress) + ' %')
        print("Features Extracted Successfully!")

    os.chdir('..')
    return
