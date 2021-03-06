## Sierpinski ~~Pyramids~~ (Half-Octahedron Flakes)
How I made Sierpinski "Pyramid" Keychains.

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/161213672-231cce4c-bea6-4edd-a4b0-b957410ad1a6.png" alt>
</p>
<p align="center">
    <em>A "pyramid."</em>
</p>

<br>

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/161213695-07ffa7c9-1215-4d3a-990f-35feb0f1c2f9.png" alt>
</p>
<p align="center">
    <em>Printing the fractals.</em>
</p>

<br>

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/160936312-2ce663da-6c52-411b-9e8c-36d12c96c889.png" alt>
</p>
<p align="center">
    <em>All 21 pyramids.</em>
</p>

### N-Flake Fractals
A Sierpinski octahedron or octahedron flake has the interesting property that all of its horizontal cross sections are closed, continuous [Sierpinkski curves](https://en.wikipedia.org/wiki/Sierpiński_curve).

<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/b/bf/Octaedron_fractal.jpg" alt>
</p>
<p align="center">
    <em>A 3 iteration octahedron flake from Wikipedia.</em>
</p>

This property lets us easily 3D print a model of the flake using spiral vase mode. While a normal 3D print goes layer by layer, completely finishing one before moving on to the next, spiral vase mode lets you construct a 3D object with a single, continuous line that is constantly moving upwards and following the outline of your part.

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/160357191-bde083d0-6133-4613-a5f8-350b79a6e0da.png" alt>
</p>
<p align="center">
    <em>A vase I printed in spiral vase mode.</em>
</p>


Since each cross section of the octahedron flake is a closed loop, we can join them together at arbitrary points to represent the surface of the flake with a single line, then print that line with spiral vase mode to construct our fractal.

Typically, only half of an octahedron flake is generated/printed as it gives then model a large face that can be attached to the print bed. 

This method has been implemented by numerous people before on [Thingiverse](https://www.thingiverse.com/thing:1356547); however, the issue with all of the currently available models is that the code used to generate them is borderline unreadable with random constants and variable names. So I decided to write a simple python generator script to make my own fractals that I could turn into cool keychains.

Currently, the easiest way to programmatically generate 3D models is [OpenSCAD](https://openscad.org) and there are many wrappers available that can generate OpenSCAD code from python. I chose to use [SolidPython](https://github.com/SolidCode/SolidPython) and made a short, **verbose** script to generate the models.
```python
from solid import *
from solid.utils import *
import math

def calculate_height(size):
    # Returns the height of an equaliterial sqaure pyramid given the size of its base.
    return (1.0 / math.sqrt(2.0)) * size

def generate_pyramid(size, height, solid_model_offset=0.0):
    # Generates a square pyramid of a given size and height with the center of the base at the origin.
    # Solid model offset is a hack to get the pyramid to generate as a single solid model for sprial vase mode printing. It adds a scalar to the size of the pyramid.
    return polyhedron(
        [   
            # Points of a square pyramid.
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

def sierpinski(iterations, size, solid_model_offset=0.0):
    if iterations == 0:
        return generate_pyramid(size, calculate_height(size + 2 * solid_model_offset), solid_model_offset)

    # Each pyramid is filled with pyramids half of its size.
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
        rotate([180, 0, 0]) # Flipped pyramid to make the half octahedron.
    ]
        
    # Recursively generate the pyramid.
    pyramids = []
    for i in range(0, len(translations)):
        pyramids.append(
            translations[i](
                rotations[i](
                    sierpinski(iterations-1, size, solid_model_offset)
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
    a = sierpinski(iterations, size, solid_model_offset)
    a = remove_solid_model_artifacts(a, size)

    return a, iterations, size, solid_model_offset


if __name__ == '__main__':
    a, iterations, size, solid_model_offset = assembly()
    scad_render_to_file(a, filepath="sierpinski-{}-{}-{}.scad".format(iterations, size, solid_model_offset), include_orig_code=False)
```

Since the recursion is handled during the OpenSCAD code generation, the generated file size grows exponentially with the number of iterations so you shouldn't really generate anything over 6 iterations with this code. However, the method used can be easily reworked into pure OpenSCAD code to get around the file size limitations. This is left as an excerise for the reader.

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/160354859-0dbb073e-5385-4350-9cb4-e03ad5af2044.png" alt>
</p>
<p align="center">
    <em>A 4 recursion pyramid.</em>
</p>

### Printability
One of the most important parts of the code is the `solid_model_offset`, which is what allows the generated pyramids to be printable. Without the offset, each small pyramid created by the recursion is treated as a separate body, only "touching" other pryamids at single point. While this is the geometrically accurate representation of the octahedron flake, in order for the model to be printable, it must be a single solid body. Thus, the offset applies a scalar to the base of each individual pyramid (scaling the heights accordingly to make the pyramids equilateral) that results in the pyramids intersecting each other, creating a solid model. In my models, this offset was set to the nozzle/line width (0.4mm).

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/160552714-5573e15d-0d6a-4bb1-ad54-bab7c27b65c7.png" alt>
</p>
<p align="center">
    <em>A 4 recursion pyramid without the solid model offset.</em>
</p>


### Keychains
While I could have also programmatically generated the keychain base in OpenSCAD, it was much easier to export the geometry of the pyramid and add the base in a parametric CAD software. The only issue with this approach was that OpenSCAD only lets you export the native geometry as a .csg file which is only supported by FreeCAD, and FreeCAD is a pain to use.

After messing around with FreeCAD's horrible sketching interface for an hour, I made the base of the pyramid and was able to combine that with the raw OpenSCAD geometry.

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/160355747-7b69ac51-e2c5-46f6-81fa-4283e271f765.png" alt>
</p>
<p align="center">
    <em>Finished model in FreeCAD.</em>
</p>

The design of the keychain was partially driven by the dimensions of my 3D printer. Since the pyramids were printed in spiral vase mode, I had to print each one "individually" before moving onto the next. Since I had to make ~20 keychains, I didn't want to have to restart the print every time.

To get around this, I could take advantage of the 400mm^2 bed of the RatRig V-Core 3 and print multiple pyramids, side by side. The only caveat with this method is that each pyramid had to be far enough from the others that the print head could mode around it without hitting completed pyramids and the pyramids had to be shorter than the x gantry so it could pass over them.

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/160666341-fbcee9dc-893d-411b-b3ab-d23329761b7c.png" alt>
</p>
<p align="center">
    <em>A view of the printhead clearance regions in Prusaslicer. I could print a maximum of 9 at a time.</em>
</p>

<br>

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/160667228-e6b3fa9c-bea0-4ca9-8cf9-3d885b92294d.png" alt>
</p>
<p align="center">
    <em>A gcode preview of the models being printed one at a time.</em>
</p>

<br>

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/161407442-b77368b3-5200-45c0-add3-281f3fcb1297.png" alt>
</p>
<p align="center">
    <em>The pyramids fit under the printer x gantry.</em>
</p>

Each keychain was printed at 200 mm/s with 4500 mm/s^2 acceleration which is relatively conservative for the V-Core 3 but I wanted to be sure that the small features came out well.

### MIT Logo
To make the keychains more personalized, I decided to emboss a MIT logo into the first layer. This was relatively easy as I found an SVG that I converted to a DXF with Inkscape.

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/160555154-39bd8523-71a0-46be-8254-fae2531be101.png" alt>
</p>
<p align="center">
    <em>The MIT logo in Inkscape.</em>
</p>

Then used the DXF to extrude a solid the height of the first layer (0.2mm) in Onshape and mirrored the logo to get it to show up the right way on the bottom of the object.

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/161372897-3e9d9322-2070-4013-aa26-1b4004a0ca0c.png" alt>
</p>
<p align="center">
    <em>The mirrored MIT logo bodies in Onshape.</em>
</p>


And finally, exported the Onshape bodies as an STL and used that as a negative volume on the pyramid in Prusaslicer.
<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/160666612-2f55e5c9-9078-4494-b30b-924b3ddf316a.png" alt>
</p>
<p align="center">
    <em>The MIT logo on the bottom layer of the model.</em>
</p>


### Printing 🎉
Printing the "pyramids" went relatively smoothly thanks to the checks and preparation of the model beforehand. Initially, I was printing the first layer too fast so the MIT logo lost some detail but after slowing it down, it showed up really well.

<p align="center">
    <img src="https://i.imgur.com/LLkTUQY.gif" alt>
</p>
<p align="center">
    <em>A view of the Sierpinski curves in each cross-section of the fractal.</em>
</p>

<br>

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/161213530-a5dd2907-b0b1-4358-90e8-7a42c1ce78d6.png" alt>
</p>
<p align="center">
    <em>MIT Logo.</em>
</p>

Here are some videos of printing everything on the RatRig V-Core 3 I built:

<iframe width="560" height="315" src="https://www.youtube.com/embed/EMgGIIW_hDI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<iframe width="560" height="315" src="https://www.youtube.com/embed/ogvxI96tBlE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<iframe width="560" height="315" src="https://www.youtube.com/embed/cC4vore8kck" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

I also uploaded both a STL of the model and a 3MF Prusaslicer file to the Github repository if you want to print your own. Just be sure you print the model in spiral vase mode and with 8 bottom layers at 0.2mm layer height (so the keychain base is printed solid as it is 1.6mm thick).

<p align="center">
    <img src="https://user-images.githubusercontent.com/16441759/161406897-1d469662-ddb6-4c19-9eb0-66e620c03296.png" alt>
</p>
<p align="center">
    <em>The print settings I used.</em>
</p>

Overall, I really enjoyed this project and was pretty happy with the end result. There are definitely ways I want to improve the code in the future, like fixing issues with some of the layer geometries, but for this specific use case the script worked very well.
