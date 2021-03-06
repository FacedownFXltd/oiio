#!/usr/bin/env python

# Creates a texture with overscan -- it looks like the usual grid in the
# 0-1 (display) window, but is red checker for a while outside that window.
#
# We then make two images using that texture:
# 1. out-exact.exr just straight maps the [0,1] range, and should look like
#    the whole grid and nothing but the grid.
# 2. out-over.exr maps the [-0.5,1.5] range, so you should see the grid,
#    surrounded by the red check border, surrounded by black. The grid
#    itself should be the "middle half" of the image.

command += (oiio_app("oiiotool") + parent+"/oiio-images/grid.tif"
            + " -resize 512x512 "
            + " -pattern checker:color1=1,0,0:color2=.25,0,0 640x640 3 "
            + "-origin -64-64 -paste +0+0 -fullsize 512x512+0+0 -o overscan-src.exr ;\n")
command += (oiio_app("maketx") + " --filter lanczos3 overscan-src.exr "
            + " -o grid-overscan.exr ;\n")
command += testtex_command ("grid-overscan.exr --res 256 256 " +
                            "--wrap black --nowarp -o out-exact.exr ;\n")
command += testtex_command ("grid-overscan.exr --res 256 256 " +
                            "--wrap black --nowarp " +
                            "--offset -0.5 -0.5 0 --scalest 2 2 " +
                            "-o out-over.exr ;\n")

outputs = [ "out-exact.exr", "out-over.exr" ]

