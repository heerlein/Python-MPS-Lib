

import matplotlib.pyplot as plt
import os
import numpy as np
from Packages.Helpers  import Helpers
from Packages.FITS import fits_handling
from Packages.PDF import pdf_routines
from Packages.Plotting import Plotting
from Packages.ISPHI import DEFINITIONS_DATA_EVALUATION as defs
from Packages.ISPHI import  ISPHI_Decode_Fits_Info
from Packages.ISPHI import  ISPHI_Processor
from Packages.DetectorLab import DetectorFacility as DF
from Packages.Common import DEFS_DATA_EVAL as comdefs
# MEAN_data and VAR_data are arrays of shape [0:number of steps on measurements sequence,rows,columns]

def showMeanVarianceofSinglePixel(RSLTS,MEAN_data, VAR_data, r, c, pdf_Report,HardwareInfo, Idx_PTC_sat,doclevel ):
    Title = HardwareInfo + 'Pixel: row: {} , column: {}'.format(r, c)
    supTitle= 'Photon Transfer Curve: Mean - Variance'
    numcolumns=MEAN_data.shape[2]
    numrows = MEAN_data.shape[1]

    pixelno=int(r * (numcolumns) + c)
    idx_cg_ptc_min=RSLTS['IDX_CG_PTC_MIN'].value[pixelno]
    idx_cg_ptc_max=RSLTS['IDX_CG_PTC_MAX'].value[pixelno]


    cg_slope = RSLTS['CG_PIXELS'].value[pixelno]
    cg_err = RSLTS['CG_PIXELS_ERR'].value[pixelno]
    fig, a = Plotting.ISPHI_Makeplot_PTC_Pixel(MEAN_data[0:, r, c], VAR_data[0:, r, c], supTitle, Title, Idx_PTC_sat,
                                               idx_cg_ptc_min, idx_cg_ptc_max,cg_slope,cg_err)
    buf = Plotting.savefigtobuf(fig)
    pdf_Report.addImageBuf(buf, 14)  # plt.scatter(MEAN_data[0:,i],VAR_data[0:,i])
    pdf_Report.doHeading('PTC of Pixel: ' + 'row: {} , column: {}'.format(r, c), 'figure')

    pdf_Report.doHeading('Results: PTC of Pixel: ' + 'row: {} , column: {}'.format(r, c), 'h'+str(doclevel))
    atuple = comdefs.tuple_single_pixel_PTC
    atuple=sorted(atuple)
    astr = Helpers.GetResults_from_Tuple_index(RSLTS,pixelno, atuple)
    print(astr)
    pdf_Report.write_code(astr, 10)
    pdf_Report.PageBreak()  # start on new page

def showPhotonsvsSensorSignalofSinglePixel(RSLTS,NoofPhotonsperPixel, MEAN_data, r, c, pdf_Report,HardwareInfo, Idx_PTC_sat,doclevel ):
    Title = HardwareInfo + 'Pixel: row: {} , column: {}'.format(r, c)
    numcolumns=MEAN_data.shape[2]
    numrows = MEAN_data.shape[1]

    pixelno=int(r * (numcolumns) + c)

    cg_ph_slope = RSLTS['CG_PHOTON'].value[pixelno]
    cg_ph_err = RSLTS['CG_PHOTON_ERR'].value[pixelno]

    idx_cg_ptc_min=RSLTS['IDX_CG_PTC_MIN'].value[pixelno]
    idx_cg_ptc_max=RSLTS['IDX_CG_PTC_MAX'].value[pixelno]
    fig = Plotting.ISPHI_Makeplot_PhotonsvsSignal(MEAN_data[0:len(NoofPhotonsperPixel), r, c],NoofPhotonsperPixel,Title,cg_ph_slope, cg_ph_err)# idx_cg_ptc_min,int(0.3*len(NoofPhotonsperPixel)))
    buf = Plotting.savefigtobuf(fig)
    pdf_Report.doHeading('Signal [ph] vs. Pixel Mean Signal [DN]: ' + 'row: {} , column: {}'.format(r, c), 'figure')
    pdf_Report.addImageBuf(buf, 14)  # plt.scatter(MEAN_data[0:,i],VAR_data[0:,i])

    pdf_Report.doHeading('Results: Absolute Signal [ph] vs. Pixel Mean Signal [DN]: ' + 'row: {} , column: {}'.format(r, c), 'h'+str(doclevel))
    atuple = comdefs.tuple_single_pixel_PhotonsvsSensorSignal
    atuple=sorted(atuple)
    astr = Helpers.GetResults_from_Tuple_index(RSLTS,pixelno, atuple)
    print(astr)
    pdf_Report.write_code(astr, 10)
    pdf_Report.PageBreak()  # start on new page


def scatterplot(x,y,Title,item, xaxis_label,yaxis_label,pdf_Report, Heading):
    fig, a = Plotting.prep_Plot()
    plt.scatter(x, y, c="b", alpha=0.5, marker='.',label=item)
    plt.grid(which='minor', alpha=0.2)
    plt.grid(which='major', alpha=0.5)
    a.legend()
    plt.title(Title)
    plt.xlabel(xaxis_label)
    plt.ylabel(yaxis_label)
    #pylab.show()
    plt.sca(a)  # return to first axis in case further data shall be plotted
    buf = Plotting.savefigtobuf(fig)
    pdf_Report.doHeading(Heading, 'figure')
    pdf_Report.addImageBuf(buf, 14)  # plt.scatter(MEAN_data[0:,i],VAR_data[0:,i])
    return fig,a

# used by Camera_Characterization_Functions.getresultsMeanVariance_asArray
def showscatterplot_pixels(Title,item,RSLTS,unit,rangemin,rangemax,pdf_Report):

    x = list(range(len(RSLTS[item].value)))
    x=x[rangemin:rangemax]
    y= RSLTS[item].value[rangemin:rangemax]
    Heading=item+'- Pixels {:6.0f} to {:6.0f}'.format(rangemin,rangemax)
    xaxis_label = "Pixel No."
    yaxis_label = item+' '+unit
    fig,a=scatterplot(x,y,Title,item,xaxis_label,yaxis_label, pdf_Report,Heading)
    return fig,a

# used by Camera_Characterization_Functions.getresultsMeanVariance_asArray
def showscatterplotylog(Title,item,RSLTS,unit,rangemin,rangemax,pdf_Report):
    fig, a = Plotting.prep_Plot()
    x = list(range(len(RSLTS[item].value)))

    plt.semilogy(x[rangemin:rangemax], RSLTS[item].value[rangemin:rangemax], c="b", alpha=0.5, marker='.',label=item)

    plt.grid(which='minor', alpha=0.2)
    plt.grid(which='major', alpha=0.5)
    a.legend()
    plt.title(Title)
    plt.xlabel("Pixel No.")
    plt.ylabel(item+' '+unit)
    #pylab.show()
    plt.sca(a)  # return to first axis in case further data shall be plotted
    buf = Plotting.savefigtobuf(fig)
    pdf_Report.addImageBuf(buf, 14)  # plt.scatter(MEAN_data[0:,i],VAR_data[0:,i])
    pdf_Report.doHeading(item + '- Pixels {:6.0f} to {:6.0f}'.format(rangemin, rangemax), 'figure')
    return fig,a


