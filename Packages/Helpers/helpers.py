# Max-Planck-Institute for Solar System Reserach
# 
# Python Script Program
#
# Filename:     helpers.py
# Description:  Several useful functions for Python programs
# Author:       K. Heerlein / MPS
# Date:         2020_07_06
# Version:      0.1
# History:      
# 2020_07_06 - port to GitHub repository
#


import os
import sys
# masks
mainDir = sys.path[0]
if __name__ == "__main__":
    sys.path.append(mainDir + r"\\Common")
    sys.path.append(mainDir + r"\\Packages")

import numpy as np
from scipy import stats
from Packages.DetectorLab.Common import DEFS_DATA_EVAL as comdefs
from collections import namedtuple
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import re
import ctypes  # An included library with Python install.
from datetime import datetime
import pickle

import logging

import time
from datetime import datetime
RSLT = namedtuple('RSLT', 'name value unit strformat comment')

def getRSLTitem(data, key):
    try:
        value = np.nan
        unit = ''
        strformat = ''
        comment = ''
        if key.upper() in data:
            item = data[key.upper()]
        elif key in data:
            item = data[key]
        else:
            item = np.nan
            print('item not found {:}'.format(key))
        if isinstance(item, Helpers.RSLT):
            unit = item.unit
            strformat = item.strformat
            comment = item.comment
            value = item.value
        else:
            value = item

    except Exception as e:
        print('Exception getitem - {:}'.format(e))
    return value, unit, strformat, comment



LINECOLORS = ['r', 'g', 'b', 'c', 'm', 'y', 'w']


def getRSLTfromHDR(hdr, kw, RSLTS, unitstr=None, formatstr=None):
    if kw in hdr:
        if unitstr == None:
            unitstr = ''
        if formatstr == None:
            formatstr = '{:}'
        if kw in RSLTS:
            vals = RSLTS[kw].value.append(hdr[kw])
        else:
            vals = []
            vals.append(hdr[kw])
        RSLTS[kw] = RSLT(kw, vals , unitstr, formatstr, hdr.comments[kw])
    return RSLTS



def makeunixtime(adatetime):
    atime = time.mktime(adatetime.timetuple())
    return atime




DARKDATA = namedtuple('DARKDATA','filename inttime hdr data timestamp')

from collections import namedtuple
ScriptInfo = namedtuple('ScriptInfo', 'Scriptname Author Copyright Credits License Maintainer Email Status Version Date')


def RSLTtoCSV(RSLT):
    value=RSLT.strformat.format(RSLT.value)
    return value

def RSLTtostr(RSLT):
    astr=RSLT.strformat.format(RSLT.value) +RSLT.unit
    return astr

def is_odd(num):
   return num % 2 != 0


# class to write RSLT data into table and provide output ready to be written to pdf

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def info(text, item):
    print('{:<20} : {:}'.format(text,item))

    return

def removelinefeed(astr):
    astr=re.sub("\n","",astr)
    return astr


def wraptext(text, width):
    lines = []
    for paragraph in text.split('\n'):
        line = []
        len_line = 0
        for word in paragraph.split(' '):
            len_word = len(word)
            if len_line + len_word <= width:
                line.append(word)
                len_line += len_word + 1
            else:
                lines.append(' '.join(line))
                line = [word]
                len_line = len_word + 1
        lines.append(' '.join(line))
    return '\n'.join(lines)


def save_imgStack_to_file(path,imgStack):
    import pickle
    filename = os.path.join(path, comdefs.cst_img_stack_Data_File)
    f = open(filename, "wb")
    for item in imgStack:
        pickle.dump(imgStack[item], open(filename, "ab"))


def saveDataset(path,PlotInfo, data, Title):
    RSLTS = {}
    for item in PlotInfo:
        RSLTS[item] = PlotInfo[item]
    RSLTS['Title'] = RSLT('Title', data,'','',Title)
    filename = os.path.join(path,renamespecialcharacters(Title)+'.p')
    f = open(filename, "wb")
    for item in RSLTS:
        pickle.dump(RSLTS[item], open(filename, "ab"))
    return RSLTS



def save_RSLTS(filename, RSLTS):

    f = open(filename, "wb")
    for item in RSLTS:
        pickle.dump(RSLTS[item], open(filename, "ab"))
    return RSLTS



# function to store the dictionary RSLTS to a file
def save_RSLTS_to_file(path,RSLTS):
    filename  = os.path.join(path, comdefs.cst_img_stack_RSLTS_File)
    save_RSLTS(filename, RSLTS)
    return

# function to store pixel results dictionary to a file
def save_pixelRSLTS_to_file(path, RSLTS):
    filename = os.path.join(path, comdefs.cst_img_stack_RSLTS_pixels_File)
    save_RSLTS(filename, RSLTS)
    return

    '''
    import json
    f = open(os.path.join(path,"dict.json"), "w")
    for item in RSLTS:
        json = json.dumps(RSLTS[item])
        f.write(json)
    f.close()
    '''
    '''
    #f = open(os.path.join(path,'RSLTS.txt','w')
    #f.write(str(RSLTS))
    #f.close()
    '''

def load_RSLTS(filename):
    RSLTS = {}
    try:
        with open(filename, 'rb') as infile:
            statusmsg('Load RSLTS from File: ',filename)
            while True:
                ARSLT = pickle.load(infile)
                RSLTS[ARSLT.name] = ARSLT
                statusmsg('Loading item: ', ARSLT.name)
    except EOFError:
        statusmsg('Reading done '.format(filename))
        pass
    return RSLTS



def load_imgStack_from_file(path):
    filename = os.path.join(path, comdefs.cst_img_stack_Data_File)
    RSLTS = load_RSLTS(filename)
    return RSLTS


