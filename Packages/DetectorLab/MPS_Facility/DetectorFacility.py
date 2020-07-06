# SOLAR ORBITER PHI/METIS
# Camera Characterization Facility - Detector Chamber
# Python Script Program
#
# Filename:     DetectorFacility.py
# Description:  Functions and Definitions regarding Detector Chamber Facility
# Author:       K. Heerlein / MPS
# Date:         2017_09_08
# Version:      1.0
# History:      2017_09_08 - First Issue


import numpy as np
from Helpers import Helpers
#from ISPHI import DEFINITIONS_DATA_EVALUATION as defs
from Common import DEFS_DATA_EVAL as comdefs
import math
#from numpy.polynomial.polynomial import polyval

# PD correctioon 627nm with HPWR LED: ----------------------------------------------------
# If the PD current at Sphere (Keithley, having negative values) is used for the PTC plot,
# with 627nm Filter and red HPWR LED, the effictive photon flux at the detector
# has to be corrected by formula : y = -1.364E+00x2 + 6.622E-04x - 2.414E-10
# The reason is that the red HPWR LED has a slight shift in Wl at higher power and
# the filter blocks more light
# The ratio was measured by K. Heerlein, 2016_04
# Reference: "2016_11_22_Measurement of Relation between PD Sphere to PD Focal Plane 617.30nm.xls"
# the correction formula to be applied is: y= -1.364E+00x2 + 6.622E-04x - 2.414E-10

cst_filte627nm_redLed_corr_a2 = -1.364E+00
cst_filte627nm_redLed_corr_a1 = 6.622E-04
cst_filte627nm_redLed_corr_b = - 2.414E-10

def CorrectPD_Current_627nm(ArrPdCurr):
    print('correcting PD data for 617nm filter ...')


    # no! this is done previously x =np.multiply(ArrPdCurr,-1)
    x = np.reshape(ArrPdCurr, (len(ArrPdCurr)))
    print(x)
    '''x=(x ** 2 * cst_filte627nm_redLed_corr_a2 )
    print(x)
    x=x * cst_filte627nm_redLed_corr_a1
    print(x)
    Arr = (x**2 * cst_filte627nm_redLed_corr_a2    + x * cst_filte627nm_redLed_corr_a1  + cst_filte627nm_redLed_corr_b) * -1E9
    print(Arr)
    '''
    Arr = np.polynomial.polynomial.polyval(x, [cst_filte627nm_redLed_corr_b,cst_filte627nm_redLed_corr_a1,cst_filte627nm_redLed_corr_a2]) # p(x) = c_0 + c_1 * x + ... + c_n * x^n
    Arr = np.reshape(Arr, (len(Arr), 1))
    print(Arr)
    #Arr = [x**2 * filte627nm_redLed_corr_a2 + x * filte627nm_redLed_corr_a1 + filte627nm_redLed_corr_b for x in ArrPdCurr]

    return Arr
# _PD correctioon 627nm with HPWR LED: ----------------------------------------------------


# PD ratio intensity at FocalPlane (Oriel) w.r.t intensity in sphere (Keitley) ----------------------------------------------------
# the ratio was measured by K. Heerlein, 2016_04
# Reference: "2016_04_21_Scan Focal Plane Photodiode.xls"

cst_RatioPD_Sphere_to_PD_FocalPlane= 150.7


cst_electroncharge=1.6*1E-19

cst_Area_PD_HamamatsuS1337=49.916 # mm^2
cst_Sens_factor_PD_Area_HamamatsuS1337=0.0006
cst_Sens_offset_PD_Area_HamamatsuS1337=-0.0254

def CalcSensitivityofPD(Wavelength):
    y=cst_Sens_factor_PD_Area_HamamatsuS1337*Wavelength*1E9+cst_Sens_offset_PD_Area_HamamatsuS1337
    return y # Sensitivity in [A/W]

cst_c=2.998*1E8 # m/s speed of light
cst_h=6.626*1E-34 # Planck quantum

cst_Area_ISPHI_pixel=1E-4 #mm^2
cst_electronspersecond=6.24151*1E18

cst_sKeithley = 'KEITHLEY='
cst_sOriel = 'ORIEL='


def CalcPhotonEnergy(Wavelength):
    # Photon Energy= h x c / lambda [J]
    Ph_Energy=cst_h*cst_c /  Wavelength
    return Ph_Energy


# correction factor: photodiode location is not in focal plane, but 175mm in front
# 1/r2
#cst_corr_PDPosition_FocalPlane=(1133/1308)**2 # assuming integrating Sphere backside as location at maximum intensity
cst_corr_PDPosition_FocalPlane=(853/1028)**2 # assuming integrating Sphere opening as location at maximum intensity