# todo avoid to store the RSLTS names for each pixel
# todo it has to be stored in a list
def getresultsMeanVariance(AVG_MEAN_data, VAR_MEAN_ydata, NoofPhotonsperPixel, biaswassubtracted = False):
    localRSLTS = {}
    print('Working on PTC and Linearity Results ...')
    if biaswassubtracted == False:
        Biaslvl = AVG_MEAN_data[0]
        readNoiseVariance = VAR_MEAN_ydata[0]
        MeanwithoutBias = [x - Biaslvl for x in AVG_MEAN_data]


    # find saturation level of ptc
    # sat=np.max(y)

    # results measured in the specific sector
    Idx_PTC_sat = np.argmax(VAR_MEAN_ydata,axis=0)
    # if data has no detectable saturation level, use saturation at 0.7 the length of data
    #2020_01_07 if Idx_PTC_sat < int(0.5*len(VAR_MEAN_ydata)): Idx_PTC_sat = int(0.7*len(VAR_MEAN_ydata))
    localRSLTS[comdefs.kw_IDX_PTC_SAT] = Helpers.RSLT('Index of Saturation (PTC) ', Idx_PTC_sat, '[idx]', '{:7d}','')
    #Helpers.printresult(localRSLTS['IDX_PTC_SAT'])

    Idx_half_PTC_sat = int(np.argmax(AVG_MEAN_data[1:] >= (0.5 * AVG_MEAN_data[Idx_PTC_sat])))
    localRSLTS[comdefs.kw_IDX_HALF_PTC_SAT] = Helpers.RSLT('Index of half Saturation (PTC) ', Idx_half_PTC_sat, '[idx]', '{:7.0f}','')
    #Helpers.printresult(localRSLTS['IDX_HALF_PTC_SAT'])

    Sat_Level_DN = AVG_MEAN_data[Idx_PTC_sat]
    localRSLTS[comdefs.kw_SAT_LVL_PTC] = Helpers.RSLT('PTC Saturation Level ', Sat_Level_DN, '[DN]', '{:7.0f}','')

    max_level_DN = np.amax(AVG_MEAN_data)
    localRSLTS[comdefs.kw_MAX_LVL] = Helpers.RSLT('Maximum Level ', max_level_DN, '[DN]', '{:7.0f}','')

    # get first indexe where saturation level is 70% of the saturation level
    idx_cg_ptc_max = int(np.argmax(AVG_MEAN_data[0:] >= (comdefs.cst_PTC_H * AVG_MEAN_data[Idx_PTC_sat])))
    astr = 'Index {:<4.0f}% of Sat.Level: '.format(comdefs.cst_PTC_H * 100) + '{:>6.0f} '.format(comdefs.cst_PTC_H)
    localRSLTS[comdefs.kw_IDX_CG_PTC_MAX] = Helpers.RSLT(astr, idx_cg_ptc_max, '[idx]', '{:7.0f}','')
    #Helpers.printresult(localRSLTS['IDX_CG_PTC_MAX'])

    # get first indexe where saturation level is >=0% of the saturation level
    idx_cg_ptc_min = int(np.argmax(AVG_MEAN_data[0:] >= (comdefs.cst_PTC_L * AVG_MEAN_data[Idx_PTC_sat])))
    astr = 'Index {:<4.0f}% of Sat.Level: '.format(comdefs.cst_PTC_L * 100) + '{:>6.0f} '.format(comdefs.cst_PTC_L)
    localRSLTS[comdefs.kw_IDX_CG_PTC_MIN] = Helpers.RSLT(astr, idx_cg_ptc_min, '[idx]', '{:7.0f}','')
    #Helpers.printresult(localRSLTS['IDX_CG_PTC_MIN'])

    astr = '{:<4.1f}% of Sat.Level: '.format(comdefs.cst_PTC_L * 100) + '{:>6.0f}'.format(
        AVG_MEAN_data[idx_cg_ptc_min])
    localRSLTS[comdefs.kw_VAL_PTC_MIN] = Helpers.RSLT(astr, AVG_MEAN_data[idx_cg_ptc_min], '[DN]', '{:7.0f}','')
    #Helpers.printresult(localRSLTS['VAL_PTC_MIN'])

    astr = '{:<4.1f}% of Sat.Level: '.format(comdefs.cst_PTC_H * 100) + '{:>6.0f}'.format(
        AVG_MEAN_data[idx_cg_ptc_max])
    localRSLTS[comdefs.kw_VAL_PTC_MAX] = Helpers.RSLT(astr, AVG_MEAN_data[idx_cg_ptc_max], '[DN]', '{:7.0f}','')
    #Helpers.printresult(localRSLTS['VAL_PTC_MAX'])

    # print('{:>2.1f}% '.format(cst_PTC_L*100)+'of PTC Saturation Level: '+'{:>5.0f}'.format(x[idx_cg_ptc_min]) + ' [DN]'+' at index '+str(idx_cg_ptc_min))
    # print('{:>2.1f}% '.format(cst_PTC_H*100)+'of PTC Saturation Level: '+'{:>5.0f}'.format(x[idx_cg_ptc_max]) + ' [DN]'+' at index '+str(idx_cg_ptc_max))
    # make linear fit in range, return the extended fit y-data and the coefficients



    print('Calculating linear regression fit for PTC ...')
    #y_VAR_MEAN_predict, cglincoefs, intercept = Helpers.linearfit(AVG_MEAN_data[1:], VAR_MEAN_ydata[1:],  idx_cg_ptc_min, idx_cg_ptc_max)

    slope, intercept, r_value, p_value, std_err = Helpers.linearfit(MeanwithoutBias[0:], VAR_MEAN_ydata[0:],  idx_cg_ptc_min, int(comdefs.cst_red_factor_slope_PTC*idx_cg_ptc_max))
    cg = slope
    cg_err = std_err/cg

    localRSLTS[comdefs.kw_cg_FitFunctionSlope] = Helpers.RSLT(
        'CG fit function slope'.format(),
        slope, '[DN/e-] +-{:5.2%}'.format(cg_err), '{:>7.5f}','')
    localRSLTS[comdefs.kw_cg_FitFunctionOffset] = Helpers.RSLT(
        'CG fit function offset)'.format(),
        intercept, '[DN]'.format(), '{:>7.5f}','')

    # intercept = intercept[0]

    # no ! ReadNoiseDN = np.sqrt(intercept[0])
    ReadNoiseDN = np.sqrt(readNoiseVariance)
    localRSLTS[comdefs.kw_READNOISEDN] = Helpers.RSLT('Read Noise ', ReadNoiseDN, '[DN]', '{:7.1f}','')
    # print(RSLTS['READNOISEDN'].unit)
    #Helpers.printresult(localRSLTS['READNOISEDN'])

    # Dynamic Resolution
    DynRes_dB = 20 * np.log10(max_level_DN / ReadNoiseDN)
    localRSLTS[comdefs.kw_DYN_RESOL] = Helpers.RSLT('Dynamic Resolution ', DynRes_dB, '[dB]', '{:7.1f}','')
    #Helpers.printresult(localRSLTS['DYN_RESOL'])
    # Effective Bit Resolution
    BitRes = np.log10(max_level_DN / ReadNoiseDN) / np.log10(2)
    localRSLTS[comdefs.kw_EFF_ADC_RESOL] = Helpers.RSLT('Effective ADC Resolution ', BitRes, '[bit]', '{:7.1f}','')
    #Helpers.printresult(localRSLTS['EFF_ADC_RESOL'])


    #print(cglincoefs)
    # Conversion Gain
    #cglincoefs[0,0]

    localRSLTS[comdefs.kw_CG] = Helpers.RSLT(
        'Conversion Gain ({:3.0f} to {:3.0f} % PTC)'.format(comdefs.cst_PTC_L * 100, comdefs.cst_PTC_H * 100),
        cg, '[DN/e-] +-{:5.2%}'.format(cg_err), '{:>7.5f}','')
    #RSLTS[Sectorname+'CG'] = Helpers.RSLT('Conversion Gain '+Sectorname+'({:2.0f} to {:3.0f} % PTC)'.format(defs.cst_PTC_L*100,defs.cst_PTC_H*100), cg, '[DN/e-]','{:>7.3f}')
    #Helpers.printresult(localRSLTS[comdefs.kw_CG])

    if NoofPhotonsperPixel != []:
        # Photon conversion gain ph/DN
        print('Calculating photon conversion gain ...')
        phslope, phintercept, ph_r_value, ph_p_value, ph_std_err = Helpers.linearfit(AVG_MEAN_data[0:],NoofPhotonsperPixel,idx_cg_ptc_min, idx_cg_ptc_max)
        ph_CG=phslope
        ph_CG_err=ph_std_err/ ph_CG
        localRSLTS[comdefs.kw_CG_PHOTON] = Helpers.RSLT(
            'Photon Conversion Gain  ({:3.0f} to {:3.0f} % PTC)'.format(comdefs.kw_PTC_L * 100, comdefs.kw_PTC_H * 100),
            ph_CG, '[ph/DN] +-{:5.2%}'.format(ph_CG_err), '{:>7.1f}','')

        localRSLTS[comdefs.kw_CG_PHOTON_ERR] = Helpers.RSLT(comdefs.kw_CG_PHOTON_ERR, ph_CG_err, '[ph/DN]'.format(ph_CG_err), '{:>7.1f}','')

    # Full Well Charge
    Sat_Level_e=Sat_Level_DN/cg
    Sat_Level_e_error=Sat_Level_DN/cg*(1-1/(1+cg_err))
    localRSLTS[comdefs.kw_FULL_WELL]=Helpers.RSLT('Full Well Charge (PTC max.) ',Sat_Level_e,'[e-] +-{:5.0f}'.format(Sat_Level_e_error),'{:7.0f}','')

    #Helpers.printresult(localRSLTS['FULL_WELL'])
    # Read Noise
    ReadNoise_e=ReadNoiseDN/cg
    ReadNoise_e_error = ReadNoiseDN/cg * (1 - 1 / (1 + cg_err))
    localRSLTS[comdefs.kw_READ_NOISE_e]=Helpers.RSLT('Read Noise ',ReadNoise_e,'[e-] +-{:5.2f}'.format(ReadNoise_e_error),'{:7.1f}','')
    #Helpers.printresult(localRSLTS['READ_NOISE_e'])

    return localRSLTS

