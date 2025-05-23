#!/usr/bin/env python3

# Copyright (c) 2021-2024 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
#

# Thes are CadQuery 3D-models of the top parts holding the coax-test-connector  
# for all Nordic's  DK's 
# 
# The position of the antenna's test connector is different dependent on the DK.
# Each top-part get's marked with the DK-information it supports 


import cadquery as cq

coax_top_with = 20
coax_top_length = 64
coax_top_thick = 2

# Start with the base plate
result = (
    cq.Workplane('front')
    .box(coax_top_length, coax_top_with, coax_top_thick)
    .faces("|Z").edges("+X or -X").fillet(0.9) 
    )

# Add the side nodges
coax_nodge_pts = [
(0,-6),
(coax_top_thick, -4),
(coax_top_thick, +4),
(0, +6)
]
coax_nodge = cq.Workplane('ZY')  # .moveTo(0.0)
coax_nodge = coax_nodge.polyline(coax_nodge_pts).close()
coax_nodge = coax_nodge.extrude(coax_top_thick)
coax_nodge = coax_nodge.translate([(coax_top_length/2 +coax_top_thick),0,-(coax_top_thick/2)])

coax_nodges = coax_nodge.union(coax_nodge.mirror((1, 0, 0), (0, 0, 0)))
result = result.union(coax_nodges).translate([coax_top_length/2,coax_top_with/2, 0 ])

# Add the coax support block

center_hole_x = 38 # was
center_hole_y = 7   # was
center_hole_x_52840 = 38.5
center_hole_y_52840 = 7
center_hole_x_52811 = 32
center_hole_y_52811 = 8
center_hole_x_54L15 = 36.5
center_hole_y_54L15 = 7
center_hole_x_54H20 = 29.5
center_hole_y_54H20 = 8
center_hole_x_54LM20a = 33.5
center_hole_y_54LM20a = 9
small_hole_radius = 3
big_hole_radius = 3.9
cable_slot_with = 4.6
support_with = 12
support_lenght = 20
support_hight = 3.7

support_block = (cq.Workplane('front').box(support_lenght, support_with, support_hight))
support_block = support_block.faces(">Z").fillet(1)
support_block = support_block.circle(big_hole_radius).cutThruAll()
support_block = support_block.faces(">Z").workplane().rect(support_lenght,cable_slot_with).cutThruAll()

# Do the final 52840 (52833 and 5340) steps
support_52840 = support_block.translate([center_hole_x_52840,center_hole_y_52840,(support_hight/2 +coax_top_thick/2)])
result_52840 = result.union(support_52840)
result_52840 = result_52840.faces(">Z").pushPoints([(center_hole_x_52840, center_hole_y_52840)]).circle(small_hole_radius).cutThruAll()
# Add text for identification of supported DK's
result_52840 = result_52840.union(cq.Workplane('front').text("52840/33\n5340",6,0.4).translate([coax_top_length/5,10, coax_top_thick/2]))
result_52840 = result_52840.translate([0,25,0]) # move to own place away from the other ones for show_objet()
show_object(result_52840)
cq.exporters.export(result_52840, "./step/52840_33_5340_coax_top.step")
cq.exporters.export(result_52840, "./stl/52840_33_5340_coax_top.stl")

# Do the final 54L15 steps
support_54L15 = support_block.translate([center_hole_x_54L15,center_hole_y_54L15,(support_hight/2 +coax_top_thick/2)])
result_54L15 = result.union(support_54L15)
result_54L15 = result_54L15.faces(">Z").pushPoints([(center_hole_x_54L15, center_hole_y_54L15)]).circle(small_hole_radius).cutThruAll()
# Add text for identification of supported DK's
result_54L15 = result_54L15.union(cq.Workplane('front').text("54L15",6,0.4).translate([coax_top_length/5,10, coax_top_thick/2]))
result_54L15 = result_54L15.translate([0,50,0]) # move to own place away from the other ones for show_objet()
show_object(result_54L15)
cq.exporters.export(result_54L15, "./step/54L15_coax_top.step")
cq.exporters.export(result_54L15, "./stl/54L15_coax_top.stl")

# Do the final 54H20 steps
support_54H20 = support_block.translate([center_hole_x_54H20,center_hole_y_54H20,(support_hight/2 +coax_top_thick/2)])
result_54H20 = result.union(support_54H20)
result_54H20 = result_54H20.faces(">Z").pushPoints([(center_hole_x_54H20, center_hole_y_54H20)]).circle(small_hole_radius).cutThruAll()
# Add text for identification of supported DK's
result_54H20 = result_54H20.union(cq.Workplane('front').text("54H20",6,0.4).translate([5*coax_top_length/6,10, coax_top_thick/2]))
result_54H20 = result_54H20.translate([0,75,0]) # move to own place away from the other ones for show_objet()
show_object(result_54H20)
cq.exporters.export(result_54H20, "./step/54H20_coax_top.step")
cq.exporters.export(result_54H20, "./stl/54H20_coax_top.stl")

# Do the final 52811 (52810, 52820 and 52832)steps
support_52811 = support_block.translate([center_hole_x_52811,center_hole_y_52811,(support_hight/2 +coax_top_thick/2)])
result_52811 = result.union(support_52811)
result_52811 = result_52811.faces(">Z").pushPoints([(center_hole_x_52811, center_hole_y_52811)]).circle(small_hole_radius).cutThruAll()
# Add text for identification of supported DK's
result_52811 = result_52811.union(cq.Workplane('front').text(" 52810\n11/20/32",5.5,0.4).translate([coax_top_length/6,10, coax_top_thick/2]))
result_52811 = result_52811.translate([0,100,0]) # move to own place away from the other ones for show_objet()
show_object(result_52811)
cq.exporters.export(result_52811, "./step/52810_11_20_32_coax_top.step")
cq.exporters.export(result_52811, "./stl/52810_11_20_32_coax_top.stl")

# Do the final 54LM20a steps
support_54LM20a = support_block.translate([center_hole_x_54LM20a,center_hole_y_54LM20a,(support_hight/2 +coax_top_thick/2)])
result_54LM20a = result.union(support_54LM20a)
result_54LM20a = result_54LM20a.faces(">Z").pushPoints([(center_hole_x_54LM20a, center_hole_y_54LM20a)]).circle(small_hole_radius).cutThruAll()
# Add text for identification of supported DK's
result_54LM20a = result_54LM20a.union(cq.Workplane('front').text("54LM20",5.5,0.4).translate([5*coax_top_length/6,10, coax_top_thick/2]))
result_54LM20a = result_54LM20a.translate([0,125,0]) # move to own place away from the other ones for show_objet()
show_object(result_54LM20a)
cq.exporters.export(result_54LM20a, "./step/54LM20a_coax_top.step")
cq.exporters.export(result_54LM20a, "./stl/54LM20a_coax_top.stl")

