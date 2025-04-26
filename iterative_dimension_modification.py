# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__
import mesh
import numpy as np
import json

model_name = 'Dimension-Modification'
part_name = 'Bracket'
feature_name = 'bracket-feature'
instance_name = 'quad8'
odb_path = 'C:/Users/Owner/OneDrive - University of Florida/@Spring 25/FEA/FEA Final Project/Final_Project_Abaqus_Files/Dimension-Modification-Job.odb'

# sketch object not embedded into a feature. Can be modified directly but isn't tied to a model 
#persistent_sketch = mdb.models[model_name].sketches['modifiable_sketch']

# custom functions
def modify_dimension_parameter(parameter_name, new_dimension):  # mm
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    p = mdb.models['Dimension-Modification'].parts['Bracket']
    s = p.features['bracket-feature'].sketch
    mdb.models['Dimension-Modification'].ConstrainedSketch(name='__edit__', 
        objectToCopy=s)
    s1 = mdb.models['Dimension-Modification'].sketches['__edit__']
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s1, 
        upToFeature=p.features['bracket-feature'], filter=COPLANAR_EDGES)
    s=mdb.models['Dimension-Modification'].sketches['__edit__']
    s.parameters[parameter_name].setValues(expression=str(new_dimension))
    s1.unsetPrimaryObject()
    p = mdb.models['Dimension-Modification'].parts['Bracket']
    p.features['bracket-feature'].setValues(sketch=s1)
    del mdb.models['Dimension-Modification'].sketches['__edit__']
    p = mdb.models['Dimension-Modification'].parts['Bracket']
    p.regenerate()

   
   
def regenerate_mesh():
    # also creates new seeds
    # not just the modified macro because need to ensure that # nodes < 1000
    seed_size = 8
    while 3>1:
        create_seed_and_mesh(seed_size)  # generate mesh
        # check node count
        assembly = mdb.models[model_name].rootAssembly   # get assembly instance
        instance = assembly.instances[instance_name]
        num_nodes_instance = len(instance.nodes)         # get node count
        print("# nodes: " + str(num_nodes_instance))
        if num_nodes_instance < 1000:
            break
        else:
            seed_size = seed_size + 0.5   # make seeds more spaced out and try generating mesh again
            
                    
def create_seed_and_mesh(size_for_seed_gen):
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    a = mdb.models['Dimension-Modification'].rootAssembly
    partInstances =(a.instances['quad8'], )
    a.seedPartInstance(regions=partInstances, size=size_for_seed_gen, deviationFactor=0.1, 
        minSizeFactor=0.1)
    a = mdb.models['Dimension-Modification'].rootAssembly
    partInstances =(a.instances['quad8'], )
    a.generateMesh(regions=partInstances)
    
    
def initialize_all_modifiable_dimensions():
    modify_dimension_parameter('D1', 140)
    modify_dimension_parameter('D2', 20)
    modify_dimension_parameter('D3', 25)
    modify_dimension_parameter('D4', 55)
    modify_dimension_parameter('D5', 110)
    modify_dimension_parameter('D6', 25)
    modify_dimension_parameter('D7', 25)
    modify_dimension_parameter('D8', 25)
    modify_dimension_parameter('D9', 10)
    regenerate_mesh()
    
    
def submit_job():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    mdb.jobs['Dimension-Modification-Job'].submit(consistencyChecking=OFF)
    mdb.jobs['Dimension-Modification-Job'].waitForCompletion()  # pause script execution until job completion
    
 
def get_max_mises():      # MPa
    # open odb
    odb = session.openOdb(name=odb_path)
    step = odb.steps['Horizontal-Load']
    frame = step.frames[1]

    stress = frame.fieldOutputs['S']  # extract the stress output

    # find max stress
    max_stress = max(stress.values, key=lambda s: s.mises).mises
    return max_stress
    
    
def compute_part_mass():   # kg
    density = 0.00000758   # kg/mm^3
    front_surface_area = compute_front_surface_area()
    thickness = 3  # mm
    mass = front_surface_area*thickness*density
    return mass
    

def compute_front_surface_area():   # mm^2
    assembly = mdb.models[model_name].rootAssembly   # get assembly instance
    instance = assembly.instances[instance_name]
    total_area = 0
    for element in instance.elements:
        nodes = element.getNodes()    # get nodes
        coords = [node.coordinates for node in nodes]  # get nodal coordinates
        A = coords[0][0:2]
        B = coords[1][0:2]
        C = coords[2][0:2]
        D = coords[3][0:2]
        # compute area
        area1 = 0.5 * abs((B[0] - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (B[1] - A[1]))
        area2 = 0.5 * abs((C[0] - A[0]) * (D[1] - A[1]) - (D[0] - A[0]) * (C[1] - A[1]))
        total_area = total_area + area1 + area2
    return total_area
    
    
# the actual script

max_allowable_stress = 800  # MPa

# import parameters from file created in external script
params_file = 'parameters.json'
with open(params_file, 'r') as f:
    params = json.load(f)

D1 = params['D1']
D2 = params['D2']
D3 = params['D3']
D4 = params['D4']
D5 = params['D5']
D6 = params['D6']
D7 = params['D7']
D8 = params['D8']
D9 = params['D9']


model_name = 'Dimension-Modification'
part_name = 'Bracket'

# Modify dimensions
modify_dimension_parameter('D1', D1)
modify_dimension_parameter('D2', D2)
modify_dimension_parameter('D3', D3)
modify_dimension_parameter('D4', D4)
modify_dimension_parameter('D5', D5)
modify_dimension_parameter('D6', D6)
modify_dimension_parameter('D7', D7)
modify_dimension_parameter('D8', D8)
modify_dimension_parameter('D9', D9)
regenerate_mesh()

# submit job
submit_job()

# get results
mass = compute_part_mass()
stress = get_max_mises()

odb = session.openOdb(name='Dimension-Modification-Job.odb')
step = odb.steps['Horizontal-Load']
frame = step.frames[1]
stress = frame.fieldOutputs['S']
max_stress = max(stress.values, key=lambda s: s.mises).mises

# Save the result (objective function value) to a JSON file
result = {
    'optimal_D1': D1,
    'optimal_D2': D2,
    'optimal_D3': D3,
    'optimal_D4': D4,
    'optimal_D5': D5,
    'optimal_D6': D6,
    'optimal_D7': D7,
    'optimal_D8': D8,
    'optimal_D9': D9,
    'objective_value': mass,
    'max_stress' : stress
}

results_file = 'results.json'
with open(results_file, 'w') as f:
    json.dump(result, f)

print(f"Simulation complete: {result}")


                                  