# Function to calculate the Linearity of the data
# using the EMVA standard and expected a valid index for the PTC saturation
# IDX where the PTC saturates and CG calculated to be passed
def GetLinearityResultsEMVA_PTCSAT(x_intensity_FocalPlane, y_data, Idx_PTC_Sat, CG):
    print('-- Function - GetLinearityResults ... start  ----------------------------------')
    localRSLTS = {}
    # avoid error in case the index is higher than actual length of data
    if Idx_PTC_Sat > len(y_data):
        Idx_PTC_Sat = len(y_data)-1
    # linear regression line fit
    idx_linfit_max = np.argmax(y_data>=(comdefs.cst_LINFIT_H*y_data[Idx_PTC_Sat])) # this was used for GSENSE setups with lowest gain * comdefs.cst_red_factor_slope_PTC
    idx_linfit_min = np.argmax(y_data>=(comdefs.cst_LINFIT_L*y_data[Idx_PTC_Sat]))

    # prevent later errors
    if idx_linfit_max <= idx_linfit_min:
        idx_linfit_max = idx_linfit_min + 5

    if idx_linfit_max > (len(y_data)-1):
        idx_linfit_min= 0
        idx_linfit_max = len(y_data)-1

    localRSLTS['IDX_LINFIT_MAX'] = Helpers.RSLT('Index Linearity Max ', idx_linfit_max, '[idx]', '{:7.0f}', '')
    s=Helpers.printresult(localRSLTS['IDX_LINFIT_MAX'])
    localRSLTS['IDX_LINFIT_MIN'] = Helpers.RSLT('Index Linearity Min ', idx_linfit_min, '[idx]', '{:7.0f}', '')
    s=Helpers.printresult(localRSLTS['IDX_LINFIT_MIN'])
    print('Calculating linear regression fit for Linearity Plot ...')
    slope, intercept, r_value, p_value, std_err = Helpers.linearfit(x_intensity_FocalPlane , y_data, idx_linfit_min, int(idx_linfit_max))
    localRSLTS[comdefs.kw_LinRegCoef] = Helpers.RSLT(comdefs.kw_LinRegCoef, slope, '', '{:2.3f}', '')
    localRSLTS[ comdefs.kw_LinRegOffset] = Helpers.RSLT(comdefs.kw_LinRegOffset, intercept, '', '{:2.3f}', '')

    if np.isnan(slope):
        idx_linfit_min = 0
        slope, intercept, r_value, p_value, std_err = Helpers.linearfit(x_intensity_FocalPlane, y_data, idx_linfit_min, int(idx_linfit_max))

    localRSLTS[comdefs.kw_linearity_FitFunctionSlope] = Helpers.RSLT(
        'linearity fit function slope )'.format(),
        slope, '[] +-{:5.2%}'.format(std_err), '{:>7.5f}','')
    localRSLTS[comdefs.kw_linearity_FitFunctionOffset] = Helpers.RSLT(
        'linearity fit function offset)'.format(),
        intercept, '[DN]'.format(), '{:>7.5f}','')

    if not np.isnan(slope):
        LINy_AVG_predict = [x * slope + intercept for x in x_intensity_FocalPlane]
        # deviation from linear regression line
        dev_linearity = []
        for z in range(len(LINy_AVG_predict)):
            dev_linearity.append((y_data[z]- LINy_AVG_predict[z]) / (y_data[Idx_PTC_Sat]*comdefs.cst_def_linearity_ref)*100)
        #was dev_linearity = (y_data- LINy_AVG_predict) / (y_data[Idx_PTC_Sat]*comdefs.kw_def_linearity_ref)*100
    else:
        LINy_AVG_predict = 0
        dev_linearity = 0
    # minimum and maximum nonlinearity in range of Min%_Level to Max%Level according to EMVA Standard
    dev_EMVA_max=np.max(dev_linearity[idx_linfit_min:idx_linfit_max])
    dev_EMVA_min=np.min(dev_linearity[idx_linfit_min:idx_linfit_max])
    Linearity_Error_EMVA=(dev_EMVA_max-dev_EMVA_min)/2 # EMVA Standard
    localRSLTS['LIN_ERR_EMVA']=Helpers.RSLT('Linearity Err. ({:3.0f} to {:3.0f} % PTC)'.format(comdefs.cst_LINFIT_L*100,comdefs.cst_LINFIT_H*100), Linearity_Error_EMVA, '[%]', '+-{:5.2f}', '')
    s=Helpers.printresult(localRSLTS['LIN_ERR_EMVA'])

    # Linerity Full Range 0 to 100%
    dev_PTC_FR_max=np.max(dev_linearity[0:Idx_PTC_Sat])
    dev_PTC_FR_min=np.min(dev_linearity[0:Idx_PTC_Sat])
    Linearity_Error_FullRange=(dev_PTC_FR_max-dev_PTC_FR_min)/2 # EMVA Standard
    localRSLTS['LIN_ERR_FULLRANGE']=Helpers.RSLT('Linearity Err. ({:3.0f} to {:3.0f} % PTC)'.format(0, 100), Linearity_Error_FullRange, '[%]', '+-{:5.2f}', '')
    Helpers.printresult(localRSLTS['LIN_ERR_FULLRANGE'])

    # Linear Range +-1%
    amax=np.amax(dev_linearity)
    print('Searching for maximum positive deviation from linearity: ' + str(amax))
    try:

        Idx_Linearity_Exceeds_two_Percent= next(x[0] for x in enumerate(dev_linearity) if (amax-x[1]) > 2)
        print('Index where linearity exceeds 2% found at: {:2.0f} value: {:2.0f}'.format(Idx_Linearity_Exceeds_two_Percent,dev_linearity[Idx_Linearity_Exceeds_two_Percent]))
        print('total dev. of 2% violated:' + str(dev_linearity[Idx_Linearity_Exceeds_two_Percent]))
        localRSLTS[comdefs.kw_IDX_LIN_EXCEEDING_TWOPERCENT] = Helpers.RSLT('Index Linearity exceeds 2% ' , Idx_Linearity_Exceeds_two_Percent, '[idx]','{:7.0f}','')
        # just check if calculation was correct
        dev_LR_max=np.max(dev_linearity[0:Idx_Linearity_Exceeds_two_Percent])
        dev_LR_min=np.min(dev_linearity[0:Idx_Linearity_Exceeds_two_Percent])
        print('dev_LR_min: '+str(dev_LR_min))
        print('dev_LR_max: '+str(dev_LR_max))
        localRSLTS['DEV_LR_MIN'] = Helpers.RSLT('Index Linearity Min' , dev_LR_min, '[idx]','{:7.0f}','')
        localRSLTS['DEV_LR_MAX'] = Helpers.RSLT('Index Linearity Max' , dev_LR_max, '[idx]','{:7.0f}','')
        Linearity_Error_OnePercent = (dev_LR_max - dev_LR_min) / 2
        print('Cross Check: Linearity Error +-1%: {:2.2f}%'.format(Linearity_Error_OnePercent))
        localRSLTS['LIN_ERR_ONEPERCENT'] = Helpers.RSLT('Linearity Err. +-1%' , Linearity_Error_OnePercent, '[%]','{:7.2f}','')
        startindex=1
        Linrange_max=np.max(y_data[startindex:Idx_Linearity_Exceeds_two_Percent-startindex])
        Linrange_min=np.min(y_data[startindex:Idx_Linearity_Exceeds_two_Percent-startindex])
        #cg=RSLTS[comdefs.kw_CG].value
        Linear_Range=(Linrange_max-Linrange_min)/CG
        localRSLTS['LIN_RANGE']=Helpers.RSLT('Linear Range +-1% ',Linear_Range,'[e-]','{:7.0f}','')
        Helpers.printresult(localRSLTS[comdefs.kw_LIN_RANGE])
    except:
        array_length = len(y_data)-1
        if array_length > 100 :array_length = 99 #on runs where  we had additional zero exp. at end, do not use those
        Idx_Linearity_Exceeds_two_Percent = array_length
        startindex = 1
        Linrange_max=np.max(y_data[startindex:Idx_Linearity_Exceeds_two_Percent-startindex])
        Linrange_min=np.min(y_data[startindex:Idx_Linearity_Exceeds_two_Percent-startindex])

        #cg=RSLTS['CG'].value
        Linear_Range=(Linrange_max-Linrange_min)/CG
        print('Index where linearity exceeds 2% not found, using max deviation at: {:2d} value: {:2.3f}'.format(
            Idx_Linearity_Exceeds_two_Percent, amax))
        dev_LR_max=np.max(dev_linearity[0:array_length])
        dev_LR_min=np.min(dev_linearity[0:array_length])
        localRSLTS['DEV_LR_MIN'] = Helpers.RSLT('Index Linearity Min' , dev_LR_min, '[idx]',
                                                       '{:7.0f}','')
        localRSLTS['DEV_LR_MAX'] = Helpers.RSLT('Index Linearity Max' , dev_LR_max, '[idx]',
                                                       '{:7.0f}','')

        localRSLTS['IDX_LIN_EXCEEDING_TWOPERCENT'] = Helpers.RSLT('Index Linearity exceeds 2% ' , Idx_Linearity_Exceeds_two_Percent, '[idx]',
                                                       '{:7.0f}','')
        Linearity_Error_OnePercent = (dev_LR_max - dev_LR_min) / 2
        localRSLTS['LIN_ERR_ONEPERCENT'] = Helpers.RSLT('Linearity Err. +-1%' , Linearity_Error_OnePercent, '[%]',
                                                       '{:7.2f}','')
        localRSLTS['LIN_RANGE']=Helpers.RSLT('Linear Range +-1% ',Linear_Range,'[e-]','{:6.0f}','')

    print('-- Function - GetLinearityResults ... done ----------------------------------')
    return localRSLTS, dev_linearity, LINy_AVG_predict


