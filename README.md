
# Scripting in Autodesk Maya
Author: [Zhao Yafei](https://github.com/walkoncross/) (email: zhaoyafei0210@gmail.com)

1. Some useful information about scripting in Autodesk Maya.
2. Some Scripts (MEL or Python) for operations in Maya.

Table of Contents:
- [Scripting in Autodesk Maya](#scripting-in-autodesk-maya)
  - [Maya Application Content](#maya-application-content)
    - [Content Tree](#content-tree)
    - [Python Interpretor Path](#python-interpretor-path)
  - [Maya APIs](#maya-apis)
      - [MEL](#mel)
      - [C++ API](#c-api)
      - [Python API](#python-api)
        - [Offical (but confusing) Python APIs](#offical-but-confusing-python-apis)
        - [PyMel](#pymel)
  - [Which Python API to use?](#which-python-api-to-use)
  - [Scripting in Maya](#scripting-in-maya)
    - [MEL and Expressions](#mel-and-expressions)
    - [Python in Maya](#python-in-maya)
      - [maya.cmds](#mayacmds)
      - [pymel.core](#pymelcore)
      - [maya.OpenMaya](#mayaopenmaya)
      - [maya.api.OpenMaya](#mayaapiopenmaya)
  - [Maya Scripts](#maya-scripts)
    - [In-product MEL scripts](#in-product-mel-scripts)
    - [nodes/objects](#nodesobjects)
    - [blendshapes](#blendshapes)
    - [expressions](#expressions)
    - [keyframe](#keyframe)
  - [Maya Commands Reference and Node Types Reference](#maya-commands-reference-and-node-types-reference)
    - [Maya 2020](#maya-2020)
    - [Maya 2019](#maya-2019)
    - [Maya 2018](#maya-2018)
    - [Maya 2017](#maya-2017)
    - [Maya 2016](#maya-2016)
    - [Maya 2015](#maya-2015)
    - [Maya 2014](#maya-2014)
    - [Maya 2013](#maya-2013)
    - [Maya 2012](#maya-2012)
    - [Maya 2011](#maya-2011)
    - [Maya 2010](#maya-2010)
    - [Maya 2009](#maya-2009)
    - [Maya 2008](#maya-2008)

## Maya Application Content

### Content Tree
For Maya 2019 on MacOS:

```
/Applications/Autodesk/maya2019/Maya.app/Contents
├── Examples
├── Frameworks
├── Info.plist
├── MacOS
├── PkgInfo
├── Resources
├── _CodeSignature
├── assets
├── bin
├── brushImages
├── brushShapes
├── icons
├── lib
├── libexec
├── modules
├── presets
└── scripts
```

### Python Interpretor Path
For Maya 2019 on MacOS, Maya's python interpretor is under '/Applications/Autodesk/maya2019/Maya':
```
/Applications/Autodesk/maya2019/Maya.app/Contents/Frameworks/Python.framework
├── Headers -> Versions/Current/Headers
├── Python -> Versions/Current/Python
├── Resources -> Versions/Current/Resources
└── Versions
    ├── 2.7
    └── Current -> 2.7
```

## Maya APIs

#### MEL
MEL short for _Maya Embedded Language_, is a scripting language written for Maya, and with which much of Maya’s functionality and user interface is built. It was designed to be concise, simple, and Maya-specific.

#### C++ API
C++ API provides deeper access to Maya’s internals. With the API you can create new node types and new MEL commands. Prior to the introduction of python in Maya, the API could only be used with C++.

#### Python API

##### Offical (but confusing) Python APIs
PyMel docs give an clear introduction for the confusing official Maya Python APIs on this page (
[Why PyMEL?](http://help.autodesk.com/view/MAYAUL/2019/ENU/?guid=__PyMel_index_html)):
```

  Rather than reinvent the wheel, Autodesk opted to provide “wrappers” around their pre-existing toolsets: the C++ API and MEL. By wrapping them they provided an alternate python interface for each, but the core code that comprises the API and MEL remained largely the same. The wrappers serve as a (hopefully) thin layer to communicate between python and the Maya code being wrapped. The nature of the wraps is slightly different for each.

  - maya.OpenMaya
  In the case of the C++ API, Autodesk went with an open source wrapper called swig which generates python functions and classes from C++ counterparts. The python layer rests on top of C++, which remains the native execution language. During execution, swig marshals data back and forth between python and C++.
  MEL itself is split into two components: commands, and everything else.

  - maya.cmds
  In the case of MEL commands, which are (effectively) written using the C++ API, Autodesk wrote the wrapping mechanism themselves such that MEL commands could also be registered and used in python as functions. The same command executed in MEL and python ultimately end up triggering the same underlying C++ API calls.
  
  - maya.mel.eval
  In order to allow execution of arbitrary MEL code such as procedures, Autodesk provided high level access to the MEL interpreter. This is as simple of a wrapper as you can get: evaluate a string representing a chunk of MEL code in the MEL interpreter and convert the result to a python object (string, float, int, and lists thereof).
  So now that python is available in Maya all of our problems are solved, right? Well, not quite. Since these new modules are just wraps of the same underlying API and MEL code that we’ve had all along and neither were intended to eventually become “pythonified”, the syntax that results from this layering of python over MEL and C++ tends to be awkward, especially to those familiar with python’s idioms.

  This syntactical awkwardness, particularly in maya.cmds, was one of the initial inspirations behind PyMEL. Think of it this way: would you rather read a book that was translated from japanese into english by a software program like babelfish or by a human who is fluent in both languages? That is a key difference between an automatic wrap like maya.cmds and a “restructured wrap” like PyMEL, which uses the maya python modules as building blocks to construct an intuitive, insightful, and pythonic API.
```

##### PyMel
[PyMel Docs](http://help.autodesk.com/view/MAYAUL/2019/ENU/?guid=__PyMel_index_html)

What is PyMel:

> PyMEL makes python scripting in Maya work the way it should. Maya’s command module is a direct translation of MEL commands into python functions. The result is a very awkward and unpythonic syntax which does not take advantage of python’s strengths – particularly, a flexible, object-oriented design. PyMEL builds on the cmds module by organizing many of its commands into a class hierarchy, and by customizing them to operate in a more succinct and intuitive way.

## Which Python API to use?
The official ones: maya.cmds/maya.mel

__Reasons__:
- Official support
- More stable
- Detailed reference ([Maya Commands Reference and Node Types Reference](#maya-commands-reference-and-node-types-reference))
- Slow update of PyMel (As of June 2020, v1.0.10 only annouced support for Maya 2018, See [Here](https://help.autodesk.com/cloudhelp/2019/JPN/Maya-Tech-Docs/PyMel/whats_new.html#version-1-0-10))


## Scripting in Maya
Cloud Help for [Scripting in Maya 2019](https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2019/ENU/Maya-Scripting/files/GUID-1C6C0BC0-002C-4035-ADC7-97AD2F390190-htm.html) on knowledge.autodesk.com.

### MEL and Expressions
Cloud Help for [MEL and Expressions in Maya 2019](https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2019/ENU/Maya-Scripting/files/GUID-E151A15C-BA1D-4E60-8DB6-9D92C6202170-htm.html) on knowledge.autodesk.com.

### Python in Maya
Cloud Help for [Python in Maya 2019](https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2019/ENU/Maya-Scripting/files/GUID-703B18A2-89E5-48A8-988A-1ED815D5566F-htm.html) on knowledge.autodesk.com.


Python scripting can be used for many tasks in Maya, from running simple commands to developing plug-ins, and several different Maya-related libraries are available targeting different tasks. The following is a brief overview of the Python libraries shipped with Maya:

#### maya.cmds
This is a Python wrapper for MEL commands, and can be used in place of MEL. For more information, see Using Python and the Python Commands Reference.

#### pymel.core
Pymel is an alternative wrapper for MEL, developed by a _third party_. It is shipped with Maya, but not supported by Autodesk. It organizes commands differently, and takes an object-oriented approach compared to the procedural approach of maya.cmds. For more information, see Using PyMEL and the PyMel Reference.

[PyMel Docs](http://help.autodesk.com/view/MAYAUL/2019/ENU/?guid=__PyMel_index_html)

#### maya.OpenMaya
This is a Python wrapper for the Maya C++ API, and referred to as Python API 1.0. It is suitable for developing plug-ins, and other tasks that require functionality not exposed by MEL. To understand the exposed classes, you should refer to the conceptual topics and the "C++ API Reference" in the Maya Developer Help. For more information, see "Maya Python API 1.0" in the Maya Developer Help.

#### maya.api.OpenMaya
This is a Python wrapper for the Maya C++ API, and referred to as Python API 2.0. This wrapper has better performance and is more "Pythonic" than the Python API 1.0. It is also a newer API, and is still under development, so not all classes exposed in 1.0 are available. For more information, see "Maya Python API 2.0" and "Maya Python API 2.0 Reference" in the Maya Developer Help.

## Maya Scripts

### In-product MEL scripts
On MacOS, Maya 2019 in-product scripts (.MEL) are under /Applications/Autodesk/maya2019/Maya.app/Contents/scripts. The content tree is as follows:

```
/Applications/Autodesk/maya2019/Maya.app/Contents/scripts
├── AETemplates
├── FBX
├── NETemplates
├── fur
├── gameFbxExporterPresets
├── muscle
├── others
├── paintEffects
├── shelves
├── startup
├── turtle
└── unsupported
```

### nodes/objects
- Get name lists of nodes/objects using cmds.ls()
  - Python Script with maya.cmds: [maya_get_nodes_list.py](./maya_get_nodes_list.py) (Tested in Maya2019) 
    __functions:__
    - get_current_scene_name()
    - export_nodes_list()
    - get_node_types()
    - get_all_node_list()
    - get_all_shape_nodes()
    - get_all_transform_nodes()
    - get_all_mesh_nodes()
    - get_all_joint_nodes()
    - get_all_blendshape_nodes()
    - get_all_geometry_nodes()
    - get_all_material_nodes()
    - get_all_texture_nodes()
    - get_all_camera_nodes()
    - get_all_light_nodes()
    - get_all_partition_nodes()
    - get_all_set_nodes()
    - get_all_container_nodes()
    - get_all_plane_nodes()
- Get node/object name list of the specified node type using cmds.ls()
  - Python Script with maya.cmds: [maya_get_nodes_list_of_type.py](./maya_get_nodes_list_of_type.py) (Tested in Maya2019) 
    __functions:__
    - get_current_scene_name()
    - export_nodes_list()
    - get_node_types()
    - get_all_node_list()
    - get_node_list_of_type(): succeeded on types: mesh/blendShape/joint/camera/constraint/..., failed on types: material/texture/light

### blendshapes
- Duplicate blendshape targets
    - default: When operating in Shape Editor, this will automatically call /Applications/Autodesk/maya2019/Maya.app/Contents/scripts/blendShapeEditorDuplicateTargets.MEL
- Export name list of target shape of the specified blendshape into .txt file
  - Python Script with maya.cmds: [maya_export_blenshape_keys_list.py](./maya_export_blenshape_keys_list.py) (Tested in Maya2019)
- Export name list of target shape of all blendshape nodes into .txt file
  - Python Script with maya.cmds: [maya_export_blenshape_keys_list_all.py](./maya_export_blenshape_keys_list_all.py) (Tested in Maya2019)
- Export target shapes of specified blendshape into .obj file
  - Python Script with maya.cmds: [maya_export_blenshape_objs.py](./maya_export_blenshape_objs.py) (Tested in Maya2019)

### expressions
- Export expressions into .txt file
  - Python Script with maya.cmds: [maya_export_expressions.py](./maya_export_expressions.py) (Tested in Maya2019)

### keyframe
- Export keyframe meshes into .obj file
  - Python Script with maya.cmds: [maya_export_keyframe_meshes_to_objs.py](./maya_export_keyframe_meshes_to_objs.py) (Tested in Maya2019)


## Maya Commands Reference and Node Types Reference
The following links were accessible as of June 2020.

### Maya 2020
  - [Commands in MEL](https://help.autodesk.com/cloudhelp/2020/ENU/Maya-Tech-Docs/Commands/index.html)
  - [Commands in Python](https://help.autodesk.com/cloudhelp/2020/ENU/Maya-Tech-Docs/CommandsPython/index.html) 
  - [Node Types](http://help.autodesk.com/cloudhelp/2020/ENU/Maya-Tech-Docs/Nodes/index.html)
### Maya 2019
  - [Commands in MEL](https://help.autodesk.com/cloudhelp/2019/ENU/Maya-Tech-Docs/Commands/index.html)
  - [Commands in Python](https://help.autodesk.com/cloudhelp/2019/ENU/Maya-Tech-Docs/CommandsPython/index.html) 
  - [Node Types](http://help.autodesk.com/cloudhelp/2019/ENU/Maya-Tech-Docs/Nodes/index.html)
### Maya 2018
  - [Commands in MEL](https://help.autodesk.com/cloudhelp/2018/ENU/Maya-Tech-Docs/Commands/index.html)
  - [Commands in Python](https://help.autodesk.com/cloudhelp/2018/ENU/Maya-Tech-Docs/CommandsPython/index.html)
  - [Node Types](http://help.autodesk.com/cloudhelp/2018/ENU/Maya-Tech-Docs/Nodes/index.html)
### Maya 2017
  - [Commands in MEL](http://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/Commands/index.html)
  - [Commands in Python](http://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/CommandsPython/index.html)
  - [Node Types](http://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/Nodes/index.html)
### Maya 2016
  - [Commands in MEL](http://help.autodesk.com/cloudhelp/2016/ENU/Maya-Tech-Docs/Commands/index.html)
  - [Commands in Python](http://help.autodesk.com/cloudhelp/2016/ENU/Maya-Tech-Docs/CommandsPython/index.html)
  - [Node Types](http://help.autodesk.com/cloudhelp/2016/ENU/Maya-Tech-Docs/Nodes/index.html)
### Maya 2015
  - [Commands in MEL](http://help.autodesk.com/cloudhelp/2015/ENU/Maya-Tech-Docs/Commands/index.html)
  - [Commands in Python](http://help.autodesk.com/cloudhelp/2015/ENU/Maya-Tech-Docs/CommandsPython/index.html)
  - [Node Types](http://help.autodesk.com/cloudhelp/2015/ENU/Maya-Tech-Docs/Nodes/index.html)
### Maya 2014
  - [Commands in MEL](https://download.autodesk.com/global/docs/maya2014/en_us/Commands/index.html)
  - [Commands in Python](https://download.autodesk.com/global/docs/maya2014/en_us/CommandsPython/index.html)
  - [Node Types](https://download.autodesk.com/global/docs/maya2014/en_us/Nodes/index.html)
### Maya 2013
  - [Commands in MEL](https://download.autodesk.com/global/docs/maya2013/en_us/Commands/index.html)
  - [Commands in Python](https://download.autodesk.com/global/docs/maya2013/en_us/CommandsPython/index.html)
  - [Node Types](https://download.autodesk.com/global/docs/maya2013/en_us/Nodes/index.html)
### Maya 2012
  - [Commands in MEL](https://download.autodesk.com/global/docs/maya2012/en_us/Commands/index.html)
  - [Commands in Python](https://download.autodesk.com/global/docs/maya2012/en_us/CommandsPython/index.html)
  - [Node Types](https://download.autodesk.com/global/docs/maya2012/en_us/Nodes/index.html)
### Maya 2011
  - [Commands in MEL](https://download.autodesk.com/us/maya/2011help/Commands/index.html)
  - [Commands in Python](https://download.autodesk.com/us/maya/2011help/CommandsPython/index.html)
  - [Node Types](https://download.autodesk.com/us/maya/2011help/Nodes/index.html)
### Maya 2010
  - [Commands in MEL](https://download.autodesk.com/us/maya/2010help/Commands/index.html)
  - [Commands in Python](https://download.autodesk.com/us/maya/2010help/CommandsPython/index.html)
  - [Node Types](https://download.autodesk.com/us/maya/2010help/Nodes/index.html)
### Maya 2009
  - [Commands in MEL](https://download.autodesk.com/us/maya/2009help/Commands/index.html)
  - [Commands in Python](https://download.autodesk.com/us/maya/2009help/CommandsPython/index.html)
  - [Node Types](https://download.autodesk.com/us/maya/2009help/Nodes/index.html)
### Maya 2008
  - [Commands in MEL](https://download.autodesk.com/us/maya/2008help/Commands/index.html)
  - [Commands in Python](https://download.autodesk.com/us/maya/2008help/CommandsPython/index.html)
  - [Node Types](https://download.autodesk.com/us/maya/2008help/Nodes/index.html)