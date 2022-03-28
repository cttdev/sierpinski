## Sierpinski ~~Pyramids~~ (Half-Octahedrons)
Spiral Vase mode is really cool. While a normal 3D print goes layer by layer, completly finishing one before moving on to the next, spiral vase mode lets you constuct a 3D object with a single, continous line that is constantly moving upwards and following the outline of your part.

Usually this feature is used for making vases with thin, continous crossections but we can "repurpose" this feature to print other cool objects.

One such object is the "sierpinski pryamid" that you can find a lot of models for on [Thingiverse](https://www.thingiverse.com/thing:1356547).

While these are called Sierpinski pryamids/tetrahedrons, but they are actually half of an Sierpinski octahedron. The reasoning behind this is that unlinke a Sierpinksi tetrahedron that has discontinous cross-sections, any horixzontial cross section of Sierpinski octahedron is a cloased, continous Sierpiński curve. This means that a Sierpinksi octahedron can be easily printed in sprila vase mode.

We also only want half an octahedron instead of the whole solid so there is a falt base that can rest on the print bed.

The main issue with all of the current models is that the code used to geenrate them is borderline unreadable with random constants and vairable names. So I dieded one afternoon to write a simple python geneator scipt to make my own pryamids that I could make into whatever I wanted.

Currently the easiet way to programacgitally generate 3D models is [OpenSCAD](https://openscad.org) but thankfully there are many wrappers avaliable that can generate openscad code from python. I chose to use [SolidPython](https://github.com/SolidCode/SolidPython) and made a short, **verbose** >:( script to generate the models.
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

Since the recursion is handled during the OpenSCAD code generation, the generated file size gros exponentially with the number of iterations so you shouldn't really generate anything over 6 iterations. However, the method used can realtivelty easily be reworked into prue OpenSCAD code. That is left as an excerise for the reader.

![image](https://user-images.githubusercontent.com/16441759/160354859-0dbb073e-5385-4350-9cb4-e03ad5af2044.png)

After generating some pryamids, I dedcided to make keychains out of them. It was realticlty easy to export the OpenSCAD code as a .cfg file then import it into yet another sketchy CAD software: FreeCAD. There I could add the keychain base and export everything as and STL for printing.

![image](https://user-images.githubusercontent.com/16441759/160355747-7b69ac51-e2c5-46f6-81fa-4283e271f765.png)

The design of the keychain was partially driven by the diemnsions of my RatRig V-Core 3. Since these were printed in sprial vase mode, I had to print each one "indivudally" before moving onto the next. I also wanted to print ~20 and didn't want to manually have to restart the print everytime. So, when the printer finshed one keychain, there had to be enough space so that it could print another one right next to the first without the toolehead hitting anything. THis meant that I could print 9 keychains at a time and they had to be short enough not to hit the printer x gantry.



Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/cttdev/sierpinski/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