# Function to calculate the Linearity of the data
# using the a provided start and end index
def GetLinearityResults_start_end(x_intensity_FocalPlane,y_data,Idx_Start, Idx_End, CG):
    print('-- Function - GetLinearityResults ... start  ----------------------------------')
    localRSLTS = {}
    # avoid error in case the index is higher than actual length of data
    if Idx_End > len(y_data):
        Idx_End = len(y_data)-1
    # linear regression line fit
    idx_linfit_max=Idx_End
    idx_linfit_min=Idx_Start

    # prevent later errors
    if idx_linfit_max <= idx_linfit_min:
        idx_linfit_max = idx_linfit_min + 5

    if idx_linfit_max > (len(y_data)-1):
        idx_linfit_min= 0
        idx_linfit_max = len(y_data)-1

    localRSLTS[comdefs.kw_IDX_LINFIT_MAX]=Helpers.RSLT('Index Linearity Max ',int(idx_linfit_max),'[idx]','{:7.0f}','')
    s=Helpers.printresult(localRSLTS[comdefs.kw_IDX_LINFIT_MAX])
    localRSLTS[comdefs.kw_IDX_LINFIT_MIN]=Helpers.RSLT('Index Linearity Min ',int(idx_linfit_min),'[idx]','{:7.0f}','')
    s=Helpers.printresult(localRSLTS[comdefs.kw_IDX_LINFIT_MIN])
    print('Calculating linear regression fit for Linearity Plot ...')
    idx_linfit_max_call = int(comdefs.cst_red_factor_slope_PTC*idx_linfit_max)
    if idx_linfit_max_call == 0:
        idx_linfit_max_call = idx_linfit_max
    slope, intercept, r_value, p_value, std_err = Helpers.linearfit(x_intensity_FocalPlane ,y_data, idx_linfit_min,idx_linfit_max_call)
    localRSLTS[comdefs.kw_LinRegCoef] = Helpers.RSLT(comdefs.kw_LinRegCoef, slope, '','{:2.3f}', '')
    localRSLTS[ comdefs.kw_LinRegOffset] = Helpers.RSLT(comdefs.kw_LinRegOffset, intercept, '','{:2.3f}', '')

    if np.isnan(slope):
        idx_linfit_min = 0
        slope, intercept, r_value, p_value, std_err = Helpers.linearfit(x_intensity_FocalPlane, y_data, idx_linfit_min, int(comdefs.cst_red_factor_slope_PTC*idx_linfit_max))
    if not np.isnan(slope):
        LINy_AVG_predict = [x * slope + intercept for x in x_intensity_FocalPlane]
        # deviation from linear regression line
        dev_linearity = []
        for z in range(len(LINy_AVG_predict)):
            dev_linearity.append((y_data[z]- LINy_AVG_predict[z]) / (y_data[Idx_End])*100)
        #was dev_linearity = (y_data- LINy_AVG_predict) / (y_data[Idx_PTC_Sat]*comdefs.kw_def_linearity_ref)*100
    else:
        LINy_AVG_predict = 0
        dev_linearity = 0
    # minimum and maximum nonlinearity in range of Min%_Level to Max%Level according to EMVA Standard
    if idx_linfit_min == idx_linfit_max:
        dev_max = 0
        dev_min = 0
    else:
        dev_max=np.max(dev_linearity[idx_linfit_min:idx_linfit_max])
        dev_min=np.min(dev_linearity[idx_linfit_min:idx_linfit_max])
    Linearity_Error=(dev_max-dev_min)/2 #
    localRSLTS[comdefs.kw_LIN_ERR]=Helpers.RSLT('Linearity Err. ({:3.0f} to {:3.0f} )'.format(Idx_Start,Idx_End),Linearity_Error,'[%]','+-{:5.2f}','')
    s=Helpers.printresult(localRSLTS[comdefs.kw_LIN_ERR])

    # Linerity Full Range 0 to 100%
    if Idx_End == 0:
        dev_FR_min = 0
        dev_FR_max = 0
    else:
        dev_FR_max=np.max(dev_linearity[0:Idx_End])
        dev_FR_min=np.min(dev_linearity[0:Idx_End])
    Linearity_Error_FullRange=(dev_FR_max-dev_FR_min)/2
    localRSLTS['LIN_ERR_FULLRANGE']=Helpers.RSLT('Linearity Err. ({:3.0f} to {:3.0f} )'.format(0,Idx_End),Linearity_Error_FullRange,'[%]','+-{:5.2f}','')
    Helpers.printresult(localRSLTS['LIN_ERR_FULLRANGE'])

    # Linear Range +-1%
    amax=np.amax(dev_linearity)
    print('Searching for maximum positive deviation from linearity: ' + str(amax))
    try:

        Idx_Linearity_Exceeds_two_Percent= next(x[0] for x in enumerate(dev_linearity) if (amax-x[1]) > 2)
        print('Index where linearity exceeds 2% found at: {:2.0f} value: {:2.0f}'.format(Idx_Linearity_Exceeds_two_Percent,dev_linearity[Idx_Linearity_Exceeds_two_Percent]))
        print('total dev. of 2% violated:' + str(dev_linearity[Idx_Linearity_Exceeds_two_Percent]))
        localRSLTS[comdefs.kw_IDX_LIN_EXCEEDING_TWOPERCENT] = Helpers.RSLT('Index Linearity exceeds 2% ' , Idx_Linearity_Exceeds_two_Percent, '[idx]','{:7.0f}','')
        # just check if calculation was correct
        dev_LR_max=np.max(dev_linearity[0:Idx_Linearity_Exceeds_two_Percent])
        dev_LR_min=np.min(dev_linearity[0:Idx_Linearity_Exceeds_two_Percent])
        print('dev_LR_min: '+str(dev_LR_min))
        print('dev_LR_max: '+str(dev_LR_max))
        localRSLTS['DEV_LR_MIN'] = Helpers.RSLT('Index Linearity Min' , dev_LR_min, '[idx]','{:7.0f}','')
        localRSLTS['DEV_LR_MAX'] = Helpers.RSLT('Index Linearity Max' , dev_LR_max, '[idx]','{:7.0f}','')
        Linearity_Error_OnePercent = (dev_LR_max - dev_LR_min) / 2
        print('Cross Check: Linearity Error +-1%: {:2.2f}%'.format(Linearity_Error_OnePercent))
        localRSLTS['LIN_ERR_ONEPERCENT'] = Helpers.RSLT('Linearity Err. +-1%' , Linearity_Error_OnePercent, '[%]','{:7.2f}','')
        startindex=1
        Linrange_max=np.max(y_data[startindex:Idx_Linearity_Exceeds_two_Percent-startindex])
        Linrange_min=np.min(y_data[startindex:Idx_Linearity_Exceeds_two_Percent-startindex])
        #cg=RSLTS[comdefs.kw_CG].value
        Linear_Range=(Linrange_max-Linrange_min)/CG
        localRSLTS['LIN_RANGE']=Helpers.RSLT('Linear Range +-1% ',Linear_Range,'[e-]','{:7.0f}','')
        Helpers.printresult(localRSLTS[comdefs.kw_LIN_RANGE])
    except:
        array_length = len(y_data)-1
        if array_length > 100 :array_length = 99 #on runs where  we had additional zero exp. at end, do not use those
        Idx_Linearity_Exceeds_two_Percent = array_length
        startindex = 1
        if Idx_Linearity_Exceeds_two_Percent <= 1:
            print('this dataset is too short - aborting')
            Linrange_max=1
            Linrange_min=0

        else:
            Linrange_max=np.max(y_data[startindex:Idx_Linearity_Exceeds_two_Percent-startindex])
            Linrange_min=np.min(y_data[startindex:Idx_Linearity_Exceeds_two_Percent-startindex])

        #cg=RSLTS['CG'].value
        Linear_Range=(Linrange_max-Linrange_min)/CG
        print('Index where linearity exceeds 2% not found, using max deviation at: {:2d} value: {:2.3f}'.format(
            Idx_Linearity_Exceeds_two_Percent, amax))
        if array_length == 0:
            dev_LR_max = 0
            dev_LR_min = 0
        else:
            dev_LR_max=np.max(dev_linearity[0:array_length])
            dev_LR_min=np.min(dev_linearity[0:array_length])
        localRSLTS['DEV_LR_MIN'] = Helpers.RSLT('Index Linearity Min' , dev_LR_min, '[idx]',
                                                       '{:7.0f}','')
        localRSLTS['DEV_LR_MAX'] = Helpers.RSLT('Index Linearity Max' , dev_LR_max, '[idx]',
                                                       '{:7.0f}','')

        localRSLTS['IDX_LIN_EXCEEDING_TWOPERCENT'] = Helpers.RSLT('Index Linearity exceeds 2% ' , Idx_Linearity_Exceeds_two_Percent, '[idx]',
                                                       '{:7.0f}','')
        Linearity_Error_OnePercent = (dev_LR_max - dev_LR_min) / 2
        localRSLTS['LIN_ERR_ONEPERCENT'] = Helpers.RSLT('Linearity Err. +-1%' , Linearity_Error_OnePercent, '[%]',
                                                       '{:7.2f}','')
        localRSLTS['LIN_RANGE']=Helpers.RSLT('Linear Range +-1% ',Linear_Range,'[e-]','{:6.0f}','')

    print('-- Function - GetLinearityResults ... done ----------------------------------')
    return localRSLTS, dev_linearity, LINy_AVG_predict


def getresultsMeanVariance_asArray(MEAN_data,VAR_data,HardwareInfo,pdf_Report,RSLTS,doclevel):
    print('Working on PTC and Linearity Results ...')

    # removed, is done in getPTC_and LinearityResults()
        #if not comdefs.kw_NoofPhotonsperPixel in RSLTS:
            #RSLTS = get_NoofPhotonsperPixel_Array([], RSLTS, b_usePDFocalPlane=False)
    # find saturation level of ptc
    # sat=np.max(y)
    pixelRSLTS = {}

    shape_columns=MEAN_data.shape[2]
    shape_rows = MEAN_data.shape[1]
    pixelRSLTS['SEQ_NUM_STEPS']=[]
    pixelRSLTS['SEQ_NUM_STEPS'] = Helpers.RSLT('No. of meas. steps ', MEAN_data.shape[0], '', '{:7.0f}','')
    Helpers.printresult(pixelRSLTS['SEQ_NUM_STEPS'])

    #MEAN_data=np.reshape(MEAN_data,[RSLTS['SEQ_NUM_STEPS'],int(shape_rows*shape_columns)])
    #VAR_data = np.reshape(VAR_data,[RSLTS['SEQ_NUM_STEPS'], int(shape_rows*shape_columns)])
    pixelRSLTS['IDX_PTC_SAT'] = []
    pixelRSLTS['IDX_HALF_PTC_SAT'] = []
    pixelRSLTS['SAT_LVL_PTC'] = []
    pixelRSLTS['MAX_LVL'] = []
    pixelRSLTS['IDX_CG_PTC_MAX'] = []
    pixelRSLTS['IDX_CG_PTC_MIN'] = []
    pixelRSLTS['VAL_PTC_MIN'] = []
    pixelRSLTS['VAL_PTC_MAX'] = []
    pixelRSLTS['READNOISEDN'] = []
    pixelRSLTS['DYN_RESOL'] = []
    pixelRSLTS['EFF_ADC_RESOL'] = []
    pixelRSLTS['CG'] = []
    pixelRSLTS['CG_PHOTON'] = []
    pixelRSLTS['CG_PHOTON_ERR'] = []
    pixelRSLTS[comdefs.kw_CG_PHOTON_MEAN] = []
    pixelRSLTS['FULL_WELL']=[]
    pixelRSLTS['READ_NOISE_e']=[]
    pixelRSLTS['CG_MEAN']=[]
    pixelRSLTS['FULL_WELL']=[]
    pixelRSLTS['CG_bad']=[]
    ARR = {}
    ARR['IDX_PTC_SAT'] = []
    ARR['IDX_HALF_PTC_SAT'] = []
    ARR['SAT_LVL_PTC'] = []
    ARR['MAX_LVL'] = []
    ARR['IDX_CG_PTC_MAX'] = []
    ARR['IDX_CG_PTC_MIN'] = []
    ARR['VAL_PTC_MIN'] = []
    ARR['VAL_PTC_MAX'] = []
    ARR['READNOISEDN'] = []
    ARR['DYN_RESOL'] = []
    ARR['EFF_ADC_RESOL'] = []
    ARR['CG'] = []
    ARR['CG_FIT_INTERCEPT'] = []
    ARR['CG_ERR'] = []

    ARR['CG_PHOTON'] = []
    ARR['CG_PHOTON_ERR'] = []
    ARR[comdefs.kw_CG_PHOTON_MEAN] = []

    ARR['FULL_WELL'] = []
    ARR['READ_NOISE_e'] = []
    ARR['CG_MEAN'] = []
    ARR['FULL_WELL'] = []
    ARR['CG_bad'] = []
    ARR['CG_low'] = []


    cg_bad_mask=np.zeros([shape_rows,shape_columns] ) # mask to mark pixels where cg could not be evaluated
    # cg_bad_mask=np.reshape(cg_bad_mask,[shape_rows*shape_columns,1])
    # get index where PTC is at saturation in average (full) image
    # get results of AVG full image
    VAR_MEAN=[]
    AVG_MEAN=[]

    # calculate AVG CG and PhotonCG inside rectangle without the shadowed area from the baffle
    ISPHIMASK, cst_coordinates_All=ISPHI_Decode_Fits_Info.create_ISPHI_MASKS(shape_rows, shape_columns)
    for i in range(VAR_data.shape[0]):
            VAR_MEAN.append(np.average(np.extract(ISPHIMASK['Frame_m265_'], VAR_data[i,:,:])))  #VAR_data[i,:,:]))
            AVG_MEAN.append(np.average(np.extract(ISPHIMASK['Frame_m265_'], MEAN_data[i,:,:]))) #MEAN_data[i,:,:]))

    VAR_MEAN=np.array(VAR_MEAN)
    AVG_MEAN=np.array(AVG_MEAN)

    # get results in  region of interest to provide the spatial avg
    #if not comdefs.kw_LinRegCoef in RSLTS: # if PTC and Linearity has not been analysed yet:
        # get global linearity results
    RSLTS = ISPHI_Processor.get_PTC_and_Linearity_results([], RSLTS, Section='', b_usePDFocalPlane=False)
    Idx_PTC_sat_avg = RSLTS[comdefs.kw_IDX_PTC_SAT].value
    x_IntensityFocalPlane = RSLTS[defs.cst_IntensityFocalPlane]

    ''' #this was done in get_PTC_and_Linearity_results
    Idx_PTC_sat_avg = np.argmax(VAR_MEAN, axis=0)
    print(Idx_PTC_sat_avg)

    # get first index where saturation level is 70% of the saturation level
    idx_cg_ptc_max_avg = np.argmax(AVG_MEAN >= (comdefs.kw_PTC_H * AVG_MEAN[Idx_PTC_sat_avg]))
    if idx_cg_ptc_max_avg == 0:
        print('Error - no valid maximum found in Variance -> using half of steps')
        idx_cg_ptc_max_avg = int(len(VAR_MEAN/2))
    # get first indexe where saturation level is >=0% of the saturation level
    idx_cg_ptc_min_avg = np.argmax(AVG_MEAN >= (comdefs.kw_PTC_L * AVG_MEAN[Idx_PTC_sat_avg]))
    Idx_half_PTC_sat = np.argmax(AVG_MEAN >= (0.5 * AVG_MEAN[Idx_PTC_sat_avg]))

    # calculate MEAN CG of Full image
    #VAR_data_predict, cglincoefs, intercept = Helpers.linearfit(AVG_MEAN, VAR_MEAN, idx_cg_ptc_min, idx_cg_ptc_max)
    slope, intercept, r_value, p_value, std_err = Helpers.linearfit(AVG_MEAN, VAR_MEAN, idx_cg_ptc_min_avg, idx_cg_ptc_max_avg)
    # Conversion Gain MEAN
    #cg_mean = cglincoefs[0, 0]
    cg_mean=slope
    
    phslope, phintercept, ph_r_value, ph_p_value, ph_std_err = Helpers.linearfit(AVG_MEAN, RSLTS[comdefs.kw_NoofPhotonsperPixel].value, RSLTS[comdefs.kw_IDX_CG_PTC_MIN].value, RSLTS[comdefs.kw_IDX_CG_PTC_MIN].value)
    ph_cg_mean = phslope
    ph_cg_mean_err = ph_std_err/ phslope
    #ARR[comdefs.kw_CG_MEAN].append(cg_mean)
    #print('calculated average CG: ', cg_mean)
    ARR[comdefs.kw_CG_PHOTON_MEAN].append(ph_cg_mean)
    '''

    print('stacking data ...')
    # get results for each individual pixel
    RSLTS = DF.getDataPD([], RSLTS,b_usePDFocalPlane=False)
    x_IntensityFocalPlane = RSLTS[defs.cst_IntensityFocalPlane].value
    for row in range(MEAN_data.shape[1]): # 20000 MEAN_data.shape[1]
        for column in range(MEAN_data.shape[2]):
            flagbad = False
            print('Pixel:','{:4d}-{:4d}'.format(row,column))
            localRSLTS = getresultsMeanVariance(MEAN_data[:,row,column], VAR_data[:,row,column],RSLTS[comdefs.kw_NoofPhotonsperPixel].value[0:])
            CG = localRSLTS[comdefs.kw_CG].value
            RSLTS = Helpers.StoreRSLTS(localRSLTS, RSLTS, '', int(row * column))
            localRSLTS, _ = GetLinearityResults(x_IntensityFocalPlane, MEAN_data[:,row,column], localRSLTS[comdefs.kw_IDX_PTC_SAT].value, CG)

            # todo: get linear regression map for for stddev data vs. Intensityfocalplane
            RSLTS = Helpers.StoreRSLTS(localRSLTS, RSLTS, '', int(row * column))
            
    return RSLTS


