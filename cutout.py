import pandas as pd
from astropy.io import fits
from astropy import wcs
import matplotlib.pyplot as plt
CUTOUT_SIZE = 10
#Assuming PyBDSM has already been run to generate source catalog
header = "Source_id, Isl_id, RA, E_RA, DEC, E_DEC, Total_flux, E_Total_flux, Peak_flux, E_Peak_flux, RA_max, E_RA_max, DEC_max, E_DEC_max, Maj, E_Maj, Min, E_Min, PA, E_PA, Maj_img_plane, E_Maj_img_plane, Min_img_plane, E_Min_img_plane, PA_img_plane, E_PA_img_plane, DC_Maj, E_DC_Maj, DC_Min, E_DC_Min, DC_PA, E_DC_PA, DC_Maj_img_plane, E_DC_Maj_img_plane, DC_Min_img_plane, E_DC_Min_img_plane, DC_PA_img_plane, E_DC_PA_img_plane, Isl_Total_flux, E_Isl_Total_flux, Isl_rms, Isl_mean, Resid_Isl_rms, Resid_Isl_mean, S_Code".split(', ')

catalog = pd.read_csv('R05D45_5x5.MOSAIC.pybdsm.srl', skiprows=6, names=header)
data = fits.open('R05D45_5x5.MOSAIC.pybdsm_gaus_model.fits')[0].data[0][0]
w = wcs.WCS('R05D45_5x5.MOSAIC.pybdsm_gaus_model.fits')

for i in range(len(catalog)):
    RA = catalog.iloc[i]['RA']
    DEC = catalog.iloc[i]['DEC']

    pix = w.wcs_world2pix(RA,DEC, 1.0, 1.0, 1)
    X_POS = int(pix[0])
    Y_POS = int(pix[1])

    if((X_POS - CUTOUT_SIZE) < 0):
        X_MIN_RANGE = 0
    else:
        X_MIN_RANGE = X_POS - CUTOUT_SIZE 

    if((X_POS + CUTOUT_SIZE) > data.shape[0]):
        X_MAX_RANGE = data.shape[0]
    else:
        X_MAX_RANGE = X_POS + CUTOUT_SIZE 

    if((Y_POS - CUTOUT_SIZE) < 0):
        Y_MIN_RANGE = 0
    else:
        Y_MIN_RANGE = Y_POS - CUTOUT_SIZE 

    if((Y_POS + CUTOUT_SIZE) > data.shape[1]):
        Y_MAX_RANGE = data.shape[1]
    else:
        Y_MAX_RANGE = Y_POS + CUTOUT_SIZE 

    plt.imsave('CUTOUTS/'+str(RA)+','+str(DEC)+'.jpg', data[Y_MIN_RANGE:Y_MAX_RANGE,X_MIN_RANGE:X_MAX_RANGE], cmap='gist_heat')
