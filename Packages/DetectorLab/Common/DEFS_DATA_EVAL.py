

#todo: for keywords use kw_UPPERCASE = 'UPPERCASE'
# for names use: name_UPPERCASE = 'Upper Case'

# standarddized names to be used in fits header
#Hardware and Test Environment
kw_HARDWARE='HARDWARE'
kw_SENSOR  = 'SENSOR'   # temperature of sensor cold finger
kw_SENSORMF= 'SENSORMF' # sensor manufacturer
kw_SENSORSN= 'SENSORSN' # sensor serial number
kw_VACUUM  = 'VACUUM'   # vacuum level



# keywords for optical and illumination setup
kw_OPTICS  = 'OPTICS'   # optics
kw_FILTERWL= 'FILTERWL' # filter wave length
kw_TESTPATT= 'TESTPATT' # CB test pattern
kw_LIGHTTYPE = 'LIGHTTYPE'     # external test light type
kw_LIGHTWL  = 'LIGHTWL'   # external test light wave length
kw_LIGHTINT = 'LIGHTINT'  # external test light intensity
kw_REFDIODE= 'REFDIODE' # lamp intensity reference diode
kw_HISTORY= 'HISTORY'     # stored processing history
kw_Lamp = 'LAMP'

kw_LAMPINTENSITY = 'LAMPINTENSITY'
name_LAMPINTENSITY = 'Lamp Intensity'

kw_LAMPWAVELENGTH = 'LAMPWL'
name_LAMPWAVELENGTH  = 'Lamp Wavelength'

kw_LIGHTSOURCE = 'LIGHTSOURCE'
name_LIGHTSOURCE = 'Light Source'

kw_LIGHTINTENSITY = 'LIGHTINTENISITY'
name_LIGHTINTENSITY = 'Light Intensity'

kw_LIGHTWL = 'LIGHTWL'
name_LIGHTWL = 'Light Wavelength'

kw_READOUTDIRECTION = 'READOUTDIR'
name_READOUTDIRECTION = 'Readout Direction'

kw_proc_Darks = "DARKS"
kw_proc_Darks1 = "DARKS1"
kw_proc_AvgStd = "AVG_STD"
kw_proc_Avg_only = "AVG"
kw_proc_Cosmetics = "Cosmetics"
kw_proc_FilterScanSensitivity = "FilterScanSensitivity"

kw_proc_ConExpVarILL = 'CONEXPVARILL'
kw_proc_ConIllVarExp = 'CONILLVAREXP'

known_processes = {kw_proc_Darks, kw_proc_Darks1, kw_proc_AvgStd, kw_proc_Avg_only, kw_proc_AvgStd, kw_proc_Cosmetics}

name_csv_data_Level0 = '_Summary_LVL0.csv'
name_csv_data_Level1 = '_Summary_LVL1.csv'

kw_CF_TEMPERATURE = 'CF_TEMPERATURE'
kw_CF_TEMPERATURE_AVG = 'CF_TEMPERATURE_AVG'

# common definitions for data evaluation

# Photon transfer curve
cst_PTC_H = 0.7  # EMVA STANDARD CG linear fit : 0 to 70%
cst_PTC_L = 0.0    # EMVA STANDARD CG linear fit : 0 to 70%

# Signal vs. Flux to obtain QE
cst_sig_flux_H = 0.7  #
cst_sig_flux_L = 0.0    #


# Photon transfer curve Mean-Noise log
cst_PTC_Mean_Noise_log_H = 0.7
cst_PTC_Mean_Noise_log_L = 0.3

cst_red_factor_slope_PTC = 0.7 # this reduction factor defines where the linear part of the CG and linear fit slope is calculated
# Linearity
# Linear fit
cst_LINFIT_L = 0.05 # EMVA standard 0.05
cst_LINFIT_H = 0.95 # EMVA standard 0.95

# linear fit in log/log plot
cst_loglog_LinFitMax = 0.7

# reference level for Deviation from Linearity
cst_def_linearity_ref = 0.9 #0.9 used for METIS characterization report, also EMVA standard