def load_RSLTS_from_file(path):
    import pickle
    RSLTS = {}
    try:
        filename = os.path.join(path, comdefs.cst_img_stack_RSLTS_File)
        with open(filename, 'rb') as infile:
            statusmsg('Load Dictionary from File: ',filename)
            while True:
                ARSLT = pickle.load(infile)
                RSLTS[ARSLT.name] = ARSLT
                if isinstance(RSLTS[ARSLT.name].value, list):
                    noofitems = len(RSLTS[ARSLT.name].value)
                else:
                    noofitems = 1
                statusmsg('Loaded: {:} - {:} items'.format(ARSLT.name,noofitems))
    except EOFError:
        statusmsg('Reading done '.format(filename))
    except:
        statusmsg('Error loading file: '.format(filename))
    pass

    return RSLTS


def load_PixelRSLTS_from_file(path):
    import pickle
    RSLTS = {}
    try:
        filename = os.path.join(path, comdefs.cst_img_stack_RSLTS_pixels_File)
        with open(filename, 'rb') as infile:
            statusmsg('Load Dictionary from File: ',filename)
            while True:
                ARSLT = pickle.load(infile)
                RSLTS[ARSLT.name] = ARSLT
                if isinstance(RSLTS[ARSLT.name].value, list):
                    noofitems = len(RSLTS[ARSLT.name].value)
                else:
                    noofitems = 1
                statusmsg('Loaded: {:} - {:} items'.format(ARSLT.name,noofitems))
    except  EOFError:
        statusmsg('Reading done '.format(filename))
    except:
        statusmsg('Error loading file: '.format(filename))

    pass
    return RSLTS

def get_dataarray(data):
    if isinstance(data, RSLT):
           data = data.value
    data = [float(i) for i in data]  # convert strings to floats
    data = np.reshape(data, len(data),1)
    return data

# get the boundary coordinates of a mask (row,column)
def boundarybox(img):
    img = (img > 0)
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.argmax(rows), img.shape[0] - 1 - np.argmax(np.flipud(rows))
    cmin, cmax = np.argmax(cols), img.shape[1] - 1 - np.argmax(np.flipud(cols))
    return rmin, rmax, cmin, cmax


def RemoveNondigits(Astr):
    Astr=re.sub("[^-0123456789E\.]","",Astr)
    if Astr[len(Astr)-1].isdigit() == False:
        Astr=Astr[:-1]
    return Astr



def remove_non_digits_from_PD_info(Astring):
    astr=re.sub("[^-0123456789E\.]","",Astring) # extract only number (remove strings from entry)
    if (len(astr)>0):
        if astr[len(astr) - 1].isdigit() == False: #remove remaining 'E' at end of string ('- 4.665E-06; CURR; DC; DISPLAY AMPS; NULL OFF; LINEAR; FLTR OFF')
            astr = astr[:-1]
    return astr

def renamespecialcharacters(Filename):


    newname = Filename.replace('#', '')
    newname = newname.replace('%', '')
    newname = newname.replace('*', '')
    newname = newname.replace('<', '')
    newname = newname.replace('>', '')
    newname = newname.replace('*', '')
    newname = newname.replace('?', '')
    newname = newname.replace('$', '')
    # newname = newname.replace('!', '')
    # newname = path.replace('\'', '-')
    newname = newname.replace('"', '')
    newname = newname.replace('\'', '')
    newname = newname.replace('Å', 'ś')
    newname = newname.replace('Å', 'ń')
    newname = newname.replace(':', '')

    # newname = path.translate(str.maketrans("","",delchars))

    # re.sub('[^\w\-_\. ]', '_', newname)

    return newname


def fitFunc(t, a, b, c):
    return a*np.exp(-b*t) + c


def linearfit(x,y,range_l,range_h):

    '''x_ = np.reshape(x[range_l:range_h+1],[range_h-range_l+1]) # 2018_02_13 KH: added "+1" because the array was misisng 1 item
    y_ = np.reshape(y[range_l:range_h+1],[range_h-range_l+1]) # 2018_02_13 KH: added "+1" because the array was misisng 1 item
    '''
    try:
        x_ = np.reshape(x[range_l:range_h+1],[range_h-range_l+1]) # 2018_09_13: missing +1 for FPA , added ??? 2018_04_16 KH: removed: +1, why was there missing 1 item ? on SUFI it works
        y_ = np.reshape(y[range_l:range_h+1],[range_h-range_l+1]) # 2018_09_13: missing +1 for FPA , added ??? 2018_04_16 KH: removed: +1 why was there missing 1 item ? on SUFI it works

        x_ = np.array(x_)
        y_ = np.array(y_)

        slope, intercept, r_value, p_value, std_err =stats.linregress(x_, y_)
    except:
        slope, intercept, r_value, p_value, std_err = np.nan



    #print("Slope calculated %5.3f" % slope)
    # The mean squared error
    #print("Slope error: %5.6f" % std_err)


    '''
    # Create linear regression object
    regr = linear_model.LinearRegression(fit_intercept=True)

    # Train the model using the training sets
    # print('Data: '+str(len(x))+'  '+str(len(y)))
    x_ = np.reshape(x[range_l:range_h],(range_h-range_l, 1))
    y_ = np.reshape(y[range_l:range_h],(range_h-range_l, 1))
    x=np.reshape(x,(len(x),1))
    regr.fit(x_,y_)
    # The mean squared error
    # Make predictions using the testing set
    y_pred = regr.predict(x)
    y_pred = np.reshape(y_pred, len(y_pred), 1)
    # The mean squared error
    print("Slope calculated %.2f" % regr.coef_[0])


    # The mean squared error
    print("Mean squared error: %.2f" % mean_squared_error(y, y_pred))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % r2_score(y, y_pred))

    # The coefficients
    # print('Coefficients: \n', regr.coef_)
    # print('Intercept:' + str(regr.intercept_))

    #y_pred_ = np.reshape(y_pred[range_l:range_h],(range_h-range_l, 1))
    # print("Mean squared error: %.2f" % mean_squared_error(y_, y_pred_))
    # Explained variance score: 1 is perfect prediction
    # print('Variance score: %.2f' % r2_score(y_, y_pred_))

    #slope, intercept, r_value, p_value, std_err = stats.linregress(x_, y_)


    # Not used: other option to calculate the linear regression:
    # alpha, beta, r_value, p_value, std_err = stats.linregress(x, y)
    # print('y={5.3}*x+{5.2}'.format(alpha,beta))


    return y_pred, regr.coef_, regr.intercept_
    
    '''
    return slope, intercept, r_value, p_value, std_err

