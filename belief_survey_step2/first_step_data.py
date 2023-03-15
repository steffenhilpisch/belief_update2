# HOW TO GENERATE THE LIST:
# STEP 1: download the `Plain` All apps data (click on 'Data' in OTree)
# STEP 2: feed the csv into `generate_possibilities_from_step1.py`
#         E.g Run `python3 generate_possibilites_from_step1.py all_apps_wide_2023-02-02.csv
#         E.g Or Write the ouptut of the script into a new file named `output.txt` `python3 generate_possibilites_from_step1.py all_apps_wide_2023-02-02.csv >> output.txt
# STEP 3: paste output of the script into the array below
possibilities = {
    ('informative', 'red'): [
        ['11', '22', 'informative'], # round3 belief 33
    ],
    ('uninformative', 'red'): [
        ['10', '20', 'uninformative'], # round3 belief 30
        ['11', '22', 'uninformative'],  # round3 belief 30
    ],
    ('informative', 'blue'): [
        ['03', '22', 'uninformative'],  # round3 belief 30
    ],
    ('uninformative', 'blue'): [
        ['04', '22', 'uninformative'],  # round3 belief 30
    ],
}

group_weights = {
('informative', 'red'): 0.25, # 25%
('uninformative', 'red'): 0.2,
('informative', 'blue'): 0.2,
('uninformative', 'blue'): 0.35,
}