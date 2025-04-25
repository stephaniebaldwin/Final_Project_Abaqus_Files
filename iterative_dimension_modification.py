# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__
import mesh

model_name = 'Dimension-Modification'
part_name = 'Bracket'
feature_name = 'bracket-feature'

# sketch object not embedded into a feature. Can be modified directly but isn't tied to a model 
persistent_sketch = mdb.models[model_name].sketches['modifiable_sketch']

# custom functions
def modify_dimension_parameter(parameter_name, new_dimension):
    part = mdb.models[model_name].parts[part_name]    # access part
    part.features[feature_name].setValues(D1=str(new_dimension))
    mdb.models[model_name].parts[part_name].regenerate()
    # access the parameter by its string key
    # persistent_sketch.parameters[parameter_name].setValues(expression=str(new_dimension))
    
def modify_dimension(parameter_name, new_dimension):
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
    s.parameters[parameter_name].setValues(expression=str(new_dimension)
    
    
def regenerate_feature():
    part = mdb.models[model_name].parts[part_name]    # access part
    #part.features[feature_name].setValues(D1='new_dimension')
    
    # delete feature with outdated sketch dimensions
    #if feature_name in part.features:
        #print('rename feature with outdated dimensions')
        #part.deleteFeatures((feature_name,))
    #    part.features.changeKey(fromName=feature_name, toName='temp')
    #else:
    #    print('Feature does not exist')
    #new_feature = part.BaseShell(sketch=persistent_sketch) # make feature with updated dims
    #part.features.changeKey(fromName=new_feature.name, toName=feature_name)
    #part.deleteFeatures(('temp',))   # delete outdated feature
    
    
def regenerate_mesh():
    # also creates new seeds
    pass
    
    
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
    regenerate_feature()
    regenerate_mesh()
    
    
def create_persistent_sketch_from_feature():
    part = mdb.models[model_name].parts[part_name]  # access the part and feature containing the sketch
    feature = part.features[feature_name]
    embedded_sketch = feature.sketch

    # create a new named sketch and copy geometry into it
    mdb.models[model_name].ConstrainedSketch(name='modifiable_sketch', objectToCopy=embedded_sketch)
    

def set_section_sketch_to_persistent():
    part = mdb.models[model_name].parts[part_name]   # get part
    # Replace the sketch for the feature
    part.features['bracket-feature'].setValues(sketch=persistent_sketch)
    mdb.models[model_name].parts[part_name].regenerate()
    
    
def submit_job():
    pass
    
    
# the actual script
# yay

#modify_dimension_parameter('D1', 142)
# regenerate_feature()