def dctToNdarray (dd, szFormat = 'f8'):
    '''
    Convert a 'rectangular' dictionnary to numpy NdArray
    entry
        dd : dictionnary (same len of list
    retrun
        data : numpy NdArray
    '''
    names = dd.keys()
    firstKey = dd.keys()[0]
    formats = [szFormat]*len(names)
    dtype = dict(names = names, formats=formats)
    values = [tuple(dd[k][0] for k in dd.keys())]
    data = np.array(values, dtype=dtype)
    for i in range(1,len(dd[firstKey])) :
        values = [tuple(dd[k][i] for k in dd.keys())]
        data_tmp = np.array(values, dtype=dtype)
        data = np.concatenate((data,data_tmp))
    return data



nocomment=''
useraw='useraw'



def getconvertedvaluestr(data, formatstr,conv_f,conv_offs):
    if type(data) == str:
        value = data
    else:
        if isinstance(data,list):
            data = [float(i) for i in data]  # convert strings to floats
            value = np.average(data)
        else:
            value = data
        if conv_f != '':
            value = value * conv_f + conv_offs
    if 'x' in formatstr:
        value =int(value)
    astr=formatstr.format(value)
    print(astr)
    return astr


def getvalue(data, item,RSLTS,unit,formatstr,conv_f,conv_offs,comment):
    if item in data:
        if type(data[item][0]) == str:
            value = data[item][0]
        else:
            if isinstance(data[item],list):
                data[item] = [float(i) for i in data[item]]  # convert strings to floats
                value = np.average(data[item])
            else:
                value = data[item][0]
            if conv_f != '':
                value = value * conv_f + conv_offs
        if 'x' in formatstr:
            value =int(value)
        if comment == useraw:
            comment='({:2.0f})'.format(data[item][0])
        else:
            comment=''
        RSLTS[item] = RSLT(item, value, unit, formatstr,comment)
        printresult(RSLTS[item])
    else:
        print('{:s} : {:s}'.format('item not found',item))
    return RSLTS