def CalcISPHIPhotonFluxperPixel(refdiodeCurrent,Wavelength,Texp):

    # PD PWR = PD Current/PD Sensitivity
    # ->
    # NoofphotonsPD = PD PWR/Ph_Energy
    # ->
    # NoofphotonsISPHIPixel = NoofphotonsPD * AreaPixel/AREA_PD *Texp
    sensitivityPD=CalcSensitivityofPD(Wavelength)
    PWR_PD=refdiodeCurrent/sensitivityPD
    NoofphotonsPD=PWR_PD/CalcPhotonEnergy(Wavelength)*cst_corr_PDPosition_FocalPlane
    NoofphotonsISPHIPixel=NoofphotonsPD*cst_Area_ISPHI_pixel/cst_Area_PD_HamamatsuS1337
    y = float(Texp) * NoofphotonsISPHIPixel
    return y


def getDataPD(callerdata, RSLTS, b_usePDFocalPlane):
    import math
    if not (comdefs.cst_PD_ORIEL in callerdata):
        print('no PD data available')
        x_intensity_FocalPlane = []
    else:

        # the PD st sphere has inverted polarity and is normally read via the Keithley instrument
        # during measurement in 2016 (SOLO/PHI/METIS)idx the Oriel picoamperemeter was used to read the PD in the sphere
        # these measurements can be distinguished by having a negative polarity in the Oriel reading

        #if math.isnan(data[comdefs.cst_PD_KEITHLEY][0]): b_usePDFocalPlane=True # old dataset that used the Oriel Reading
        b_only_Orieldata = False
        data = {}
        b_filtercorrection = False
        if callerdata == []:  #use results
            if b_usePDFocalPlane == False:
                # if the High Power LED 627nm with the 627nm filter was used, data has to be corrected
                # try to get info about lamp used
                s1 = ''
                s2 = ''
                s3 = Helpers.getvalue_in_RSLTS(RSLTS, comdefs.cst_Filter)  # was: s3 = RSLTS[comdefs.cst_Filter].value
                if comdefs.cst_Lamp in RSLTS:
                    s1 = str(Helpers.getvalue_in_RSLTS(RSLTS, comdefs.cst_Lamp))
                if comdefs.cst_LampWavelength in RSLTS:
                    s2 = str(Helpers.getvalue_in_RSLTS(RSLTS, comdefs.cst_LampWavelength))
                if ('LED' in (s1 or s2)) and (('617.30nm' in (s1 or s2) or ('617.30nm' in s3))):
                    b_filtercorrection = True
            data[comdefs.cst_PD_ORIEL] = Helpers.getarray_from_RSLTS(RSLTS,comdefs.cst_PD_ORIEL)
            data[comdefs.cst_PD_KEITHLEY] = Helpers.getarray_from_RSLTS(RSLTS, comdefs.cst_PD_KEITHLEY)
        else:
            if b_usePDFocalPlane == False:
                # if the High Power LED 627nm with the 627nm filter was used, data has to be corrected
                # try to get info about lamp used
                s1 = ''
                s2 = ''
                val = Helpers.getvalue_in_RSLTS(callerdata, comdefs.cst_Filter)

                if isinstance(val, list) and (len(val)>0):
                    val = val[0]
                    s3 = val  # was: s3 = RSLTS[comdefs.cst_Filter].value
                else:
                    s3=''

                if comdefs.cst_Lamp in callerdata:
                    val = Helpers.getvalue_in_RSLTS(callerdata, comdefs.cst_Lamp)
                    if isinstance(val,list):
                        val = val[0]
                    s1 = str(val)
                if comdefs.cst_LampWavelength in callerdata:
                    val = Helpers.getvalue_in_RSLTS(callerdata, comdefs.cst_LampWavelength)
                    if isinstance(val,list):
                        val = val[0]
                    s2 = str(val)
                if ('LED' in (s1 or s2)) and (('617.30nm' in (s1 or s2) or ('617.30nm' in s3))):
                    b_filtercorrection = True

            if isinstance(callerdata[comdefs.cst_PD_ORIEL],Helpers.RSLT):
                data[comdefs.cst_PD_ORIEL] = callerdata[comdefs.cst_PD_ORIEL].value
                data[comdefs.cst_PD_KEITHLEY] = callerdata[comdefs.cst_PD_KEITHLEY].value
            else:
                data[comdefs.cst_PD_ORIEL] = callerdata[comdefs.cst_PD_ORIEL]
                data[comdefs.cst_PD_KEITHLEY] = callerdata[comdefs.cst_PD_KEITHLEY]

        if np.average(data[comdefs.cst_PD_ORIEL]) < 0: # normally it is measures the focal plane annd is positive, if not, the PD current at in the sphere was measured
            # this indicates that the PD in the Sphere was read via the Oriel instrument
            RSLTS['PD_USED'] = Helpers.RSLT('PD current', ' measured in Int. Sphere !', '', '{}','')
            # data from Sphere is acquired with Oriel
            if (isinstance(data[comdefs.cst_PD_ORIEL], list)):
                x_intensity_Sphere = [float(i)*-1 for i in data[comdefs.cst_PD_ORIEL]]  # convert strings to floats
            else:
                x_intensity_Sphere = float(data[comdefs.cst_PD_ORIEL])*-1  # convert strings to floats
            b_only_Orieldata = True
        else:
            # get data for focal plane and sphere
            if (isinstance(data[comdefs.cst_PD_KEITHLEY],list)):
                x_intensity_Sphere = [float(i)*-1 for i in data[comdefs.cst_PD_KEITHLEY]] #convert strings to floats
            else:
                x_intensity_Sphere = float(data[comdefs.cst_PD_KEITHLEY])*-1  # convert strings to floats
            if (isinstance(data[comdefs.cst_PD_ORIEL],list)):
                x_intensity_FocalPlane = [float(i) for i in data[comdefs.cst_PD_ORIEL]] #convert strings to floats
            else:
                x_intensity_FocalPlane = float(data[comdefs.cst_PD_ORIEL])  # convert strings to floats


        if  math.isnan(x_intensity_Sphere[0]): b_usePDFocalPlane = True
        if b_usePDFocalPlane:
            RSLTS['PD_USED'] = Helpers.RSLT('PD current ', 'measured near Focal Plane !', '', '{}','')
            s = Helpers.printresult(RSLTS['PD_USED'])
        else:
            # to get the PD effective current at the focal plane
            # the ratio between PD_FP and PD_Spaher has to be applied
            print('applying ratio 150 between PD_FP and PD_Sphere ..')
            RSLTS['PD_CORRECTION'] = Helpers.RSLT('PD curr. correction: divided by ',cst_RatioPD_Sphere_to_PD_FocalPlane, '', '{:7.1f}', '')
            s = Helpers.printresult(RSLTS['PD_CORRECTION'])
            x_intensity_FocalPlane = np.divide(x_intensity_Sphere, cst_RatioPD_Sphere_to_PD_FocalPlane)

            # Note: when using the LED with the narrow band 617nm filter
            # the relation between PD current at sphere to PD current at Focal plane may shift with the operating current
            # of the LED !
            # a correction formula has to be added then !!!
            if b_filtercorrection == True:
                print('correcting for 617nm filter..')
                RSLTS['PD_CORRECTION'] = Helpers.RSLT('PD curr.', ' corrected for 617nm Filter  !', '', '{}', '')
                s = Helpers.printresult(RSLTS['PD_CORRECTION'])
                # correct red LED, 627nm filter
                x_intensity_FocalPlane = CorrectPD_Current_627nm(x_intensity_Sphere)

            '''if RSLTS[comdefs.cst_LampWavelength].value == 'Xenon':
                print('Xenon run  .. keep PD data untouched')
                x_intensity_FocalPlane = x_intensity_Sphere  # diodes where swapped for the measurement
            
            elif (RSLTS[comdefs.cst_LampWavelength].value == 'LED 627nm'):
                    #x_intensity_FocalPlane = np.reshape(x_intensity_FocalPlane, (len(x_intensity_FocalPlane), 1))
            else:
               exit('getDataPD - Error - lamp wavelength not defined ! - expected "LED 627nm" or "Xenon" ')
            '''
        x_intensity_FocalPlane = np.reshape(x_intensity_FocalPlane, (len(x_intensity_FocalPlane)))
        print(x_intensity_FocalPlane)
    RSLTS[comdefs.cst_IntensityFocalPlane] = Helpers.RSLT(comdefs.cst_IntensityFocalPlane,x_intensity_FocalPlane,'','','')
    return  RSLTS #data


def GetWavelengthUsed(FitsInfoFilter,FitsInfoWavelength):
    try:

        if isinstance(FitsInfoFilter, Helpers.RSLT):
            if isinstance(FitsInfoFilter.value,list):
                FitsInfoFilter = FitsInfoFilter.value[0]
                FitsInfoWavelength = FitsInfoWavelength.value[0]
            else:
                FitsInfoFilter = FitsInfoFilter.value
                FitsInfoWavelength = FitsInfoWavelength.value
        if 'empty' in FitsInfoFilter:
            if 'LED 627nm' in FitsInfoWavelength:
                WL=627*1E-9
            elif 'Xenon' in FitsInfoWavelength:
                WL = 500 * 1E-9
            else:
                WL = Helpers.RemoveNondigits(FitsInfoWavelength)
                WL=WL*1E-9
        else:
            WL=Helpers.RemoveNondigits(FitsInfoFilter)
            WL=float(WL)*1E-9
    except:
        WL=550E-9
    return WL