# linear range
cst_Linear_Range_Spec = 0.01 # linear range +- 1%

# Fixed Pattern Noise
# definition of range for linear regressions line
cst_FPN_L = 0.1
cst_FPN_H = 0.7

cst_PRNU_H = 0.5

# pre-defined keywords in ISPHI camera FITS header
kw_PROJECT = 'PROJECT'
kw_PURPOSE = 'PURPOSE'
kw_SUBJECT = 'SUBJECT'
kw_ENGINEER = 'ENGINEER' # use operator 
kw_OPERATOR = 'OPERATOR'
kw_SITE = 'SITE'
kw_SWCLASS = 'SWCLASS'
kw_SWVER = 'SWVER'
kw_LVSDSLIB = 'LVSDSLIB'
kw_CAM_ID = 'CAM_ID'
kw_EGSE_VER = 'EGSE_VER'

kw_Path = 'PATH'
kw_Filename ='FILENAME'
kw_Filenames ='FILENAMES'
kw_Sequence = 'SEQUENCE'
kw_TestSequence = 'TESTSEQUENCE'
kw_Hardware = 'HARDWARE'



kw_IMG_SIZE = 'IMG_SIZE'
kw_IMG_WIDTH = 'IMG_WIDTH'
kw_IMG_HEIGHT = 'IMG_HEIGHT'
kw_ROI_NAME = 'ROI_NAME'
kw_ROI_AREA = 'ROI_AREA'
kw_ROI_SHAPE = 'ROI_SHAPE'
kw_AVG_WIDTH = 'AVG_WIDTH'
kw_AVG_HEIGHT = 'AVG_HEIGHT'

kw_SUM ='SUM'

kw_IntensityFocalPlane = 'INTENSITY@FOCAL_PLANE'
name_IntensityFocalPlane = 'Intensity@Focal_Plane'

kw_NoofPhotonsperPixel = 'NOOFPHOTONSPERPIXEL'
name_NoofPhotonsperPixel = 'NoofPhotonsperPixel'
# constants for variables holding stack of images

kw_Stack_AVG_img = 'STACK_AVG_IMG'
name_Stack_AVG_img = 'Stack_AVG_img'

kw_Stack_STD_img = 'STAC_STD_IMG'
name_Stack_STD_img = 'Stack_STD_img'

name_Stack_VAR_img = 'STACK_VAR_IMG'
kw_Stack_VAR_img = 'Stack_VAR_img'

kw_img_stack_Data_File = "_img_stack.p"
kw_img_stack_RSLTS_File = "_img_stack_RSLTS.p"
kw_img_stack_RSLTS_pixels_File = "_img_stack_RSLTS_pixels.p"

kw_LinRegCoef = 'LIN_REG_COEF'
name_LinRegCoef = 'Linear Regression Coefficient'

kw_LinRegOffset = 'LIN_REG_OFFS'
name_LinRegOffset = 'Linear_Regression_Offset'

kw_AVG_MEAN ='AVG_MEAN'
kw_AVG_STD = 'AVG_STD'
kw_AVG_MIN = 'AVG_MIN'
kw_AVG_MAX = 'AVG_MAX'
kw_STD_MEAN = 'STD_MEAN'
kw_STD_STD = 'STD_STD'
kw_STD_MIN = 'STD_MIN'
kw_STD_MAX = 'STD_MAX'
kw_Processing_History = 'PROCESSING_HISTORY'
name_Processing_History = 'Processing History'

kw_SEQ_NUM_STEPS = 'SEQ_NUM_STEPS'
kw_MASK_NAME = 'MASK_NAME'
kw_IntTime='INTTIME' # 2019_10_25 was: 'Int. Time' use uppercase and no blanks !
kw_DET_TEMP ='DETTEMP' # 2019_10_25 was: 'Det. Temp' use uppercase and no blanks !
kw_DET_TEMP_AVG = 'DETTEMP_AVG'

kw_TestPattern = 'TEST_PATTERN' # 2019_10_25 was: 'Test Pattern' use uppercase and no blanks !

