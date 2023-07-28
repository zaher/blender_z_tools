# Z Tools

Blender 3.4 Tools

## Create Convex

This will create a new Object from group of selected faces in Face Map with the name "Convex" for each Object

New Objects are created in a  new Collection called "Convex"

## Export

Export functions will fix mesh name to the same name of object name, this help OpenSIM handle the linkset

Export Individual: Will export each project as DAE file into "output" folder, each Object will have a standalone file exported, using the same name of object.

Export Grouped: Will export to 3 .dea files,

    Objects that have Face Map :  Face Group named "Convex",
    Objects that created from Face Map:  Face Group, it is a convex mesh for first objects.
    Objects that doesn't have Face Map:  "Convex", for parts of the object that have no need for a Convex.
