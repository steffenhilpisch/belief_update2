# how to call: python3 generate_possibilites_from_step1.py /home/rune/Downloads/all_apps_wide_2023-02-02\(2\).csv

# small script that reads the data from step1 and outputs the data that is needed for step2
import argparse
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a file')
    parser.add_argument('file', type=argparse.FileType('r'), help='the input file eg. all_apps_wide-2023-02-02.csv')
    args = parser.parse_args()

    with args.file as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')

        # get the names of the columns
        column_names = next(reader)

        # get the index of the columns we are interested in
        belief_round1 = column_names.index("belief_survey.1.player.belief")
        belief_round2 = column_names.index("belief_survey.2.player.belief")
        belief_round3 = column_names.index("belief_survey.3.player.belief")
        belief_verification3 = column_names.index("belief_survey.3.player.verification")

        print("OUTPUT:")
        for row in reader:
            selected = [row[i] for i in [belief_round1, belief_round2, belief_verification3]]
            # convert last column
            selected[2] = "informative" if selected[2] == "true" else ("uniformative" if selected[2] == "fake" else f"unkown ({selected[2]})")
            print(f"{selected}, # round3 belief {row[belief_round3]}")
