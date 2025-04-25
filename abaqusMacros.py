# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

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
    mdb.jobs['Dimension-Modification-Job'].submit(consistencyChecking=OFF)


def to_visualization_module():
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
    session.mdbData.summary()
    odb = session.odbs['C:/Users/Owner/OneDrive - University of Florida/@Spring 25/FEA/FEA Final Project/Final_Project_Abaqus_Files/Dimension-Modification-Job.odb']
    session.viewports['Viewport: 1'].setValues(displayedObject=odb)


def modify_dimension():
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
    s.parameters['D1'].setValues(expression='140')


