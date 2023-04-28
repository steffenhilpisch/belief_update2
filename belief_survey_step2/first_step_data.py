# HOW TO GENERATE THE LIST:
# STEP 1: download the `Plain` All apps data (click on 'Data' in OTree)
# STEP 2: feed the csv into `generate_possibilities_from_step1.py`
#         E.g Run `python3 generate_possibilites_from_step1.py all_apps_wide_2023-02-02.csv
#         E.g Or Write the ouptut of the script into a new file named `output.txt` `python3 generate_possibilites_from_step1.py all_apps_wide_2023-02-02.csv >> output.txt
# STEP 3: paste output of the script into the array below
possibilities = [
        ['55', '60', 'informative'], # round3 belief 70
        ['70', '79', 'informative'], # round3 belief 90
        ['60', '70', 'uninformative'],  # round3 belief 60
        ['70', '85', 'uninformative'],  # round3 belief 70
        ['60', '50', 'informative'],  # round3 belief 30
        ['75', '50', 'informative'],  # round3 belief 10
        ['60', '50', 'uninformative'],  # round3 belief 60
        ['75', '41', 'uninformative'],  # round3 belief 40
        ['55', '65', 'uninformative'],  # round3 belief 50
]