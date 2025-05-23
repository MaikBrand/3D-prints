#!/usr/bin/env python3

# Copyright (c) 2021-2024 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
#

# This is a CadQuery 3D-model of a slide-in clip-on plate's  
# for Nordic's 52810/52811/52820/52832 DK's 
# 
# 3 different models will be exported:
#   - without coax-cable support
#   - with support for Maruta-coax-test-connector (see Readme-file)
#   - with support for MS156-coax-test-connector (see Readme-file)
# 
# The additional needed coax-support-top is identical for both test-connectors
# and the 3D-model is defined in file coax_tops.py 

import cadquery as cq


pad_thick = 1.85
pad_x = 64
pad_y = 75
pad_y_antenna = 3  # cover the antenna

# Start with the base plate
result = (
    cq.Workplane('front')
    .box(pad_x, pad_y + pad_y_antenna, pad_thick)
    .translate([pad_x/2, (pad_y - pad_y_antenna)/2, pad_thick/2])
    )

# Position of the studs going into holes of the DK
stud_points = [(13.5, 69 ),
               (41.5, 69)]
stud_diam = 3.0

stud = cq.Workplane('front').workplane(offset=pad_thick)
stud = stud.pushPoints(stud_points)
stud = stud.circle(stud_diam/2).extrude(2)
stud = stud.workplane(offset=1.4)
stud = stud.pushPoints(stud_points)
stud = stud.sphere(stud_diam/2 + 0.15)
stud = stud.workplane(offset=-2.2)
stud = stud.pushPoints(stud_points)
stud = stud.circle(stud_diam/2 + 1).extrude(0.5)

result = result.union(stud)

# Add the side rails
rail_x = 7
rail_y = 45
rail_z = pad_thick

rail = cq.Workplane('front').box(rail_x, rail_y, rail_z)
rail = rail.edges("|Y and <X").fillet(.7)
rail = rail.translate([-rail_x/2, rail_y/2 - pad_y_antenna, rail_z/2])
rails = rail.union(rail.mirror((1, 0, 0), (pad_x/2, 0, 0)))

result = result.union(rails)

# Add the grove to slot the DK in
a = (cq.Workplane('front').box(6, 3, 2).translate([3, -1.5, pad_thick +1 ]))
b = (cq.Workplane('front').box(2, 6, 2).translate([-1, 0, pad_thick +1 ]))
c = (cq.Workplane('front').box(8, 6, 2).translate([2, 0, pad_thick +3 ]))
grove_left = a.union(b)
grove_left = grove_left.union(c)
grove_left = grove_left.edges("|Z and <X and <Y" ).fillet(4)
grove_right = grove_left.mirror((1, 0, 0), (pad_x/2, 0, 0))
groves = grove_left.union(grove_right).translate([0, 35,0])

result = result.union(groves)

# Add slots in the middle to remove material
slot_w = 8
slot_l = 36
slot_spacing = slot_w * 2
nslots = 4

plane = result.workplane(centerOption='ProjectedOrigin', origin=(pad_x/2, pad_y/2 -5, 0))
slots = plane.rarray(1, slot_spacing, 1, nslots).slot2D(slot_l, slot_w, 0)

# Add even more slots on the side above the groves to remove material
slot_w = 6
slot_l = 25
slot_spacing = 50
nslots = 2

plane = result.workplane(centerOption='ProjectedOrigin',origin=(pad_x/2, pad_y/2 +15, 0))
result = plane.rarray(slot_spacing, 1, nslots, 1).slot2D(slot_l, slot_w, 90)

result = result.cutThruAll()

# Add even more slots on the side below the groves to remove material
slot_w = 6
slot_l = 25
slot_spacing = 50
nslots = 2

plane = result.workplane(centerOption='ProjectedOrigin',origin=(pad_x/2, +17, 0))
result = plane.rarray(slot_spacing, 1, nslots, 1).slot2D(slot_l, slot_w, 90)

result = result.cutThruAll()

# Add text for identification of supported DK's
result_A = result.union(cq.Workplane('front').text("52810/11/20/32-DK",6,0.4 , kind="bold").translate([pad_x/2,0, pad_thick]))

show_object(result_A)

# Export first design as file formats used by 3D printers
cq.exporters.export(result_A, "./step/52810_11_20_32-DK_clip.step")
cq.exporters.export(result_A, "./stl/52810_11_20_32-DK_clip.stl")

# Re-use the first design to make a second design with Murata-coax-cable support
# Add Sides for holder of coax-antenna-cable support
coax_side_thick = 2
coax_side_with = 20
coax_side_hight = 14.5

coax_side_pts = [
    (0,0),
    (coax_side_hight,0),
    (coax_side_hight,6),
    (coax_side_hight-2,4),
    (coax_side_hight-2,coax_side_with-4),
    (coax_side_hight,coax_side_with-6),
    (coax_side_hight,coax_side_with),
    (0,coax_side_with)
]

coax_support_side = cq.Workplane('ZY').moveTo(0.0)
coax_support_side = coax_support_side.polyline(coax_side_pts).close()
coax_support_side = coax_support_side.extrude(coax_side_thick)
coax_support_side = coax_support_side.translate([0,35,0])
coax_supports_sides = coax_support_side.union(coax_support_side.mirror((1, 0, 0), (pad_x/2, 0, 0)))
result_Murata = result.union(coax_supports_sides)

# Add text for identification of supported DK's
result_Murata = result_Murata.union(cq.Workplane('front').text("52810_11_20_32-Murata",6,0.4 , kind="bold").translate([pad_x/2,0, pad_thick]))

# Move the second part to a bit so the parts are shown apart of each other
result_Murata = result_Murata.translate([0,1.5*pad_y,0])

show_object(result_Murata)

# Export second design as file formats used by 3D printers
cq.exporters.export(result_Murata, "./step/52810_11_20_32-DK_Murata_coax_clip.step")
cq.exporters.export(result_Murata, "./stl/52810_11_20_32-DK_Murata_coax_clip.stl")

# Re-use the first design to make a third design with MS156-coax-cable support
# Add Sides for holder of coax-antenna-cable support
coax_side_thick = 2
coax_side_with = 20
coax_side_hight = 19.5

coax_side_pts = [
    (0,0),
    (coax_side_hight,0),
    (coax_side_hight,6),
    (coax_side_hight-2,4),
    (coax_side_hight-2,coax_side_with-4),
    (coax_side_hight,coax_side_with-6),
    (coax_side_hight,coax_side_with),
    (0,coax_side_with)
]

coax_support_side = cq.Workplane('ZY').moveTo(0.0)
coax_support_side = coax_support_side.polyline(coax_side_pts).close()
coax_support_side = coax_support_side.extrude(coax_side_thick)
coax_support_side = coax_support_side.translate([0,35,0])
coax_supports_sides = coax_support_side.union(coax_support_side.mirror((1, 0, 0), (pad_x/2, 0, 0)))
result_MS156 = result.union(coax_supports_sides)

# Add text for identification of supported DK's
result_MS156 = result_MS156.union(cq.Workplane('front').text("52810_11_20_32-MS156",6,0.4 , kind="bold").translate([pad_x/2,0, pad_thick]))

# Move the third part a bit so the parts are shown apart of each other
result_MS156 = result_MS156.translate([0,3*pad_y,0])

show_object(result_MS156)

# Export third design as file formats used by 3D printers
cq.exporters.export(result_MS156, "./step/52810_11_20_32-MS156_coax_clip.step")
cq.exporters.export(result_MS156, "./stl/52810_11_20_32-MS156_coax_clip.stl")