def plotCGMap_test():
    '''
            # info valid for each sector
            #print('i:',i)
            # results measured in the specific sector
            Sat_Level_DN = MEAN_data[RSLTS[comdefs.kw_IDX_PTC_SAT],row,column] # was : Idx_PTC_sat_avg
            ARR['SAT_LVL_PTC'].append(Sat_Level_DN)
            max_level_DN = np.amax(MEAN_data[:,row,column])
            ARR['MAX_LVL'].append(max_level_DN)
            # get first index where saturation level is 70% of the saturation level
            idx_cg_ptc_max = np.argmax(MEAN_data[0:,row,column] >= (comdefs.kw_PTC_H * MEAN_data[Idx_PTC_sat_avg,row,column]))
            # get first indexe where saturation level is >=0% of the saturation level
            idx_cg_ptc_min = np.argmax(MEAN_data[0:,row,column] >= (comdefs.kw_PTC_L * MEAN_data[Idx_PTC_sat_avg,row,column]))
            # error checking
            if idx_cg_ptc_max < 5:
                idx_cg_ptc_max = 5  # KH 2018_05_16, in areas of the baffle no change from light, try range 0 to 5
            if idx_cg_ptc_max <= (idx_cg_ptc_min):
                print('Error: idx_cg_ptc_max <= idx_cg_ptc_min - using idx_cg_ptc_min +1 !')
                idx_cg_ptc_max = idx_cg_ptc_min+1
            ARR['IDX_CG_PTC_MAX'].append(idx_cg_ptc_max)



            ARR['IDX_CG_PTC_MIN'].append(idx_cg_ptc_min)

            ARR['VAL_PTC_MIN'].append(MEAN_data[idx_cg_ptc_min, row,column])

            ARR['VAL_PTC_MAX'].append(MEAN_data[idx_cg_ptc_max,row,column])


            # 2018_02_15: KH modified: find slope, use intersection at 0
            x = MEAN_data[idx_cg_ptc_min:idx_cg_ptc_max-idx_cg_ptc_min, row, column]
            y = VAR_data[idx_cg_ptc_min:idx_cg_ptc_max-idx_cg_ptc_min,row,column]
            try:
                cg,cg_std_err = Helpers.findslope(x,y)
            except:
                cg = 1E-6
                cg_std_err = 1


            #slope, intercept, r_value, p_value, std_err = Helpers.linearfit(MEAN_data[0:,row,column], VAR_data[0:,row,column], idx_cg_ptc_min,    idx_cg_ptc_max)


            # 2018_02_15: KH modified: find slope, use intersection at 0
            x = MEAN_data[idx_cg_ptc_min:idx_cg_ptc_max-idx_cg_ptc_min, row, column]
            y = RSLTS[comdefs.kw_NoofPhotonsperPixel].value[idx_cg_ptc_min:idx_cg_ptc_max-idx_cg_ptc_min]
            try:
                phslope, ph_std_err = Helpers.findslope(x, y)
            except:
                phslope = 10000 # dummy, just set it to useless value
                phslope_std_err = 1

            # was: phslope, phintercept, ph_r_value, ph_p_value, ph_std_err = Helpers.linearfit(MEAN_data[0:, row, column],NoofPhotonsperPixel[0:], idx_cg_ptc_min, idx_cg_ptc_max)


            if abs(phslope) >= 1.5*ph_cg_mean:
                ARR['CG_PHOTON'].append(ph_cg_mean)
                print('Photon CG calculation >1.5x of AVG Photon CG of {:2.1f}: set to average'.format(ph_cg_mean), [row, column])
                ARR['CG_PHOTON_ERR'].append(ph_cg_mean_err)
            else:
                ARR['CG_PHOTON'].append(phslope)
                ph_CG_err = ph_std_err / phslope
                ARR['CG_PHOTON_ERR'].append( ph_CG_err)

            # Conversion Gain
            # was cg= slope
            cg_error=cg_std_err/cg # error of calculated slope in %
            print('working on pixel: x{:4d}, y{:4d}: slope:{:2.3f} +-{:5.2%}'.format(column, row, cg, cg_error))
            # if cg is below 0 or <0.5 the AVG CG -> mark as bad
            if abs(cg_error)> 0.5:
                # print('CG calculation negative: set to NaN',[row,column])
                print('CG calculation with large uncertainty of {:2.1%}: set to average:{:1.3f}'.format(abs(cg_error),cg_mean), [row, column])
                # cg=np.nan #0.001# cg_mean # if data is bad, use average cg value
                cg = cg_mean
                # do not mark the optical baffle pixels as bad
                if (row > 265) and (column > 265) and (row < 1785) and (column < 1783):
                    ARR['CG_bad'].append([row, column])
                    cg_bad_mask[row, column] = 1  # mark as bad
                    flagbad = True
            else:
                if cg <=0:
                    #print('CG calculation negative: set to NaN',[row,column])
                    print('CG calculation negative of AVG CG of {:1.3f}: set to average'.format(cg_mean), [row, column])
                    #cg=np.nan #0.001# cg_mean # if data is bad, use average cg value
                    cg = cg_mean
                    # do not mark the optical baffle pixels as bad
                    if (row > 265) and (column>265) and (row<1785) and (column<1783):
                        ARR['CG_bad'].append([row,column])
                        cg_bad_mask[row,column] = 1  # mark as bad
                        flagbad=True
                elif cg <=0.5*cg_mean:
                    print('CG calculation <50% of AVG CG of {:1.3f}: set to average'.format(cg_mean),[row,column])
                    #cg=np.nan #nan 0.001# cg_mean # if data is bad, use average cg value
                    cg = cg_mean
                    # do not mark the optical baffle pixels as bad
                    if (row > 265) and (column>265) and (row<1785) and (column<1783):
                        ARR['CG_low'].append([row, column])
                        cg_bad_mask[row,column] = 1  # mark as bad
                        flagbad = True

            if flagbad:
                ARR['CG'].append(np.nan)
                ARR['CG_ERR'].append(np.nan)
                ARR['CG_FIT_INTERCEPT'].append(np.nan)
                ARR['READNOISEDN'].append(np.nan)
                ARR['DYN_RESOL'].append(np.nan)
                ARR['EFF_ADC_RESOL'].append(np.nan)
                ARR['FULL_WELL'].append(np.nan)
                ARR['READ_NOISE_e'].append(np.nan)
            else:
                ARR['CG'].append(cg)
                ARR['CG_ERR'].append(cg_error)
                ARR['CG_FIT_INTERCEPT'].append(intercept)

                # no ! ReadNoiseDN = np.sqrt(intercept[0])
                ReadNoiseDN = np.sqrt(VAR_data[0, row, column])
                ARR['READNOISEDN'].append(ReadNoiseDN)

                # Dynamic Resolution
                DynRes_dB = 20 * np.log10(max_level_DN / ReadNoiseDN)
                ARR['DYN_RESOL'].append(DynRes_dB)

                # Effective Bit Resolution
                BitRes = np.log10(max_level_DN / ReadNoiseDN) / np.log10(2)
                ARR['EFF_ADC_RESOL'].append(BitRes)

                # Full Well Charge
                Sat_Level_e = Sat_Level_DN / cg
                ARR['FULL_WELL'].append(Sat_Level_e)

                # Read Noise
                ReadNoise_e = ReadNoiseDN / cg
                ARR['READ_NOISE_e'].append(ReadNoise_e)

        pixelRSLTS['IDX_PTC_SAT'] = Helpers.RSLT('Index of Saturation (PTC) ', ARR['IDX_PTC_SAT'], '[idx]', '{:7.0f}','')
        pixelRSLTS['SAT_LVL_PTC'] = Helpers.RSLT('PTC Saturation Level ', ARR['SAT_LVL_PTC'], '[DN]', '{:7.0f}','')
        pixelRSLTS['MAX_LVL'] = Helpers.RSLT('Maximum Level ', ARR['MAX_LVL'], '[DN]', '{:7.0f}','')

    astr = 'Index {:<4.0f}% of Sat.Level: '.format(comdefs.kw_PTC_H * 100)
    pixelRSLTS['IDX_CG_PTC_MAX'] = Helpers.RSLT(astr, ARR['IDX_CG_PTC_MAX'], '[idx]', '{:7.0f}','')

    astr = 'Index {:<4.0f}% of Sat.Level: '.format(comdefs.kw_PTC_L * 100)
    pixelRSLTS['IDX_CG_PTC_MIN'] = Helpers.RSLT(astr, ARR['IDX_CG_PTC_MIN'], '[idx]', '{:7.0f}','')

    astr = '{:<4.1f}% of Sat.Level: '.format(comdefs.kw_PTC_L * 100)
    pixelRSLTS['VAL_PTC_MIN'] =(Helpers.RSLT(astr, ARR['VAL_PTC_MIN'], '[DN]', '{:7.0f}',''))

    astr = '{:<4.1f}% of Sat.Level: '.format(comdefs.kw_PTC_H * 100)
    pixelRSLTS['VAL_PTC_MAX'] = Helpers.RSLT(astr, ARR['VAL_PTC_MAX'], '[DN]', '{:7.0f}','')

    pixelRSLTS['READNOISEDN'] =  Helpers.RSLT('Read Noise ', ARR['READNOISEDN'], '[DN]', '{:7.1f}','')
    pixelRSLTS['DYN_RESOL'] = Helpers.RSLT('Dynamic Resolution ', ARR['DYN_RESOL'], '[dB]', '{:7.1f}','')
    pixelRSLTS['EFF_ADC_RESOL'] = Helpers.RSLT('Effective ADC Resolution ', ARR['EFF_ADC_RESOL'], '[bit]', '{:7.1f}','')

    pixelRSLTS['CG_PIXELS'] = Helpers.RSLT('CG calc. from Pixels ' + '({:3.0f} to {:3.0f} % PTC)'.format(comdefs.kw_PTC_L * 100, comdefs.kw_PTC_H * 100), ARR['CG'], '[DN/e-]', '{:>7.3f}','')
    #RSLTS['CG_PIXELS'] = Helpers.RSLT('CG calc. from Pixels ' + '({:3.0f} to {:3.0f} % PTC)'.format(comdefs.kw_PTC_L * 100, comdefs.kw_PTC_H * 100), ARR['CG'], '[DN/e-]', '{:>7.3f}','')
    pixelRSLTS['CG_PIXELS_ERR'] = Helpers.RSLT('calculated CG Intercept', ARR['CG_ERR'], '[%]', '+-{:>5.2%}','')


    pixelRSLTS['CG_PHOTON'] = Helpers.RSLT('Photon CG calc. from Pixels ' + '({:3.0f} to {:3.0f} % PTC)'.format(comdefs.kw_PTC_L * 100, comdefs.kw_PTC_H * 100), ARR['CG_PHOTON'], '[ph/DN]', '{:>7.3f}','')
    pixelRSLTS['CG_PHOTON_ERR'] = Helpers.RSLT('Uncertainty: photon CG calc. from pixels' + '({:2.0f} to {:3.0f} % PTC)'.format(comdefs.kw_PTC_L * 100, comdefs.kw_PTC_H * 100), ARR['CG_PHOTON_ERR'], '[%]', '+-{:>5.2%}','')

    pixelRSLTS['CG_PIXELS_ERR'] = Helpers.RSLT('Uncertainty: CG calc. from pixels' + '({:2.0f} to {:3.0f} % PTC)'.format(comdefs.kw_PTC_L * 100, comdefs.kw_PTC_H * 100), ARR['CG_ERR'], '[%]', '+-{:>5.2%}','')
    #RSLTS['CG_PIXELS_ERR'] = Helpers.RSLT('CG calc. from Pixels Error' + '({:2.0f} to {:3.0f} % PTC)'.format(comdefs.kw_PTC_L * 100, comdefs.kw_PTC_H * 100), ARR['CG_ERR'], '[%]', '+-{:>5.2%}','')



    pixelRSLTS['FULL_WELL'] = Helpers.RSLT('Full Well Charge (PTC max.) ', ARR['FULL_WELL'], '[e-]', '{:7.0f}','')
    pixelRSLTS['READ_NOISE_e'] = Helpers.RSLT('Read Noise ', ARR['READ_NOISE_e'], '[e-]', '{:7.1f}','')




    print('CG Bad info')
    pixelRSLTS['CG_BAD_NOOF'] = Helpers.RSLT('No. of pixels CG <=0', len(ARR['CG_bad']), '', '{:7.0f}','')
    pixelRSLTS['CG_LOW_NOOF'] = Helpers.RSLT('No. of pixels CG <=50% of AVG CG', len(ARR['CG_low']), '','{:7.0f}','')
    RSLTS['CG_BAD_NOOF']=pixelRSLTS['CG_BAD_NOOF']
    RSLTS['CG_LOW_NOOF']=pixelRSLTS['CG_LOW_NOOF']
    t=[]
    tuple_CG_Bad=[]

    ctr_badcolumn_even=[0] *shape_columns
    ctr_badcolumn_odd = [0] *shape_columns
    for i in range(len(ARR['CG_bad'])):
                row=ARR['CG_bad'][i][0]
                column=ARR['CG_bad'][i][1]
                if Helpers.is_odd(row):
                    ctr_badcolumn_odd[column]=ctr_badcolumn_odd[column]+1
                else:
                    ctr_badcolumn_even[column] = ctr_badcolumn_even[column] + 1

    for i in range(shape_columns):
        if ctr_badcolumn_odd[i]>0:
            Name='CG_BAD_COLUMN_ODD'+'_{:04d}'.format(i)
            t.append(Name)
            pixelRSLTS[Name] = Helpers.RSLT('No. of pixels CG <=0 in Column '+str(i)+ '-odd', ctr_badcolumn_odd[i], '', '{:7.0f}','')
        if ctr_badcolumn_even[i]>0:
            Name = 'CG_BAD_COLUMN_EVEN' + '_{:04d}'.format(i)
            t.append(Name)
            pixelRSLTS[Name] = Helpers.RSLT('No. of pixels CG <=0 in Column '+str(i)+ '-even', ctr_badcolumn_even[i], '', '{:7.0f}','')

    ctr_lowcolumn_even = [0] * shape_columns
    ctr_lowcolumn_odd = [0] * shape_columns
    for i in range(len(ARR['CG_low'])):
        row = ARR['CG_low'][i][0]
        column = ARR['CG_low'][i][1]
        if Helpers.is_odd(row):
            ctr_lowcolumn_odd[column] = ctr_lowcolumn_odd[column] + 1
        else:
            ctr_lowcolumn_even[column] = ctr_lowcolumn_even[column] + 1

    for i in range(shape_columns):
        if ctr_lowcolumn_odd[i] > 0:
            Name = 'CG_LOW_COLUMN_ODD' + '_{:04d}'.format(i)
            t.append(Name)
            pixelRSLTS[Name] = Helpers.RSLT('No. of pixels <50% AVG CG in Column ' + str(i) + '-odd', ctr_lowcolumn_odd[i], '',
                                       '{:7.0f}','')
        if ctr_lowcolumn_even[i] > 0:
            Name = 'CG_LOW_COLUMN_EVEN' + '_{:04d}'.format(i)
            t.append(Name)
            pixelRSLTS[Name] = Helpers.RSLT('No. of pixels <50% AVG CG in Column ' + str(i) + '-even', ctr_lowcolumn_even[i],
                                       '', '{:7.0f}','')

    # create final tuple from basic keywords and the found bad columns
    for value in comdefs.tuple_CG_BAD:
        tuple_CG_Bad.append(value)
    for item in t:
        tuple_CG_Bad.append(item)

    # create a tuple selection
    newtuple = tuple(tuple_CG_Bad)
    sorted(newtuple)




    astr = Helpers.GetResults_from_Tuple(pixelRSLTS, newtuple)
    print(astr)
    pdf_Report.write_code(astr, 10)
    pdf_Report.PageBreak()  # start on new page
    '''

    '''
    RSLTS['DYN_RESOL']=np.reshape(RSLTS['DYN_RESOL'],[shape_rows,shape_columns])
    RSLTS['CG']=np.reshape(RSLTS['CG'],[shape_rows,shape_columns])
    RSLTS['READ_NOISE_e']=np.reshape(RSLTS['READ_NOISE_e'],[shape_rows,shape_columns])
    RSLTS['FULL_WELL']=np.reshape(RSLTS['FULL_WELL'],[shape_rows,shape_columns])
    '''
    print('CG MAP')
    CGMAP = pixelRSLTS['CG_PIXELS'].value
    print('CG MAP Reshape')
    CGMAP=np.reshape(CGMAP,[shape_rows,shape_columns])
    #cg_bad_mask = np.reshape(cg_bad_mask, [shape_rows , shape_columns])

    pdf_Report.doHeading('Figure: Conversion Gain Map', 'h3')
    Title=HardwareInfo+' Conversion Gain Map'
    fig = Plotting.ISPHI_Plot_CG_MAP(CGMAP, cg_bad_mask,Title, False,bandwidth=20)  # add here readoutreverse info

    buf = Plotting.savefigtobuf(fig)
    pdf_Report.addImageBuf(buf, 14)
    print('Histogram')
    fig = Plotting.plot_Histogram(CGMAP, Title,bandwidth=20)
    buf = Plotting.savefigtobuf(fig)
    pdf_Report.doHeading('Figure: Conversion Gain Map - Histogram', 'h3')
    pdf_Report.addImageBuf(buf, 14)
    pdf_Report.PageBreak()  # start on new page


    print('Photon CG MAP')
    CGABSMAP = pixelRSLTS['CG_PHOTON'].value
    print('CG Photon MAP Reshape')
    CGABSMAP=np.reshape(CGABSMAP,[shape_rows,shape_columns])
    #cg_bad_mask = np.reshape(cg_bad_mask, [shape_rows , shape_columns])

    pdf_Report.doHeading('Figure: Photon Conversion Gain Map', 'h3')
    Title=HardwareInfo+'Photon Conversion Gain Map'
    fig = Plotting.ISPHI_Plot_CGABS_MAP(CGABSMAP,Title, False,bandwidth=20)  # add here readoutreverse info

    buf = Plotting.savefigtobuf(fig)
    pdf_Report.addImageBuf(buf, 14)
    print('Histogram')
    fig = Plotting.plot_Histogram(CGABSMAP, Title,bandwidth=20) # add here readoutreverse info
    buf = Plotting.savefigtobuf(fig)
    pdf_Report.doHeading('Figure: Photon Conversion Gain Map - Histogram', 'h3')
    pdf_Report.addImageBuf(buf, 14)
    pdf_Report.PageBreak()  # start on new page

    # save fits files as maps
    # cg

    print('Done, returning ...')
    return RSLTS, CGMAP,CGABSMAP,pixelRSLTS



