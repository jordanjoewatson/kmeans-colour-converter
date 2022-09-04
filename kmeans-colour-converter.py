import itertools
import os
from PIL import Image
from sys import argv
from sklearn.cluster import KMeans

if len(argv) != 3:
    print("python3 img.py <imagetochange> <output_directory>")
    exit()

outputfile = os.path.join(argv[2], 'output{}.png')

# Add or remove colours here for a different amount of colours than 4 
COLORS = [
        (255,255,255),
        (159,119,224),
        (32,50,85),
        (216,201,241)
]

img = Image.open(argv[1])

# read in all pixel values
pixel_values = []
for h in range(0, img.height):
    for w in range(0, img.width):
        pxl = img.getpixel((w,h))
        pixel_values.append((pxl))

km = KMeans(n_clusters=len(COLORS), init='k-means++', random_state=42)
km.fit(pixel_values)

y = km.fit_predict(pixel_values)

# create mappings
mappings = []
# Following line is for three colours instead of four, alter to include more or less colours
# for (a,b,c) in ...
# mappings.append({ 0:a, 1:b, 2:c })
for (a,b,c,d) in itertools.permutations(range(0,len(COLORS)), len(COLORS)):
    mappings.append({ 0:a, 1:b, 2:c, 3:d })

mappingitr = 0
for mapping in mappings:
    itr = 0
    mappingitr += 1
    print("generating image {}".format(mappingitr))
    for h in range(0, img.height):
        for w in range(0, img.width):
            pxl = img.getpixel((w,h))

            group = mapping[y[itr]]
            rgb = COLORS[group]

            img.putpixel((w,h), rgb)

            itr += 1

    img.save(outputfile.format(mappingitr))
