
{
name: "GEO",
index: "world",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "", // world volume has no mother
type: "box",
size: [2000.0, 2000.0, 2000.0], // mm, half-length
material: "aluminum",
invisible: 1,
}

{
name: "GEO",
index: "monochrom_housing",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "world",
type: "tube",
r_max: 89.408,
size_z: 61.722,
position: [0.0, 0.0, 0.0],
material: "pmt_vacuum",
color: [0.2, 0.4, 0.6, 0.5],
drawstyle: "solid",
}

//Aluminum interface between monochromator housing and vacuum
{
 name: "GEO",
 index: "monochrom_Surf",
 valid_begin: [0, 0],
 valid_end: [0, 0],
 mother: "world",
 type: "border",
 volume1: "world",
 volume2: "monochrom_housing",
 surface: "aluminum",
 color: [0.2, 0.7, 0.2, 0.8],
 drawstyle: "solid",
 }

{
name: "GEO",
index: "shutter_tunnel",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "world",
type: "tube",
r_max: 31.754,
size_z: 78.867, 
position: [147.727,22.07,0.0], 
rotation: [0.0,90.0,0.0],
material: "pmt_vacuum",
color: [0.6, 0.4, 0.6, 0.2],
drawstyle: "solid",
}

//Aluminum interface between shutter_tunnel and vacuum
{
 name: "GEO",
 index: "tunnelSurface",
 valid_begin: [0, 0],
 valid_end: [0, 0],
 mother: "world",
 type: "border",
 volume1: "world",
 volume2: "shutter_tunnel",
 surface: "aluminum",
 color: [0.2, 0.7, 0.2, 0.8],
 drawstyle: "solid",
 }


//////////// FILTER WHEEL STEEL STRUCTURE ////////////
{
name: "GEO",
index: "filter_wheel_steel",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "shutter_tunnel",
type: "tube",
r_max: 31.75,
r_min: 11.1125,
size_z: 17.526,
position: [0.0, 0.0, -17.399],
rotation: [0.0,0.0,0.0],
material: "stainless_steel",
color: [0.2, 0.4, 0.6, 0.2],
drawstyle: "solid",
}

//////////// MONOCHROMATOR SLIT ////////////

// monochromator slit 1
{
name: "GEO",
index: "monochrom_screen_1",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "monochrom_housing",
type: "box",
size: [1.5875, 12.7, 38.099999999999994], // mm, half-length
position: [62.637, 42.263, 0.0],
material: "stainless_steel",
color: [0.2, 0.4, 0.6, 0.5],
drawstyle: "solid",
}


{
name: "GEO",
index: "monochrom_screen_2",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "monochrom_housing",
type: "box",
size: [1.5875, 12.7, 38.099999999999994], // mm, half-length
position: [62.637, 1.8770000000000016, 0.0],
material: "stainless_steel",
color: [0.2, 0.4, 0.6, 0.5],
drawstyle: "solid",
}

{
name: "GEO",
index: "monochrom_screen_top",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "monochrom_housing",
type: "box",
size: [1.5875, 7.492999999999999, 12.7], // mm, half-length
position: [62.637, 22.07, 26.924],
material: "stainless_steel",
color: [0.2, 0.4, 0.6, 0.5],
drawstyle: "solid",
}

{
name: "GEO",
index: "monochrom_screen_bottom",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "monochrom_housing",
type: "box",
size: [1.5875, 7.492999999999999, 12.7], // mm, half-length
position: [62.637, 22.07, -26.924],
material: "stainless_steel",
color: [0.2, 0.4, 0.6, 0.5],
drawstyle: "solid",
}

//////////// SLIT NEAR SAMPLES ////////////
{
name: "GEO",
index: "sample_wheel_slit_1",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "shutter_tunnel",
type: "box",
size: [38.099999999999994, 15.875, 1.5875], // mm, half-length
position: [0.0, 16.764, 17.65299999999999],
material: "stainless_steel",
color: [0.2, 0.4, 0.6, 0.5],
drawstyle: "solid",
}

{
name: "GEO",
index: "sample_wheel_slit_2",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "shutter_tunnel",
type: "box",
size: [38.099999999999994, 15.875, 1.5875], // mm, half-length
position: [0.0, -16.764, 17.65299999999999],
material: "stainless_steel",
color: [0.2, 0.4, 0.6, 0.5],
drawstyle: "solid",
}

