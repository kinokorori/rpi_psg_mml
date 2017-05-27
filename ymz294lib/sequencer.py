# -*- coding:utf-8 -*-

import ymz294
import mml
import time

class Sequencer:
    # initialize.
    # @param psgplayer ymz294.PSGPlayer instance
    def __init__(self, psgplayer):
        self.psgplayer = psgplayer
    
    # play sound by MML string
    # @param chA_MML a MML string for PSG channel A
    # @param chB_MML a MML string for PSG channel B
    # @param chC_MML a MML string for PSG channel C
    # @param core_freq frequency of the octave 4's A
    def playMML(self, chA_MML, chB_MML="", chC_MML="", core_freq=440):
        parser = mml.Parser(core_freq)
        chA_seq = parser.parse(chA_MML)
        chB_seq = parser.parse(chB_MML)
        chC_seq = parser.parse(chC_MML)

        wait_a = 0
        index_a = 0
        wait_b = 0
        index_b = 0
        wait_c = 0
        index_c = 0
        eom = 0 #End of mml
        while(index_a < len(chA_seq) or index_b < len(chB_seq) or index_c < len(chC_seq)):
            if wait_a <= 0:
                if index_a < len(chA_seq):
                    seq = chA_seq[index_a]
                    wait_a = seq["duration"]
                    self.__play_tone__(ymz294.PSGPlayer.CHANNEL_A, seq)
                    index_a += 1
                else:
                    self.psgplayer.setMute(True, ymz294.PSGPlayer.CHANNEL_A)
                    eom |= 1
                    
            if wait_b <= 0:
                if index_b < len(chB_seq):
                    seq = chB_seq[index_b]
                    wait_b = seq["duration"]
                    self.__play_tone__(ymz294.PSGPlayer.CHANNEL_B, seq)
                    
                    index_b += 1
                else:
                    self.psgplayer.setMute(True, ymz294.PSGPlayer.CHANNEL_B)
                    eom |= 2
                    
            if wait_c <= 0:
                if index_c < len(chC_seq):
                    seq = chC_seq[index_c]
                    wait_c = seq["duration"]
                    self.__play_tone__(ymz294.PSGPlayer.CHANNEL_C, seq)
                    index_c += 1
                else:
                    self.psgplayer.setMute(True, ymz294.PSGPlayer.CHANNEL_C)
                    eom |= 4
                                
            wait = min(wait_a + ((eom & 1) == 1) * 10, wait_b + ((eom & 2) == 2) * 10, wait_c + ((eom & 4) == 4) * 10)
            time.sleep(wait)
            if wait_a > 0: wait_a -= wait
            if wait_b > 0: wait_b -= wait
            if wait_c > 0: wait_c -= wait

        time.sleep(max(wait_a, wait_b, wait_c))

    def __play_tone__(self, channel, seq):
        if seq["freq"] != 0:
            self.psgplayer.setMute(False, channel)
            self.psgplayer.playSound(channel, seq["freq"])
            #print seq["freq"]
        else:
            #mute
            self.psgplayer.setMute(True, channel)
            #self.psgplayer.playSound(channel, 20000)
            return
        if seq["tie_slur"] == False:
            env = self.psgplayer.getEnvelopType()
            if env is not None and channel == ymz294.PSGPlayer.CHANNEL_A:
                self.psgplayer.setEnvelopType(env)
