#!/usr/bin/env python3

from sunpy.data.sample import AIA_171_IMAGE
import sunpy.map

# We now create the Map using the sample data.
aiamap = sunpy.map.Map(AIA_171_IMAGE)

# Now we do a quick plot.
aiamap.peek()
aiamap.show()