kw_Filter = 'FILTER'# 2019_10_25 use uppercase and no blanks !
kw_PD_ORIEL = 'PD_ORIEL'
kw_PD_KEITHLEY = 'PD_KEITHLEY'
kw_PD_REF = 'PD_REFERENCE'

kw_DARKSGN_DNps = 'DS_DNpers'
name_DARKSGN_DNps = 'Dark Signal DN/s'

kw_BIAS_LVL = 'BIAS_LVL[DN]'
name_BIAS_LVL = 'Bias Level [DN]'

kw_DARKSGN_electrons = 'DSe-'
name_DARKSGN_electrons = 'Dark Signal e-'

kw_OUTLIERS = 'OUTLIERS'


kw_OUTLIERS_less01 = 'OUTLIERS < (AVG-99%)'
kw_OUTLIERS_less05 = 'OUTLIERS < (AVG-95%)'
kw_OUTLIERS_less10 = 'OUTLIERS < (AVG-90%)'
kw_OUTLIERS_less20 = 'OUTLIERS < (AVG-80%)'
kw_OUTLIERS_less50 = 'OUTLIERS < (AVG-50%)'
kw_OUTLIERS_less75 = 'OUTLIERS < (AVG-25%)'
kw_OUTLIERS_less80 = 'OUTLIERS < (AVG-20%)'
kw_OUTLIERS_less90 = 'OUTLIERS < (AVG-10%)'
kw_OUTLIERS_less95 = 'OUTLIERS < (AVG-05%)'

kw_COORDINATES = 'COORDINATES'
kw_COORDINATES_less01 = 'COORDINATES < (AVG-99%)'
kw_COORDINATES_less05 = 'COORDINATES < (AVG-95%)'
kw_COORDINATES_less10 = 'COORDINATES < (AVG-90%)'
kw_COORDINATES_less20 = 'COORDINATES < (AVG-80%)'
kw_COORDINATES_less50 = 'COORDINATES < (AVG-50%)'
kw_COORDINATES_less75 = 'COORDINATES < (AVG-25%)'
kw_COORDINATES_less80 = 'COORDINATES < (AVG-20%)'
kw_COORDINATES_less90 = 'COORDINATES < (AVG-10%)'
kw_COORDINATES_less95 = 'COORDINATES < (AVG-05%)'


kw_list_HOTPXL_THRS = [2, 3, 5 , 10]
kw_HOTPXL = 'HOT PIXELS'
kw_HOTPXL_ab2   = 'HOT PIXELS >  2x'
kw_HOTPXL_ab3   = 'HOT PIXELS >  3x'
kw_HOTPXL_ab5   = 'HOT PIXELS >  5x'
kw_HOTPXL_ab10  = 'HOT PIXELS > 10x'

kw_COORD_HOTPXL = 'COORD. HOT PIXELS'
kw_COORD_HOTPXL_2  = 'COORD. HOT PIXELS >  2x'
kw_COORD_HOTPXL_3  = 'COORD. HOT PIXELS >  3x'
kw_COORD_HOTPXL_5  = 'COORD. HOT PIXELS >  5x'
kw_COORD_HOTPXL_10 = 'COORD. HOT PIXELS > 10x'


kw_PH_ENERGY = 'PH_ENERGY'
kw_SENS_PD = 'SENS_PD'
kw_CORR_PD_POS = 'CORR_PD_POS'
kw_AREA_PD = 'AREA_PD'
kw_AREA_PIXEL = 'AREA_PIXEL'
kw_QE_SignalFlux = 'QE_SignalFlux'


kw_Hotx10 = 'HOTX10'
kw_Hotx5 = 'HOTX5'
kw_Hotx3 = 'HOTX3'
kw_Coldx10 = 'COLDX10'
kw_Coldx5 = 'COLDX5'
kw_Coldx3 = 'COLDX3'


kw_FWHM = 'FWHM'
kw_FWHM_err =  'FWHM_ERROR'
name_FWHM_err =  'FWHM Error'

