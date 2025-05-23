#!/usr/bin/env python3

# Copyright (c) 2021-2024 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
#

# This is a CadQuery 3D-model of a slide-in holder plate  
# for Nordic's PPK2

import cadquery as cq


pad_thick = 1.85
pad_x = 64
pad_y = 137

ppk_with = 55
ppk_hight = 86
ppk_thick = 10
hight_increase = (pad_y - ppk_hight)
holding_lip = (pad_thick + 3)

# Draw the base plate
result = (cq.Workplane('front').box(pad_x, pad_y, pad_thick)
          .translate([pad_x/2, pad_y/2, pad_thick/2]))

# Draw the side rails
rail_x = 7
rail_y = 40

rail_z = pad_thick

rail = cq.Workplane('front').box(rail_x, rail_y, rail_z)
rail = rail.edges("|Y and <X").fillet(.7)
rail = rail.translate([-rail_x/2, rail_y/2, rail_z/2])
rails = rail.union(rail.mirror((1, 0, 0), (pad_x/2, 0, 0)))

result = result.union(rails)

#Draw the grove to slot the PPK2 in
a = (cq.Workplane('front').box(pad_thick, ppk_hight, ppk_thick).translate([(pad_x/2 -ppk_with/2 -pad_thick/2), ppk_hight/2 + hight_increase,(ppk_thick/2 + pad_thick)]))
a2 = (cq.Workplane('front').box(holding_lip, ppk_hight, pad_thick).translate([(pad_x/2 -ppk_with/2 + holding_lip/2 -pad_thick), ppk_hight/2 + hight_increase,(ppk_thick + 1.5*pad_thick)]))
b = (cq.Workplane('front').box(pad_thick, ppk_hight, ppk_thick).translate([(pad_x/2 +ppk_with/2 +pad_thick/2), ppk_hight/2 + hight_increase,(ppk_thick/2 + pad_thick)]))
b2 = (cq.Workplane('front').box(holding_lip, ppk_hight, pad_thick).translate([(pad_x/2 +ppk_with/2 - holding_lip/2 +pad_thick), ppk_hight/2 + hight_increase,(ppk_thick +1.5*pad_thick)]))
c = (cq.Workplane('front').box(ppk_with, pad_thick, ppk_thick).translate([pad_x/2, hight_increase +pad_thick/2, (ppk_thick/2 + pad_thick)]))
c2 = (cq.Workplane('front').box(ppk_with, holding_lip, pad_thick).translate([pad_x/2, hight_increase +holding_lip/2, (ppk_thick + 1.5*pad_thick)]))

result = result.union(a)
result = result.union(a2)
result = result.union(b)
result = result.union(b2)
result = result.union(c)
result = result.union(c2)

# Cut openings for connectors
logic_offset = (hight_increase + pad_thick + 45)
logic_length = 30
measure_offset = (hight_increase + pad_thick + 15)
measure_length = 17
onoff_offset = (hight_increase + pad_thick + 38)
usb_power_offset = (hight_increase + pad_thick + 18)
usb_data_offset = (hight_increase + pad_thick + 58)
hole_length = 10

logic_cut = (cq.Workplane('front').box(holding_lip,logic_length,ppk_thick+pad_thick)
            .translate([(pad_x/2 -ppk_with/2 + holding_lip/2 -pad_thick),logic_offset + logic_length/2, (ppk_thick+pad_thick)/2 + pad_thick]))
result  = result.cut(logic_cut)

measure_cut = (cq.Workplane('front').box(holding_lip,measure_length,ppk_thick+pad_thick)
            .translate([(pad_x/2 -ppk_with/2 + holding_lip/2 -pad_thick), measure_offset + measure_length/2, (ppk_thick+pad_thick)/2 + pad_thick]))
result  = result.cut(measure_cut)

onoff_cut = (cq.Workplane('front').box(holding_lip,hole_length,ppk_thick+pad_thick)
            .translate([(pad_x/2 +ppk_with/2 - holding_lip/2 +pad_thick), onoff_offset + hole_length/2, (ppk_thick+pad_thick)/2 + pad_thick]))
result  = result.cut(onoff_cut)

usb_power_cut = (cq.Workplane('front').box(holding_lip,hole_length,ppk_thick+pad_thick)
                .translate([(pad_x/2 +ppk_with/2 - holding_lip/2 +pad_thick), usb_power_offset + hole_length/2, (ppk_thick+pad_thick)/2 + pad_thick]))
result  = result.cut(usb_power_cut)

usb_data_cut = (cq.Workplane('front').box(holding_lip,hole_length,ppk_thick+pad_thick)
                .translate([(pad_x/2 +ppk_with/2 - holding_lip/2 +pad_thick), usb_data_offset + hole_length/2, (ppk_thick+pad_thick)/2 + pad_thick]))
result  = result.cut(usb_data_cut)


# Add slots in the middle to remove material
slot_w = 8.5
slot_l = 40
slot_spacing = slot_w * 2
nslots = 8

plane = result.workplane(centerOption='ProjectedOrigin', origin=(pad_x/2, pad_y/2 +1 , 0))
slots = plane.rarray(1, slot_spacing, 1, nslots).slot2D(slot_l, slot_w, 0)
result = result.cutThruAll()

# Add text for identification
result = result.union(cq.Workplane('front').text("PPK2",8,0.4 , kind="bold").translate([pad_x/2,17.5,2]))

show_object(result)

# Export design as file formats used by 3D printers
cq.exporters.export(result, "./step/PPK2.step")
cq.exporters.export(result, "./stl/PPK2.stl")
