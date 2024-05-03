# Z Tools

Blender 4.x Tools

## Create Convex

This will create a new Object from group of selected faces into Convex data for each Object

New Objects are created in a new Collection called "Convex"

### Tutorial

Switch to "Edit Mode"

Select faces that you want to make convex from it

Show "Z Tools" addon panel (press n), Click "Assign To Convex"

Switch to "Object Mode"

In addon panel (press n to show), click button "Create Convex", you will have new objects with same names added "-Convex" in Convex collection

Creating Convex Example:

![Imgur](https://i.imgur.com/OTTdBNW.gif)

## Export DAE

Export objects as ".dae" file into "output" folder.

Export will fix mesh(data) name to the same name of object name, this help OpenSIM handle the linkset.

**Export Individual**: Will export each object, each Object will have a standalone file exported, using the same name of object.

**Export Grouped**: Will export to 3 ".dae" files only,

1 - Objects that have Convex :  Face Group named "Convex",

2 - Objects that created from Convex:  it is a convex mesh for first objects.

3 - Objects that doesn't have Convex:  "Convex", for parts of the object that have no need for a Convex.

**Export by Collections**: Will export to ".dae" files by collections names.