kw_FLATFIELD_FILENAME = 'FLATFIELD_FILENAME'
kw_FLATFIELD_MIN = 'FLATFIELD_MIN'
kw_FLATFIELD_MAX = 'FLATFIELD_MAX'
kw_100x100_PRNU = '100x100_PRNU'

kw_IDX_CG_PTC_MIN = 'IDX_CG_PTC_MIN'
kw_IDX_CG_PTC_MAX = 'IDX_CG_PTC_MAX'


kw_MAX_LVL= 'MAX_LVL'
kw_READNOISEDN ='READNOISEDN'
kw_DYN_RESOL = 'DYN_RESOL'
kw_EFF_ADC_RESOL = 'EFF_ADC_RESOL'
kw_VAL_PTC_MIN = 'VAL_PTC_MIN'
kw_VAL_PTC_MAX = 'VAL_PTC_MAX'
kw_SAT_LVL_PTC = 'SAT_LVL_PTC'
kw_IDX_PTC_SAT = 'IDX_PTC_SAT'
kw_IDX_PTC_SAT_pixels = 'IDX_PTC_SAT_Pixels'
kw_IDX_HALF_PTC_SAT = 'IDX_HALF_PTC_SAT'
kw_IDX_HALF_PTC_SAT_pixels = 'IDX_HALF_PTC_SAT_Pixels'
kw_IDX_LIN_EXCEEDING_TWOPERCENT = 'IDX_LIN_EXCEEDING_TWOPERCENT'
kw_CG = 'CG'
kw_cg_FitFunctionSlope = 'cg_slope'
kw_cg_FitFunctionOffset ='cg_offset'
kw_linearity_FitFunctionSlope = 'linearity_slope'
kw_linearity_FitFunctionOffset ='linearity_offset'


kw_CG_MEAN = 'CG_MEAN'
kw_CG_PHOTON = 'CG_PHOTON'
kw_CG_PHOTON_MEAN = 'CG_PHOTON_MEAN'
kw_CG_PHOTON_ERR = 'CG_PHOTON_ERR'
kw_CG_SIGNAL_NOISE = 'CG_SIGNAL_NOISE'
kw_CG_PIXELS = 'CG_PIXELS'
kw_CG_PIXELS_ERR = 'CG_PIXELS_ERR'
kw_CG_BAD_NOOF = 'CG_BAD_NOOF'
kw_CG_LOW_NOOF = 'CG_LOW_NOOF'
kw_READNOISE_SIGNAL_NOISE = 'READNOISE_SIGNAL_NOISE'

kw_FULL_WELL = 'FULL_WELL'
kw_READ_NOISE_e = 'READ_NOISE_e'
kw_LIN_ERR_EMVA = 'LIN_ERR_EMVA'
kw_LIN_ERR = 'LIN_ERR'
kw_LIN_ERR_FULLRANGE = 'LIN_ERR_FULLRANGE'

kw_LIN_RANGE = 'LIN_RANGE'
kw_PRNU = 'PRNU'

kw_Temperatures = 'TEMPERATURES'
kw_FileDates = 'FILEDATES'
kw_FileDate = 'FILEDATE'
kw_FileNames = 'FILENAMES'
kw_ImageDate = 'Image Date/Time'

kw_ReverseReadout = 'REVERSE_READOUT'
name_ReverseReadout = 'Reverse Readout'
# kw_ReadoutDirection = 'Readout Direction'  # obsolete -> use uppercase, no spaces

kw_DEV_LR_MIN = 'DEV_LR_MIN'
kw_DEV_LR_MAX = 'DEV_LR_MAX'
kw_IDX_LINFIT_MIN = 'IDX_LINFIT_MIN'
kw_IDX_LINFIT_MAX = 'IDX_LINFIT_MAX'


tuple_Filenames={
    kw_Filenames
}




tuple_Filename={
    kw_Filename
}

