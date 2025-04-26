# do optimization using the 3rd party libraries that abaqus cae won't let me have :(
from skopt import gp_minimize
import json
import subprocess
import pandas as pd
import os

# create log file
results_file = "optimization_log.csv"
if not os.path.exists(results_file):    # If file doesn't exist, create it with headers
    df = pd.DataFrame(columns=["Iteration", "Dimensions", "MaxStress", "Mass"])
    df.to_csv(results_file, index=False)


# define seach space for inputs
space = [(100, 180),  # Range for D1
         (5, 40),     # etc
         (10,45),
         (20,80),
         (80, 140),
         (10,45),
         (10,45),
         (10,45),
         (3,20)]

# Function to check if the results file exists and has been updated
def file_exists_and_updated(results_file):
    try:
        # Check if file exists and is not empty
        with open(results_file, 'r') as f:
            data = json.load(f)
            if 'objective_value' in data:
                return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    return False


# define objective func
def objective_function(params):
    D1, D2, D3, D4, D5, D6, D7, D8, D9 = params

    params_file = 'parameters.json'
    with open(params_file, 'w') as f:
        json.dump({'D1': float(D1),'D2': float(D2), 'D3': float(D3), 'D4': float(D4), 'D5': float(D5),
                   'D6': float(D6), 'D7': float(D7), 'D8': float(D8), 'D9':float(D9)}, f)

    # Call the Abaqus script to run the simulation (waits for the job to complete)
    #command = f"abaqus python iterative_dimension_modification.py"
    #command = r'"C:\SIMULIA\Commands\abq2024LE.bat" python "C:\Users\Owner\OneDrive - University of Florida\@Spring 25\FEA\FEA Final Project\Final_Project_Abaqus_Files\iterative_dimension_modification.py"'
    command = r'"C:\SIMULIA\Commands\abq2024LE.bat" cae noGUI=iterative_dimension_modification.py'

    subprocess.run(command, check=True)

    # Wait for the results file to be updated
    results_file = 'results.json'
    while not file_exists_and_updated(results_file):
        time.sleep(5)  # Check every 5 seconds

    # Read the results from the file
    with open(results_file, 'r') as f:
        results = json.load(f)

    # update log file
    log_file = "optimization_log.csv"
    df = pd.read_csv(log_file)

    new_row = {
        "Iteration": len(df),
        "Dimensions": [D1, D2, D3, D4, D5, D6, D7, D8, D9],
        "MaxStress": results['max_stress'],
        "Mass": results['mass']
    }
    df = df.append(new_row, ignore_index=True)
    df.to_csv(log_file, index=False)


    mass_biased = results['mass']
    if results['max_stress'] > 800: # add extra weight if max stress is exceeded
        mass_biased = 1000*0.238916112923454*((results['max_stress'] - 800)/800)

    # The result is the stress or any other output you'd like to minimize/maximize
    return mass_biased


# do optimization
res = gp_minimize(objective_function, space, n_calls=50, random_state=42)

# Extract the optimal dimensions from the result
optimal_D1, optimal_D2, optimal_D3, optimal_D4,optimal_D5,optimal_D6,optimal_D7,optimal_D8,optimal_D9 = res.x
optimal_result = {
    'optimal_D1': optimal_D1,
    'optimal_D2': optimal_D2,
    'optimal_D3': optimal_D3,
    'optimal_D4': optimal_D4,
    'optimal_D5': optimal_D5,
    'optimal_D6': optimal_D6,
    'optimal_D7': optimal_D7,
    'optimal_D8': optimal_D8,
    'optimal_D9': optimal_D9,
    'mass': res.fun
}






