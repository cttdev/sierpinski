## Sierpinski ~~Pyramids~~ (Half-Octahedrons)
How I made Sierpinski "Pryamid" Keychains.

### N-Flake Fractals
A Sierpinski octahedron or octahedron flake has the intresting property that all of its horizontial corss sections are closed, continous [Sierpinkski curves](https://en.wikipedia.org/wiki/Sierpiński_curve).

<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/b/bf/Octaedron_fractal.jpg" alt>
</p>
<p align="center">
    <em>A 3 iteration octahedron flake from Wikipedia.</em>
</p>

This property lets us easily 3D print a model of the flake using a method known as speila vase mode. While a normal 3D print goes layer by layer, completely finishing one before moving on to the next, spiral vase mode lets you construct a 3D object with a single, continuous line that is constantly moving upwards and following the outline of your part.

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/160357191-bde083d0-6133-4613-a5f8-350b79a6e0da.png" alt>
</p>
<p align="center">
    <em>A vase I printed in spiral vase mode.</em>
</p>


Since each cross section of the octahedron falke is a closed loop, we can join them together at arbitary points to represent the surface of the flake with a single line, then print that line with spiral vase mode to construct our fractal.

Typically, only half of an octahedron falke is generated/printed as it gives then model a large face that can be attached to the print bed. 

This method has been implment by numerous people before on [Thingiverse](https://www.thingiverse.com/thing:1356547); however, the  issue with all of the currently avaible models is that the code used to generate them is borderline unreadable with random constants and variable names. So I decided to write a simple python generator script to make my own fractals that I could turn into cool keychains.

Currently, the easiest way to programmatically generate 3D models is [OpenSCAD](https://openscad.org) and there are many wrappers available that can generate OpenSCAD code from python. I chose to use [SolidPython](https://github.com/SolidCode/SolidPython) and made a short, **verbose** script to generate the models.
```python
from solid import *
from solid.utils import *
import math

def calculate_height(size):
    # Returns the height of an equaliterial sqaure pryamid given the size of its base.
    return (1.0 / math.sqrt(2.0)) * size

def generate_pyramid(size, height, solid_model_offset=0.0):
    # Generates a square pryamid of a given size and height with the center of the base at the origin.
    # Solid model offset is a hack to get the pryamid to generate as a single solid model for sprial vase mode printing. It adds a scalar to the size of the pryamid.
    return polyhedron(
        [   
            # Points of a square pryamid.
            [size/2 + solid_model_offset, size/2 + solid_model_offset, 0],
            [-size/2 - solid_model_offset, size/2 + solid_model_offset, 0],
            [-size/2 - solid_model_offset, -size/2 - solid_model_offset, 0],
            [size/2 + solid_model_offset, -size/2 - solid_model_offset, 0],
            [0, 0, height] # Top Point
        ],
        [
            [0, 1, 2, 3], # Bottom face
            [4, 1, 0],
            [4, 2, 1],
            [4, 3, 2],
            [4, 0, 3]
        ]
    )

def sirpinski(iterations, size, solid_model_offset=0.0):
    if iterations == 0:
        return generate_pyramid(size, calculate_height(size + 2 * solid_model_offset), solid_model_offset)

    # Each pryamid is filled with pryamids half of its size.
    size = size/2
    height = calculate_height(size)

    # Setup the translations and rotations.
    translations = [
        translate([size/2, size/2]),
        translate([-size/2, size/2]),
        translate([-size/2, -size/2]),
        translate([size/2, -size/2]),
        translate([0, 0, height]),
        translate([0, 0, height])
    ]

    rotations = [
        rotate([0, 0, 0]),
        rotate([0, 0, 0]),
        rotate([0, 0, 0]),
        rotate([0, 0, 0]),
        rotate([0, 0, 0]),
        rotate([180, 0, 0]) # Flipped pryamid to make the half octahedron.
    ]
        
    # Recursively generate the pryamid.
    pyramids = []
    for i in range(0, len(translations)):
        pyramids.append(
            translations[i](
                rotations[i](
                    sirpinski(iterations-1, size, solid_model_offset)
                )
            )
        )

    return union()(pyramids)

def remove_solid_model_artifacts(model, size):
    # Removes artifacts on the first layer of the model that are a result of the offset applied to the size of the pyramids to get them to generate as a single, solid model.
    # NOTE: This significantly reduces preview performance in openscad so it should only be done on the final model.
    size = 2 * size

    return intersection()(translate([-size/2, -size/2, 0])(cube(size)), model)

def assembly():
    iterations = 4
    size = 40
    solid_model_offset = 0.4

    a = union()
    a = sirpinski(iterations, size, solid_model_offset)
    a = remove_solid_model_artifacts(a, size)

    return a, iterations, size, solid_model_offset


if __name__ == '__main__':
    a, iterations, size, solid_model_offset = assembly()
    scad_render_to_file(a, filepath="sierpinski-{}-{}-{}.scad".format(iterations, size, solid_model_offset), include_orig_code=False)
```

Since the recursion is handled during the OpenSCAD code generation, the generated file size grows exponentially with the number of iterations so you shouldn't really generate anything over 6 iterations with this code. However, the method used can realtivelty easily be reworked into prue OpenSCAD code to get around the file size limitations.

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/160354859-0dbb073e-5385-4350-9cb4-e03ad5af2044.png" alt>
</p>
<p align="center">
    <em>A 4 recursion pryamid I generated.</em>
</p>

### Printability
One part of the code that I have ignore up unitl now is the `solid_model_offset`, which is what allows these generated pryamids to be printable. Without the offset, each "pryamid" created by the resuion is treated as a seperate body, only joined to another at a single pont. While this is the geometrically accurate represneation of the octahedron flake, inforder for the model to be printable, it must be a single solid body. Thus, the offset appleies a scalr to the base of each indivual pryamid (scaling the heights accorsdingly to make the pryamids equaliterial) that results in the pryamids intresting each other in the model. In my models, this offset was set to the nozzle/line width (0.4mm).

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/160552714-5573e15d-0d6a-4bb1-ad54-bab7c27b65c7.png" alt>
</p>
<p align="center">
    <em>A 4 recursion pryamid without the solid model offset.</em>
</p>


### Keychains
While I could have also programtically generated the keychain base in OpenSCAD, it was much easier to expoert the geometry of the prysamid and add the base in parametic CAd software. The only issue with this approach was that OpenSCAD only lets you export the native geometry as a .csg file which only FreeCAD supports, and I had no idea how to use FreeCAD.

After messing around with FreeCAD's horrible sketching interface for an hour, I made the base of the pryamid and was able to combine that with the raw OpenSCAD geometry.

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/160355747-7b69ac51-e2c5-46f6-81fa-4283e271f765.png" alt>
</p>
<p align="center">
    <em>Finihsed model in FreeCAD</em>
</p>


The design of the keychain was partially driven by the diemnsions of my 3D printer. Since the pryamids were printed in sprial vase mode, I had to print each one "indivudally" before moving onto the next. Since I had to make ~20 keychains, I didn't want to have to resart the print every time.

To get around this, I could take advantage of the 400mm^2 bed of the RatRig V-Core 3 and print multiple pryamids, side by side. The only caviat with this method is that each pryamid had to be far enough from the others that the print head could mode around it without hitting completed pryamids and the pryamids had to be shorter than the x gantry so it could pass over them.

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/160554253-99451645-cdfe-43f1-b21b-5dee57bf2e93.png" alt>
</p>
<p align="center">
    <em>A view of the printhead clerance regions in Prusaslicer. I could do a maximum of 9 at a time.</em>
</p>

Each keychain was printed at 200 mm/s with 4500 mm/s^2 acceleration which is realtively conservaite for the V-Core 3 but I wanted to be sure that the small features came out well.

### MIT Logo
Wanting to make the keychains more detailed, I decided to embosss a MIT logo into the first layer. This was realtively easy as I found an SVG that I converted to a DXF with Inkscape.

![image](https://user-images.githubusercontent.com/16441759/160555154-39bd8523-71a0-46be-8254-fae2531be101.png)

Used the DXF to extrude a solid the height of the first layer in Onshape.

Mirrored the logo to get it to show up the right way on the bottom of the object.

And finally, exported the Onshape bodies as an STL and used that as a negative volume on the pyramid in Prusaslicer.
![image](https://user-images.githubusercontent.com/16441759/160556087-50c67a2f-8f4c-4d38-b161-31568281fe9d.png)

