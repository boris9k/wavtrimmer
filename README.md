# wavtrimmer
Leading and ending silence trimmer for wav files

To use the program, make directories named input and output in the directory of the program. 
Put the .wav files that you want edit in the input folder. After running the program edited 
copies of the files will be in the output folder. 

On running the program you will be asked to default input front interval. It is the time 
between where you want the cut to be made and the first nonsilence in the file. Similary, 
back interval is the time from the last nonsilence to the time of the cut. After entering
default values for the front and back intervals, you will be asked to enter the set of 
filename beginings for which you want to use different cut intervals. Enter the filename
beginings separated by spaces, for example: ca a f <enter>. You can add as many exeptional 
filename beginings groups as you like. After entering exeptional filename beginings and 
their associated 