{
name: "GEO",
index: "sample_wheel_slit_top",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "shutter_tunnel",
type: "box",
size: [15.875, 38.099999999999994, 1.5875], // mm, half-length
position: [19.431, 0.0, 17.65299999999999],
material: "stainless_steel",
color: [0.2, 0.4, 0.6, 0.5],
drawstyle: "solid",
}

{
name: "GEO",
index: "sample_wheel_slit_bottom",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "shutter_tunnel",
type: "box",
size: [15.875, 38.099999999999994, 1.5875], // mm, half-length
position: [-19.431, 0.0, 17.65299999999999],
material: "stainless_steel",
color: [0.2, 0.4, 0.6, 0.5],
drawstyle: "solid",
}

////// ADD BORDERS TO MAKE BACK OF SAMPLE WHEEL SLIT RELFECTIVE (VERT SECTIONS 1 and 2)
{
 name: "GEO",
 index: "sampleSlitSurf1",
 valid_begin: [0, 0],
 valid_end: [0, 0],
 mother: "world",
 type: "border",
 volume1: "shutter_tunnel",
 volume2: "sample_wheel_slit_1",
 surface: "stainless_steel",
 color: [0.2, 0.7, 0.2, 0.8],
 drawstyle: "solid",
 }
 
 {
 name: "GEO",
 index: "sampleSlitSurf2",
 valid_begin: [0, 0],
 valid_end: [0, 0],
 mother: "world",
 type: "border",
 volume1: "shutter_tunnel",
 volume2: "sample_wheel_slit_2",
 surface: "stainless_steel",
 color: [0.2, 0.7, 0.2, 0.8],
 drawstyle: "solid",
 }

/////// SAMPLE AND TPB VOLUMES //////////////

{
name: "GEO",
index: "sample_vol",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "shutter_tunnel",
type: "tube",
r_max: 11.1125,
size_z: 1.5875,
position: [0.0, 0.0, -20.6375],
material: "acrylic_suvt",
color: [0.2, 0.4, 0.2, 0.8],
drawstyle: "solid",
}


{
name: "GEO",
index: "tpb_vol_vac",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "shutter_tunnel",
type: "tube",
r_max: 11.1125,
size_z: 0.0005,
position: [0.0, 0.0, -19.0495],
material: "tpb",
color: [0.8, 0.9, 0.2, 0.8],
drawstyle: "solid",
}

{
 name: "GEO",
 index: "sample_vol_tpb",
 valid_begin: [0, 0],
 valid_end: [0, 0],
 mother: "shutter_tunnel",
 type: "border",
 volume1: "shutter_tunnel",
 volume2: "tpb_vol_vac",
 surface: "tpb_surface",
 color: [0.2, 0.7, 0.2, 0.8],
 drawstyle: "solid",
 }

////// GEOMETRY AROUND PHOTODIODE ////////
{
name: "GEO",
index: "alVolAroundPhotoDiode",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "shutter_tunnel",
type: "tube",
r_max: 31.75,
r_min: 17.3355,
size_z: 38.1,
position: [0.0, 0.0, -73.02499999999999],
material: "aluminum",
color: [0.1, 0.1, 0.6, 0.3],
drawstyle: "solid",
}

// Black plastic behind photodiode
{
name: "GEO",
index: "plasticBehindPhotoDiode",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "shutter_tunnel",
type: "tube",
r_max: 17.3355,
size_z: 12.7,
position: [0.0, 0.0, -53.974999999999994],
material: "acrylic_black",
color: [0.6, 0.1, 0.6, 0.3],
drawstyle: "solid",
}


/////// DETECTOR VOLUME //////////////

{
name: "GEO",
index: "detector_vol",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "shutter_tunnel",
type: "box",
size: [5.0, 5.0, 1.5], // mm, half-length
position: [0.0, 0.0, -39.599999999999994],
rotation: [0.0, 0.0, 45.0],
material: "acrylic_black",
color: [0.7, 0.4, 0.3, 0.8],
drawstyle: "solid",
}

{
name: "GEO",
index: "detector_vol_vac",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "shutter_tunnel",
type: "box",
size: [5.0, 5.0, 5e-06], // mm, half-length
position: [0.0, 0.0, -38.09999499999999],
rotation: [0.0, 0.0, 45.0],
material: "pmt_vacuum",
color: [0.2, 0.2, 0.9, 0.8],
drawstyle: "solid",
}





