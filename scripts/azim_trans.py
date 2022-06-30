#!/usr/bin/env python
# Copyright 2022 Ross Vicario
# Azimuthal Equidistant Projection

import numpy as np

class AzimuthalProjection:
    # input paramters: start point in lat/lon, radius of earth
    # for best results, choose start point close to center
    def __init__(self, lat=0, lon=0, radius=6371000):
        self.phi1 = lat
        self.lon = lon
        self.radius = radius
        # these trig values are memoized
        self.cos_phi1 = np.cos(lat)
        self.sin_phi1 = np.sin(lat)

    # latlon_to_xy converts a lat/lon coord pair to Cartesian plane
    # input: lat/lon of the point to be converted
    # output: tuple (x,y), the displacement from origin point in meters
    def latlon_to_xy(self, lat, lon):
        # memoize some trig values
        cos_lat = np.cos(lat)
        sin_lat = np.sin(lat)
        cos_lon = np.cos(lon-self.lon)

        # c is the angular distance from the center
        c = np.arccos(self.sin_phi1 * sin_lat \
            + self.cos_phi1 * cos_lat * cos_lon)
        k = c / np.sin(c)

        # Find x,y on the Cartesian plane. Units: angular distance
        x = k * cos_lat * np.sin(lon - self.lon)
        y = k * (self.cos_phi1 * sin_lat - self.sin_phi1 * cos_lat * cos_lon)

        # convert x,y to linear distance from origin
        x *= self.radius
        y *= self.radius
        
        return x,y

AP = AzimuthalProjection(34,85)
d = AP.latlon_to_xy(34,85-.0002)
print(d)
