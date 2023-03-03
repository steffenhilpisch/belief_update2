# HOW TO GENERATE THE LIST:
# STEP 1: download the `Plain` All apps data (click on 'Data' in OTree)
# STEP 2: feed the csv into `generate_possibilities_from_step1.py`
#         E.g Run `python3 generate_possibilites_from_step1.py all_apps_wide_2023-02-02.csv
#         E.g Or Write the ouptut of the script into a new file named `output.txt` `python3 generate_possibilites_from_step1.py all_apps_wide_2023-02-02.csv >> output.txt
# STEP 3: paste output of the script into the array below
possibilities = [
                [24, 65, "informative"],
                [54, 65, "informative"],
                [23, 87, "informative"],
                [54, 90, "informative"],
                [3, 84, "uninformative"],
                [12, 20, "informative"],
            ]