# this tuple is used to evaluate data in every selected sector of image area
tuple_to_CSV_AVG_STD = {
    kw_SUM,
    kw_ROI_AREA,
    kw_ROI_SHAPE,
    kw_AVG_MEAN,
    kw_AVG_STD,
    kw_AVG_MIN,
    kw_AVG_MAX,
    kw_STD_MEAN,
    kw_STD_STD,
    kw_STD_MIN,
    kw_STD_MAX,
    kw_Filter,
    }

tuple_FWHM = {
    kw_FWHM
    }

tuple_single_pixel_PTC={
kw_SEQ_NUM_STEPS,
kw_IDX_CG_PTC_MIN,
kw_IDX_CG_PTC_MAX,
kw_VAL_PTC_MIN,
kw_VAL_PTC_MAX,
kw_EFF_ADC_RESOL,
kw_READNOISEDN,
kw_READ_NOISE_e,
kw_FULL_WELL,
kw_DYN_RESOL,
kw_CG_PIXELS,
kw_CG_PIXELS_ERR
}

tuple_CG_BAD={
kw_CG_BAD_NOOF,
kw_CG_LOW_NOOF
}

tuple_num_HotPixels={
kw_HOTPXL_ab2,
kw_HOTPXL_ab3,
kw_HOTPXL_ab5,
kw_HOTPXL_ab10
}


tuple_coord_HotPixels={
kw_COORD_HOTPXL_2,
kw_COORD_HOTPXL_3,
kw_COORD_HOTPXL_5,
kw_COORD_HOTPXL_10
}

tuple_Outliers_noof={
kw_OUTLIERS_less01,
kw_OUTLIERS_less05,
kw_OUTLIERS_less10,
kw_OUTLIERS_less20,
kw_OUTLIERS_less50,
kw_OUTLIERS_less75,
kw_OUTLIERS_less80,
kw_OUTLIERS_less90,
kw_OUTLIERS_less95
}

tuple_Flatfield={
kw_FLATFIELD_FILENAME,
kw_FLATFIELD_MIN,
kw_FLATFIELD_MAX
}



tuple_DarkSignal={
kw_DET_TEMP,
kw_IntTime,
kw_SEQ_NUM_STEPS,
kw_IMG_SIZE,
kw_ROI_NAME,
kw_ROI_AREA,
kw_ROI_SHAPE,
kw_DARKSGN_DNps,
kw_BIAS_LVL,
kw_HOTPXL_ab2,
kw_HOTPXL_ab3,
kw_HOTPXL_ab5,
kw_HOTPXL_ab10
}


# do not modify : it is used by the summary table of the individual sectors
tuple_MeasureSectors_PTC = (
kw_READNOISEDN,
kw_DYN_RESOL,
kw_EFF_ADC_RESOL,
kw_VAL_PTC_MIN,
kw_VAL_PTC_MAX,
kw_SAT_LVL_PTC,
kw_IDX_PTC_SAT,
kw_IDX_HALF_PTC_SAT,
kw_CG,
kw_FULL_WELL,
kw_READ_NOISE_e,
kw_LIN_ERR_EMVA,
kw_LIN_ERR_FULLRANGE,
kw_LIN_RANGE,
kw_PRNU
)


tuple_LOGNoise_LOGSignal_PTC = (
kw_DET_TEMP,
kw_SEQ_NUM_STEPS,
kw_IMG_SIZE,
kw_ROI_NAME,
kw_ROI_AREA,
kw_ROI_SHAPE,
kw_CG_SIGNAL_NOISE,
kw_READNOISE_SIGNAL_NOISE
)


tuple_Outliers_coord={

kw_COORDINATES_less01,
kw_COORDINATES_less05,
kw_COORDINATES_less10,
kw_COORDINATES_less20,
kw_COORDINATES_less50,
kw_COORDINATES_less75,
kw_COORDINATES_less80,
kw_COORDINATES_less90,
kw_COORDINATES_less95
}


