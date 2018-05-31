#!/usr/bin/env python
# Run with : ./profile.sh <obj file>
import cProfile
import pstats
import sys
try:
    from StringIO import StringIO
except:
    from io import StringIO

print(len(sys.argv), sys.argv)

if len(sys.argv) < 2:
    print("Usage: ./profile.sh <obj file>")
    exit(1)

pr = cProfile.Profile()
pr.enable()
import pywavefront
pywavefront.Wavefront(sys.argv[1])
pr.disable()

# Print the stats
s = StringIO()
sortby = 'tottime'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())

