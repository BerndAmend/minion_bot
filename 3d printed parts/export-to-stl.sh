#!/bin/sh

set -x
set -e

openscad -q --hardwarnings -o foot.stl -D part=\"foot\" Assembled.scad
openscad -q --hardwarnings -o mount.stl -D part=\"mount\" Assembled.scad