tuple_single_pixel_PhotonsvsSensorSignal={
kw_SEQ_NUM_STEPS,
kw_IDX_CG_PTC_MIN,
kw_IDX_CG_PTC_MAX,
kw_VAL_PTC_MIN,
kw_VAL_PTC_MAX,
kw_CG_PHOTON,
kw_CG_PHOTON_ERR
}


tuple_PRNU = (
kw_ROI_NAME,
kw_ROI_AREA,
kw_ROI_SHAPE,
kw_PRNU
)

tuple_PRNU_Common = (
kw_DET_TEMP,
kw_SEQ_NUM_STEPS,
kw_IMG_SIZE,
kw_MASK_NAME
)



tuple_Signal_Flux_QE = (
kw_DET_TEMP,
kw_SEQ_NUM_STEPS,
kw_IMG_SIZE,
kw_ROI_NAME,
kw_ROI_AREA,
kw_ROI_SHAPE,
kw_LAMPWAVELENGTH,
kw_Filter,
kw_CG,
kw_PH_ENERGY,
kw_SENS_PD,
kw_CORR_PD_POS,
kw_AREA_PD,
kw_AREA_PIXEL,
kw_QE_SignalFlux
)

tuple_PH_DN = (
kw_DET_TEMP,
kw_SEQ_NUM_STEPS,
kw_IMG_SIZE,
kw_ROI_NAME,
kw_ROI_AREA,
kw_ROI_SHAPE,
kw_LAMPWAVELENGTH,
kw_Filter,
kw_PH_ENERGY,
kw_SENS_PD,
kw_CORR_PD_POS,
kw_AREA_PD,
kw_AREA_PIXEL,
kw_CG_PHOTON
)



tuple_CameraPerformance = (
kw_READNOISEDN,
kw_DYN_RESOL,
kw_EFF_ADC_RESOL,
kw_VAL_PTC_MIN,
kw_VAL_PTC_MAX,
kw_SAT_LVL_PTC,
kw_IDX_PTC_SAT,
kw_IDX_HALF_PTC_SAT,
kw_CG,
kw_FULL_WELL,
kw_READ_NOISE_e,
kw_LIN_ERR_EMVA,
kw_LIN_ERR_FULLRANGE,
kw_LIN_RANGE,
kw_PRNU,
kw_BIAS_LVL,
kw_QE_SignalFlux
)



tuple_Outliers_noof={

kw_OUTLIERS_less01,
kw_OUTLIERS_less05,
kw_OUTLIERS_less10,
kw_OUTLIERS_less20,
kw_OUTLIERS_less50,
kw_OUTLIERS_less75,
kw_OUTLIERS_less80,
kw_OUTLIERS_less90,
kw_OUTLIERS_less95
}

tuple_Linearity = {
kw_SEQ_NUM_STEPS,
kw_SAT_LVL_PTC,
kw_MAX_LVL,
kw_IDX_LINFIT_MIN,
kw_IDX_LINFIT_MAX,
kw_LinRegCoef,
kw_LinRegOffset,
kw_LIN_ERR_EMVA,
kw_LIN_ERR_FULLRANGE,
kw_IDX_LIN_EXCEEDING_TWOPERCENT,
kw_DEV_LR_MIN,
kw_DEV_LR_MAX,
kw_LIN_RANGE

}


