# -*- coding: utf-8 -*-
"""
    Leading and ending silence trimmer for wav files 
    Copyright (C) <2018>  <Boris Stupovski>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import glob
from shutil import copyfile
from pydub import AudioSegment

class wordbeginings ( object ):
    """
    This class contains list of sets of exeptional word beginings, each set has 
    two adjoint real numbers that are the lenght of the intervals to be cut from
    the front and from the back. Default intervals  
    don't have a set, just the real numbers. The number of exeptional sets is 
    also recorded.
    """
    def __init__( self, defint1, defint2 ):
       """
       Assumes defint1 and defint2 are floats. 
       Creates wordbeginings istance with with defint1 as
       the default front interval and defint2 as the default back interval, 
       and empty list of exeptional sets. 
       """
       self.dint1 = defint1
       self.dint2 = defint2
       self.data = []
       self.numex = 0
        
    def addset( self, wset, int1, int2 ):
        """
        Assumes wset is a set of str and int1 and int2 are floats. Adds wset as the 
        set of exeptional word beginings and the asociated front and back intervals.
        """
        self.data.append( ( wset, int1, int2 ) )
        self.numex += 1
        
    def getset( self, i  ):
        return self.data[ i ]
    
    def getdint1( self ):
        return self.dint1
    
    def getdint2( self ):
        return self.dint2
    
    def getnumex( self ):
        return self.numex
    
def detect_leading_silence(sound, rel_silence_threshold = 20.0, chunk_size = 10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < sound.dBFS - rel_silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


def trimfront( filepath, inter, siltresh = 20):
    """
    Assumes filepath is string. and inter is float, and siltresh is float between 0 and 50.
    Returns AudioSegment trimed from the front.
    """
    sound = AudioSegment.from_file( filepath, format = 'wav' )
    start_trim = max( detect_leading_silence( sound, siltresh ) - inter, 0 )
    
    return sound[ start_trim : len( sound ) ]

def trimback( filepath, inter, siltresh = 20):
    """
    Assumes filepath is string. and inter is float, and siltresh is float between 0 and 50.
    Returns AudioSegment trimed from the back.
    """
    sound = AudioSegment.from_file( filepath, format = 'wav' )
    end_trim = max( detect_leading_silence( sound.reverse(), siltresh ) - inter, 0 )
    
    return sound[ 0 : ( len( sound ) - end_trim ) ]

def setsinput():
    """
    Asks user to first input the default fornt and back intervals, then succesively sets of 
    exeptional word beginings and intervals for them. If just enter is pressed, 
    when aked to fill exeptional word beginings the input process is terminated.
    Users input is stored in an istance of a wordbeginings class that is retuned.
    """
    while True:
        try:
            int1 = float(input( 'Enter the default FRONT interval value (miliseconds): ' ))  
            break
        except ValueError:
            print('That was not a real number. Please try again...')
    while True:
        try:
            int2 = float(input( 'Enter the default BACK interval value (miliseconds): ' ))  
            break
        except ValueError:
            print('That was not a real number. Please try again...')
    wbeg = wordbeginings( int1, int2 )
            
    while True:
        inpt = input( 'Enter the exeptional word beginings group (strings of letters separated by blank spaces); ' 
                     + '(if you don\'t want to add any more groups, just press enter): ' ) 
        if inpt == '':
            break
        while True:
            try:
                int1 = float(input( 'Enter the FRONT interval value for words begining in just entered set: ' ))
                break
            except ValueError:
                print('That was not a real number. Please try again...')
        while True:
            try:
                int2 = float(input( 'Enter the BACK interval value for the words begining in just entered set: ' ))
                break
            except ValueError:
                print('That was not a real number. Please try again...')
        wbeg.addset( set( str.split( str( inpt ) ) ), int1, int2 )
        
    return wbeg

def ctrlinput():
    """
    Asks user to input (y/n) two times. Returns one of the following tuples:
    ('n','n'), ('n','y'), ('y','n'), ('y','y'). This tuple will be used when 
    deciding how to cut the .wav files. 
    """
    while True:
        a = str( input( 'Do you want to front-cut? (y/n): ' ) )
        if a != 'n' and a != 'y':
            print('Please enter \'y\' or \'n\'...')
        if a == 'n' or a == 'y':
            break
    while True:
        b = str( input( 'Do you want to back-cut? (y/n): ' ) )
        if b != 'n' and b != 'y':
            print('Please enter \'y\' or \'n\'...') 
        if a == 'n' or a == 'y':
            break        
    
    return ( a, b ) 

def modfiles( wbeg, ctrl, siltresh ):
    """
    Assumes that wbeg is an istance of the class wordbeginings and that ctrl is
    one of the following tuples ('n','n'), ('n','y'), ('y','n'), ('y','y'). 
    Copies files from the input directory to the output directory, and then
    modifies the copies in the output directory. 
    """
    inputpath = 'input'
    outputpath = 'output'

    for filename in os.listdir(inputpath):
        copyfile( inputpath + '/' + filename, outputpath + '/' + filename )
        
    for filename in os.listdir(outputpath):
        isex = False
        for i in range( wbeg.getnumex() ):
            for elem in wbeg.getset( i )[ 0 ]:
                if elem == filename[ 0 : len( elem ) ]:
                    if ctrl[ 0 ] == 'y':
                        sound = trimfront( outputpath + '/' + filename, wbeg.getset( i )[ 1 ], siltresh )
                        sound.export( outputpath + '/' + filename, format = "wav")
                    if ctrl[ 1 ] == 'y':
                        sound = trimback( outputpath + '/' + filename, wbeg.getset( i )[ 2 ], siltresh )
                        sound.export( outputpath + '/' + filename, format = "wav")    
                    isex = True
                    break
                    break
                    
        if isex == False:
            if ctrl[ 0 ] == 'y':
                sound = trimfront( outputpath + '/' + filename, wbeg.getdint1(), siltresh )
                sound.export( outputpath + '/' + filename, format = "wav")            
            if ctrl[ 1 ] == 'y':
                sound = trimback( outputpath + '/' + filename, wbeg.getdint2(), siltresh )
                sound.export( outputpath + '/' + filename, format = "wav") 
                
def readsiltre():
    """
    Reads user input for scilence treshhold.
    """
    while True:
        try:
            siltresh = float(input( 'Enter relative scilence treshold in dB (real number between 0 and 50): ' ))
            assert siltresh > 0 and siltresh < 50
            return siltresh
        except ValueError:
            print('That was not a real number. Please try again...')
            

"""
Main program
"""
wordsets = setsinput()
ctrl = ctrlinput()
siltre = readsiltre()
modfiles( wordsets, ctrl, siltre )
input('Your files are in the output folder. Press any key to exit...')


    
    
            




            

            
        
    
        

        
    
    

    
    
        
