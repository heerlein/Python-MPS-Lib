import serial

import time
import logging
from Packages.Helpers import Helpers

cst_CRLF = '\r\n'
n_FuseTripped = 'FuseTripped'
n_OutpState = 'OutpState'
n_CurrLimit = 'CurrLimit'
n_Current = 'Current'
n_Voltage = 'Voltage'
n_Power = 'Power'
numchannels = 4
import threading

from PyQt5.QtCore import *
import sys

class HM4040():

    def __init__(self, portName=None, str_serialnumber=''):
        self.loop = QEventLoop()
        self.sleeptimer = QTimer()
        self.baudrate = 9600
        self.readTimeout = 500
        self.writeTimeout = 500
        self.portName = portName
        self.serialPort = serial.Serial(self.portName, baudrate=self.baudrate, timeout=self.readTimeout,
                                write_timeout=self.writeTimeout)
        self.identified = False
        self.identify(str_serialnumber)
        self.CH1_ON = None
        self.CH2_ON = None
        self.CH3_ON = None
        self.CH4_ON = None

        if self.identified:
            self.chstatus = []
            self.StatusMainOutput = None
            self.StatusUnithasTripped = False
            self.StatusTotalPwr = 0
            for i in range(4):
                adict = {}
                self.chstatus.append(adict)
                self.chstatus[i]['Channel'] = i+1


            self.getHK()
            self.checkifAnyFusehastripped()
            self.initialized = True
        else:
            self.initialized = False
            logging.error('Unit could not be matched with identification {:} - got: {:}'.format(str_serialnumber, astr))

    def identify(self, str_serialnumber):
        astr = self.identity()
        if astr == str_serialnumber:
            self.identified = True
            return True
        else:
            self.identified = False
            return False

    def handle_data(data):
        print(data)

    def identity(self):
        command = '*IDN?'
        ret = self.write(command)
        return ret

    def openPort(self):
        if not self.serialPort.is_open:
            self.serialPort.open()

    def closePort(self):
        self.serialPort.close()

    def getOutpStat(self, ch):
        self.selChannel(ch)
        command = 'OUTP:STAT?'
        ret = self.write(command)
        if ret is not '':
            res = bool(int(ret))
            self.chstatus[ch-1][n_OutpState] = res
            if ch == 1:
                self.CH1_ON = res
            elif ch == 2:
                self.CH2_ON = res
            elif ch == 3:
                self.CH3_ON = res
            elif ch == 4:
                self.CH4_ON = res

        return ret


    def getStatusMainOutput(self):
        command = 'OUTP:GEN ?'
        ret = self.write(command)
        self.StatusMainOutput = bool(int(ret))

    def setMainOutput(self, On = False):
        if On:
            command = 'OUTP:GEN ON'
        else:
            command = 'OUTP:GEN OFF'
        ret = self.write(command)
        logging.info('HMP4040 - Main Output set to {:}'.format(On))
        self.getStatusMainOutput()
        return ret

    def getVers(self):
        command = 'SYST:VERS?'
        ret = self.write(command)
        print('Version is {:}'.format(ret))

    def write(self, strcommand):
        self.openPort()
        strcommand = strcommand + cst_CRLF
        self.serialPort.write(strcommand.encode('utf-8'))
        Helpers.qtEventSleep(100)
        #self.sleeptimer.singleShot(100, self.loop.quit)
        #self.loop.exec_()
        #time.sleep(0.1)
        astr = self.serialPort.read(self.serialPort.in_waiting)
        #self.closePort()
        return astr.decode().replace('\n', '')



    def chan_applyVoltageCurrent(self, channel, Voltage, Current):
        if (channel is not None) and (channel>0) and (channel<5):
            self.selChannel(channel)
            command = 'APPL {:}, {:}'.format(Voltage, Current)
            ret = self.write(command)

    def selChannel(self, channel: int = 0):
        command = 'INST:NSEL ' + str(channel)
        #print('selected channel {:}'.format(channel))
        ret = self.write(command)
        return ret

    def measVoltage(self):
        command = 'MEAS:VOLT ?'
        ret = self.write(command)
        #print('measured {:} V'.format(ret))
        return ret

    def measCurrent(self):
        command = 'MEAS:CURR ?'
        ret = self.write(command)
        #print('measured: {:} A'.format(ret))
        return ret

    def getCurrSetting(self):
        command = 'CURR?'
        ret = self.write(command)
        #print('Current Limit: {:} A'.format(ret))
        return ret

    def setOnOutpCh(self, ch=None, On= False):
        if (ch is not None) and (ch>0) and (ch<5):
            self.selChannel(ch)
            if On:
                command = 'OUTP:SEL ON'
            else:
                command = 'OUTP:SEL OFF'
        ret = self.write(command)
        print('set Output ch:{:} to {:}'.format(ch, On))
        self.getOutpStat(ch)
        return ret


    def ch_SetOVP(self, ch, voltage):
        if (ch is not None) and (ch>0) and (ch<5):
            self.selChannel(ch)
            command = 'VOLT:PROT:LEV {:}'.format(voltage)
            ret = self.write(command)
            print('set OVP for  channel:{:} to {:}'.format(ch, voltage))
        return ret

    def ch_ActFuse(self, ch, Activate):
        if (ch is not None) and (ch>0) and (ch<5):
            self.selChannel(ch)
            if Activate:
                command = 'FUSE:STAT ON'
                print('Fuse for channel:{:} activated !'.format(ch))
            else:
                command = 'FUSE:STAT OFF'
                print('Fuse for channel:{:} deactivated !'.format(ch))
            ret = self.write(command)
        return ret

    def setFuseLinkAll(self):
        self.selChannel(1)
        command = 'FUSE:LINK 2'
        ret = self.write(command)
        command = 'FUSE:LINK 3'
        ret = self.write(command)
        command = 'FUSE:LINK 4'
        ret = self.write(command)
        command = 'FUSE:DEL 111'
        ret = self.write(command)

        self.selChannel(2)
        command = 'FUSE:LINK 1'
        ret = self.write(command)
        command = 'FUSE:LINK 3'
        ret = self.write(command)
        command = 'FUSE:LINK 4'
        ret = self.write(command)
        command = 'FUSE:DEL 111'
        ret = self.write(command)

        self.selChannel(3)
        command = 'FUSE:LINK 1'
        ret = self.write(command)
        command = 'FUSE:LINK 2'
        ret = self.write(command)
        command = 'FUSE:LINK 4'
        ret = self.write(command)
        command = 'FUSE:DEL 111'
        ret = self.write(command)

        self.selChannel(4)
        command = 'FUSE:LINK 1'
        ret = self.write(command)
        command = 'FUSE:LINK 2'
        ret = self.write(command)
        command = 'FUSE:LINK 3'
        ret = self.write(command)
        command = 'FUSE:DEL 111'
        ret = self.write(command)

        print('All Fuses linked !')

    def closeEvent(self, event):
        self.serialPort.close()
        super().closeEvent(event)

    def getHK(self):
        value = None
        try:
            self.getStatusMainOutput()
            hastripped = False
            TotalPWR = 0
            for i in range(numchannels):
                self.selChannel(i + 1)
                value = self.measVoltage()
                if value is not '':
                    self.chstatus[i][n_Voltage] = float(value)
                value = self.measCurrent()
                if value is not '':
                    self.chstatus[i][n_Current] = float(value)
                value = self.getCurrSetting()
                if value is not '':
                    self.chstatus[i][n_CurrLimit] = float(value)
                value = self.getOutpStat(i+1)
                value = self.checkFuseTripped()
                if value is not '':
                    self.chstatus[i][n_FuseTripped] = bool(int(value))

                self.chstatus[i][n_Power] = self.chstatus[i][n_Current] * self.chstatus[i][n_Voltage]
                hastripped = hastripped or self.chstatus[i][n_FuseTripped]
                TotalPWR = TotalPWR + self.chstatus[i][n_Power]

            self.StatusUnithasTripped = hastripped
            self.StatusTotalPwr = TotalPWR
            rslt = True
        except Exception as e:
            logging.error('PSU_HMP4040 getHK - {:} - {:}'.format(e, value))
            rslt = False
        return rslt

    def checkFuseTripped(self):
        command = 'FUSE:TRIP?'
        ret = self.write(command)

        return ret


    def checkifAnyFusehastripped(self):
        atleastOneFusehastripped = False
        if (self.StatusMainOutput is not True) or (self.StatusUnithasTripped):
            for i in range(4):
                if self.chstatus[i][n_FuseTripped] == True:
                    atleastOneFusehastripped = True
        return atleastOneFusehastripped