tuple_allResults = \
    (
    kw_Path,
    kw_Filename,
    kw_Sequence,
    kw_SEQ_NUM_STEPS,
    kw_Hardware,
    kw_SENSORSN,
    kw_ReverseReadout,
    kw_TestPattern,
    kw_LAMPINTENSITY,
    kw_LAMPWAVELENGTH,
    kw_Lamp,
    kw_Filter,
    kw_CF_TEMPERATURE_AVG,
    kw_DET_TEMP,
    kw_Processing_History,
    kw_IMG_SIZE,
    kw_MASK_NAME,
    kw_ROI_AREA,
    kw_READNOISEDN,
    kw_DYN_RESOL,
    kw_EFF_ADC_RESOL,
    kw_VAL_PTC_MIN,
    kw_VAL_PTC_MAX,
    kw_SAT_LVL_PTC,
    kw_IDX_PTC_SAT,
    kw_IDX_HALF_PTC_SAT,
    kw_CG,
    kw_CG_PHOTON,
    kw_CG_PHOTON_ERR,
    kw_CG_SIGNAL_NOISE,
    kw_CG_PIXELS,
    kw_CG_PIXELS_ERR,
    kw_FULL_WELL,
    kw_READ_NOISE_e,
    kw_LIN_ERR_EMVA,
    kw_LIN_ERR_FULLRANGE,
    kw_LIN_RANGE,
    kw_PRNU,
    kw_100x100_PRNU,
    kw_QE_SignalFlux,

    kw_OUTLIERS_less01,
    kw_OUTLIERS_less05,
    kw_OUTLIERS_less10,
    kw_OUTLIERS_less20,
    kw_OUTLIERS_less50,
    kw_OUTLIERS_less75,
    kw_OUTLIERS_less80,
    kw_OUTLIERS_less90,
    kw_OUTLIERS_less95,

    kw_CG_BAD_NOOF,
    kw_CG_LOW_NOOF

     )




test_tuple_ShortHeader = (kw_Filename,
                          kw_Sequence,
                          kw_Hardware,
                          kw_SENSORSN,
                          kw_TestPattern,
                          kw_LAMPINTENSITY,
                          kw_LAMPWAVELENGTH,
                          kw_Lamp,
                          kw_Filter,
                          kw_CF_TEMPERATURE_AVG,
                          kw_DET_TEMP
                          )

tuple_meas_DARKS = (
    kw_ROI_NAME,
    kw_ROI_AREA,
    kw_AVG_MEAN,
    kw_AVG_STD,
    kw_AVG_MIN,
    kw_AVG_MAX,
    kw_AVG_WIDTH,
    kw_AVG_HEIGHT,
    kw_Hotx10,
    kw_Hotx5,
    kw_Hotx3,
    kw_Coldx10,
    kw_Coldx5,
    kw_Coldx3,
    kw_STD_MEAN,
    kw_STD_STD,
    kw_STD_MIN,
    kw_STD_MAX
)


tuple_meas_AVG = (
    kw_AVG_MEAN,
    kw_AVG_STD,
    kw_AVG_MIN,
    kw_AVG_MAX,
    kw_AVG_WIDTH,
    kw_AVG_HEIGHT,
    kw_ROI_AREA,
    kw_ROI_SHAPE,
    kw_ROI_NAME

)

# meas tuples are measured in all defined sectors
tuple_meas_AVG_STD =(
    kw_AVG_MEAN,
    kw_AVG_STD,
    kw_AVG_MIN,
    kw_AVG_MAX,
    kw_STD_MEAN,
    kw_STD_STD,
    kw_STD_MIN,
    kw_STD_MAX,
    kw_AVG_WIDTH,
    kw_AVG_HEIGHT,
    kw_ROI_AREA,
    kw_ROI_SHAPE,
    kw_ROI_NAME
)

test_tuple_Darks = (
    kw_Filename,
    kw_Sequence,
    kw_Hardware,
    kw_SENSORSN,
        kw_IntTime,
          kw_ReverseReadout,
          kw_READOUTDIRECTION,
          kw_CF_TEMPERATURE_AVG,
        kw_DET_TEMP,
        kw_TestPattern,
        kw_LAMPINTENSITY,
        kw_LAMPWAVELENGTH,
        kw_Lamp,
        kw_Filter,
        kw_PD_ORIEL,
        kw_PD_KEITHLEY,
        kw_IMG_SIZE,
        kw_Processing_History,
        sorted(list(tuple_meas_DARKS))
    )

test_tuple_DarkSignalvsTemperature = (
    'Sequence TextFile',
    kw_Filename,
    kw_Sequence,
    kw_DARKSGN_DNps,
    kw_BIAS_LVL,
    kw_Hardware,
    kw_SENSORSN,
        kw_IntTime,
          kw_CF_TEMPERATURE_AVG,
        kw_DET_TEMP,
        kw_TestPattern,
        kw_LAMPINTENSITY,
        kw_LAMPWAVELENGTH,
        kw_Lamp,
        kw_Filter,
        kw_IMG_SIZE,
        kw_Processing_History,
        sorted(list(tuple_meas_DARKS))
    )



