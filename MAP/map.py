#TODO : Try to decode the map
import math
import requests
import zlib
import os

fileUrl='https://static.virtualregatta.com/ressources/maps/dalles/vro2k16/'
resolution=1
longitude=14
latitude=-61

tile_longitude=( resolution * math.floor(longitude / resolution))
tile_latitude = resolution * math.ceil(latitude /resolution)
longitude_folder=int(tile_longitude/10)
latitude_folder=int(tile_latitude/10)
resolution=str(resolution)
resolution,tile_longitude,tile_latitude,longitude_folder,latitude_folder=str(resolution),str(tile_longitude),str(tile_latitude),str(longitude_folder),str(latitude_folder)
fileName=resolution+"_"+tile_longitude+"_"+tile_latitude+".deg"
fileUrl+= resolution+'/'+longitude_folder+'/'+latitude_folder+'/'+fileName


exempleUrl='https://static.virtualregatta.com/ressources/maps/dalles/vro2k16/1/0/4/1_-4_44.deg'
response = requests.get(fileUrl)
fileName='map.deg'
open(fileName, "wb").write(response.content)


file_size = os.path.getsize(fileName)
print("File Size is :", file_size, "bytes")

"""with open(fileName,'rb') as f:
    header=f.read(11)
    gzbuf=f.read()
    databuf=zlib.decompress(gzbuf,-zlib.MAX_WBITS)"""

with open(fileName, 'rb') as f :
    #octet 1: version du fichier
    version =int.from_bytes( f.read(1) , "big")

    #octets 2 et 3: latitude de la tuile, le premier octet indique le signe, 1 pour négatif, 0 pour positif, le second contient la valeur absolue de la latitude
    signe=int.from_bytes( f.read(1) , "big")
    val_abs=int.from_bytes( f.read(1) , "big")
    lat_tuile=val_abs*(-1)**signe

    #octets 4 et 5: longitude de la tuile,
    signe = int.from_bytes(f.read(1), "big")
    val_abs = int.from_bytes(f.read(1), "big")
    long_tuile = val_abs * (-1) ** signe

    #irrelevant byte Octet 6
    byte_6=f.read(1)

    #octet 7 et 8 largeur (et hauteur)
    largeur,hauteur=f.read(1),f.read(1)
    size=int.from_bytes(largeur+hauteur, "big")
    if size==730 :print('correct size')
    else : print('wrong size')
    #octets 9 à 11: date de génération du fichier
    year= 2040- int.from_bytes(f.read(1), "big")
    month= 1+ int.from_bytes(f.read(1), "big")
    day=int.from_bytes(f.read(1), "big")

    rest=f.read()
rest=zlib.decompress(rest,-15)

import numpy as np
data=np.frombuffer(rest,dtype=np.int8)
data.resize((730,730))

import matplotlib.pyplot as plt
plt.figure()
plt.imshow(data)
plt.show()

#TODO : We need to uncompressed the gzip data stored in rest.