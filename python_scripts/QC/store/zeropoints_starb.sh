#!/bin/tcsh
#!
#!
#--------------------------------------------------------------------------
# set the root directory name dfits and fitsort 
# ***************************************************
#set fitsdr             = /Users/sjs/soft/fits
set fitsdr              = /home/sjs/soft/bin

#--------------------------------------------------------------------------
# set the root directory name for ML and HK data 
# ***************************************************
#

#Temp for test
#set hkdata_dir          = /Users/sjs/data/ATLAS/zeropoints
set hkdata_dir          = /data/dbstore4/psat04/atlas/red/02a/58430
#set mldata_dir         = /data/dbstore4/psat04/atlas/red/01a

set filelist1 = `ls $hkdata_dir/*.fz`

echo "FILE                                                	MJD-OBS       	CAMID   	FILTER	MAGZPT	MAG5SIG	AIRMASS	SEEING	SKYMAG	CLOUD	MOONSKY	MANGLE" > zeropoints.dat

   foreach file1 ($filelist1[*])
   $fitsdr/dfits -x 1 $file1 | $fitsdr/fitsort MJD-OBS CAMID FILTER MAGZPT MAG5SIG AIRMASS  SEEING SKYMAG CLOUD MOONSKY MANGLE | grep -v 'FILE' >> zeropoints.dat
   end

