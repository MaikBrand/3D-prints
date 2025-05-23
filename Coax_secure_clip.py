#!/usr/bin/env python3

# Copyright (c) 2021-2024 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
#

# This is a CadQuery 3D-model of a secure clip for the coax test connector
# for Nordic's DK's
import cadquery as cq

coax_top_with = 20
coax_top_thick = 2 + 0.2
support_lenght = 20
support_hight = 4


clip_pts = [
(0,0),
(0, coax_top_with + 3*coax_top_thick),
((support_hight + 3*coax_top_thick), coax_top_with + 3*coax_top_thick),
((support_hight + 3*coax_top_thick), coax_top_with),
((support_hight + 2*coax_top_thick), coax_top_with),
((support_hight + 2*coax_top_thick), coax_top_with+ 2*coax_top_thick),
((support_hight + 1*coax_top_thick), coax_top_with+ 2*coax_top_thick),
((support_hight + 1*coax_top_thick), coax_top_with+ 1.2*coax_top_thick),
((1*coax_top_thick), coax_top_with+ 1.2*coax_top_thick),
((1*coax_top_thick), 1.8*coax_top_thick),
((support_hight+1*coax_top_thick), 1.8*coax_top_thick),
((support_hight+1*coax_top_thick), 1*coax_top_thick),
((support_hight+2*coax_top_thick), 1*coax_top_thick),
((support_hight+2*coax_top_thick), 3*coax_top_thick),
((support_hight+3*coax_top_thick), 3*coax_top_thick),
((support_hight+3*coax_top_thick),0),
]
result = cq.Workplane('front')
result = result.polyline(clip_pts).close().extrude(15)
result = result.edges("|X or |Y").fillet(0.7)

show_object(result)

# Export  second design as file formats used by 3D printers
cq.exporters.export(result, "./step/Coax_connector_secure_clip.step")
cq.exporters.export(result, "./stl/Coax_connector_secure_clip.stl")