test_tuple_AVG = (kw_Filename,
                  kw_Sequence,
                  kw_Hardware,
                  kw_SENSORSN,
                  kw_IntTime,
                  kw_ReverseReadout,
                  kw_CF_TEMPERATURE_AVG,
                  kw_DET_TEMP,
                  kw_TestPattern,
                  kw_LAMPINTENSITY,
                  kw_LAMPWAVELENGTH,
                  kw_Lamp,
                  kw_Filter,
                  kw_PD_ORIEL,
                  kw_PD_KEITHLEY,
                  kw_IMG_SIZE,
                  kw_ROI_NAME,
                  kw_ROI_AREA,
                  kw_Processing_History,
                  sorted(list(tuple_meas_AVG))
            )


test_tuple_AVG_STD = (kw_Filename,
                      kw_Sequence,
                      kw_Hardware,
                      kw_SENSORSN,
                      kw_IntTime,
                      kw_ReverseReadout,
                      kw_CF_TEMPERATURE_AVG,
                      kw_DET_TEMP,
                      kw_TestPattern,
                      kw_LAMPINTENSITY,
                      kw_LAMPWAVELENGTH,
                      kw_Lamp,
                      kw_Filter,
                      kw_PD_ORIEL,
                      kw_PD_KEITHLEY,
                      kw_IMG_SIZE,
                      kw_ROI_NAME,
                      kw_ROI_AREA,
                      kw_Processing_History,
                      sorted(list(tuple_meas_AVG_STD))
                          )




test_tuple_CSV_AVG_STD = (
    kw_Filename,
          kw_IntTime,
          sorted(list(tuple_meas_AVG_STD)),
          kw_Sequence,
          kw_Hardware,
          kw_SENSORSN,
          kw_ReverseReadout,
          kw_CF_TEMPERATURE_AVG,
          kw_DET_TEMP,
          kw_TestPattern,
          kw_LAMPINTENSITY,
          kw_LAMPWAVELENGTH,
          kw_Lamp,
          kw_Filter,
          kw_PD_ORIEL,
          kw_PD_KEITHLEY,
          kw_IMG_SIZE,
          kw_ROI_NAME,
          kw_ROI_AREA,
          kw_Processing_History)

tuple_meas_OUTLIERS = (
        kw_OUTLIERS_less01,
        kw_OUTLIERS_less05,
        kw_OUTLIERS_less10,
        kw_OUTLIERS_less20,
        kw_OUTLIERS_less50,
        kw_OUTLIERS_less75,
        kw_OUTLIERS_less80,
        kw_OUTLIERS_less90,
        kw_OUTLIERS_less95
)
test_tuple_Particles = (kw_Filename,
                        kw_Sequence,
                        kw_Hardware,
                        kw_SENSORSN,
                        kw_IntTime,
                        kw_ReverseReadout,
                        kw_CF_TEMPERATURE_AVG,
                        kw_DET_TEMP,
                        kw_TestPattern,
                        kw_LAMPINTENSITY,
                        kw_LAMPWAVELENGTH,
                        kw_Lamp,
                        kw_Filter,
                        kw_PD_ORIEL,
                        kw_PD_KEITHLEY,
                        kw_IMG_SIZE,
                        kw_ROI_NAME,
                        kw_ROI_AREA,
                        sorted(list(tuple_meas_AVG)),
                        sorted(list(tuple_meas_OUTLIERS)),
                        kw_Processing_History)




tuple_File_Info = (
    kw_Filenames
        )

tuple_Cosmetics = ( # used by ISPHI\_200_Cosmetics
    sorted(list(tuple_meas_OUTLIERS)),
    kw_PROJECT,
    kw_PURPOSE,
    kw_SUBJECT,
    kw_ENGINEER,
    kw_SITE
    )
