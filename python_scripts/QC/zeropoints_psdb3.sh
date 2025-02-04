#!/bin/tcsh
#!
#!
#--------------------------------------------------------------------------
# set the root directory name dfits and fitsort 
# ***************************************************
#set fitsdr             = /Users/sjs/soft/fits
set fitsdr              = /home/sjs/soft/bin
set qcdir               = /home/atls/QC

mv $qcdir/zeropoints.dat $qcdir/store 

#--------------------------------------------------------------------------
# set the root directory name for ML and HK data 
# ***************************************************
#

#Temp for test
#set hkdata_dir          = /Users/sjs/data/ATLAS/zeropoints
set hkdata_dir          = /data/dbstore4/psat04/atlas/red/01a
#set mldata_dir         = /data/dbstore4/psat04/atlas/red/01a
 echo "FILE                                                                      MJD-OBS       CAMID     FILTER	MAGZPT	MAG5SIG	AIRMASS	SEEING	SKYMAG	CLOUD	MOONSKY	MANGLE" > zeropoints.dat

set dirlist1 =  `ls $hkdata_dir | grep 5 | grep -v a`
echo $dirlist1 
foreach dir1 ($dirlist1[*]) 

#Before 57308, sky QC params not complete 
 if (`expr $dir1 \> 57300`) then
 set filelist1 = `ls $hkdata_dir/$dir1/*.fz`
 echo $filelist1 
     foreach file1 ($filelist1[*])
    $fitsdr/dfits -x 1 $file1 | $fitsdr/fitsort MJD-OBS CAMID FILTER MAGZPT MAG5SIG AIRMASS  SEEING SKYMAG CLOUD MOONSKY MANGLE | grep -v 'FILE' >> zeropoints.dat
     end
 endif
end

# Timings 
#[atls@starbase ~/QC]$ hostname
#starbase.mp.qub.ac.uk
#[atls@starbase ~/QC]$ time ./zeropoints_starb.sh
#    1.538u 4.412s 0:05.39 110.2%0+0k 1229768+7608io 0pf+0w

#[atls@psdb3 ~/QC]$ hostname
#psdb3.starfleet
#[atls@psdb3 ~/QC]$ time ./zeropoints_starb.sh
#    0.794u 2.156s 0:02.84 103.5%0+0k 56+640io 0pf+0w