def statusmsg(Message, *args):
    print('{:>25s} : {:s}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S") , Message))
    for a in args:
        print(a)



# function to create a single result out of a list of RSLTS
# the "name","strformat" and "comment" is used from first item
# data is combined as list in "value"
def combinelistofRSLTStoRSLT(callerdata):
    localRSLT = {}
    if isinstance(callerdata,list): # list of headers
        for key in callerdata[0]:
            a = [x[key].value for x in callerdata]
            name = callerdata[0][key].name
            unit = callerdata[0][key].unit
            value = a
            strformat = callerdata[0][key].strformat
            comment = callerdata[0][key].comment
            localRSLT[key] = RSLT(name, value,unit,strformat,comment)
    return localRSLT

def get_centerregion_from_image(data):
    width = data.shape[1]
    height = data.shape[0]
    x = int(width / 4)
    y = int(height / 4)
    x1 = int(width / 2)
    y1 = int(height / 2)
    # print(data[y1 - y:y1 + y, x1 - x:x1 + x])
    return(data[y1 - y:y1 + y, x1 - x:x1 + x])


def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


# from an image array
# get horizontal and vertical cut
def hvsplit(imagedata):
    if len(imagedata.shape) == 3:
        numcolumns = imagedata.shape[1]
        numrows = imagedata.shape[2]
        numframes = imagedata.shape[0]
        #get average of the frames
        imagedata = np.average(imagedata)
    else:
        numcolumns = imagedata.shape[0]
        numrows = imagedata.shape[1]
        numframes = 1

    hcuts = np.hsplit(imagedata, numrows)
    avghcut = [np.average(x) for x in hcuts]
    xrows = np.arange(numrows)

    vcuts = np.vsplit(imagedata, numcolumns)
    avgvcut = [np.average(x) for x in vcuts]
    xcolumns = np.arange(numcolumns)
    '''
    plt.plot(xrows, avgvcut, label='AVG vertical cut')
    plt.plot(xcolumns, avghcut, label='AVG horizontal cut')
    plt.legend()
    '''
    return avgvcut, avghcut, vcuts, hcuts, xrows, xcolumns, numframes

def getItemValueinRSLTS(RSLTS,sel, AVG=False):

    if sel in RSLTS:
        RSLT=RSLTS[sel]
        if isinstance(RSLT,(bool,float,str,int)):
            value = RSLT
            name = sel
            strformat = '{:}'
            unit = ''
            comment=''
            Notes = ''
        elif len(RSLT)==5:

            '''if len(RSLTS[sel].name) > maxlen:
                maxlen = len(RSLTS[sel].name)
            '''
            if isinstance(RSLT.value, list):  # does it contain an array for the value ?

                name = RSLT.name
                unit = RSLT.unit
                strformat = RSLT.strformat
                comment = RSLT.comment
                if isinstance(RSLT.value[0], (str)): # list of strings
                    if len(RSLT.value) == 1:
                        substr = RSLT.value[0]  # only one item
                    elif RSLT.value[0] == RSLT.value[1]:
                        substr = RSLT.value[0] # array of the same strings
                    else:
                        substr = '\n' # start on next line
                        for item in RSLT.value:
                            substr = substr + item + '\n'
                    value = substr
                else: # list, if different, show min and max, avg
                    if AVG:
                        value = np.average(RSLT.value)
                    else:
                        min = np.min(RSLT.value)
                        max = np.max(RSLT.value)
                        if min != max:
                            avg = np.nanmean(RSLT.value)  # ignore nan values
                            subfmt = 'Min: ' + strformat + ' Max: ' + strformat + ' Avg: ' + strformat
                            value= subfmt.format(min,max,avg)
                            comment = '({:d} items)'.format(len(RSLT.value))
                            strformat = '{:}'
                        else:
                            value = RSLT.value[0]

            else:
                # debug only print('it is not a list ', RSLTS[sel].name)
                '''if len(RSLTS[sel].name) > maxlen:
                    maxlen = len(RSLTS[sel].name)
                '''
                value = RSLT.value
                if isinstance(value, str):
                    if len(value)> 80:
                        value='\n'+value # start with new line
                name = RSLT.name
                strformat = RSLT.strformat
                unit = RSLT.unit
                comment = RSLT.comment
                Notes = ''
        else:  # tuple of type 'key,value
            if isinstance(RSLT, dict):
                # added when reading in data from PHI_QM
                value = RSLT[0]
                name = sel
                strformat = '{:}'
                unit = ''
                comment = ''
                Notes = ''
            else:
                value = RSLT
                name = sel
                strformat = '{:}'
                unit = ''
                comment=''
                Notes = ''
        #print('debug ',key)
        '''s = r'{:<'+str(maxlen)+'} : ' + strformat+ ' {:<5}' + ' {:}' #was fixed at :<30
        if isinstance(value, tuple):  # there may be passed tuples of value + error[%]
            aline = s.format(name, value[0], value[1], unit,comment)
        else:
            aline = s.format(name, value, unit,comment)
        '''
    else:
        aline =''
        print('Key not found: '+sel)
        value = ''
    return value

def findmaxlen(RSLTS, Selector):
    def do(RSLTS, sel, maxlen):
        if sel in RSLTS:
            item = RSLTS[sel]
            if isinstance(item, (bool, float, str, int, np.int64)):
                if len(sel) > maxlen:
                    maxlen = len(sel)
            elif isinstance(item[0], str):
                if len(sel) > maxlen:
                    maxlen = len(sel)
            elif isinstance(item, RSLT): #type HELPERS.RSLT
                if len(item.name) > maxlen:
                    maxlen = len(item.name)
            elif isinstance(item, list):
                if len(str(item[0])) > maxlen:
                    maxlen = len(str(item[0]))
        return maxlen

    maxlen = 0
    for sel in Selector:
        #print('debug: selector {:}'.format(sel))
        if isinstance(sel, list):
            for item in sel:
                maxlen= do(RSLTS, item, maxlen)
        else:
            maxlen = do(RSLTS, sel, maxlen)
    return maxlen

# last update 2020_01_09
# 2020_01_09: nan value accepted and passed through
# able to pass Selector as single key and list of keys

def GetResults_from_Tuple(RSLTS, Selector):
    astr = ''

    def do(sel, maxlen):

        if sel in RSLTS: 
            RSLT=RSLTS[sel]
            if isinstance(RSLT, (bool, float, str, int, np.int64)):
                value = RSLT
                name = sel
                strformat = '{:}'
                unit = ''
                comment=''
                Notes = ''
            elif len(RSLT) == 1:
                value = RSLT[0]
                name = sel
                strformat = '{:}'
                unit = ''
                comment = ''
                Notes = ''

            elif len(RSLT) == 5:
                name = RSLT.name
                unit = RSLT.unit
                strformat = RSLT.strformat
                comment = RSLT.comment
                if isinstance(RSLT.value, (float, (np.float64, np.int64, int, str))):
                    value = RSLT.value
                elif (isinstance(RSLT.value, list) and (len(RSLT.value)>1) ):  # does it contain an array for the value ?
                    if isinstance(RSLT.value[0], (str)): # list of strings
                        alist = [RSLT.value[0]]
                        anitem = alist[0]
                        for i in range(1, len(RSLT.value)):
                            if not (anitem in RSLT.value[i]): # if the list of strings has different values
                                alist.append(RSLT.value[i])
                        substr='\n' # start on next line
                        if len(alist) > 1:
                            for item in alist:
                                substr = substr+item+'\n'
                        else:
                            substr = alist[0]
                        value=substr
                    elif np.isnan(RSLT.value[0]):
                        value = RSLT.value[0]
                        strformat = '{:}'
                    else: # list, if different, show min and max, avg
                        #print('debug - {:}'.format(RSLT.name))
                        try:
                            min = np.min(RSLT.value)
                            max = np.max(RSLT.value)
                            if min != max:
                                avg = np.nanmean(RSLT.value)  # ignore nan values
                                subfmt = 'Min: ' + strformat + ' Max: ' + strformat + ' Avg: ' + strformat
                                value = subfmt.format(min,max,avg)
                                comment = '({:d} items)'.format(len(RSLT.value))
                                strformat = '{:}' # the resulting value is now a string !
                            else:
                                value = RSLT.value[0]
                        except:
                            print('error  GetResults_from_Tuple finding min/max {:}'.format(RSLT.name))
                            value = RSLT.value[0]
                else:
                    if (isinstance(RSLT.value, list) and (len(RSLT.value)==1) ):
                        value = RSLT.value[0]
                        strformat = RSLT.strformat
                        if isinstance(value, str):
                            if len(value)> 80:
                                value='\n'+value # start with new line
                        elif np.isnan(value):
                            strformat = '{:}'
                        name = RSLT.name
                        unit = RSLT.unit
                        comment = RSLT.comment
                        Notes = ''
                    else:
                        value = RSLT.value
                        if isinstance(value, str):
                            if len(value)> 80:
                                value='\n'+value # start with new line
                        name = RSLT.name
                        strformat = RSLT.strformat
                        unit = RSLT.unit
                        comment = RSLT.comment
                        Notes = ''
            else:  # tuple of type 'key,value
                value = RSLT
                name = sel
                strformat = '{:}'
                unit = ''
                comment=''
                Notes = ''
            #print('debug ',key)
            if strformat =='':
                strformat = '{:}'
            s = r'{:<'+str(maxlen)+'} : ' + strformat + ' {:<5}' + ' {:}' #was fixed at :<30
            if isinstance(value, tuple):  # there may be passed tuples of value + error[%]
                aline = s.format(name, value[0], value[1], unit, comment)
            else:
                aline = s.format(name, value, unit, comment)
        else:
            aline =''
            print('Key not found: '+sel)
        return aline, maxlen


    maxlen = findmaxlen(RSLTS, Selector)
    if isinstance(Selector, str): # just a single str as key
        aline, maxlen = do(Selector, maxlen)
        if aline != '': astr += '\n' + aline
    else:
        for key in Selector:
            if isinstance(key,(list, tuple, set)):
                for item in key:
                    aline, maxlen = do(item, maxlen)
                    if aline != '': astr += '\n' + aline
            else: # only one single item
                aline, maxlen = do(key,maxlen)
                if aline != '': astr += '\n' + aline
    return astr

csv_separator=';'
commentchar='# '


def fileexists(Filename):
    if os.path.isfile(Filename):
        result = True
    else:
        result = False
        statusmsg('Error - File not found', Filename)
    return result

def GetcsvFileHeader(RSLTS, Selector):
    astr = ''
    for key in Selector:
        aline = commentchar+'{:<25} : {}'.format(key, RSLTS[key]) + '\n'
        astr = astr + aline
    return astr


class SliceMaker(object):
    def __getitem__(self, item):
        return item


# sort the data
def sort(x,y):
    from operator import itemgetter
    L = sorted(zip(x, y), key=itemgetter(0))
    new_x, new_y = zip(*L)
    return np.asarray(new_x), np.asarray(new_y)

''' obsolete - use GetResults_from_Tuple
def GetResults(RSLTS, Selector):

    def getitem(sel):
        if sel in RSLTS:
            value = RSLTS[sel]

        else:
            print('GetResults - Key not found: ', sel)
            value = ''
        aline = '{:<25} : {}'.format(sel, value) + '\n'
        return aline

    astr = ''
    for key in Selector:
        if isinstance(key, list):  # list of selectors provided
            for item in key:
                sel = item
                astr = astr + getitem(sel)
        else:
            sel = key
            astr = astr + getitem(sel)
    return astr
'''

def GetHeaders(Selector):
    astr = ''
    for header in Selector:
        aline = '{:<25}'.format(header) + ';'
        astr = astr + aline
    return astr


from scipy.optimize import curve_fit
from scipy import  exp
def gaus(x,a,x0,sigma):
    return a*exp(-(x-x0)**2/(2*sigma**2))

''' no tested yet
def gauss(x, p): # p[0]==mean, p[1]==stdev
    return 1.0/(p[1]*np.sqrt(2*np.pi))*np.exp(-(x-p[0])**2/(2*p[1]**2))
'''

def findslope(x,y):
    a, b, _, _ = np.linalg.lstsq(np.reshape(x,[len(x),1]), np.reshape(y,[len(y),1]))
    slope = float(a[0])
    varx = np.square(np.std(x))
    vary = np.square(np.std(y))

    ssym = sum(np.square(y))
    N = len(x)
    R2 = 1 - float(b[0]) / ssym
    # 'mse' is a mean square error (the sum of squared residuals divided by number
    # of model parameters), which can be calculated directly as:
    #   mse = sum((y-(slope*x+intercept))**2) / (N-2)
    # But equivalently it can also be calculated in a faster way as:
    mse = (1 - R2) * vary / (N - 2)
    stderr_slope = np.sqrt(mse / varx)

    testN = len(x)
    testxmean = np.sum(x) / testN
    testymean = np.sum(y) / testN
    testvarx = np.dot( x-np.mean(x),x-np.mean(x))
    testvary = np.dot( y-np.mean(y),y-np.mean(y))
    testcovxy = np.dot( x-np.mean(x),y-np.mean(y))
    testslope = testcovxy / testvarx
    testintercept = testymean - testslope * testxmean
    testr_den = np.sqrt(testvarx * testvary)
    tiny = 0.1E-2
    if (abs(testr_den) < tiny):
        testr = 0
    else:
        testr = testcovxy / testr_den
    # Normalize to[-1, 1] in case     of     numerical     error     propagation
    if (testr > 1):
        testr = 1
    elif (testr < -1):
        testr = -1
    # 'mse' is a mean square error (the sum of squared residuals divided by number
    # of model parameters), which can be calculated directly as:
    #   mse = sum((y-(slope*x+intercept))**2) / (N-2)
    # But equivalently it can also be calculated in a faster way as:
    mse = (1 - testr ** 2) * testvary / (N - 2)
    stderr_slope = np.sqrt(mse / testvarx)
    stderr_intercept = np.sqrt(mse * (1 / N + testxmean ** 2 / testvarx))
    return testslope, stderr_slope


def linfitzero(x,*p):
    a,b = p
    return a * x + b

# Lorentz fit function
def lorentz(x, *p):
    I, gamma, x0 = p
    return I * gamma**2 / ((x - x0)**2 + gamma**2)

def errorfunc(p,x,z):
        return lorentz(p,x)-z


def fitLorentz(p, x, y):
    return curve_fit(lorentz, x, y, p0=p)

def fitGaus(p,x,y):
    return curve_fit(gaus, x, y, p0=p)

# returns the header row for the csv
# 2018_02_13: KH: also a list of keys can be passed
def GetHeaderRow_csv(Selector):
    astr = ''
    def do(item, astr):
        if isinstance(item, list):
            for name in item:
                aline = '{:}'.format(name) + csv_separator
                astr = astr + aline
        else:
            aline = '{:}'.format(item) + csv_separator
            astr = astr + aline
        return astr

    for header in Selector:
        if isinstance(header, list):
            for item in header:
                astr = do(item, astr)
        else:
            astr = do(header, astr)

    return astr


def getarray_from_RSLTS(RSLTS, sel):
    if sel in RSLTS:
        RSLT = RSLTS[sel]
        # print('debug ',key)
        if len(RSLT) == 5:  # tuple of type 'name,value,unit,format
                value = RSLT.value  # provide the list in the value
                name = RSLT.name
                strformat = RSLT.strformat
                unit = RSLT.unit
                comment = RSLT.comment
                Notes = 'AVG of {:d} items'.format(len(RSLT.value))
        else:
            value = RSLT.value
            name = RSLT.name
            strformat = RSLT.strformat
            unit = RSLT.unit
            Notes = ''
            comment = RSLT.comment
    else:
        print('Key not found: ' + sel)
        value = []
    return value


def getvalue_in_RSLTS(RSLTS, sel):
     if sel in RSLTS:
         RSLT=RSLTS[sel]
         #print('debug ',key)
         if len(RSLT)==5: # tuple of type 'name,value,unit,format
             if isinstance(RSLT.value,list): # does it contain an array for the value ?
                 if isinstance(RSLT, (int, float)):
                     value = np.nanmean(RSLT.value)  # ignore nan values
                 else:
                     value = RSLT.value[0]  # for example list of filenames, just pass first one
                 name=RSLT.name
                 strformat=RSLT.strformat
                 unit=RSLT.unit
                 comment = RSLT.comment
                 Notes='AVG of {:d} items'.format(len(RSLT.value))
             else:
                 value=RSLT.value
                 name = RSLT.name
                 strformat = RSLT.strformat
                 unit = RSLT.unit
                 Notes = ''
                 comment = RSLT.comment
         else:# tuple of type 'key,value
             value = RSLT
             name = sel
             strformat = '{:}'
             unit = ''
             Notes = ''
             comment = nocomment
         s=r''+strformat+' {:}'
         valuestring=s.format(value,comment)
         if len(valuestring)> 30: valuestring=insert_newlines(valuestring,30)
         if len(name) > 30: name = insert_newlines(name, 30)
         #data.append({'item': sel,'name':name, 'value': valuestring, 'unit': unit , 'comment':comment, 'notes':Notes })
     else:
         print('Key not found: '+sel)
         value = []
     return value


def getSummaryDataTable(RSLTS,thetuple):
    def getitem():
         if sel in RSLTS:
             RSLT=RSLTS[sel]
             #print('debug ',key)
             if len(RSLT)==5: # tuple of type 'name,value,unit,format
                 if isinstance(RSLT.value,list): # does it contain an array for the value ?
                     if isinstance(RSLT, (int, float)):
                         value = np.nanmean(RSLT.value)  # ignore nan values
                     else:
                         value = RSLT.value[0]  # for example list of filenames, just pass first one
                     name=RSLT.name
                     strformat=RSLT.strformat
                     unit=RSLT.unit
                     comment = RSLT.comment
                     Notes='AVG of {:d} items'.format(len(RSLT.value))
                 else:
                     value=RSLT.value
                     name = RSLT.name
                     strformat = RSLT.strformat
                     unit = RSLT.unit
                     Notes = ''
                     comment = RSLT.comment
             else:# tuple of type 'key,value
                 value = RSLT
                 name = sel
                 strformat = '{:}'
                 unit = ''
                 Notes = ''
                 comment = nocomment
             s=r''+strformat+' {:}'
             valuestring=s.format(value,comment)
             if len(valuestring)> 30: valuestring=insert_newlines(valuestring,30)
             if len(name) > 30: name = insert_newlines(name, 30)
             data.append({'item': sel,'name':name, 'value': valuestring, 'unit': unit , 'comment':comment, 'notes':Notes })
         else:
             print('Key not found: '+sel)
         return

    #tuple=defs.tuple_UVDA_allResults
    data=[]

    for key in thetuple:
        if isinstance(key,list): # list of selectors provided
            for item in key:
                sel = item
                getitem()
        else:
            sel=key
            #print('Debug: ',sel)
            getitem()
    return data

# todo store pixel results in array
# todo maintain avg results where ?
def StoreRSLTS(localRSLTS, RSLTS, Section, Pixel):

    #if item is in tuple for reoccuring parameters, only store once , common for all

    if Pixel == []:
        for item in localRSLTS:
            RSLTS[Section+item] = RSLT(localRSLTS[item].name+Section,localRSLTS[item].value,localRSLTS[item].unit, localRSLTS[item].strformat, localRSLTS[item].comment)
    else:
       for item in localRSLTS:
            if not (item+'_Pixel') in RSLTS:
                RSLTS[item+'_Pixel'] = RSLT(localRSLTS[item].name+'_Pixel' + Section, [],
                                                 localRSLTS[item].unit, localRSLTS[item].strformat,
                                                 localRSLTS[item].comment)
            RSLTS[item + '_Pixel'].value.append(localRSLTS[item].value)

    return RSLTS

#store item from fits header to RSLT
def storefromHDR(RSLTS, newname, fitshditemname=None, hdr=None ,val=None,  strformat='{:}', strunit='', strcomment=''):
    strformat = strformat
    strunit = strunit
    strcomment = strcomment
    if newname is not None:
        itemname = newname
    else:
        itemname = fitshditemname
    try:
        if fitshditemname == None:
            # we expect a already calculated value that shall be stored to newname in RSLTS
            val = val
        else:
            # we expect a fits hdr and shall store the val to RSLTS under newname
        #todo:if item exists, add value to list
            val = hdr[fitshditemname]
            if strcomment == '':
                strcomment = hdr.comments[fitshditemname]

        #we return always a list in value
        if itemname in RSLTS:
            vals = RSLTS[itemname].value.append(val)
        else:
            vals = []
            vals.append(val)
        RSLTS[itemname] = Helpers.RSLT(itemname, vals, strunit, strformat, strcomment)
    except:
        print('error getting {:} from header'.format(itemname))
    return RSLTS


def store(item, arrRSLTS, RSLTS):
    strformat = '{:}'
    strunit = '[]'
    strcomment = ''
    if item == comdefs.cst_DET_TEMP:
        strformat = '{:+2.1f}'
        strunit = '[°C]'
    if isinstance(item, (RSLT)):
        RSLTS[item] = RSLT(item, arrRSLTS[item].value, arrRSLTS[item][0].unit, arrRSLTS[item][0].strformat,
                                   arrRSLTS[item][0].comment)
    else:
        RSLTS[item] =  RSLT(item, arrRSLTS[item], strunit, strformat, strcomment)
    return RSLTS


def makelistuppercase(alist):
    # everything uppercase
    newlist = []
    for item in alist:
        if isinstance(item, list):
            for it in item:
                if isinstance(it, list):
                    for k in it:
                        newlist.append(k.upper())
                else:
                    newlist.append(it.upper())
        else:
            newlist.append(item.upper())
    return newlist







# return single data line for the csv
def GetResults_csv(RSLTS, Selector):
    def getitem(sel):
        if sel in RSLTS:
            if isinstance(RSLTS[sel], (np.int64, int, bool, str, float)):
                value = RSLTS[sel]
            elif len(RSLTS[sel]) == 5:  # tuple of type 'name,value,unit,format,comment
                if isinstance(RSLTS[sel].value, list):  # does it contain an array for the value ?
                    if len(RSLTS[sel].value) == 1:
                        value = RSLTS[sel].value[0]
                        s_format = RSLTS[sel].strformat
                        value = s_format.format(value)
                    elif isinstance(RSLTS[sel].value[0], (int, float)):
                        if isinstance(RSLTS[sel].value[0], int):
                            try:
                                value = int(np.nanmean(RSLTS[sel].value))  # ignore nan values, get back average
                            except:
                                print('exception: found strings in expected list integers -> using only first item')
                                value = int(RSLTS[sel].value[0])
                        else:
                            value = np.nanmean(RSLTS[sel].value)  # ignore nan values, get back average
                        s_format = RSLTS[sel].strformat
                        value = s_format.format(value)
                    else:
                        try:
                            s_format = RSLTS[sel].strformat
                            value = s_format.format(RSLTS[sel].value[0])
                        except:
                            value = RSLTS[sel].value[0]  # for example list of filenames, just pass first one
                else:
                    try:
                        s_format=RSLTS[sel].strformat
                        value = s_format.format(RSLTS[sel].value)
                        #value = '{:>2.4E}'.format(RSLTS[sel].value)
                    except:
                        value = RSLTS[sel].value
            else:
                value = RSLTS[sel]
        else:
            print('key not found :', sel)
            value = np.nan
        if isinstance(value, str):
            value = value.replace(csv_separator, '') # remove characters having the csv_separator
        aline = "{:}".format(value) + csv_separator
        return aline

    astr = ''
    for key in Selector:
        if isinstance(key,list): # list of selectors provided
            for item in key:
                sel = item
                aline = getitem(sel)
                astr = astr + aline
        else:
            sel=key
            aline = getitem(sel)
            astr = astr + aline
    return astr


def getarrvaluesfromRSLT(RSLT,rangemin, rangemax):
    arr=[]
    for i in range(rangemin, rangemax):
        arr.append(RSLT[i].value)
    return arr

def GetResults_from_Tuple_index(RSLTS,index,Selector):
    astr = ''
    maxlen=0
    def getitem(sel,maxlen):
        if len(RSLTS[sel].name) > maxlen:
            maxlen = len(RSLTS[sel].name)
        print(sel)
        RSLT = RSLTS[sel]
        s = r'{:<' + str(maxlen) + '} : ' + RSLT.strformat + ' {:<5}'  # was :<43
        if isinstance(RSLT.value, list):
            aline = s.format(RSLT.name, RSLT.value[index], RSLT.unit)  # if the result is an array (of pixel values)
        else:
            aline = s.format(RSLT.name, RSLT.value, RSLT.unit)
        return aline,maxlen

    for key in Selector:
        if isinstance(key,list): # list of selectors provided
            for item in key:
                sel = item
                if sel in RSLTS:
                   aline,maxlen=getitem(sel,maxlen)
                   astr += '\n' + aline
                else:
                   print('Key not found: ' + key)

        else:
            sel=key
            if sel in RSLTS:
                aline,maxlen = getitem(sel,maxlen)
                astr += '\n'+ aline
            else:
                print('Key not found: '+key)
    return astr



def printresult(RSLT):
    if isinstance(RSLT.value, tuple): # there may be passed tuples of value + error[%]
        s = r'{:<20} : ' + RSLT.strformat + ' {:}'
        out = s.format(RSLT.name, RSLT.value[0],RSLT.value[1], RSLT.unit)
    elif isinstance(RSLT.value,(list)):
        s = r'{:<20} : ' + RSLT.strformat + ' {:}'
        for i in range(len(RSLT.value)):
            out=s.format(RSLT.name,RSLT.value[i],RSLT.unit)
            print(out)
    else:
        out = '{:} {:} {:}'.format(RSLT.name, RSLT.value, RSLT.unit)
        print(out)
    return out


def search_index_Array_Where(arr,b):
     try:
        k=arr.index(b)
        return k
     except ValueError:
        return 'not found'


#this will find the first match
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)



