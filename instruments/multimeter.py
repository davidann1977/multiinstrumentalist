#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vxi11
import time
import logging

class S7081:

    def __init__(self, ip, gpib_address, title='Solartron 7081'):
        self.title = title
        logging.debug(self.title+' init started')
        self.ip = ip
        self.gpib_address = gpib_address
        self.instr =  vxi11.Instrument(self.ip, "gpib0,"+str(self.gpib_address))
        self.instr.timeout = 60*1000
        self.instr.clear()
        self.instr.write("INItialise")
        time.sleep(3)
        #self.instr.write("BEEp")
        self.instr.write("DELIMITER=END")
        self.instr.write("OUTPUT,GP-IB=ON")
        self.instr.write("FORMAT=ENGINEERING")
        #self.instr.write("DRIFT,OFF")
        self.instr.write("MODe=VDC: RANge=Auto: NInes=8")

    def read(self):
        logging.debug(self.title+' reading started')
        self.instr.write("MEAsure, SIGLE")
        self.read_val = self.instr.read()
        
    def get_title(self):
        logging.debug(self.title+' get_title')
        return self.title
        
    def get_read_val(self):
        logging.debug(self.title+' returns '+self.read_val)
        return self.read_val


class K2001:

    def __init__(self, ip, gpib_address, title='Keithley 2001'):
        self.title = title
        logging.debug('K2001 init started')
        self.ip = ip
        self.gpib_address = gpib_address
        self.instr =  vxi11.Instrument(self.ip, "gpib0,"+str(self.gpib_address))
        self.instr.timeout = 60*1000
        self.instr.clear()
        
    def config_DCV_9digit(self):
        logging.debug('K2001 config_DCV_9digit started')
        self.instr.write("*RST")
        self.instr.write(":SYST:AZER:TYPE SYNC")
        self.instr.write(":SYST:LSYN:STAT ON")
        self.instr.write(":SENS:FUNC 'VOLT:DC'")
        self.instr.write(":SENS:VOLT:DC:DIG 9; NPLC 10; TCON REP")
        self.instr.write(":SENS:VOLT:DC:AVER:STAT ON")
        self.instr.write(":SENS:VOLT:DC:RANG 20")
        self.instr.write(":FORM:ELEM READ")
        
    def config_DCV_9digit_1000(self): #Max filtering
        logging.debug('K2001 config_DCV_9digit_1000 started')
        self.instr.write("*RST")
        self.instr.write(":SYST:AZER:TYPE SYNC")
        self.instr.write(":SYST:LSYN:STAT ON")
        self.instr.write(":SENS:FUNC 'VOLT:DC'")
        self.instr.write(":SENS:VOLT:DC:DIG 9; NPLC 10")
        self.instr.write(":SENS:VOLT:DC:AVER:STAT ON")
        self.instr.write(":SENS:VOLT:DC:AVER:COUN 100")
        self.instr.write(":SENS:VOLT:DC:AVER:TCON REP")
        self.instr.write(":SENS:VOLT:DC:AVER:STAT ON")
        self.instr.write(":SENS:VOLT:DC:FILT:LPAS:STAT ON")
        self.instr.write(":FORM:ELEM READ")

    def read(self):
        logging.debug('K2001 read started')
        self.read_val = self.instr.ask("READ?")
        
    def get_title(self):
        return self.title
        
    def get_read_val(self):
        return self.read_val


class R6581T:

    def __init__(self, ip, gpib_address, title='Advantest R6581T'):
        self.title = title
        logging.debug(self.title+' init started')
        self.ip = ip
        self.gpib_address = gpib_address
        self.instr =  vxi11.Instrument(self.ip, "gpib0,"+str(self.gpib_address))
        self.instr.timeout = 60*1000
        self.instr.clear()
        logging.debug("*IDN? -> "+self.instr.ask("*IDN?"))
        
    def config_DCV_9digit(self):
        logging.debug(self.title+' config_DCV_9digit started')
        self.instr.write("*RST")
        self.instr.ask("*OPC?")
        self.instr.write("CONFigure:VOLTage:DC")
        self.instr.write(":SENSe:VOLTage:DC:RANGe:AUTO ON")
        self.instr.write(":SENSe:VOLTage:DC:DIGits MAXimum")
        self.instr.write(":SENSe:VOLTage:DC:NPLCycles MAXimum")
        #self.instr.write(":SENSe:VOLTage:DC:APERture MAXimum")
        #self.instr.write(":SENSe:VOLTage:DC:PROTection OFF")
        #self.instr.write(":SENSe:ZERO:AUTO OFF")
        
        self.instr.write(":CALCulate:DFILter:STATe ON")
        self.instr.write(":CALCulate:DFILter AVERage")
        self.instr.write(":CALCulate:DFILter:AVERage 15")
        #self.instr.write(":DISPlay OFF")
        #self.instr.write(":DISPlay ON")
        
    def read(self):
        logging.debug(self.title+' reading started')
        self.read_val = self.instr.ask("READ?")
        self.int_temp = self.instr.ask(":SENSe:ITEMperature?")
        
    def get_title(self):
        logging.debug(self.title+' get_title')
        return self.title
        
    def get_read_val(self):
        logging.debug(self.title+' returns '+self.read_val)
        return self.read_val
        
    def get_int_temp(self):
        logging.debug(self.title+' returns '+self.int_temp)
        return self.int_temp
        
        
        
class R6581T_temp:

    def __init__(self, r6581t, title='R6581T Int Temp Sensor'):
        self.title = title
        logging.debug(self.title+' init started')
        self.r6581t = r6581t
    
    def read(self):
        logging.debug(self.title+' reading started')
        self.read_val = self.r6581t.get_int_temp()
        
        
    def get_read_val(self):
        logging.debug(self.title+' returns '+str(self.read_val()))
        return self.read_val
        
    def get_title(self):
        logging.debug(self.title+' get_title')
        return self.title
