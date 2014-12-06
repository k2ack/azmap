#!/usr/bin/env python

import unittest
import logging

from mlocs import toLoc

import gzip
import base64
import csv
import StringIO
    

logger = logging.getLogger('azimuth')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/tmp/az-util.log')
fh.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)-8s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

__version__ = '0.0.1'
__doc__ = '''
Compute the azimuth between two points on an x,y plane starting with locators
'''
def relative_offset(m,lon_0,lat_0,lon_1,lat_1):
    p = m.gcpoints(lon_0,lat_0,lon_1,lat_1,2)
    return (p[0][1] - p[0][0], p[1][1]-p[1][0])

def relative_offset_qth(m,qth_o,grid_dest=None,lonlat_dest=None):
    lat_o,lon_o = toLoc(qth_o)
    if grid_dest is not None:
        lat_dx,lon_dx = toLoc(grid_dest)
    else:
        lat_dx, lon_dx = lonlat_dest
 
    return relative_offset(m,lon_o,lat_o,lon_dx,lat_dx)
    
def to_polar(x,y,units='r'):
    '''returns in degrees from 0 = North'''
    from math import sqrt,atan2,pi,degrees
    convert = lambda theta: theta
    if units[:1] == 'd':
        convert = degrees
    return ( sqrt(x**2.+y**2.),convert(atan2(x,y)%(2*pi)) )


'''This is a csv text blob that maps DXCC code to locator it is only here to make this notebook as self contained as possible. Better to just read a text file and build a dict - but for my redditors - this means the notebook doesn't need anything but your ADIF file of contacts for building your own map.'''


_dxdc ='''
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
REdYYVDqtmhQxff5VnQlJ6n+A7HKD5Q='''

_dxcc = dict()

for code,locator in csv.reader(
        StringIO.StringIO(
            gzip.zlib.decompress(
                base64.decodestring(_dxdc)))):
    _dxcc[int(code)] = locator

def all_dxcc():
    return sorted(_dxcc.keys())

def loc_for_dxcc(dxcc_num):
    ''' Take an ADIF DXCC entity integer and return a locator that represents that entity.
    The hard work was done in the base64 blob above being decoded into a dict() that maps
    entity : locator_string
    Returns None if we don't know the answer.
    Data taken from RUMlog's internal database courtesy of DL2RUM.
    '''
    r = None
    if dxcc_num in _dxcc:
        r = _dxcc[dxcc_num]
    return r



class AzimuthUtilTests(unittest.TestCase):
    from math import radians as r
    epsilon = 1e-8
    def testLocators(self):
        from math import pi
        from math import radians as r
        class proj_helper(object):
            def __init__(self):
                pass
            def gcpoints(self,a,b,c,d,n):
                return [ [a,c],[b,d] ]
            
        td = [ ( 'DO20','DO21',0.0,self.epsilon ),
               ( 'DO16','DO15',180.0,self.epsilon) ]
        m = proj_helper()
        for c in td:
            d,a = to_polar(*relative_offset_qth(m,c[0],c[1]))
            self.assertLess((a-r(c[2]))%(2*pi),c[3])
            
    def test_to_polar_1(self):
        from math import radians as r
        res_list= [ (0, 	1,	r(0.0)),	
                    (1, 	0,	r(90.0)),	
                    (0, 	-1,	r(180.0)),	
                    (-1,	0,	r(270.0)),	
                    (1, 	1,	r(45.0)),	
                    (1, 	-1,	r(135.0)),	
                    (-1,	-1,	r(225.0)),	
                    (-1,	1,	r(315.0)) ]
        for x,y,theta in res_list:
            self.assertEqual(to_polar(x,y)[1], theta)
            
        
        self.assertEqual(to_polar(0,1,units='d')[1] , 0.0)
        self.assertEqual(to_polar(1,0,units='d')[1] , 90.0)
        self.assertEqual(to_polar(0,-1)[1] , r(180.0))
        self.assertEqual(to_polar(-1,0)[1]  , r(270.0))
        


if __name__ == '__main__':
    unittest.main()