from reportlab.platypus import PageTemplate, BaseDocTemplate, NextPageTemplate, PageBreak
from reportlab.platypus import Frame


from reportlab.platypus import (
          BaseDocTemplate,
          PageTemplate,
          Frame,
          Paragraph,
          ParagraphAndImage,
          Image,
          Spacer)


def get_NoofPhotonsperPixel_Array(caller_localRSLTS, RSLTS, b_usePDFocalPlane):
    # start Calculate the no. of photons per pixel for each step in the sequence
    RSLTS = DF.getDataPD(caller_localRSLTS, RSLTS, b_usePDFocalPlane)
    # x_intensity_FocalPlane = x_intensity_FocalPlane[0:-2]  # the sequences had the last two files zeroexp
    if caller_localRSLTS == []: # valuesare already provided in RSLTS
        data = RSLTS
        arrTexp = data['Int. Time'].value
    else:
        # try to get filter info from data, either provided in RSLTS or in the data
        if isinstance(caller_localRSLTS,list): # list of RSLTS
            data =  caller_localRSLTS[0]
        else:
            data = caller_localRSLTS
        arrTexp = [float(i) for i in data['Int. Time']]  # convert strings to floats

    if comdefs.kw_Filter in data:
        WL = DF.GetWavelengthUsed(data[comdefs.kw_Filter],data[comdefs.kw_LampWavelength]) #RSLTS['Filter'].value, RSLTS['Lamp Wavelength'].value)
    else:
        WL = DF.GetWavelengthUsed(RSLTS[comdefs.kw_Filter], RSLTS[ comdefs.kw_LampWavelength])  # RSLTS['Filter'].value, RSLTS['Lamp Wavelength'].value)

    NoofPhotonsperPixel = []

    RSLTS[comdefs.kw_PH_ENERGY] = Helpers.RSLT('Photon Energy at {:5.2f} nm'.format(WL * 1E9), DF.CalcPhotonEnergy(WL),
                                      '[J]', '{:7.3E}','')
    RSLTS[comdefs.kw_SENS_PD] = Helpers.RSLT('Sensitivity of PD at {:5.2f} nm'.format(WL * 1E9),
                                    DF.CalcSensitivityofPD(WL), '[A/W]', '{:7.3f}','')

    RSLTS[comdefs.kw_CORR_PD_POS] = Helpers.RSLT('Correction Factor PD Position', DF.cst_corr_PDPosition_FocalPlane, '',
                                        '{:7.3f}','')
    RSLTS[comdefs.kw_AREA_PD] = Helpers.RSLT('Effective Area of Photodiode', DF.cst_Area_PD_HamamatsuS1337, '[mm^2]',
                                    '{:7.3e}','')
    RSLTS[comdefs.kw_AREA_PIXEL] = Helpers.RSLT('Area of Pixel', DF.cst_Area_ISPHI_pixel, '[mm^2]', '{:7.3e}','')

    for i in range(len(RSLTS[comdefs.kw_IntensityFocalPlane].value)):
        NoofPhotonsperPixel.append(DF.CalcISPHIPhotonFluxperPixel(RSLTS[comdefs.kw_IntensityFocalPlane].value[i], WL, arrTexp[i]))
        print('{:s}[{:3d}] : {:6.0f}'.format('No. of Photons per pixel - file', i,  NoofPhotonsperPixel[i]))
    RSLTS[comdefs.kw_NoofPhotonsperPixel] = Helpers.RSLT(comdefs.kw_NoofPhotonsperPixel,NoofPhotonsperPixel,'','{:6.0f}','')

        # end: Calculate the no. of photons per pixel for each step in the sequence
    return  RSLTS


