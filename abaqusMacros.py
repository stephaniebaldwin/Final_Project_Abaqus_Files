# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

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
    s.parameters['D1'].setValues(expression='143')
    s1.unsetPrimaryObject()
    p = mdb.models['Dimension-Modification'].parts['Bracket']
    p.features['bracket-feature'].setValues(sketch=s1)
    del mdb.models['Dimension-Modification'].sketches['__edit__']
    p = mdb.models['Dimension-Modification'].parts['Bracket']
    p.regenerate()


def create_seed_and_mesh():
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
    a.seedPartInstance(regions=partInstances, size=8.0, deviationFactor=0.1, 
        minSizeFactor=0.1)
    a = mdb.models['Dimension-Modification'].rootAssembly
    partInstances =(a.instances['quad8'], )
    a.generateMesh(regions=partInstances)


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


def open_odb():
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
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a = mdb.models['Dimension-Modification'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    o3 = session.openOdb(
        name='C:/Users/Owner/OneDrive - University of Florida/@Spring 25/FEA/FEA Final Project/Final_Project_Abaqus_Files/Dimension-Modification-Job.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=o3)
    session.viewports['Viewport: 1'].makeCurrent()
    session.mdbData.summary()


