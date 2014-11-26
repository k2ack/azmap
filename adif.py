import unittest
import logging
import os
import re
import datetime as dt

logger = logging.getLogger('adif')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/tmp/adif-util.log')
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
Read an ADIF file and create a list of dicts that represent the QSOs...
Basic, simple reader. Nothing fancy.
'''



class ADIFReader(object):
    char_debug = False
    def __init__(self,readable):
        self.readable = readable
        self.rec_no = 0
    def adifFixup(self,rec):
        ''' In place modify rec to convert from unicode to appropriate types. 
        Also change any common, simple errors - like missing band w freq set, etc.'''

        convert  = { int : [ 'dxcc','cqz','ituz','tx_pwr' ] }
        defaults = { int : -1 }
        
        
        for k in sorted(rec):
            if k[-5:] == '_date':
                rec[k] = dt.datetime.strptime(rec[k],"%Y%m%d").date()
            elif k == 'freq':
                rec[k] = float(rec[k])
            elif k[:5] == 'time_':
                v = rec[k]
                l = len(v)
                if l == 5 or l == 6:
                    fmt='%H%M%S'
                elif l == 3 or l == 4:
                    fmt='%H%M'
                rec[k] = dt.datetime.strptime(rec[k],fmt).time()
            elif k == 'tx_pwr':
                tx_pwr_fixes = {'unknown' : -1 }
                v = rec[k].lower()
                if v in tx_pwr_fixes:
                    rec[k] = tx_pwr_fixes[v]
                    
        for k in convert:
            for field in convert[k]:
                if field in rec:
                    try:
                        rec[field] = k(rec[field])
                    except ValueError as v:
                        logger.error('unable to convert field %s (record %d) to type %s : %s',
                                     field,self.rec_no,str(k),rec[field])
                        rec[field] = defaults[k]
        return rec
    
        
    def load(self):
        # Code inspired by http://jeremy.cowgar.com/2010/09/20/adif_parser_in_python/
        # A little crude for now.
        raw = self.readable.read()

        # Find the EOH, in this simple example we are skipping
        # header parsing.
        pos = 0
        m = re.search('', raw, re.IGNORECASE)
        if m != None:
            # Start parsing our ADIF file after the  marker
            pos = m.end()

        recs = []
        rec = dict()
        while True:
            # Find our next field definition <...>
            pos = raw.find('<', pos)
            if pos == -1:
                 return recs
            endPos = raw.find('>', pos)

            # Split to get individual field elements out
            fieldDef = raw[pos + 1:endPos].split(':')
            fieldName = fieldDef[0].lower()
            if fieldName == 'eor':
                self.adifFixup(rec)     # fill in information from lookups
                recs.append(rec)   # append this record to our records list
                self.rec_no += 1
                logger.debug('New Record Recorded @+%d record: %s:  %s',self.rec_no,endPos,str(rec))
                rec = dict()       # start a new record
                pos = endPos
            elif fieldName == 'eoh':
                header = recs
                recs = []
                rec = dict()
            elif len(fieldDef) > 1:
                # We have a field definition with a length, get it's
                # length and then assign the value to the dictionary
                fieldLen = int(fieldDef[1])
                rec[fieldName] = raw[endPos + 1:endPos + fieldLen + 1].replace('&lt;', '<')
            pos = endPos
        return recs

    def qsos(self):
        from exceptions import DeprecationWarning
        raise DeprecationWarning()
    
# ----------------------------------------------------------------
# Tests

class ADIFReaderTestCase(unittest.TestCase):
    sample_adif_record='''<call:5>K6SRZ <qso_date:8>20130527 <time_on:6>083100 <band:3>20m <freq:7>14.0711 <mode:5>PSK31
        <rst_sent:3>599 <rst_rcvd:3>599 <qsl_rcvd:1>N <qsl_sent:1>N <dxcc:3>291 <cqz:1>3 <ituz:1>6 
        <tx_pwr:3>100 
        <app_rumlog_qsl:1>- <lotw_qsl_sent:1>N <lotw_qsl_rcvd:1>N <eqsl_qsl_sent:1>N <eqsl_qsl_rcvd:1>N <pfx:2>K6 <eor>'''
    rumlog_sample = '''ADIF Export from RumLog by DL2RUM
        tom@dl2rum.de
        For further info visit: http://www.dl2rum.de
        
        <adif_ver:5>2.2.6
        <programid:6>RUMlog
        <programversion:5>5.1.3
        <station_callsign:5>K2ACK
        <operator:5>K2ACK
        <my_name:4>Alan
        
        <eoh>

        <call:5>K6SRZ <qso_date:8>20130527 <time_on:6>083100 <band:3>20m <freq:7>14.0711 <mode:5>PSK31
        <rst_sent:3>599 <rst_rcvd:3>599 <qsl_rcvd:1>N <qsl_sent:1>N <dxcc:3>291 <cqz:1>3 <ituz:1>6 
        <tx_pwr:3>100 
        <app_rumlog_qsl:1>- <lotw_qsl_sent:1>N <lotw_qsl_rcvd:1>N <eqsl_qsl_sent:1>N <eqsl_qsl_rcvd:1>N <pfx:2>K6 <eor>'''

    def testNull(self):
        import StringIO
        q = ADIFReader(StringIO.StringIO('')).load()
        self.assertEqual(type(q),list)
        self.assertEqual(len(q),0)

    def check_first_qso(self,q):
        epsilon = 1e-7
        verify = { 'call':'K6SRZ',
                   'qso_date' :  dt.date(2013,5,27),
                   'freq' : lambda x : (x-14.0711) < epsilon,
                   'time_on' : dt.time(8,31,00),
                   'mode' : 'PSK31',
                   'band' : '20m',
                   'rst_sent' :'599',
                   'rst_rcvd' : '599',
                   'qsl_rcvd':'N',
                   'qsl_sent':'N',
                   'dxcc':291,
                   'cqz':3,
                   'ituz':6,
                   'tx_pwr':100,
                   'app_rumlog_qsl':'-',
                   'lotw_qsl_sent':'N',
                   'lotw_qsl_rcvd':'N',
                   'eqsl_qsl_sent':'N',
                   'eqsl_qsl_rcvd':'N',
                   'pfx':'K6' }

        for key in sorted(verify):
            expected = verify[key]
            if type(expected) == type(lambda x:True):
                self.assertTrue(expected(q[key]))
            else:
                self.assertEqual(q[key],expected)
        if False:
            self.assertEqual(q['call'],'K6SRZ')
            self.assertLess(q['freq'] - 14.0711 , epsilon)
            self.assertEqual(q['time_on'], dt.time(8,31,00))
            self.assertEqual(q['mode'],'PSK31')
            self.assertEqual(q['band'],'20m')
            self.assertEqual(q['rst_sent'],'599')
            self.assertEqual(q['dxcc'],291)

            self.assertEqual('this needs to check the whole QSO properly','in particular types need to be converted and checked')
        
    def testADIFSingleQso(self):
        import StringIO
        a = ADIFReader(StringIO.StringIO(self.sample_adif_record)).load()
        self.assertEqual(type(a),list)
        self.assertEqual(len(a),1)
        self.assertEqual(type(a[0]),dict)
        self.check_first_qso(a[0])

    def testRumLogAdi(self):
        import StringIO
        a = ADIFReader(StringIO.StringIO(self.rumlog_sample)).load()
        self.assertEqual(type(a[0]),dict)
        self.check_first_qso(a[0])
        
if __name__ == '__main__':
    unittest.main()


    
