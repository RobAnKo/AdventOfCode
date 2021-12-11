#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 18:01:59 2021

@author: robinkoch
"""


from itertools import cycle
import numpy as np
class Decoder():
    def __init__(self,input_line):
        
        print()
        #list of segments
        self.true_segments = 'abcdefg'
        
        #define mapping from digits to true signals and vice versa
        digits = range(10)
        signals = ['abcefg',
                 'cf',
                 'acdeg',
                 'acdfg',
                 'bcdf',
                 'abdfg',
                 'abdefg',
                 'acf',
                 'abcdefg',
                 'abcdfg',
                 'abcefg',
                 ]
        self.segment_digit_map = dict(zip(signals,digits))
        self.digit_segment_map = dict(zip(digits, signals))
        
        
        #store input and output
        self.input = input_line.split("|")[0].strip().split(" ")
        self.output = input_line.split("|")[1].strip().split(" ")
        
        #print(self.input)
        #create a mapping defining which true segments correspond to which 
        #falsely wired segments
        #self.true_segments = 'abcdefg'
        #possible_segments = ['abcdefg']
        #self.possible_segment_mappings = dict(zip(self.true_segments, cycle(possible_segments)))
        
        #initiate the correction map from true signals to wrong signals
        self.correction_map = dict()
        
        
    #This function translates a given signal into a signal based on the correction mapping
    def correct_signal(self, input_signal):
        return "".join(sorted([self.correction_map[i] for i in input_signal]))
        

    def translate_signal_to_number(self, signal):
        return str(self.segment_digit_map[signal])
    
    
    def figure_out_segment_mapping(self):
        #count occurences of each segment in all the signals
        segment_count = {s:sum([s in signal for signal in self.input]) for s in self.true_segments}
        
        #find lengths of signals
        signal_lengths = [len(signal) for signal in self.input]
        
        #initiate dict mapping from numbers to signals
        known_signals = dict()
        
        #initiate dict mapping from numbers to positions
        #known_positions = dict()
        
        #find position and signal of 1,4,7 and 8
        pos1 = signal_lengths.index(2)
        #known_positions[1] = pos1
        known_signals[1] = self.input[pos1]
        
        pos4 = signal_lengths.index(4)
        #known_positions[4] = pos4
        known_signals[4] = self.input[pos4]
        
        # pos7 = signal_lengths.index(3)
        # known_positions[7] = pos7
        # known_signals[7] = self.input[pos7]
        
        # pos8 = signal_lengths.index(7)
        # known_positions[8] = pos8
        # known_signals[8] = self.input[pos8]
        
        
        # #find position of 2
        # for s,c in segment_count.items():
        #     if c == 9:
        #         segment_with_9_occurences = s
        #         break
        # pos2 = int(np.where([segment_with_9_occurences not in signal for signal in self.input])[0])
        # known_positions[2] = pos2
        # known_signals[2] = self.input[pos2]
        
        # #find position of 3
        # pos3 = int(np.where([np.all([seg in signal for seg in known_signals[1]]) and 
        #                      length == 5 
        #                      for signal,length in zip(self.input, signal_lengths)])[0])
        # known_positions[3] = pos3
        # known_signals[3] = self.input[pos3]
        
        # #find position of 5
        # pos_of_len5 = [i for i,l in enumerate(signal_lengths) if l==5]
        # pos5 = [pos for pos in pos_of_len5 if pos not in [pos2,pos3]][0]
        # known_positions[5] = pos5
        # known_signals[5] = self.input[pos5]
        
        # #find position of 6
        # pos6 = int(np.where([not np.all([seg in signal for seg in known_signals[1]]) and
        #                      length == 6 
        #                      for signal,length in zip(self.input, signal_lengths)])[0])
        # known_positions[6] = pos6
        # known_signals[6] = self.input[pos6]
        
        # #find position of 9
        # for s,c in segment_count.items():
        #     if c == 4:
        #         segment_with_4_occurences = s
        #         break
        # pos9 = int(np.where([segment_with_4_occurences not in signal and
        #                      length == 6
        #                      for signal, length in zip(self.input, signal_lengths)])[0])
        # known_positions[9] = pos9
        # known_signals[9] = self.input[pos9]
        
        # #find position of 0
        # pos0 = [p for p in range(10) if p not in known_positions.values()][0]
        # known_positions[0] = pos0
        # known_signals[0] = self.input[pos0]
        
        
        for count, correct_segment in zip([4,6,9], 'ebf'):
            wrong_segment = [seg for seg,c in segment_count.items() if c == count][0]
            self.correction_map[wrong_segment] = correct_segment
            
        
        #find the segment corresponding to "a"
        seg = [seg for seg,c in segment_count.items() if c == 8 and 
               seg not in known_signals[1]][0]
        self.correction_map[seg] = 'a'

        #find the segment corresponding to "c"
        seg = [seg for seg,c in segment_count.items() if c == 8 and 
               seg in known_signals[1]][0]
        self.correction_map[seg] = 'c'
        
        
        #find the segment corresponding to "d"
        seg = [seg for seg,c in segment_count.items() if c == 7 and 
               seg in known_signals[4]][0]
        self.correction_map[seg] = 'd'
        
        
        #find the segment corresponding to "g"
        seg = [seg for seg,c in segment_count.items() if c == 7 and 
               seg not in known_signals[4]][0]
        self.correction_map[seg] = 'g'
        
        
        
    def calculate_output(self):
        self.figure_out_segment_mapping()
        self.correct_output = [self.correct_signal(signal) for signal in self.output]
        self.number = int("".join([self.translate_signal_to_number(signal) for signal in self.correct_output]))
        return(self.number)
        
        
        