def stackImages_calculate_store(path):
    std_fits_files = [fileName for fileName in os.listdir(path) if fileName.endswith("_STD.fits")]
    avg_fits_files = [fileName for fileName in os.listdir(path) if fileName.endswith("_AVG_-BIAS.fits")]

    localRSLTS = {}
    imgStack = {}
    if len(avg_fits_files) > 0:
        avg_fits_files.sort()
        std_fits_files.sort()
        # data = {}
        for i in range(len(avg_fits_files) ):
            # print('Array of files:', '\n', all_fits_files)
            print(avg_fits_files[i])
            print(std_fits_files[i])
            avgfilename = avg_fits_files[i]
            stdfilename = std_fits_files[i]
            avg_img = fits_handling.GetFitsData_unflipped(os.path.join(path, avgfilename)) #[0:10,0:2047]) # use only part: [0:100,0:1023] [0:100,0:1023]
            std_img = stddata=fits_handling.GetFitsData_unflipped(os.path.join(path, stdfilename))# [0:10,0:2047] # use only part:[0:500,0:2047] [0:100,0:1023]
            hdr = fits_handling.GetFitsHeader(os.path.join(path, avgfilename))
            if i == 0:
                #avgimage_data = []
                #varimage_data=[]
                # create arrays
                dataframe=fits_handling.GetFitsData_unflipped(os.path.join(path, avgfilename))
                cnt=len(avg_fits_files)
                avgimage_data = []
                stdimage_data = []
                #avgimage_data = np.array([cnt,dataframe.shape[0],dataframe.shape[1]])
                #varimage_data = np.array(avgimage_data.shape)
            avgimage_data.append(avg_img)
            stdimage_data.append(stddata)
            arrayRSLTS = ISPHI_Decode_Fits_Info.Get_ISPHI_FITS_HDR_INFO_appendvaluetolist(hdr, os.path.join(path, avgfilename), localRSLTS)
            arrayRSLTS = ISPHI_Decode_Fits_Info.make_measurements_appendresultstolist(avg_img, stddata, arrayRSLTS , Sectorname='')
            imgStack[comdefs.kw_Stack_AVG_img] = Helpers.RSLT(comdefs.kw_Stack_AVG_img,avgimage_data,'','','Stack of AVG data')
            imgStack[comdefs.kw_Stack_STD_img] = Helpers.RSLT(comdefs.kw_Stack_STD_img,stdimage_data,'','','Stack of STD data')


            # doppelt gemoppelt

            # besser so?:
            #FullFilename = os.path.join(path, avgfilename)
            #localRSLTS=ISPHI_Decode_Fits_Info.Get_ISPHI_DATA_RESULTS_GEN(avgimage_data[i], stddata, hdr, '', FullFilename, PathIndex='', MaskName='', b_ReverseReadout='')
            print(i)
        #avgimage_data=np.array(avgimage_data)
        #stdimage_data=np.array(stdimage_data)
        Helpers.save_RSLTS_to_file(path, arrayRSLTS)
        Helpers.save_imgStack_to_file(path, imgStack)
    return localRSLTS

def calc_CG_onPixelLevelStoretoFile(path,HardwareInfo,pdf_Report,RSLTS,ImgStack,b_usePDFocalPlane,doclevel):
    print('Function - calc_CG_onPixelLevel ...')
        # localRSLTS, x_intensity_FocalPlane = DF.getDataPD([], localRSLTS, b_usePDFocalPlane)

        # start Calculate the no. of photons per pixel for each step in the sequence

    #RSLTS = Helpers.load_RSLTS_from_file(path)

    avgimage_data = np.array(ImgStack[comdefs.kw_Stack_AVG_img].value)
    if comdefs.kw_Stack_STD_img in ImgStack:
        varimage_data = np.square( np.array(ImgStack[comdefs.kw_Stack_STD_img].value))
    elif comdefs.kw_Stack_VAR_img in ImgStack:
        varimage_data = np.array(ImgStack[comdefs.kw_Stack_VAR_img_img].value)


    if pdf_Report != []:
        pdf_Report.doHeading('Analyis on Single Pixel Level', 'h'+str(doclevel))
    RSLTS=getresultsMeanVariance_asArray(avgimage_data,varimage_data,HardwareInfo,pdf_Report,RSLTS,doclevel=doclevel)
    Helpers.save_pixelRSLTS_to_file(path, RSLTS)

