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

In my new virtualenv, install matplotlib with :

    pip install matplotlib

Then install basemap from:

    pip install git+https://github.com/matplotlib/basemap.git#egg=basemap

At this point your list of installed packages in the virtualenv should be very similar to:

    basemap >=1.0.8
    matplotlib >=1.4.2
    mlocs >=1.0.5
    mock >=1.0.1
    nose >=1.3.4
    numpy >=1.9.1
    pyparsing >=2.0.3
    python-dateutil >=2.2
    pytz >=2014.9
    six >=1.8.0
    wsgiref >=0.1.2
