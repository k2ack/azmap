#!/usr/bin/env python

import unittest
import logging
from mlocs import toLoc

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
