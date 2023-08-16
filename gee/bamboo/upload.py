#-*-coding:utf-8-*-
import shapefile as shp
import csv
import codecs
import os

def trans_point(folder, fn, delimiter=','):
    '''transfer a csv file to shapefile'''
    # create a point shapefile
    output_shp = shp.Writer(folder + "%s.shp"%fn.split('.')[0], shp.POINT)
    # for every record there must be a corresponding geometry.
    output_shp.autoBalance = 1
    # create the field names and data type for each.you can omit fields here
    # 顺序一定要与下面的保持一致
    output_shp.field('ID', 'N', 10000) # string, max-length
    output_shp.field('Class', 'N', 10000) # string, max-length
    output_shp.field('Lon', 'F', 10000, 8) # float
    output_shp.field('Lat', 'F', 10000, 8) # float
#    output_shp.field('scene_id', 'N')  # int
    counter = 1 # count the features
    # access the CSV file
    with codecs.open(r'D:\qq' + 'BambooSamples.csv' + os.sep, 'rb', 'utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        next(reader, None) # skip the header
        #loop through each of the rows and assign the attributes to variables
        for row in reader:
            try:
#                photo_url = row[0]
                ID = int(row[0])
                Class = int(row[1])
                Lon= float(row[2])
                Lat = float(row[3])


                output_shp.point(Lon, Lat) # create the point geometry
                output_shp.record(ID, Class, Lon, Lat) # add attribute data
                if counter % 10000 == 0:
                    print("Feature " + str(counter) + " added to Shapefile.")
                counter = counter + 1
            except:
                print(row)

