#!/usr/bin/env python3

# Copyright (c) 2021-2024 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
#

# This is a CadQuery 3D-model of a rail-rig to hold a defined number 
# of Nordic's DK's with a mounted slide-in-plate
# 
import cadquery as cq

print_tol = 0.075 #was .2

num_DKs_in_rig = 12

# Taken from the a *_clip.py file
wing_x = 7
pad_z = (2.15)  # added 0.15 to get a better slide-in
pad_x = 64
pad_y = 53

rail_sidewall_thick = 2
rail_tolerance = 0.5            # Extra padding between the slot edge and the rail
pcb_tolerance = 2               # Distance from the rail to the main PCB pad
rail_x = wing_x + rail_sidewall_thick + rail_tolerance - pcb_tolerance
rail_y = rail_sidewall_thick * 2 + pad_z
rail_z = 35
dk_clearance = 15

# Draw the base pad
base_z = 2
base_x = wing_x * 2 + pad_x + (2 * rail_sidewall_thick) + (rail_tolerance * 2)
result = cq.Workplane('front').box(base_x, dk_clearance, base_z).translate([0, 0, -base_z/2])

# Add a support to make the base more stiff
support = cq.Workplane('front').box(base_x - 2*rail_x, 2, 2).translate([0,dk_clearance/2 -1, 1])
support = support.faces(">Z").fillet(0.8)
result = result.union(support)


# Draw one rail with guide
# rail_x, rail_y, rail_z
lower_pts = [
    (-rail_x/2, -rail_y/2),
    (-rail_x/2, rail_y/2),
    (rail_x/2, rail_y/2),
    (rail_x/2, rail_y/2 - rail_sidewall_thick ),
    (-rail_x/2 + rail_sidewall_thick, rail_y/2 - rail_sidewall_thick ),
    (-rail_x/2 + rail_sidewall_thick, -rail_y/2 + rail_sidewall_thick),
    (rail_x/2, -rail_y/2 + rail_sidewall_thick),
    (rail_x/2, -rail_y/2),
]
upper_pts = [
    (-rail_x/2 -3, -rail_y/2 -3),
    (-rail_x/2 -3, rail_y/2 +3),
    (rail_x/2, rail_y/2 +3),
    (rail_x/2, rail_y/2 +3 - rail_sidewall_thick),
    (-rail_x/2 -3 + rail_sidewall_thick, rail_y/2 +3 - rail_sidewall_thick),
    (-rail_x/2 -3 + rail_sidewall_thick, -rail_y/2 -3 + rail_sidewall_thick),
    (rail_x/2, -rail_y/2 -3 + rail_sidewall_thick),
    (rail_x/2, -rail_y/2 -3),
]

rail = cq.Workplane("front").polyline(lower_pts).close()
rail = rail.extrude(rail_z)
rail = rail.workplane(offset = rail_z/2)
rail = rail.polyline(lower_pts).close()
rail = rail.workplane(offset=4.0)
rail = rail.polyline(upper_pts).close()
rail = rail.loft(combine=True)
rail = rail.faces("+Z").edges().fillet(0.75)

# Add corners on the lower parts of the rail's for stability
corner = cq.Workplane("YZ").polyline([(-rail_y/2, 0),
                                      (-rail_y/2 -3, 0),
                                      (-rail_y/2, 3),
                                      ]).close()
corner = corner.extrude(rail_x)
corner = corner.translate([-rail_x/2, 0, 0])
corners = corner.union(corner.mirror((0, 1, 0), (0, 0, 0)))

rail = rail.union(corners)

# Move the rail to the edge and duplicate it by mirrowing to the other edge
rail = rail.translate([rail_x/2, 0, 0])  # Place leftmost edge at origin
rail = rail.translate([-base_x/2, 0, 0]) # Move side edge to leftmost of base
rails = rail.union(rail.mirror((1, 0, 0), (0, 0, 0))) # Mirror to rightmost edge of base

result = result.union(rails)

# Duplicate until wished rig-size
obj = result
for n in range(num_DKs_in_rig):
    result = result.union(obj.translate([0, dk_clearance * n, 0]))

# Add clips for chaining rail-rig's 
port_offset = 15
d = 2
port_pts = [(d, 0),
            (d, d),
            (2*d, 2*d),
            (2*d, 3*d),
            (-2*d, 3*d),
            (-2*d, 2*d),
            (-d, d),
       (-d, 0)]
port_a = cq.Workplane('front').polyline(port_pts).close().extrude(-base_z)
port_a = port_a.translate([-port_offset/2, 0, 0])
port_ab = port_a.union(port_a.mirror((1, 0, 0), (0, 0, 0)))
port_ab = port_ab.translate([-port_offset, num_DKs_in_rig*dk_clearance - dk_clearance/2, 0])
port_abcd = port_ab.union(port_ab.mirror((1, 0, 0), (0, 0, 0)))

result = result.union(port_abcd)

def inc(val, inc, center):
    if val > center:
        val += inc
    else:
        val -= inc
    return val

def scale(point, factor):
    x, y = point
    x = inc(x, factor, d/2)
    y = inc(y, factor, 2*d)
    return (x, y)

port_pts_pad = [scale(pt, print_tol) for pt in port_pts]

port_hole_a = (cq.Workplane('front').
        polyline(port_pts_pad).close()
        .extrude(-(base_z + 2))
        .translate([0, -.1, 2]))


port_hole_a = port_hole_a.translate([-port_offset/2, 0, 0])
port_hole_ab = port_hole_a.union(port_hole_a.mirror((1, 0, 0), (0, 0, 0)))

port_hole_ab = port_hole_ab.translate([-port_offset, dk_clearance/2, 0])
port_hole_abcd = port_hole_ab.union(cq.Workplane('front').box(base_x - 2*rail_x, 2, 2).translate([0,dk_clearance/2 -1, 1]))

port_hole_abcd = port_hole_ab.union(port_hole_ab.mirror((1, 0, 0), (0, 0, 0)))

# Add support-bar 
support2 = cq.Workplane('front').box(base_x - 2*rail_x, 2, 2).translate([0,-dk_clearance/2 +1, 1])
support2 = support2.faces(">Z").fillet(0.8)
result = result.union(support2)

result = result.cut(port_hole_abcd.translate([0, -dk_clearance, 0]))

show_object(result)

# Export printer files
cq.exporters.export(result, "./step/12x_dk_rails.step")
cq.exporters.export(result, "./stl/12x_dk_rails.stl")
