#!/usr/bin/env python3
import sys

# Do not import other stuff before the arguments are valid
argc=len(sys.argv)

if argc<2:
    print("usage: %s input_file [output_file]" % sys.argv[0])
    exit(-1)

import numpy as np
import face_recognition as fr
import csv

input_filename=sys.argv[1]
output_filename=""
if argc>=3:
    output_filename=sys.argv[2]
else:
    parts=input_filename.split('.')
    parts[-1]="face"
    output_filename='.'.join(parts)
print("output data to `%s'" % output_filename)

image=fr.load_image_file(input_filename)
encoding=fr.face_encodings(image)[0]
# Now write the data to the output file
np.savetxt(output_filename,encoding)