def basicEGSESetup(mydevice):
    mydevice.setMainOutput(False)

    mydevice.getVers()
    mydevice.setFuseLinkAll()

    mydevice.chan_applyVoltageCurrent(1, 12, 0.5)
    mydevice.ch_SetOVP(1, 15)
    mydevice.ch_ActFuse(1, True)

    mydevice.chan_applyVoltageCurrent(2, 5, 0.2)
    mydevice.ch_SetOVP(2, 6)
    mydevice.ch_ActFuse(2, True)

    mydevice.chan_applyVoltageCurrent(3, 5, 0.5)
    mydevice.ch_SetOVP(3, 6)
    mydevice.ch_ActFuse(3, True)

    mydevice.chan_applyVoltageCurrent(4, 28.1, 1)
    mydevice.ch_SetOVP(4, 30)
    mydevice.ch_ActFuse(4, True)

    mydevice.setOnOutpCh(1, True)
    mydevice.setOnOutpCh(2, True)
    mydevice.setOnOutpCh(3, True)
    mydevice.setOnOutpCh(4, True)


if __name__ == "__main__":
    mydevice = HM4040('COM5')

    mydevice.getHK()

    if (mydevice.StatusMainOutput is not True) or (mydevice.UnithasTripped):
        resetAll = False
        for i in range(4):
            if mydevice.chstatus[i][n_FuseTripped] == True:
                resetAll = True
        if resetAll:
            mydevice.setMainOutput(False)
            basicEGSESetup(mydevice)
        mydevice.setMainOutput(True)


    while (1):
        mydevice.getHK()
        for i in range(4):
            print(mydevice.chstatus[i])

    '''    
        for i in range(4):
            mydevice.selChannel(i+1)
            mydevice.measVoltage()
            mydevice.measCurrent()
            mydevice.getCurrSetting()
    '''
    mydevice.output(False)
    mydevice.getOutpStat()


    print('done')