# this will find all matches:
def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

# this will match a pattern:


def findFileswithSubstring(substr, path):
    # finds all directories recursively
    listofDirs=[x[0] for x in os.walk(path)]
    print('findFileswithSubstring ....')
    print('Found the following directories:')
    for i in range(0, len(listofDirs)):
        print(listofDirs[i])
    all_fits_files = []
    for k in range(0,len(listofDirs)):
        mypath=listofDirs[k]
        print('looking for substring on files in directory: ',mypath)
        # all_fits_files = filter(lambda x: x.endswith('.fits'), os.listdir(mypath))
        all_fits_files = [os.path.join(mypath,fileName) for fileName in os.listdir(mypath) if substr in fileName]
        all_fits_files = [fileName for fileName in all_fits_files if fileName.endswith(".fits")]
    return all_fits_files

import  fnmatch
def find_files_with_pattern(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

# example: find('*.txt', '/path/to/dir')
def insert_newlines(string, every):
    return '\n'.join(string[i:i+every] for i in range(0, len(string), every))

def correct_negative_and_Zero(img):
    amin=np.min(img)
    print('Minimum in Data:',amin)

    # avoid negative / zero values
    if amin<0:
        img=img-amin+0.01
        astr=',Negative Data detected, corrected by: '+str( -amin+0.01)
        s_history = astr
        print(astr)
    if amin==0:
        img=img+0.1
        astr =',Zero Values detected, adding ' + str(0.1)
        s_history =  astr
        print(astr)
    amin=np.min(img)
    print('minimum:',amin)

    return img,s_history


def numberOfSetBits(i):
    i = i - ((i >> 1) & 0x55555555)
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
    return (((i + (i >> 4) & 0xF0F0F0F) * 0x1010101) & 0xffffffff) >> 24


def FindPixelsBelowThreshold(IMG,im_med,Mask,Threshold):
    # median filter calculate quotient image/median_img
    im_med = IMG / im_med
    matrix_data_belowthreshold = np.logical_and(Mask==True, im_med < Threshold).astype(bool) # hier fehlt noch, dass nur der Bereich innerhalb der Maske berücksichtigt wird
    n = sum(sum(matrix_data_belowthreshold))
    print('found pixels below threshold of {:2.0f}% :'.format(Threshold*100),n)
    return matrix_data_belowthreshold, n


def FindPixelsAboveThreshold(IMG,im_med,Mask,Threshold):
    # median filter calculate quotient image/median_img
    if isinstance(im_med,(float,str,int)): # not an image, make matrix
        value= float(im_med)
        im_med = np.zeros(IMG.shape)
        im_med.fill(value)
    im_med = IMG / im_med
    matrix_data_abovethreshold = np.logical_and(Mask==True, im_med > Threshold).astype(bool) # hier fehlt noch, dass nur der Bereich innerhalb der Maske berücksichtigt wird
    n = sum(sum(matrix_data_abovethreshold))
    print('found pixels above threshold of {:2.1f} x Medium Signal:'.format(Threshold),n)
    return matrix_data_abovethreshold, n


# read bytes from file
# returns numpy array of bytes
# KH 2019_07_05 used for EUI data offset maps
def readbytesFromFile(FullFilename):
    with open(FullFilename, mode='rb') as file: # b is important -> binary
        fileContent = np.fromfile(file, dtype=np.byte)
    return fileContent



#  bit crunching functions

# convert 2s compliment value to integer
# bitlen is the no of bits without sign bit
# 2019_07_05 KH used for EUI data offset maps
def twos_complement_to_int(value, bitWidth):
    if value >= (2**bitWidth+1):
        a = -2**bitWidth+ (value & (2**bitWidth-1))
    else:
        a = value
    return a


# convert integer value to 2s compliment
# bitlen is the no of bits without sign bit
# 2019_07_05 KH used for EUI data offset maps
def int_to_twos_complement(value, bitWidth):
    if (value> (2**bitWidth)-1) or  (value< -(2**bitWidth)):
        # This catches when someone tries to give a value that is out of range
        raise ValueError("Value: {} out of range of {}-bit value.".format(value, bitWidth))
    else:
        if value < 0:
            value = (2**bitWidth-abs(value)) +2**bitWidth
        else:
            value = value
    return value
