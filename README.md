azmap
=====

Azimuth Mapping for Contacts

This no longer needs Pandas. Just basemap and matplotlib.
log.adi - this should be your ADIF formatted log file.
Try to put as many grids in there as possible.

You can likely see the notebook in the viewer using:

http://nbviewer.ipython.org/github/k2ack/azmap/blob/master/AzimuthMapExperiment.ipynb

_Note_: The figures are large here because I've edited my local ipython notebook configuration to set a 12x8 figure size. This is explained in part here: http://stackoverflow.com/questions/17230797/how-to-set-the-matplotlib-figure-default-size-in-ipython-notebook

Getting Started
===============

You need a working `matplotlib` and `basemap` installation.
* http://matplotlib.org/basemap/
* http://matplotlib.org/
618  pip install matplotlib
  619  pip freeze
  620  pip install basemap
  621  pip install http://matplotlib.org/basemap/#egg=basemap
  622  pip install git+http://matplotlib.org/basemap/#egg=basemap
  623  pip install git+https://github.com/matplotlib/basemap.git#egg=basemap
  624  pip install git+https://github.com/matplotlib/basemap.git#egg=basemap
  625  pip install git+https://github.com/matplotlib/basemap.git#egg=basemap
  626  pip install git+https://github.com/matplotlib/basemap.git#egg=basemap
  627  pip install git+file:///Users/alan/Documents/scm/github/basemap/#egg=basemap
