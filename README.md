# wavtrimmer
Leading and ending silence trimmer for wav files

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

To use the program, make directories named input and output in the directory of the program. 
Put the .wav files that you want edit in the input folder. After running the program edited 
copies of the files will be in the output folder. The program uses pydub module which is not 
common in the installations of python, so you might need to install it first.

On running the program you will be asked to default input front interval. It is the time 
between where you want the cut to be made and the first non-silence in the file. Similarly, 
back interval is the time from the last non-silence to the time of the cut. After entering
default values for the front and back intervals, you will be asked to enter the set of 
filename beginnings for which you want to use different cut intervals. Enter the filename
beginnings separated by spaces, for example: ca a f <enter>. You can add as many exceptional 
filename beginnings groups as you like. After entering exceptional filename beginnings and 
their associated cut intervals, you will be asked whether you want to cut from front, back, 
or both. Finally, you will be asked for the relative silence threshold in dB. Everything 
that is less loud than average loudness of the file minus the relative silence threshold
will be considered as silence. This parameter goes from 0 (everything is considered silence) 
to 50 (any noise is not silence). Depending on how much noise your files have, you should 
experiment with this parameter to find the value that suits your purposes. Rule of thumb is 
that the less this number is, more will be cut.  
