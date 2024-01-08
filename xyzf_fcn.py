#!/usr/bin/env python
# coding: utf-8

# #### Script for parsing force from LAMMPS trajectory file

# In[1]:


import os
import numpy as np


# In[2]:


class FilePreparation:
    def __init__(self, prefix, parent_dir):
        self.prefix = prefix
        self.parent_dir = parent_dir
        self.sub_dirs = [dir for dir in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, dir)) and dir.startswith(prefix)]

    def extract_from_file(self, dir, file):
        infile = open(os.path.join(dir, file), 'r')

        num_frame = 2001
        num_frame_start = 1900
        line_per_frame = 12011
        line_to_skip = num_frame_start * line_per_frame
    
        num_cg_NP = 2  # 18 nanoparticles in the 
        num_atom_per_NP = 6001
        num_atom_total = num_cg_NP * num_atom_per_NP
        title_line = 9
        unit_conv = 4.18 * 0.0002015431312467687 
    
        for _ in range(line_to_skip):
            next(infile)
            
        total_force = []
        total_pos = []    
        for i in range(num_frame_start, num_frame):
            for _ in range(title_line):
                next(infile)
            
            force = np.zeros((2,3))
            pos = np.zeros((2,3))
            for j in range(num_atom_total):
                line = infile.readline().split()
                if float(line[0]) <= 6001:
                    force[0,:] += unit_conv * np.array([line[6], line[7], line[8]]).astype(float)
                    if float(line[0]) == 1:
                        pos[0,:] = np.array([line[3], line[4], line[5]]).astype(float)
                else: 
                    force[1,:] += unit_conv * np.array([line[6], line[7], line[8]]).astype(float)
                    if float(line[0]) == 6002:
                        pos[1,:] = np.array([line[3], line[4], line[5]]).astype(float)
        
            total_force.append(force)
            total_pos.append(pos)
        
        total_force = np.stack(total_force)
        total_pos = np.stack(total_pos)
    
        avg_NP1_force = np.average(total_force[:,0,:], axis=0)
        avg_NP2_force = np.average(total_force[:,1,:], axis=0)
        avg_NP1_pos = np.average(total_pos[:,0,:], axis=0)
        avg_NP2_pos = np.average(total_pos[:,1,:], axis=0)
        
        results = {"avg_NP1_force": avg_NP1_force, "avg_NP2_force": avg_NP2_force, "avg_NP1_pos": avg_NP1_pos, "avg_NP2_pos": avg_NP2_pos}
        return results

    def write_to_file(self, results, num_cg_NP):
        with open("umbrella.xyzf",'a') as f:
            f.write(str(num_cg_NP)+ '\n')
            f.write(str(1000) + " " + str(1000) + " " + str(1000) + '\n')
            f.write('A' + " " + str(results["avg_NP1_pos"][0]) + " " + str(results["avg_NP1_pos"][1]) + " " + str(results["avg_NP1_pos"][2]) + " " + \
                  str(results["avg_NP1_force"][0]) + " " + str(results["avg_NP1_force"][1]) + " " + str(results["avg_NP1_force"][2]) + '\n')
            f.write('A' + " " + str(results["avg_NP2_pos"][0]) + " " + str(results["avg_NP2_pos"][1]) + " " + str(results["avg_NP2_pos"][2]) + " " + \
                  str(results["avg_NP2_force"][0]) + " " + str(results["avg_NP2_force"][1]) + " " + str(results["avg_NP2_force"][2]) + '\n')

# The new method to process directories and files
    def process_files(self):
        for dir in self.sub_dirs:
            d_eq = float(dir.split('-')[0].replace(self.prefix, ''))
            sub_dir_path = os.path.join(self.parent_dir, dir)
    
            for file in os.listdir(sub_dir_path):
                if file.endswith(".lammpstrj"):
                    results = self.extract_from_file(sub_dir_path, file)
                    self.write_to_file(results, 2)


# In[3]:


if __name__ == "__main__":
    file_process = FilePreparation("r_", './')
    file_process.process_files()


# In[ ]:




