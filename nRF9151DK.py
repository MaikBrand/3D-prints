#!/usr/bin/env python3

# Copyright (c) 2021-2024 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
#

# This is a CadQuery 3D-model of  slide-in clip-on plate's  
# for Nordic's nRF9151 Development Kit (nRF9151DK). 
# 

import cadquery as cq


pad_thick = 1.85
pad_x = 64
pad_y = 80
pad_y_antenna = 3  # cover the antenna

# Draw the base plate
result = (
    cq.Workplane('front')
    .box(pad_x, pad_y + pad_y_antenna, pad_thick)
    .translate([pad_x/2, (pad_y - pad_y_antenna)/2, pad_thick/2])
    )

# Position of the studs going into holes of the DK
stud_points = [(7.6, 37.7+20.78),
               (56, 44.2+20.78)]
stud_diam = 3.0

stud = cq.Workplane('front').workplane(offset=pad_thick)
stud = stud.pushPoints(stud_points)
stud = stud.circle(stud_diam/2).extrude(2)
stud = stud.workplane(offset=1.4)
stud = stud.pushPoints(stud_points)
stud = stud.sphere(stud_diam/2 + 0.15)
stud = stud.workplane(offset=-2.2)
stud = stud.pushPoints(stud_points)
stud = stud.circle(stud_diam/2 + 1).extrude(0.4)

result = result.union(stud)

# Add the side rails
rail_x = 7
rail_y = 60
rail_z = pad_thick

rail = cq.Workplane('front').box(rail_x, rail_y, rail_z)
rail = rail.edges("|Y and <X").fillet(.7)
rail = rail.translate([-rail_x/2, rail_y/2 - pad_y_antenna, rail_z/2])
rails = rail.union(rail.mirror((1, 0, 0), (pad_x/2, 0, 0)))

result = result.union(rails)

# Add the grove to slot the DK in
a = (cq.Workplane('front').box(6, 3, 2).translate([3, -1.5, pad_thick +1 ]))
b = (cq.Workplane('front').box(2, 6, 2).translate([-1, 0, pad_thick +1 ]))
c = (cq.Workplane('front').box(3, 6, 2).translate([-0.5, 0, pad_thick +3 ]))
grove = a.union(b)
grove = grove.union(c)
grove = grove.edges("|Z and <X and <Y" ).fillet(4)
groves = grove.union(grove.mirror((1, 0, 0), (pad_x/2, 0, 3)))

result = result.union(groves)

# Add slots in the middle to remove material
slot_w = 8
slot_l = 40
slot_spacing = slot_w * 2
nslots = 5

plane = result.workplane(centerOption='ProjectedOrigin', origin=(pad_x/2, pad_y/2 + 1, 0))
slots = plane.rarray(1, slot_spacing, 1, nslots).slot2D(slot_l, slot_w, 0)

# Add even more slots on the side to remove material
slot_w = 8
slot_l = 40
slot_spacing = 55
nslots = 2

plane = result.workplane(centerOption='ProjectedOrigin',origin=(pad_x/2, pad_y/2 - 5, 0))
result = plane.rarray(slot_spacing, 1, nslots, 1).slot2D(slot_l, slot_w, 90)

result = result.cutThruAll()

# Add text for identification of supported DK's
result_A = result.union(cq.Workplane('front').text("nRF9151DK v1.0.0",4.5,0.1).translate([pad_x/2,17, pad_thick]))

show_object(result_A)

# Export first design as file formats used by 3D printers
cq.exporters.export(result_A, "./step/nrf9151dk_clip.step")
cq.exporters.export(result_A, "./stl/nrf9151dk_clip.stl")
