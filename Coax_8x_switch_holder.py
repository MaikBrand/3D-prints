#!/usr/bin/env python3

# holder for the 8 port coax switch fitting to a rail-rig


import cadquery as cq

print_tol = 0.02 #was .2
distance_between_DKs = 15 #from DK_rails.py
hub_length = 190
width = 33
hight = 125
wall_thickness = 2


top =    (cq.Workplane('front').box(hub_length, wall_thickness,width)) #.translate([0, hight/2, hub_with/2]))
top = top.translate([0, hight/2, width/2])
bottom = (cq.Workplane('front').box(hub_length, wall_thickness,width).translate([0, -hight/2, width/2]))
results = top.union(bottom)

lower_pts = [
    (-1, 0),
    (-1, 39),
    (1, 39),
    (1, 0)
]
mid_pts = [
    (-1.5, 0),
    (-8.5, 3),
    (-8.5, 35),
    (-4.5, 35),
    (-1.5, 39),
    (1.5, 39),
    (4.5, 35),
    (8.5, 35),
    (8.5, 3),
    (1.5, 0),
]

upper_pts = [
    (-1.5, 0),
    (-4.5, 3),
    (-4.5, 35),
    (-1.5, 39),
    (1.5, 39),
    (4.5, 35),
    (4.5, 3),
    (1.5, 0),
]

spacer = (cq.Workplane("front").box(wall_thickness, (hight + wall_thickness), width).translate([-distance_between_DKs*2, 0, (width/2)]))
spacer_support =  (cq.Workplane("front").box(5*wall_thickness, hight + wall_thickness, wall_thickness))        
spacer_support = spacer_support.translate([-distance_between_DKs*2, 0,wall_thickness/2 ])

spacer = spacer.add(spacer_support)

connector = cq.Workplane().polyline(lower_pts).close()
connector = connector.workplane(offset=6.0)
connector = connector.polyline(mid_pts).close()
connector = connector.loft(combine=True)
connector = connector.translate([-distance_between_DKs*2,-(hight/2 -wall_thickness/2),(width-6) ])
spacer = spacer.add(connector)
connector_upper = cq.Workplane().polyline(upper_pts).close().extrude(8)
connector_upper = connector_upper.faces("+Z").edges().fillet(1)
connector_upper = connector_upper.edges("|Z").fillet(1)
connector_upper = connector_upper.translate([-distance_between_DKs*2,-(hight/2 -wall_thickness/2),width])
spacer = spacer.add(connector_upper)

results = results.union(spacer)
spacer4 = spacer.mirror((1, 0, 0), (0, 0, 0)).translate([-distance_between_DKs*8,0,0])
results = results.union(spacer4)
spacer5 = spacer.mirror((1, 0, 0), (0, 0, 0))
results = results.union(spacer5)
spacer6 = spacer.mirror((1, 0, 0), (0, 0, 0)).translate([distance_between_DKs*4,0,0])
results = results.union(spacer6)

show_object(results)

cq.exporters.export(results, "Coax_8port_switch_stand.step")
cq.exporters.export(results, "Coax_8port_switch_stand.stl")
