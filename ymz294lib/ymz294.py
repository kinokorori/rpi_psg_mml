# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# high level controller for YMZ294
class PSGPlayer:
    CHANNEL_A = 0
    CHANNEL_B = 1
    CHANNEL_C = 2
    
    def __init__(self, dpin_bcm_array, wrpin, cspin, a0pin):
        self.ymz294_ = YMZ294(dpin_bcm_array, wrpin, cspin, a0pin)
        self.env_type = None
        self.volumes = [0,0,0]

    # set the sound volume of the channel.
    # @param channel channel(CHANNEL_A or CHANNEL_B or CHANNEL_C)
    # @param volume volume(from 0 to 15)
    # @param use_envelop True or False. if True, ymz294 use inner envelop, and ignore volume
    def setVolume(self, channel, volume, use_envelop = False):
        ch = int(channel)
        if channel < 0 or channel > 2:
            print "invalid channel."
            return
        
        addr = 0x8 + ch
        if use_envelop:
            self.ymz294_.write_data(addr, 0x10 | volume)
            self.volumes[channel] = 0x10 | volume
        else:
            self.ymz294_.write_data(addr, volume)
            self.volumes[channel] = volume

    # set the mixer
    # @param enable_A_tone  true: enable chA tone output, false: disable chA tone output
    # @param enable_A_noise true: enable chA noise output, false: disable chA noise output
    # @param enable_B_tone  true: enable chB tone output, false: disable chB tone output
    # @param enable_B_noise true: enable chB noise output, false: disable chB noise output
    # @param enable_C_tone  true: enable chC tone output, false: disable chC tone output
    # @param enable_C_noise true: enable chC noise output, false: disable chC noise output
    def setMixer(self, enable_A_tone, enable_A_noise, enable_B_tone, enable_B_noise,
                enable_C_tone, enable_C_noise):
        bit = not (enable_A_tone)
        bit |= (not enable_B_tone) << 1
        bit |= (not enable_C_tone) << 2
        bit |= (not enable_A_noise) << 3
        bit |= (not enable_B_noise) << 4
        bit |= (not enable_C_noise) << 5
        self.ymz294_.write_data(0x7, bit)
        
    # play the sound.
    # @param channel channel(CHANNEL_A or CHANNEL_B or CHANNEL_C)
    # @param freq Frequency of sound
    def playSound(self, channel, freq):
        ch = int(channel)
        if channel < 0 or channel > 2:
            print "invalid channel."
            return
        
        addrL = ch * 2
        addrH = ch * 2 + 1
        tp_low, tp_high = self.__calc_tp__(freq)
        self.ymz294_.write_data(addrL, tp_low)
        self.ymz294_.write_data(addrH, tp_high)
        
    # set the noise frequency.
    # @param freq Frequency of noise (4032 ~ 125000)
    def setNoise(self, freq):
        if freq < 4032: freq = 4032
        elif freq > 125000: freq = 125000
        np = (2000000 / freq) / 16
        np = int(np) & 0x1f
        self.ymz294_.write_data(0x6, np)
        
    # set the envelop frequency.
    # @param freq envelop frequency(0.12 ~ 7814Hz)
    def setEnvelopFreq(self, freq):
        if freq <= 0: freq = 1
        ep = (2000000 / freq) / 256
        if ep > 65535: ep = 65535
        epL = int(ep) & 0xff
        epH = (int(ep) & 0xff00) >> 8
        self.ymz294_.write_data(0x0b, epL)
        self.ymz294_.write_data(0x0c, epH)
        
    # set the envelop pattern
    # @param env_type the envelop pattern
    def setEnvelopType(self, env_type):
        self.env_type = int(env_type) & 0xf
        self.ymz294_.write_data(0xd, self.env_type)
        
    # get the envelop pattern
    # @return envelop pattern
    def getEnvelopType(self):
        return self.env_type

    def setMute(self, is_mute_on, channel = CHANNEL_A):
        if is_mute_on == True:
            self.ymz294_.write_data(0x8 + channel, 0)
        else:
            self.ymz294_.write_data(0x8 + channel, self.volumes[channel])
    
    def __calc_tp__(self, freq):
        tp = (2000000 / freq) / 16
        tp_low = int(tp) & 0xff
        tp_high = (int(tp) & 0xf00) >> 8
        return (tp_low, tp_high)

        

# low level controller for YMZ294
class YMZ294:
    # initialize the instance
    # @param dpin_bcm_array set d0~d7 pin number array(tuple), ex) (17,27,22,10,9,11,5,6) 
    # @param wrpin set /WR pin number.
    # @param cspin set /CS pin number.
    # @param a0pin set A0 pin number.
    def __init__(self, dpin_bcm_array, wrpin, cspin, a0pin):
        if len(dpin_bcm_array) != 8:
            print "[CAUTION]Size of dpin_bcm_array is incorrect."
            exit()
        self.dpin_ = dpin_bcm_array
        self.wrpin_ = wrpin
        self.cspin_ = cspin
        self.a0pin_ = a0pin
        
        for d in self.dpin_:
            GPIO.setup(d, GPIO.OUT)
        GPIO.setup(self.wrpin_, GPIO.OUT)
        GPIO.setup(self.cspin_, GPIO.OUT)
        GPIO.setup(self.a0pin_, GPIO.OUT)
    
    # Write the value to the address
    # @param addr register address
    # @param val value
    def write_data(self, addr, val):
        # write addr
        GPIO.output(self.wrpin_, 0)
        GPIO.output(self.cspin_, 0)
        GPIO.output(self.a0pin_, 0)
        self.__set_dpins__(addr)
        GPIO.output(self.wrpin_, 1)
        GPIO.output(self.cspin_, 1)

        # write val
        GPIO.output(self.wrpin_, 0)
        GPIO.output(self.cspin_, 0)
        GPIO.output(self.a0pin_, 1)
        self.__set_dpins__(val)
        GPIO.output(self.wrpin_, 1)
        GPIO.output(self.cspin_, 1)

        
    def __set_dpins__(self, val):
        bit = val
        for dout in self.dpin_:
            b = bit & 0x1
            GPIO.output(dout, b)
            bit = bit >> 1
