#!/usr/bin/env python

# Note that this should be used with original GALFIT.

from glob import glob
import pyfits
import sys, os
import numpy

shape = (100,100)

bands = ['u', 'g', 'r', 'i', 'z', 'Y', 'J', 'H', 'K']
zp = numpy.array([16.75,15.957,15.0,14.563,14.259,14.162,13.955,13.636,13.525])

def make_images(model='A', noiselevel=5,
                bandsel=['u', 'g', 'r', 'i', 'z', 'Y', 'J', 'H', 'K']):
    
    noisebands = 10**(-0.4*(zp-15.0)) * noiselevel

    noise = []
    for n in noisebands:
        noise.append(numpy.random.normal(0.0, n, shape))

    gals = glob('model%s.galfit'%model)

    for g in gals:
        os.system('galfit %s'%g)
        imgname = g.replace('.galfit', '')
        img = pyfits.open(imgname+'.fits')
        for j, b in enumerate(bands):
            if b in bandsel:
                ext = img['MODEL_'+b]
                print ext.name, j, noisebands[j]
                ext.data += noise[j]
                ext.writeto(imgname+'_%i%s_n%i.fits'%(j+1, b, noiselevel), clobber=True)

if __name__ =='__main__':
    make_images('A', 5)
    make_images('A', 50, ['H'])
    make_images('B', 5)
    make_images('B', 50, ['H'])
    make_images('C', 5)
    make_images('D', 5)
