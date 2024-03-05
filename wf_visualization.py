import statistics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def create_summary():
    with open('data_processed/extracted_features_list', 'r') as extracted_features_list:
        top_margin_array = []
        letter_size_array = []
        line_spacing_array = []
        word_spacing_array = []
        slant_angle_array = []
        label_hash = {
            0: "EXTREMELY RECLINED",
            1: "A LITTLE OR MODERATELY RECLINED",
            2: "A LITTLE INCLINED",
            3: "MODERATELY INCLINED",
            4: "EXTREMELY INCLINED",
            5: "STRAIGHT",
            6: "IRREGULAR"
        }
        with open('data_processed/discreet_features_list', 'r') as discreet_features_list:
            for list_raw in discreet_features_list:
                discreet_content = list_raw.split()
                slant_angle_array.append(int(discreet_content[6]))
        for data in extracted_features_list:
            content = data.split()
            top_margin_array.append(float(content[1]))
            letter_size_array.append(float(content[2]))
            line_spacing_array.append(float(content[3]))
            word_spacing_array.append(float(content[4]))

        with open('data_processed/summary.txt', 'w') as summary:
            summary.write("Quantitative features:\n")
            summary.write("1. Top Margin\n")
            summary.write("\t min: %s\n" % min(top_margin_array))
            summary.write("\t max: %s\n" % max(top_margin_array))
            summary.write("\t median: %s\n\n" % statistics.median(top_margin_array))
            summary.write("2. Letter Size\n")
            summary.write("\t min: %s\n" % min(letter_size_array))
            summary.write("\t max: %s\n" % max(letter_size_array))
            summary.write("\t median: %s\n\n" % statistics.median(letter_size_array))
            summary.write("3. Line Spacing\n")
            summary.write("\t min: %s\n" % min(line_spacing_array))
            summary.write("\t max: %s\n" % max(line_spacing_array))
            summary.write("\t median: %s\n\n" % statistics.median(line_spacing_array))
            summary.write("4. Word Spacing\n")
            summary.write("\t min: %s\n" % min(word_spacing_array))
            summary.write("\t max: %s\n" % max(word_spacing_array))
            summary.write("\t median: %s\n\n" % statistics.median(word_spacing_array))
            summary.write("Qualitative Feature :\n1. Angle of Slant\n")
            summary.write("\t Number of categories: %s\n" % len(label_hash))
            summary.write("\t Most Frequent Category: %s\n" % label_hash[
                max(set(slant_angle_array), key=slant_angle_array.count)])
            summary.write("\t Least Frequent Category: %s\n" % label_hash[
                min(set(slant_angle_array), key=slant_angle_array.count)])
            print('', file=summary)

    return top_margin_array, letter_size_array, line_spacing_array, word_spacing_array, slant_angle_array


def compute_pairwise_correlation(top_margin_array, letter_size_array, line_spacing_array, word_spacing_array):
    with open('data_processed/correlations.txt', 'w') as correlations:
        data = {
            'Top margin': top_margin_array,
            'Letter size': letter_size_array,
            'Line spacing': line_spacing_array,
            'Word spacing': word_spacing_array
        }

        dataframe = pd.DataFrame(data, columns=['Top margin', 'Letter size', 'Line spacing', 'Word spacing'])
        matrix = dataframe.corr()
        correlations.write("Correlation matrix is : \n\n")
        correlations.write(matrix.to_string())
        print('', file=correlations)

    return


def create_plots(top_margin_array, letter_size_array, line_spacing_array, word_spacing_array, slant_angle_array):
    top_margin_scatter = np.array(top_margin_array)
    letter_size_scatter = np.array(letter_size_array)
    line_spacing_scatter = np.array(line_spacing_array)
    word_spacing_scatter = np.array(word_spacing_array)

    fig, ax = plt.subplots()
    ax.set(title='Top margin VS Letter size', xlabel='Top margin', ylabel='Letter size')
    plt.scatter(top_margin_scatter, letter_size_scatter)
    fig.savefig("visuals/topmargin_vs_lettersize.png")

    fig2, ax2 = plt.subplots()
    ax2.set(title='Top margin VS Line spacing', xlabel='Top margin', ylabel='Line Spacing')
    plt.scatter(top_margin_scatter, line_spacing_scatter)
    fig2.savefig("visuals/topmargin_vs_linespacing.png")

    fig3, ax3 = plt.subplots()
    ax3.set(title='Top margin VS Line spacing', xlabel='Top margin', ylabel='Word Spacing')
    plt.scatter(top_margin_scatter, word_spacing_scatter)
    fig3.savefig("visuals/topmargin_vs_wordspacing.png")

    fig4, ax4 = plt.subplots()
    ax4.set(title='Letter Size VS Line spacing', xlabel='Letter Size', ylabel='Line Spacing')
    plt.scatter(letter_size_scatter, line_spacing_scatter)
    fig4.savefig("visuals/lettersize_vs_linespacing.png")

    fig5, ax5 = plt.subplots()
    ax5.set(title='Letter Size VS Word spacing', xlabel='Letter Size', ylabel='Word Spacing')
    plt.scatter(letter_size_scatter, word_spacing_scatter)
    fig5.savefig("visuals/lettersize_vs_wordspacing.png")

    fig6, ax6 = plt.subplots()
    ax6.set(title='Line spacing VS Word spacing', xlabel='Line Spacing', ylabel='Word Spacing')
    plt.scatter(line_spacing_scatter, word_spacing_scatter)
    fig6.savefig("visuals/linespacing_vs_wordspacing.png")

    fig7, ax7 = plt.subplots()
    ax7.set(title='Histogram for Slant Angle Categories', xlabel='Slant Angles Categories', ylabel='Frequency')
    plt.hist(slant_angle_array, color='skyblue', edgecolor='black')
    fig7.savefig('visuals/slant_angle_histogram.png')

    return


def run():
    print("Creating plots for visualization")
    top_margin_array, letter_size_array, line_spacing_array, word_spacing_array, slant_angle_array = create_summary()
    compute_pairwise_correlation(top_margin_array, letter_size_array, line_spacing_array, word_spacing_array)
    create_plots(top_margin_array, letter_size_array, line_spacing_array, word_spacing_array, slant_angle_array)
    print("Visuals created successfully")
    return
