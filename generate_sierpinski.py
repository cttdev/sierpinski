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
