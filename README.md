# Z Tools

Blender 3.4 Tools

## Create Convex

This will create a new Object from group of selected faces in Face Map with the name "Convex" for each Object

New Objects are created in a  new Collection called "Convex"

### Tutorial

Switch "Edit Mode"

Select faces that you want to make convex from it

Go to on left Panel and find Face Map, Create new map, name it "Convex", Assign this faces to it

![Screenshot01](https://i.imgur.com/YsH6CPi.png)

Now press n to see panel of addon, click button "Create Convex", you will have new objects with same names added "-Convex" in Convex collection

![Screenshot01](https://i.imgur.com/UDmglQK.png)

Creating Convex Example:

![Imgur](https://i.imgur.com/qq9xYsJ.gif)

## Export

Export functions will fix mesh name to the same name of object name, this help OpenSIM handle the linkset

Export Individual: Will export each project as DAE file into "output" folder, each Object will have a standalone file exported, using the same name of object.

Export Grouped: Will export to 3 .dea files,

1 - Objects that have Face Map :  Face Group named "Convex",

2 - Objects that created from Face Map:  Face Group, it is a convex mesh for first objects.

3 - Objects that doesn't have Face Map:  "Convex", for parts of the object that have no need for a Convex.
