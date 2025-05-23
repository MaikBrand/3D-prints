#!/usr/bin/env python3

# Copyright (c) 2021-2024 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
#

# This is a CadQuery 3D-model of a slide-in holder plate  
# for Nordic's Audio-5340 DK 
 
import cadquery as cq

pad_thick = 1.85
pad_x = 64
pad_y = 137

audio_with = 55
audio_hight = 86
audio_thick = 8
hight_increase = (pad_y - audio_hight)
holding_lip = (pad_thick + 1.8)

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
a = (cq.Workplane('front').box(pad_thick, audio_hight, audio_thick).translate([(pad_x/2 -audio_with/2 -pad_thick/2), audio_hight/2 + hight_increase,(audio_thick/2 + pad_thick)]))
a2 = (cq.Workplane('front').box(holding_lip, audio_hight, pad_thick).translate([(pad_x/2 -audio_with/2 + holding_lip/2 -pad_thick), audio_hight/2 + hight_increase,(audio_thick + 1.5*pad_thick)]))
b = (cq.Workplane('front').box(pad_thick, audio_hight, audio_thick).translate([(pad_x/2 +audio_with/2 +pad_thick/2), audio_hight/2 + hight_increase,(audio_thick/2 + pad_thick)]))
b2 = (cq.Workplane('front').box(holding_lip, audio_hight, pad_thick).translate([(pad_x/2 +audio_with/2 - holding_lip/2 +pad_thick), audio_hight/2 + hight_increase,(audio_thick +1.5*pad_thick)]))
c = (cq.Workplane('front').box(audio_with, pad_thick, audio_thick).translate([pad_x/2, hight_increase +pad_thick/2, (audio_thick/2 + pad_thick)]))
c2 = (cq.Workplane('front').box(audio_with, holding_lip, pad_thick).translate([pad_x/2, hight_increase +holding_lip/2, (audio_thick + 1.5*pad_thick)]))

result = result.union(a)
result = result.union(a2)
result = result.union(b)
result = result.union(b2)
result = result.union(c)
result = result.union(c2)

# Cut openings for connectors
hole_length = 10
battery_offset = (hight_increase + pad_thick + 38)
battery_length = 10
onoff_offset = (hight_increase + pad_thick + 18)
sd_debug_offset = (hight_increase + pad_thick + 45)
sd_debug_length = 27
nfc_offset = (hight_increase + pad_thick + 12)
nfc_length = 15
jack_offset = (4) 

battery_cut = (cq.Workplane('front').box(holding_lip,hole_length,audio_thick+pad_thick)
            .translate([(pad_x/2 -audio_with/2 + holding_lip/2 -pad_thick),battery_offset + hole_length/2, (audio_thick+pad_thick)/2 + pad_thick]))
result  = result.cut(battery_cut)

onoff_cut = (cq.Workplane('front').box(holding_lip,hole_length,audio_thick+pad_thick)
            .translate([(pad_x/2 -audio_with/2 + holding_lip/2 -pad_thick), onoff_offset + hole_length/2, (audio_thick+pad_thick)/2 + pad_thick]))
result  = result.cut(onoff_cut)

sd_debug_cut = (cq.Workplane('front').box(holding_lip,sd_debug_length,audio_thick+pad_thick)
            .translate([(pad_x/2 +audio_with/2 - holding_lip/2 + pad_thick), sd_debug_offset + sd_debug_length/2, (audio_thick+pad_thick)/2 + pad_thick]))
result  = result.cut(sd_debug_cut)

nfc_cut = (cq.Workplane('front').box(holding_lip,nfc_length,audio_thick+pad_thick)
            .translate([(pad_x/2 +audio_with/2 - holding_lip/2 + pad_thick), nfc_offset + nfc_length/2, (audio_thick+pad_thick)/2 + pad_thick]))
result  = result.cut(nfc_cut)

jack_cut1 = (cq.Workplane('front').box(hole_length, holding_lip +1 ,audio_thick+pad_thick)
                .translate([pad_x/2 - jack_offset - hole_length/2, (hight_increase +pad_thick), (audio_thick+pad_thick)/2 + pad_thick]))
result  = result.cut(jack_cut1)

jack_cut2 = (cq.Workplane('front').box(hole_length, holding_lip +1 ,audio_thick+pad_thick)
                .translate([pad_x/2 + jack_offset + hole_length/2 , (hight_increase +pad_thick), (audio_thick+pad_thick)/2 + pad_thick]))
result  = result.cut(jack_cut2)


# Add slots in the middle to remove material
slot_w = 8.5
slot_l = 40
slot_spacing = slot_w * 2
nslots = 8

plane = result.workplane(centerOption='ProjectedOrigin', origin=(pad_x/2, pad_y/2 +1 , 0))
slots = plane.rarray(1, slot_spacing, 1, nslots).slot2D(slot_l, slot_w, 0)
result = result.cutThruAll()

# Add text for identification 
result = result.union(cq.Workplane('front').text("Audio_5340",8,0.4 , kind="bold").translate([pad_x/2,17.5,2]))

show_object(result)

# Export design as file formats used by 3D printers
cq.exporters.export(result, "./step/Audio_DK_5340_holder.step")
cq.exporters.export(result, "./stl/Audio_DK_5340_holder.stl")
