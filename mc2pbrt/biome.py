"""
Copyright (c) 2014, Eric Haines
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
"""

# This code is rewrite from https://github.com/erich666/Mineways/blob/master/Win/biomes.cpp

from tuple_calculation import plus, mult
from util import clamp

BIOMES = [
    ["Ocean", 0.500000, 0.500000],
    ["Plains", 0.800000, 0.400000],
    ["Desert", 2.000000, 0.000000],
    ["Mountains", 0.200000, 0.300000],
    ["Forest", 0.700000, 0.800000],
    ["Taiga", 0.250000, 0.800000],
    ["Swamp", 0.800000, 0.900000],
    ["River", 0.500000, 0.500000],
    ["Nether", 2.000000, 0.000000],
    ["The End", 0.500000, 0.500000],
    ["Frozen Ocean", 0.000000, 0.500000],
    ["Frozen River", 0.000000, 0.500000],
    ["Snowy Tundra", 0.000000, 0.500000],
    ["Snowy Mountains", 0.000000, 0.500000],
    ["Mushroom Fields", 0.900000, 1.000000],
    ["Mushroom Field Shore", 0.900000, 1.000000],
    ["Beach", 0.800000, 0.400000],
    ["Desert Hills", 2.000000, 0.000000],
    ["Wooded Hills", 0.700000, 0.800000],
    ["Taiga Hills", 0.250000, 0.800000],
    ["Mountain Edge", 0.200000, 0.300000],
    ["Jungle", 0.950000, 0.900000],
    ["Jungle Hills", 0.950000, 0.900000],
    ["Jungle Edge", 0.950000, 0.800000],
    ["Deep Ocean", 0.500000, 0.500000],
    ["Stone Shore", 0.200000, 0.300000],
    ["Snowy Beach", 0.050000, 0.300000],
    ["Birch Forest", 0.600000, 0.600000],
    ["Birch Forest Hills", 0.600000, 0.600000],
    ["Dark Forest", 0.700000, 0.800000],
    ["Snowy Taiga", -0.500000, 0.400000],
    ["Snowy Taiga Hills", -0.500000, 0.400000],
    ["Giant Tree Taiga", 0.300000, 0.800000],
    ["Giant Tree Taiga Hills", 0.300000, 0.800000],
    ["Wooded Mountains", 0.200000, 0.300000],
    ["Savanna", 1.200000, 0.000000],
    ["Savanna Plateau", 1.000000, 0.000000],
    ["Badlands", 2.000000, 0.000000],
    ["Wooded Badlands Plateau", 2.000000, 0.000000],
    ["Badlands Plateau", 2.000000, 0.000000],
    ["Small End Islands", 0.500000, 0.400000],
    ["End Midlands", 0.500000, 0.400000],
    ["End Highlands", 0.500000, 0.400000],
    ["End Barrens", 0.500000, 0.400000],
    ["Warm Ocean", 0.800000, 0.400000],
    ["Lukewarm Ocean", 0.800000, 0.400000],
    ["Cold Ocean", 0.800000, 0.400000],
    ["Deep Warm Ocean", 0.800000, 0.400000],
    ["Deep Lukewarm Ocean", 0.800000, 0.400000],
    ["Deep Cold Ocean", 0.800000, 0.400000],
    ["Deep Frozen Ocean", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["The Void", 0.500000, 0.500000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Sunflower Plains", 0.800000, 0.400000],
    ["Desert Lakes", 2.000000, 0.000000],
    ["Gravelly Mountains", 0.200000, 0.300000],
    ["Flower Forest", 0.700000, 0.800000],
    ["Taiga Mountains", 0.250000, 0.800000],
    ["Swamp Hills", 0.800000, 0.900000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Ice Spikes", 0.000000, 0.500000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Modified Jungle", 0.950000, 0.900000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Modified Jungle Edge", 0.950000, 0.800000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Tall Birch Forest", 0.600000, 0.600000],
    ["Tall Birch Hills", 0.600000, 0.600000],
    ["Dark Forest Hills", 0.700000, 0.800000],
    ["Snowy Taiga Mountains", -0.500000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Giant Spruce Taiga", 0.250000, 0.800000],
    ["Giant Spruce Taiga Hills", 0.250000, 0.800000],
    ["Gravelly Mountains+", 0.200000, 0.300000],
    ["Shattered Savanna", 1.100000, 0.000000],
    ["Shattered Savanna Plateau", 1.000000, 0.000000],
    ["Eroded Badlands", 2.000000, 0.000000],
    ["Modified Wooded Badlands Plateau", 2.000000, 0.000000],
    ["Modified Badlands Plateau", 2.000000, 0.000000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
    ["Unknown Biome", 0.800000, 0.400000],
]

GRASS_CORNER = [
    (191, 183, 85),
    (128, 180, 151),
    (71, 205, 51)
]

FOLIAGE_CORNER = [
    (174, 164, 42),
    (96, 161, 123),
    (26, 191, 0)
]


def getBiomeName(biome_id):
    """Get biome name by biome id"""
    return BIOMES[biome_id]


def getFoliageColor(biome_id, elevation):
    """Get foliage color by biome id and height"""
    return _getColor(biome_id, elevation, FOLIAGE_CORNER)


def getGrassColor(biome_id, elevation):
    """Get grass color by biome id and height"""
    return _getColor(biome_id, elevation, GRASS_CORNER)


def _getColor(biome_id, elevation, corner):
    """Calculate biome color by traingle lerp.

    Args:
        biome_id: Biome ID
        evelation: height of block
        corner: Color of 3 corners of triangle.
    Returns:
        (r, g, b)
    """
    b = BIOMES[biome_id]
    temp = clamp(b[1] - elevation*0.00166667)
    rain = clamp(b[2])*temp
    alpha = [temp-rain, 1-temp, rain]
    ret_color = (0., 0., 0.)
    for i in range(3):
        ret_color = plus(ret_color, mult(corner[i], alpha[i]))
    ret_color = mult(ret_color, 1./255)
    ret_color = tuple(map(clamp, ret_color))
    return ret_color
