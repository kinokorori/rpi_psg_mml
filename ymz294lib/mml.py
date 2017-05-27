# -*- coding:utf-8 -*-

import re


class Parser:

    # initialize.
    # @param core_freq frequency of A4. for example ASA's standard is 440Hz, Contemporary Baroque is 415Hz.
    # @param default_tempo default value of tempo. you can change this value in MML.
    # @param default_octave default value of octave. you can change this value in MML.
    # @param default_length default value of note length. you can change this value in MML.
    def __init__(self, core_freq = 440, default_tempo = 120, default_octave = 4, default_length = 4):
        self.coreFrequency = core_freq
        self.defaultTempo = default_tempo
        self.defaultOctave = default_octave
        self.defaultLength = default_length
        self.patternNumber = re.compile("[0-9]+")
    
    
    # parse the MML.
    # @param mml MML string.
    # @return dictionaries in a tuple ({"freq":freq, "duration":duration, "tie_slur":TF}, ...)
    #   freq ... Frequency. if 0 then Rest
    #   duration ... Tone duration (ms)
    #   tie_slur ... if True then tie or slur
    def parse(self, mml):
        currentOctave = self.defaultOctave
        currentLength = self.defaultLength
        currentTempo = self.defaultTempo
        
        result = []
        mml_index = 0
        tie_slur = False
        while (mml_index < len(mml)):
            if mml[mml_index] == 'R':
                mml_index += 1
                freq = 0
                duration, mml_index = self.__parse_note_duration__(mml, mml_index,currentLength, currentTempo)
                result.append({"freq":freq, "duration":duration, "tie_slur":False})
            elif mml[mml_index] == '>':
                if currentOctave < 8:
                    currentOctave += 1
                mml_index += 1
            elif mml[mml_index] == '<':
                if currentOctave > 1:
                    currentOctave -= 1
                mml_index += 1
            elif mml[mml_index] == 'O':
                mml_index += 1
                val, mml_index = self.__find_number__(mml, mml_index, mml_index + 1)
                if val is None:
                    print "[WARNING]parse error 'O', at %d" % mml_index
                else:
                    if val < 1 or val > 8:
                        print "[IGNORE]invalid octave(%d)" % val
                    else:
                        currentOctave = val
                        #print "Octave%d" % val
            elif mml[mml_index] == 'L':
                mml_index += 1
                val, mml_index = self.__find_number__(mml, mml_index, mml_index + 3)
                if val is None:
                    print "[WARNING]parse error 'L' at %d" % mml_index
                else:
                    if val < 1 or val > 128:
                        print "[IGNORE]invalid default length(%d)" % val
                    else:
                        currentLength = val
            elif mml[mml_index] == '&':
                mml_index += 1
                tie_slur = True
                continue
                
            elif mml[mml_index] == 'T':
                mml_index += 1
                val, mml_index = self.__find_number__(mml, mml_index, mml_index + 3)
                if val is None:
                    print "[WARNING]parse error 'T' at %d" % mml_index
                else:
                    if val < 1:
                        print "[IGNORE]invalid tempo(%d)" % val
                    else:
                        currentTempo = val
            else:
                freq, duration, mml_index = self.__parse_tone__(mml, mml_index, currentOctave, currentLength, currentTempo)
                #print "freq=%f, duration=%fms" % (freq, duration)
                result.append({"freq":freq, "duration": duration, "tie_slur": tie_slur})
                
            tie_slur = False
        return result

    ## private defines
    
    __SCALE__ = (("C", 0), ("D", 2), ("E", 4), ("F", 5), ("G", 7), ("A", 9), ("B", 11))
    
    def __parse_tone__(self, mml, mml_index, octave, length, tempo):
        scale_index = 255
        # parse melody (CDEFGAB)
        for scl in self.__SCALE__:
            if scl[0] == mml[mml_index]:
#                print scl[0]
                scale_index = scl[1]
                break
        if scale_index == 255:
            return (0, 0, mml_index + 1)
        mml_index += 1
        
        # parse flat and sharp
        if mml_index < len(mml):
            if mml[mml_index] == '#' or mml[mml_index] == '+':
                scale_index += 1
                mml_index += 1
            elif mml[mml_index] == '-':
                scale_index -= 1
                mml_index += 1
            if scale_index >= 88 or scale_index < 0:
                print "[WARNING]out of melody range"
                return (0, 0, mml_index + 1)
        
        # calc frequency
        ex = ((12 * octave + scale_index) - 57) / 12.0
        freq = (2 ** ex) * self.coreFrequency
        duration, mml_index = self.__parse_note_duration__(mml, mml_index, length, tempo)
        
        return (freq, duration, mml_index)
        
    def __parse_note_duration__(self, mml, mml_index, default_length, tempo):
        calc_dur = lambda sl: (60.0 / tempo) * (4.0 / sl)
        
        # duration
        scale_len, mml_index = self.__find_number__(mml, mml_index, mml_index + 3)
        if scale_len == None or scale_len < 0:
            scale_len = default_length
            
        dur = calc_dur(scale_len)
        
        # dot
        if mml_index < len(mml):
            if mml[mml_index] == '.':
#                dur += calc_dur(scale_len * 2)
                dur *= 1.5
                mml_index += 1
            
        return (dur, mml_index)
        
        
    def __find_number__(self, mml, start_index, end_index):
        obj = self.patternNumber.search(mml, start_index, end_index)
        if obj is None or obj.start() != start_index:
#            print "Missing pattern."
            return (None, start_index)
        return (int(obj.group(0)), obj.end())
                
