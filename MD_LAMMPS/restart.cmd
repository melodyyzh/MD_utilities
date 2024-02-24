# Restart script to start all the umbrella runs (run2)
r0s=`cat umbrellas_remain.dat`
  
for i in $r0s
do

  old_dir="r_${i}-k_35"
  new_dir="r_${i}-k_35_run1"
  rm -rf $new_dir
  mkdir $new_dir

  step=400000
  awk -v i="$i" -v step="$step" '{if($2=="springX"){sub($4,i)}} {if($1=="run"){sub($2,step)}} {print}' template.in.lammps > $new_dir/in.lammps
  
  last_restart=`ls -lrt $old_dir/nvt*restart | tail -n 1 | awk '{print $NF}'`
  cp $last_restart $new_dir/generic.restart
  cp job.cmd $new_dir

  cd $new_dir
  sbatch job.cmd
  cd - # Move back to base directory
  echo "just submitted $i"

done

#r_old=200.0

#cd r_${r_old}-k_5
#srun -n 24 $lmp -i in.twoParticles > out.lammps
#cd -

#for i in {0..30}

#do

    # Calculate the target separation distance, create the corresponding directory

#  d=`python3 -c "import sys; print(round(195-float(sys.argv[1])*5.0,1))" ${i}`
  
#  new_dir="r_${d}-k_5"
#  #rm -rf $new_dir
#  mkdir $new_dir

  # Substitute particle distance     

#  awk -v d="${d}" '{if($2=="springX"){sub($4,d)}} /timestep/{print "reset_timestep 0"} {print}' template.in.lammps > $new_dir/in.lammps      # I modified this line because I used parameter to represent final equilibrium distance 

  # Copy the most recently printed restart file from the previous run

#  last_restart=`ls -lrt r_${r_old}-k_5/nvt*restart | tail -n 1 | awk '{print $NF}'`

#  cp $last_restart $new_dir/generic.restart

  # Run the job

#  cd $new_dir

#  srun -n 24 $lmp -i in.lammps > out.lammps

#  cd - # Move back to base directory

#  r_old=${d}
#  echo "just finished $i"
#done

