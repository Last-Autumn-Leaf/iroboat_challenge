
import math
import requests
import zlib
import os
import numpy as np
import matplotlib.pyplot as plt


tuile_size=730
VALID_RESOLUTION = [1,6,18,30,45]

def get_tuile(resolution=1,latitude=44,longitude=-4,getHeader=False,debug=False):
    """
    :param resolution: should be 1,6,18,30,45
    :param latitude: should be between ]-90;90]
    :param longitude: should be between [-180;180[
    :param debug: print usefull data
    :return:data,header
        data is a (730x730) np array
        header is empty if getHeader=False
    """

    if resolution not in VALID_RESOLUTION:
        raise ValueError(str(resolution)+' is not a valid resolution !')
    if latitude>90 or latitude<=-90 :
        raise ValueError(str(latitude)+' is not a valid latitude !')
    if longitude>=180 or longitude<-180 :
        raise ValueError(str(longitude)+' is not a valid longitude !')


    fileUrl='https://static.virtualregatta.com/ressources/maps/dalles/vro2k16/'

    tile_longitude=( resolution * math.floor(longitude / resolution))
    tile_latitude = resolution * math.ceil(latitude /resolution)
    longitude_folder=int(tile_longitude/10)
    latitude_folder=int(tile_latitude/10)
    resolution=str(resolution)
    resolution,tile_longitude,tile_latitude,longitude_folder,latitude_folder=str(resolution),str(tile_longitude),str(tile_latitude),str(longitude_folder),str(latitude_folder)
    fileName=resolution+"_"+tile_longitude+"_"+tile_latitude+".deg"
    fileUrl+= resolution+'/'+longitude_folder+'/'+latitude_folder+'/'+fileName
    if debug:
        print(fileUrl)
    response = requests.get(fileUrl)
    fileName='current_tuile.deg'
    open(fileName, "wb").write(response.content)


    file_size = os.path.getsize(fileName)
    if debug :
        print("File Size is :", file_size, "bytes")


    with open(fileName, 'rb') as f :
        if getHeader :
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
        else :
            f.read(11)
        rest=f.read()

    header=[version,lat_tuile,long_tuile,size,(day,month,year)] if getHeader else []
    rest=zlib.decompress(rest,-15)


    data=np.frombuffer(rest,dtype=np.int8)
    data.resize((730,730))
    return data,header

def get_world_map(resolution=45,collisionOnly=False,debug=False):
    """
    :param resolution: should be 1,6,18,30,45
    :param debug: print usefull data
    :param collisionOnly : keep in memory only mixted tuile
    :return: world_map, memory_map
        world_map a np array of size(730*180/resolution x 730*360/resolution) where strictly negative value represents water
        memory_map an np.array of size (180x360) where '0' is a tuile where there are only water, '1' is a mixte tuile and '2' represents only ground
    """
    if resolution not in VALID_RESOLUTION:
        raise ValueError(str(resolution)+' is not a valid resolution !')

    world_map=np.zeros((int(tuile_size*2*90/resolution),
                        int(tuile_size*2*180/resolution)))

    memory_map=np.zeros((int(2*90/resolution),
                        int(2*180/resolution)))
    i,j=0,0
    ii,jj=i,j
    if debug :
        print(world_map.shape)
    for latitude in range(90,-90,-resolution):
        for longitude in range(-180,180,resolution):
            current_tuile=get_tuile(resolution,latitude,longitude,debug=debug)[0]
            if collisionOnly :
                if current_tuile.min() <0 and current_tuile.max() >=0 : # On n'enregistre que les tuiles mixtes
                    world_map[i:i+tuile_size,j:j+tuile_size]=current_tuile
                    memory_map[ii, jj] = '1'
            else:
                world_map[i:i + tuile_size, j:j + tuile_size] = current_tuile
                if world_map[i:i+tuile_size,j:j+tuile_size].max() <0 : # que de l'eau
                    memory_map[ii,jj]='0'

                if world_map[i:i+tuile_size,j:j+tuile_size].min() <0 and world_map[i:i+tuile_size,j:j+tuile_size].max() >=0: # Tuilde mixte
                    memory_map[ii,jj]='1'

                elif world_map[i:i+tuile_size,j:j+tuile_size].min() >=0: # Que de la terre
                    memory_map[ii,jj]='2'

            j+=tuile_size
            jj+=1
        i+=tuile_size
        ii+=1
        j=0
        jj=0
    return world_map,memory_map

if __name__=='__main__':
    decode_Map=True
    resolution=6

    if decode_Map:
        world_map,memory_map= get_world_map(resolution,collisionOnly=True)
        # Saving :
        fileName = 'decoded_map_5s.npy' %str(resolution)
        with open(fileName, 'wb') as f:
            np.save(f, world_map)
            np.save(f, memory_map)

        #displaying
        plt.figure()
        plt.imshow(world_map)
        plt.title('Carte du monde')
        plt.figure()
        plt.imshow(memory_map)
        plt.title('Tuile stockée')
        plt.show()

def get_decoded_map(fileName = 'decoded_map.npy') :
    with open(fileName, 'rb') as f:
        world_map = np.load(f)
        memory_map = np.load(f)
    return world_map,memory_map