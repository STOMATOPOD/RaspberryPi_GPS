#!/usr/bin/env python
# Copyright 2022 Ross Vicario
# Azimuthal Equidistant Projection
# Source: https://mathworld.wolfram.com/AzimuthalEquidistantProjection.html

import numpy as np

class AzimuthalProjection:
    # input paramters: start point in lat/lon, radius of earth
    # for best results, don't move far from start point
    def __init__(self, lat=0, lon=0, radius=6371000):
        self.phi1 = np.deg2rad(lat)
        self.lon = np.deg2rad(lon)
        self.radius = radius
        # these trig values are memoized
        self.cos_phi1 = np.cos(self.phi1)
        self.sin_phi1 = np.sin(self.phi1)

    # latlon_to_xy converts a lat/lon coord pair to Cartesian plane
    # input: lat/lon (units: degrees)
    # output: tuple (x,y), the displacement in meters
    def latlon_to_xy(self, inLat, inLon):
        # convert degrees to radians
        lat = np.deg2rad(inLat)
        lon = np.deg2rad(inLon)
        # memoize some trig values
        cos_lat = np.cos(lat)
        sin_lat = np.sin(lat)
        cos_lon = np.cos(lon-self.lon)

        # placeholder to check for rounding errors
        temp = (self.sin_phi1 * sin_lat \
            + self.cos_phi1 * cos_lat * cos_lon)
        # correct for rounding errors
        if temp > 1:
            temp = 1

        # c is the angular distance from the center
        c = np.arccos(temp)

        if c == 0:
            k = 1
        else:
            k = c / np.sin(c)

        # Find x,y on the Cartesian plane. Units: angular distance
        # longitude is x, it measures east-west displacement
        x = k * cos_lat * np.sin(lon - self.lon)
        # latitude is y, it measures north-south displacement
        y = k * (self.cos_phi1 * sin_lat - self.sin_phi1 * cos_lat * cos_lon)

        # multiply by radius to convert x,y to linear distance from origin
        x *= self.radius
        y *= self.radius
        
        return x,y
