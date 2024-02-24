## Utilities for Molecular Dynamics Simulation
Targeting simulation in LAMMPS at this stage

## Content in MD_LAMMPS
- `in.lammps`: LAMMPS input file for an individual umbrella sampling run between 2 polymer grafted nanoparticles. Includes information on output variables in the LAMMPS trajectory files
- `umbrella.cmd`: a Bash command script that automatically changes variables before handing the job to the SLURM job scheduling system
- `restart.cmd`: a Bash command script that restart an umbrella sampling run
- `parse_force.py`: a python script that parse the force and position from each LAMMPS trajactory file in each umbrella sampling folder, finds the mean force, and store them in a dictionary

## Content 
- `signac_copy_files.py`: an example script to copy and rename files from each folder in the workspace to a target directory for plotting. 

## Build & Execute
Refer to the `umbrella.cmd` file for information about the required modules
