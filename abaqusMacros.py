# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

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
    s = p.features['Shell planar-1'].sketch
    mdb.models['Dimension-Modification'].ConstrainedSketch(name='__edit__', 
        objectToCopy=s)
    s2 = mdb.models['Dimension-Modification'].sketches['__edit__']
    g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
    s2.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s2, 
        upToFeature=p.features['Shell planar-1'], filter=COPLANAR_EDGES)
    s2.unsetPrimaryObject()
    del mdb.models['Dimension-Modification'].sketches['__edit__']
    p = mdb.models['Dimension-Modification'].parts['Bracket']
    p.regenerate()


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


