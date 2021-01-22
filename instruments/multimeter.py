#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vxi11
import time
import logging
import threading
import serial
import statistics
import multiprocessing 




class multimeter:

    read_val = 0
    title = ""

    measuring = False
    readable = False
    
    def is_readable(self):
        return self.readable
    
    
    def connect(self):
        self.lock.acquire()
        self.instr.open()
        
        
    def get_title(self):
        return self.title
        
        
    def get_read_val(self):
        self.connect()
        try:
            self.read_val = self.instr.read()
            self.instr.close()
            self.measuring = False
        except:
            logging.error("Error in %s get_read_val" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
        logging.debug("%s reading %s" % (self.title, self.read_val))
        return self.read_val
        
        
    def read_stb(self):
        self.connect()
        try:
            self.stb = self.instr.read_stb()
            self.instr.close()
        except:
            logging.error("Error in %s read_stb" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
            
            
    def is_measuring(self):
        return self.measuring



class S7081(multimeter):

    def __init__(self, ip, gpib_address, lock, title='Solartron 7081'):
        self.title = title
        self.lock = lock
        logging.debug(self.title+' init started')
        self.ip = ip
        self.gpib_address = gpib_address
        self.lock.acquire()
        try:
            self.instr =  vxi11.Instrument(self.ip, "gpib0,"+str(self.gpib_address))
            self.instr.clear()
            self.instr.write("INItialise")
            time.sleep(5)
            self.instr.write("BEEp")
            self.instr.write("DELIMITER=END")
            self.instr.write("OUTPUT,GP-IB=ON")
            self.instr.write("FORMAT=ENGINEERING")
            self.instr.close()
        except:
            logging.error("Error in %s __init__" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
            
    def config_10DCV_9digit(self):
        self.connect()
        try:
            self.instr.write("DRIFT,OFF")
            self.instr.write("MODe=VDC: RANge=10: NInes=8")
            self.instr.close()
        except:
            logging.error("Error in %s __init__" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
            
    def config_10k_9digit(self):
        self.connect()
        try:
            #self.instr.write("DRIFT,ON")
            self.instr.write("DRIFT,OFF")
            self.instr.write("MODe=KOHM: RANge=10: NInes=8")
            self.instr.close()
        except:
            logging.error("Error in %s __init__" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
        

    def measure(self):
        logging.debug(self.title+' measure started')
        self.measuring = True
        self.connect()
        try:
            self.instr.write("MEAsure, SIGLE")
            self.instr.close()
        except:
            logging.error("Error in %s measure" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
            
            
        
        
    def is_ready_to_read(self):
        self.read_stb()
        ready = self.stb == 24
        return ready
        
        
        
        
        


class K2001(multimeter):

    def __init__(self, ip, gpib_address, lock, title='Keithley 200X'):
        self.read_val = 0
        self.title = title
        self.lock = lock
        logging.debug(self.title+' init started')
        self.ip = ip
        self.gpib_address = gpib_address
        self.lock.acquire()
        try:
            self.instr =  vxi11.Instrument(self.ip, "gpib0,"+str(self.gpib_address))
            self.instr.clear()
            logging.debug("*IDN? -> "+self.instr.ask("*IDN?"))
            self.instr.close()
        except:
            logging.error("Error in %s __init__" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
        
        
    def config_20DCV_9digit_fast(self):
        self.connect()
        try:
            self.instr.write("*RST")
            self.instr.write(":SYST:AZER:TYPE SYNC")
            self.instr.write(":SYST:LSYN:STAT ON")
            self.instr.write(":SENS:FUNC 'VOLT:DC'")
            self.instr.write(":SENS:VOLT:DC:DIG 9; NPLC 10")
            self.instr.write(":SENS:VOLT:DC:AVER:STAT ON")
            self.instr.write(":SENS:VOLT:DC:RANG 20")
            self.instr.write(":FORM:ELEM READ")
            self.instr.close()
        except:
            logging.error("Error in %s config_20DCV_9digit_fast" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
        
        
    def config_20DCV_9digit_filtered(self):
        self.connect()
        try:
            self.instr.write("*RST")
            self.instr.write(":SYST:AZER:TYPE SYNC")
            self.instr.write(":SYST:LSYN:STAT ON")
            self.instr.write(":SENS:FUNC 'VOLT:DC'")
            self.instr.write(":SENS:VOLT:DC:DIG 9; NPLC 10")
            self.instr.write(":SENS:VOLT:DC:AVER:STAT ON")
            self.instr.write(":SENS:VOLT:DC:AVER:COUN 50")
            self.instr.write(":SENS:VOLT:DC:AVER:TCON REP")
            self.instr.write(":SENS:VOLT:DC:AVER:STAT ON")
            self.instr.write(":SENS:VOLT:DC:RANG 20")
            #self.instr.write(":SENS:VOLT:DC:FILT:LPAS:STAT ON")
            self.instr.write(":FORM:ELEM READ")
            self.instr.close()
        except:
            logging.error("Error in %s config_20DCV_9digit_filtered" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
            
    def config_2ADC_9digit_filtered(self):
        self.connect()
        try:
            self.instr.write("*RST")
            self.instr.write(":SYST:AZER:TYPE SYNC")
            self.instr.write(":SYST:LSYN:STAT ON")
            self.instr.write(":SENS:FUNC 'CURRent:DC'")
            self.instr.write(":SENSe:CURRent:DC:RANGe 2")
            self.instr.write(":SENS:CURRent:DC:DIG 9; NPLC 10")
            self.instr.write(":SENS:CURRent:DC:AVER:STAT ON")
            self.instr.write(":SENS:CURRent:DC:AVER:COUN 50")
            self.instr.write(":SENS:CURRent:DC:AVER:TCON REP")
            self.instr.write(":SENS:CURRent:DC:AVER:STAT ON")
            #self.instr.write(":SENS:CURRent:DC:FILT:LPAS:STAT ON")
            self.instr.write(":FORM:ELEM READ")
            self.instr.close()
        except:
            logging.error("Error in %s config_2ADC_9digit_filtered" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()


    def measure(self):
        logging.debug(self.title+' measure started')
        self.measuring = True
        self.connect()
        try:
            self.read_val = self.instr.write("READ?")
            self.instr.close()
        except:
            logging.error("Error in %s measure" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
            
        
        
    def is_ready_to_read(self):
        self.read_stb()
        ready = self.stb & 0b00010000
        return ready
        
        
        
class K2002(K2001):
    pass
    
    

class R6581T(multimeter):

    def __init__(self, ip, gpib_address, lock, title='Advantest R6581T'):
        self.read_val = 0
        self.title = title
        self.lock = lock
        logging.debug(self.title+' init started')
        self.ip = ip
        self.int_temp = 0
        self.gpib_address = gpib_address
        self.lock.acquire()
        try:
            self.instr =  vxi11.Instrument(self.ip, "gpib0,"+str(self.gpib_address))
            self.instr.clear()
            logging.debug("*IDN? -> "+self.instr.ask("*IDN?"))
            self.int_temp = 0
            self.instr.close()
        except:
            logging.error("Error in %s __init__" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
        
        
    def config_10DCV_9digit_fast(self):
        self.connect()
        try:
            logging.debug(self.title+' config_10DCV_9digit_fast started')
            self.instr.write("*RST")
            #self.instr.ask("*OPC?")
            self.instr.write("CONFigure:VOLTage:DC")
            self.instr.write(":SENSe:VOLTage:DC:RANGe:1.00E+01")
            #self.instr.write(":SENSe:VOLTage:DC:RANGe:AUTO ON")
            self.instr.write(":SENSe:VOLTage:DC:DIGits MAXimum")
            self.instr.write(":SENSe:VOLTage:DC:NPLCycles 10")
            self.instr.write(":SENSe:VOLTage:DC:RANGe 10")
            
            #self.instr.write(":SENSe:VOLTage:DC:PROTection OFF")
            #self.instr.write(":SENSe:ZERO:AUTO OFF")
            self.instr.close()
        except:
            logging.error("Error in %s config_10DCV_9digit_fast" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
        
        
    def config_10DCV_9digit_filtered(self):
        self.connect()
        try:
            logging.debug(self.title+' config_10DCV_9digit_filtered started')
            self.instr.write("*RST")
            #self.instr.ask("*OPC?")
            self.instr.write("CONFigure:VOLTage:DC")
            self.instr.write(":SENSe:VOLTage:DC:RANGe 10")
            self.instr.write(":SENSe:VOLTage:DC:DIGits MAXimum")
            self.instr.write(":SENSe:VOLTage:DC:NPLCycles 10")
            
            #self.instr.write(":SENSe:VOLTage:DC:PROTection OFF")
            #self.instr.write(":SENSe:ZERO:AUTO OFF")
            
            self.instr.write(":CALCulate:DFILter:STATe ON")
            self.instr.write(":CALCulate:DFILter AVERage")
            self.instr.write(":CALCulate:DFILter:AVERage 10")
            self.instr.close()
        except:
            logging.error("Error in %s config_10DCV_9digit_filtered" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
            
            
    def config_100k4W_9digit_filtered(self):
        self.connect()
        try:
            logging.debug(self.title+' config_100k4W_9digit_filtered started')
            self.instr.write("*RST")
            #self.instr.ask("*OPC?")
            self.instr.write("CONFigure:FRESistance")
            self.instr.write(":SENSe:FRESistance:RANGe 1.00E+05")
            self.instr.write(":SENSe:FRESistance:DIGits MAXimum")
            self.instr.write(":SENSe:FRESistance:NPLCycles 10")
            self.instr.write(":SENSe:FRESistance:SOURce OCOMpensated")
            self.instr.write(":SENSe:FRESistance:POWer HI")
            
            #self.instr.write(":SENSe:VOLTage:DC:PROTection OFF")
            #self.instr.write(":SENSe:ZERO:AUTO OFF")
            
            self.instr.write(":CALCulate:DFILter:STATe ON")
            self.instr.write(":CALCulate:DFILter AVERage")
            self.instr.write(":CALCulate:DFILter:AVERage 10")
            self.instr.close()
        except:
            logging.error("Error in %s config_10DCV_9digit_filtered" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
            
            
    def config_10k4W_9digit_filtered(self):
        self.connect()
        try:
            logging.debug(self.title+' config_10k4W_9digit_filtered started')
            self.instr.write("*RST")
            #self.instr.ask("*OPC?")
            self.instr.write("CONFigure:FRESistance")
            self.instr.write(":SENSe:FRESistance:RANGe 1.00E+04")
            self.instr.write(":SENSe:FRESistance:DIGits MAXimum")
            self.instr.write(":SENSe:FRESistance:NPLCycles 10")
            #self.instr.write(":SENSe:FRESistance:SOURce OCOMpensated")
            self.instr.write(":SENSe:FRESistance:POWer HI")
            
            #self.instr.write(":SENSe:VOLTage:DC:PROTection OFF")
            #self.instr.write(":SENSe:ZERO:AUTO OFF")
            
            self.instr.write(":CALCulate:DFILter:STATe ON")
            self.instr.write(":CALCulate:DFILter AVERage")
            self.instr.write(":CALCulate:DFILter:AVERage 10")
            self.instr.close()
        except:
            logging.error("Error in %s config_10DCV_9digit_filtered" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
        
        
    def config_10R4W_9digit_filtered(self):
        self.connect()
        try:
            logging.debug(self.title+' config_10R4W_9digit_filtered started')
            self.instr.write("*RST")
            #self.instr.ask("*OPC?")
            self.instr.write("CONFigure:FRESistance")
            self.instr.write(":SENSe:FRESistance:RANGe 1.00E+01")
            self.instr.write(":SENSe:FRESistance:DIGits MAXimum")
            self.instr.write(":SENSe:FRESistance:NPLCycles 10")
            self.instr.write(":SENSe:FRESistance:SOURce OCOMpensated")
            self.instr.write(":SENSe:FRESistance:POWer HI")
            
            #self.instr.write(":SENSe:VOLTage:DC:PROTection OFF")
            #self.instr.write(":SENSe:ZERO:AUTO OFF")
            
            self.instr.write(":CALCulate:DFILter:STATe ON")
            self.instr.write(":CALCulate:DFILter AVERage")
            self.instr.write(":CALCulate:DFILter:AVERage 10")
            self.instr.close()
        except:
            logging.error("Error in %s config_10DCV_9digit_filtered" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
            
        
    def measure(self):
        logging.debug(self.title+' measure started')
        self.measuring = True
        self.connect()
        try:
            self.int_temp = self.instr.ask(":SENSe:ITEMperature?")
            self.instr.write("READ?")
            self.instr.close()
        except:
            logging.error("Error in %s measure" % self.title, exc_info=True)
            pass
        finally:
            self.lock.release()
        
        
    def get_int_temp(self):
        return self.int_temp
        
        
    def is_ready_to_read(self):
        self.read_stb()
        ready = self.stb == 16
        return ready




class HPM7177(multimeter):

    def __init__(self, dev='/dev/ttyUSB0', baud=921600, nfilter=10000, title='HPM7177'):
        self.title = title
        logging.debug(self.title+' init started')
        self.dev = dev
        self.baud = baud
        self.nfilter = nfilter
        self.buffer = bytearray()
        self.readings = []
        self.serial = serial.Serial(self.dev, self.baud)
        self.thread_1 = threading.Thread(target=self.readserial, args=(self.dev, self.baud, self.buffer))
        self.thread_1.daemon = True
        self.thread_1.start()
        

        


    def readserial(self, dev, baud, buf):
        s = serial.Serial(dev, baud)
        while True:
                reading=s.read(10000*6)
                buf.extend(reading)
        
        
    def process(self):
        while (len(self.readings)<self.nfilter):
            if (len(self.buffer)>5):
                if(self.buffer[4]==160 and self.buffer[5]==13):
                    number = int.from_bytes(self.buffer[:4], byteorder='big', signed=False)
                    del self.buffer[:6]
                    self.readings.append(number)
                else:
                    logging.debug(self.title+' ditching a byte')
                    del self.buffer[0]

        mean=(statistics.mean(self.readings)-2147448089.450398)/147862000
        self.readings.clear()
        self.buffer.clear()
        logging.debug(self.title+' result= '+str(mean))
        self.read_val=mean
        self.readable=True
        self.measuring=False
        
        
    def measure(self):
        self.measuring=True
        self.thread_2 = threading.Thread(target=self.process)
        self.thread_2.daemon = True
        self.thread_2.start()
        
        
    def is_ready_to_read(self):
        logging.debug(self.title+' is_ready_to_read started')
        return self.readable


    def get_read_val(self):
        logging.debug(self.title+' get_read_val started')
        self.readable=False
        return self.read_val