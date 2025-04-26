# do optimization using the 3rd party libraries that abaqus cae won't let me have :(
from skopt import gp_minimize
import json
import subprocess
import pandas as pd
import os
import time

# create log file
results_file = "optimization_log.csv"
if not os.path.exists(results_file):    # If file doesn't exist, create it with headers
    df = pd.DataFrame(columns=["Iteration", "Dimensions", "MaxStress", "Mass"])
    df.to_csv(results_file, index=False)

# initialize input json
params_file = r"C:\Users\Owner\OneDrive - University of Florida\@Spring 25\FEA\FEA Final Project\Final_Project_Abaqus_Files\parameters.json"
initial_params = {
    'D1': 140,
    'D2': 20,
    'D3': 25,
    'D4': 55,
    'D5': 110,
    'D6': 25,
    'D7': 25,
    'D8': 25,
    'D9': 10
}
with open(params_file, 'w') as f:
        json.dump(initial_params, f)

# initialize results
results_file = r"C:\Users\Owner\OneDrive - University of Florida\@Spring 25\FEA\FEA Final Project\Final_Project_Abaqus_Files\results.json"
result = {
    'optimal_D1': 140,
    'optimal_D2': 20,
    'optimal_D3': 25,
    'optimal_D4': 55,
    'optimal_D5': 110,
    'optimal_D6': 25,
    'optimal_D7': 25,
    'optimal_D8': 25,
    'optimal_D9': 10,
    'objective_value': 0,
    'max_stress' : 0
}
with open(results_file, 'w') as f:
    json.dump(result, f)


# Define search space for inputs
space = [(120, 160),  # Range for D1
         (18, 22),     # etc
         (20,30),
         (50,60),
         (100,120),
         (22,30),
         (22,30),
         (22,25),
         (7,13)]

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

# Define objective function
def objective_function(params):
    D1, D2, D3, D4, D5, D6, D7, D8, D9 = params

    # Use the initial parameters if no optimization is done yet
    updated_params = {
        'D1': float(D1) if D1 is not None else initial_params['D1'],
        'D2': float(D2) if D2 is not None else initial_params['D2'],
        'D3': float(D3) if D3 is not None else initial_params['D3'],
        'D4': float(D4) if D4 is not None else initial_params['D4'],
        'D5': float(D5) if D5 is not None else initial_params['D5'],
        'D6': float(D6) if D6 is not None else initial_params['D6'],
        'D7': float(D7) if D7 is not None else initial_params['D7'],
        'D8': float(D8) if D8 is not None else initial_params['D8'],
        'D9': float(D9) if D9 is not None else initial_params['D9']
    }

    with open(params_file, 'w') as f:
        json.dump(updated_params, f)

    # Call the Abaqus script to run the simulation (waits for the job to complete)
    command = f"abaqus cae noGUI=iterative_dimension_modification.py"
    command = f'"C:\\SIMULIA\\Commands\\abq2024LE.bat" cae noGUI="C:\\Users\\Owner\\OneDrive - University of Florida\\@Spring 25\\FEA\\FEA Final Project\\Final_Project_Abaqus_Files\\iterative_dimension_modification.py"'
    command = [
        r"C:\SIMULIA\Commands\abq2024LE.bat",
        "cae",
        r"noGUI=C:\Users\Owner\OneDrive - University of Florida\@Spring 25\FEA\FEA Final Project\Final_Project_Abaqus_Files\iterative_dimension_modification.py"
    ]


    #subprocess.run(command, check=True)
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("Error during Abaqus execution:", e)
        print("Stdout:", e.stdout)
        print("Stderr:", e.stderr)

    
    # Wait for the results file to be created and updated
    results_file = 'results.json'
    while not file_exists_and_updated(results_file):
        time.sleep(5)  # Check every 5 seconds

    # Read the results from the file
    with open(results_file, 'r') as f:
        results = json.load(f)

    mass_biased = results['objective_value']
    if results['max_stress'] > 800:  # Add extra weight if max stress is exceeded
        mass_biased = 1000 * 0.238916112923454 * ((results['max_stress'] - 800) / 800)
    
    # Append results to the log file
    optimal_result = {
    "optimal_D1": result["optimal_D1"],
    "optimal_D2": result["optimal_D2"],
    "optimal_D3": result["optimal_D3"],
    "optimal_D4": result["optimal_D4"],
    "optimal_D5": result["optimal_D5"],
    "optimal_D6": result["optimal_D6"],
    "optimal_D7": result["optimal_D7"],
    "optimal_D8": result["optimal_D8"],
    "optimal_D9": result["optimal_D9"]
    }
    log_data = pd.read_csv(results_file)
    log_data = pd.concat([log_data, pd.DataFrame([{
        "Iteration": len(log_data) + 1,
        "Dimensions": optimal_result,
        "MaxStress": results['max_stress'],
        "Mass": results['objective_value']
    }])], ignore_index=True)
    log_data.to_csv(results_file, index=False)

    # The result is the stress or any other output you'd like to minimize/maximize
    return mass_biased

# Run optimization
res = gp_minimize(objective_function, space, n_calls=50, random_state=42)

# Extract the optimal dimensions from the result
optimal_D1, optimal_D2, optimal_D3, optimal_D4, optimal_D5, optimal_D6, optimal_D7, optimal_D8, optimal_D9 = res.x
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

# Append results to the log file
#log_data = pd.read_csv(results_file)
#log_data = pd.concat([log_data, pd.DataFrame([{
#    "Iteration": len(log_data) + 1,
#    "Dimensions": optimal_result,
#    "MaxStress": results['max_stress'],
#    "Mass": results['objective_value']
#}])], ignore_index=True)

#log_data.to_csv(results_file, index=False)