def getACGGMAP_plot_etc(path,pdfReport, HardwareInfo):

    #todo work with RSLTS and
    #todo load RSLTS from file, then do the maps, plots., etc
    RSLTS, ACGMAP, ACGABSMAP, pixelRSLTS = callnewfunction()
    #todo get linear regression cooficients mean Signal vs. Intensity / Texp
    FullFilename=os.path.join(path,RSLTS[comdefs.kw_Filename].value[0]) # was: FullFilename=os.path.join(path,avg_fits_files[0])
    filename=fits_handling.ISPHI_StoreCGMAPtoFits(ACGMAP, FullFilename)

    b_single_pixel_plots = False
    if b_single_pixel_plots:
        # optional plots of single pixel
        shape_columns = avgimage_data.shape[2]
        shape_rows = avgimage_data.shape[1]

        r = 5
        c = 300
        pixelno = int(r * (shape_columns) + c)
        showMeanVarianceofSinglePixel(pixelRSLTS, avgimage_data,varimage_data, r, c, pdf_Report, HardwareInfo, pixelRSLTS['IDX_CG_PTC_MAX'].value[pixelno], doclevel)
        r = 5
        c = 301
        pixelno = int(r * (shape_columns) + c)
        showMeanVarianceofSinglePixel(pixelRSLTS, avgimage_data,varimage_data, r, c, pdf_Report, HardwareInfo,
                                      pixelRSLTS['IDX_CG_PTC_MAX'].value[pixelno], doclevel)

        r = 6
        c = 300
        pixelno = int(r * (shape_columns) + c)
        showMeanVarianceofSinglePixel(pixelRSLTS, avgimage_data,varimage_data, r, c, pdf_Report, HardwareInfo,
                                      pixelRSLTS['IDX_CG_PTC_MAX'].value[pixelno], doclevel)

        r = 6
        c = 302
        pixelno = int(r * (shape_columns) + c)
        showMeanVarianceofSinglePixel(pixelRSLTS,avgimage_data,varimage_data, r, c, pdf_Report, HardwareInfo,
                                      pixelRSLTS['IDX_CG_PTC_MAX'].value[pixelno], doclevel)

        r = 5
        c = 301
        pixelno = int(r * (shape_columns) + c)
        showPhotonsvsSensorSignalofSinglePixel(pixelRSLTS, NoofPhotonsperPixel,avgimage_data, r, c, pdf_Report,
                                               HardwareInfo, pixelRSLTS['IDX_CG_PTC_MAX'].value[pixelno], doclevel)
        '''
        r=50
        c=400
        showMeanVarianceofSinglePixel(RSLTS,MEAN_data, VAR_data, r, c, pdf_Report,HardwareInfo,Idx_PTC_sat_avg)

        r=100
        c=500
        showMeanVarianceofSinglePixel(RSLTS,MEAN_data, VAR_data, r, c, pdf_Report, HardwareInfo,Idx_PTC_sat_avg)

        r=1000
        c=400
        showMeanVarianceofSinglePixel(RSLTS,MEAN_data, VAR_data, r, c, pdf_Report, HardwareInfo,Idx_PTC_sat_avg)

        r=2000
        c=50
        showMeanVarianceofSinglePixel(RSLTS,MEAN_data, VAR_data, r, c, pdf_Report, HardwareInfo,Idx_PTC_sat_avg)

        r=2000
        c=100
        showMeanVarianceofSinglePixel(RSLTS,MEAN_data, VAR_data, r, c, pdf_Report, HardwareInfo,Idx_PTC_sat_avg)
        '''
        print('Scatterplot 1')
        rangel = 0
        rangeh = 8191
        showscatterplot_pixels(HardwareInfo, 'DYN_RESOL', pixelRSLTS, '[dB]', rangel, rangeh, pdf_Report)
        showscatterplot_pixels(HardwareInfo, 'CG_PIXELS', pixelRSLTS, '[DN/e-]', rangel, rangeh, pdf_Report)
        pdf_Report.PageBreak()  # start on new page
        showscatterplotylog(HardwareInfo, 'READ_NOISE_e', pixelRSLTS, '[e-]', rangel, rangeh, pdf_Report)
        showscatterplotylog(HardwareInfo, 'FULL_WELL', pixelRSLTS, '[e-]', rangel, rangeh, pdf_Report)

        pdf_Report.PageBreak()  # start on new page
        print('Scatterplot 2')
        rangel = 8192
        rangeh = 16383
        showscatterplot_pixels(HardwareInfo, 'DYN_RESOL', pixelRSLTS, '[dB]', rangel, rangeh, pdf_Report)
        showscatterplot_pixels(HardwareInfo, 'CG_PIXELS', pixelRSLTS, '[DN/e-]', rangel, rangeh, pdf_Report)
        pdf_Report.PageBreak()  # start on new page
        showscatterplotylog(HardwareInfo, 'READ_NOISE_e', pixelRSLTS, '[e-]', rangel, rangeh, pdf_Report)
        showscatterplotylog(HardwareInfo, 'FULL_WELL', pixelRSLTS, '[e-]', rangel, rangeh, pdf_Report)

        # pylab.show()

        pdf_Report.PageBreak()  # start on new page
        print('Scatterplot 3')
        plt.rcParams[
            'agg.path.chunksize'] = 10000  # bug fix for error :self._renderer.draw_path(gc, path, transform, rgbFace) OverflowError: In draw_path: Exceeded cell block limit
        rangel = 0
        rangeh = len(pixelRSLTS['CG_PIXELS'].value)
        showscatterplot_pixels(HardwareInfo, 'DYN_RESOL', pixelRSLTS, '[dB]', rangel, rangeh, pdf_Report)
        showscatterplot_pixels(HardwareInfo, 'CG_PIXELS', pixelRSLTS, '[DN/e-]', rangel, rangeh, pdf_Report)
        pdf_Report.PageBreak()  # start on new page
        showscatterplotylog(HardwareInfo, 'READ_NOISE_e', pixelRSLTS, '[e-]', rangel, rangeh, pdf_Report)
        showscatterplotylog(HardwareInfo, 'FULL_WELL', pixelRSLTS, '[e-]', rangel, rangeh, pdf_Report)

        pdf_Report.PageBreak()  # start on new page
        print('Scatterplot 4')  # Plot of AVG over rows for each column'

        item = 'READNOISEDN'
        y = np.reshape(pixelRSLTS[item].value, [shape_rows, shape_columns])
        y = np.nanmean(y, axis=0)
        x = list(range(len(y)))
        unit = '[DN]'
        xaxis_label = 'Column'
        yaxis_label = item + ' ' + unit
        Heading = item + ' per Column, AVG over {:3.0f} rows'.format(shape_rows)
        Title = HardwareInfo + '\n' + Heading
        scatterplot(x, y, Title, item, xaxis_label, yaxis_label, pdf_Report, Heading)
        pdf_Report.PageBreak()  # start on new page

        print('Scatterplot 5')  # Plot of AVG over columns for each row'
        item = 'READNOISEDN'
        y = np.reshape(pixelRSLTS[item].value, [shape_rows, shape_columns])
        y = np.nanmean(y, axis=1)
        x = list(range(len(y)))
        unit = '[DN]'
        xaxis_label = 'Row'
        yaxis_label = item + ' ' + unit
        Heading = item + ' per Row, AVG over {:3.0f} columns'.format(shape_columns)
        Title = HardwareInfo + '\n' + Heading
        scatterplot(x, y, Title, item, xaxis_label, yaxis_label, pdf_Report, Heading)

    if pdf_Report != '':
        pdf_Report.write_code('CG Map saved to: \n'+ os.path.dirname(filename)+'\n'+os.path.basename(filename), 10)

    filename=fits_handling.ISPHI_StoreCGABSMAPtoFits(ACGABSMAP, FullFilename)
    if pdf_Report != []:
        pdf_Report.write_code('Photon CG Map saved to: \n'+ os.path.dirname(filename)+'\n'+os.path.basename(filename), 10)

    return pdf_Report,RSLTS,pixelRSLTS


def create_Calc_CG_on_PixelLevel(path,pdf_Report,HardwareInfo,RSLTS,b_usePDFocalPlane, doclevel):
    pdf_Report,RSLTS=calc_CG_onPixelLevel(path, HardwareInfo, pdf_Report,RSLTS,b_usePDFocalPlane, doclevel)
    return pdf_Report,RSLTS


def test():
    mypath=r'H:\solo\metis\images\_VLDA\_FS\30018\MET_VLDA_FS_PCB\ConExpVarIllFlat\noFilter\JP\m05degC\VLDA_15MHz\CG_0.7_CDS_2\66802\0.02s\Processed'
    pdf_ReportName = os.path.join(mypath, 'test.pdf')
    pdf_Report = pdf_routines.Mypdf(pdf_ReportName)
    HardwareInfo='Hardware Info'
    RSLTS = {}
    pdf_Report,RSLTS=create_Calc_CG_on_PixelLevel(mypath,pdf_Report,HardwareInfo,RSLTS,b_usePDFocalPlane=False,doclevel=2)
    pdf_Report.Store()


# last change 2010_01_09
# 2020_01_09: accept nan values, in this case change format'
def getSummaryDataTable(RSLTS, atuple):
    atuple = atuple
    data=[]
    #tuple=sorted(tuple)
    for key in atuple:
         if key in RSLTS:
             RSLT = RSLTS[key]
             print('key:', key)
             Notes = ''
             if isinstance(RSLTS[key], tuple):
                 if len(RSLT) == 5: # tuple of type 'name,value,unit,format,comment
                     if isinstance(RSLT.value, list): # does it contain an array for the value ?
                         if isinstance(RSLT.value[0], str):
                             value = RSLT.value[0]
                         else:
                            if len(RSLT.value) > 1:
                                value = np.nanmean(RSLT.value)  # ignore nan values
                                Notes = 'AVG of {:d} items'.format(len(RSLT.value))
                            else:
                                value = RSLT.value[0]
                         name=RSLT.name
                         strformat=RSLT.strformat
                         unit=RSLT.unit
                         comment=RSLT.comment

                     else:
                         value = RSLT.value
                         name = RSLT.name
                         strformat = RSLT.strformat
                         unit = RSLT.unit
                         Notes = ''
                         Comment = RSLT.comment
                 else:# tuple of type 'key,value
                     value = RSLT
                     name = key
                     strformat = '{:}'
                     unit = ''
                     Notes = ''
                     comment=''
                 if isinstance(value, float):
                    if np.isnan(value):
                        strformat = '{:}'
             s=r''+strformat
             s=s.format(value)
             if len(s)> 30: s=Helpers.insert_newlines(s,30)
             if len(name) > 30: name = Helpers.insert_newlines(name, 30)
             data.append({'item': key,'name':name, 'value': s.format(value), 'unit': unit , 'notes':Notes })
         else:
             print('Key not found: '+key)
    return data




def getComparisonSectorsDataTable(RSLTS,Sectornames,tuple_selection):
    # create a tuple selection with global and sector specific contents
    t = []
    t_PTC = []
    for Sectorname in Sectornames:
        for value in tuple_selection:
            s = Sectorname + value
            t.append(s)
        #for value in defs.tuple_ISPHI_PRNU_Global:
         #   t_PTC.append(value)
        for item in t:
            t_PTC.append(item)

    sectorstuple = tuple(t_PTC)
    data=[]
    # get the data and write to table data format
    # like: Item:, RSLT_S1, RSLT_S2 , etc.



    # item Sectorname: value Sectorname: value Sectorname: value unit
    for key in tuple_selection:
        _dataline = {}
        _dataline['item']=key
        for Sectorname in Sectornames:
             selection = Sectorname + key
             if selection in RSLTS:
                 RSLT=RSLTS[selection]
                 #print('debug ',selection)
                 if len(RSLT)==5: # tuple of type 'name,value,unit,format, comment
                     if isinstance(RSLT.value,list): # does it contain an array for the value ?
                         value=np.nanmean(RSLT.value) # ignore nan values
                         name=RSLT.name
                         strformat=RSLT.strformat
                         unit=RSLT.unit
                         Notes='AVG of {:d} pixels'.format(len(RSLT.value))
                         comment=RSLT.comment
                     else:
                         value=RSLT.value
                         name = RSLT.name
                         strformat = RSLT.strformat
                         unit = RSLT.unit
                         Notes = ''
                         comment = RSLT.comment
                 else:# tuple of type 'key,value
                     value = RSLT
                     name = selection
                     strformat = '{:}'
                     unit = ''
                     Notes = ''
                     comment = ''
                 s = r'' + strformat
                 s = s.format(value)
                 if len(s) > 30: s = Helpers.insert_newlines(s, 30)
                 if len(name) > 30: name = Helpers.insert_newlines(name, 30)
                 _dataline[Sectorname] = s
                 _dataline['unit'] = unit
             else:
                print('Key not found: '+selection)
        if len(_dataline) >0: data.append(_dataline)

    return data


#test()
