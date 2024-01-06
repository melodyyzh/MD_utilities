#!/bin/bash

#SBATCH --job-name=ligand_nanoparticle_umbrella_sampling 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1 
#SBATCH --time=10:00:00
#SBATCH --account=rklinds1
#SBATCH --partition=standard
#SBATCH -o stdoutmsg

#define module and excutable 
source /home/yiyuanmz/codes/chimes_calculator-myfork/etc/lmp/modfiles/UM-ARC.mod 
lmp=/home/yiyuanmz/codes/chimes_calculator-myfork/etc/lmp/exe/lmp_mpi_chimes

# Assumes you're using keq = 35
# Assumes directories structured like:r_<dist>-k_35

# Assumes you've already run r = 131 with k = 35
# Assumes you're running from the directory that will *contain* r_<dist>-k_<keq> directories

r_old=103.0

#cd r_${r_old}-k_35
#$lmp -i in.twoParticles > out.lammps
#cd -

for i in {8..9}

do

    # Calculate the target separation distance, create the corresponding directory

  d=`python3 -c "import sys; print(round(127.5-float(sys.argv[1])*3.5,1))" ${i}`
  
  new_dir="r_${d}-k_35"
  rm -rf $new_dir
  mkdir $new_dir

  # Substitute particle distance     

  awk -v d="${d}" '{if($2=="springX"){sub($4,d)}} /timestep/{print "reset_timestep 0"} {print}' template.in.lammps > $new_dir/in.lammps      # I modified this line because I used parameter to represent final equilibrium distance 

  # Copy the most recently printed restart file from the previous run

  last_restart=`ls -lrt r_${r_old}-k_35/nvt*restart | tail -n 1 | awk '{print $NF}'`

  cp $last_restart $new_dir/generic.restart

  # Run the job

  cd $new_dir

  $lmp -i in.lammps > out.lammps

  cd - # Move back to base directory

  r_old=${d}
  echo "just finished $i"
done

#Collapse

