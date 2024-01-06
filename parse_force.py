#!/usr/bin/env python
# coding: utf-8

# In[11]:


import numpy as np
import math
import os
import matplotlib.pyplot as plt


# ### units 
# ##### energy: kcal/mol
# ##### force: kcal/mol-Angstrom

# In[2]:


# Prefix for directories
prefix = "r_"
parent_dir = './'

# Initialize empty dictionary for storing sum values
sum_dict = {}

# Get all subdirectories start with 'r_'
sub_dirs = [dir for dir in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, dir)) and dir.startswith(prefix)]


# In[3]:


# Traverse through each subdirectory of parent folder
for dir in sub_dirs:
    # Get d_eq value from directory name, split directory name by '-' 
    d_eq = float(dir.split('-')[0].replace(prefix, ''))
    sub_dir_path = os.path.join(parent_dir, dir)

    # Assuming all the files within subdirectory should be parsed
    for file in os.listdir(sub_dir_path):
        if file.endswith(".lammpstrj"):
            # Update the infile path
            infile = open(os.path.join(sub_dir_path, file), 'r')
            
            num_frame = 2001
            num_frame_start = 1900
            line_per_frame = 12011
            line_to_skip = num_frame_start * line_per_frame

            num_cg_NP = 2  # 18 nanoparticles in the 
            num_atom_per_NP = 6001
            num_atom_total = num_cg_NP * num_atom_per_NP
            title_line = 9

            total_force = []
            total_pos = []

            for _ in range(line_to_skip):
                next(infile)

            for i in range(num_frame_start, num_frame):
                for _ in range(title_line):
                    next(infile)
                    
                force = np.zeros((2,3))
                pos = np.zeros((2,3))
                for j in range(num_atom_total):
                    line = infile.readline().split()
                    if float(line[0]) <= 6001:
                        force[0,:] += np.array([line[6], line[7], line[8]]).astype(float)
                        if float(line[0]) == 1:
                            pos[0,:] = np.array([line[3], line[4], line[5]]).astype(float)
                    else: 
                        force[1,:] += np.array([line[6], line[7], line[8]]).astype(float)
                        if float(line[0]) == 6002:
                            pos[1,:] = np.array([line[3], line[4], line[5]]).astype(float)
                
                total_force.append(force)
                total_pos.append(pos)
                
            total_force = np.stack(total_force)
            total_pos = np.stack(total_pos)

            # Find avg position
            dist = []
            for i in range(total_pos.shape[0]):
                NP_dist = math.sqrt((total_pos[i,1,0] - total_pos[i,0,0])**2 + (total_pos[i,1,1] - total_pos[i,0,1])**2 + (total_pos[i,1,2] - total_pos[i,0,2])**2)
                dist.append(NP_dist)

            # calculate spring force and net force on NP1
            spring_force = []
            k = 35 # spring constant
            for i in range(total_pos.shape[0]):
                force = -k*(d_eq - dist[i])   # deltax = eql - actual here
                spring_force.append(force)
            
            net_force = []
            for i in range(total_force.shape[0]):
                net = total_force[i,0,0] - spring_force[i]
                net_force.append(net)
            sum_val = np.sum(net_force)/len(net_force)
            
            # After calculating the sum, add it to the dictionary using d_eq as key
            sum_dict[d_eq] = sum_val 

# Print the dictionary with sum for each distance
print(sum_dict)


# In[25]:


x_values = list(sum_dict.keys())
y_values = list(sum_dict.values())

y_values_neg = [-y for y in y_values]

plt.figure(figsize=(8,5))
plt.scatter(x_values, y_values_neg, c='blue', label="net force fx")

plt.title("Force acting on NP2 from umbrella sampling")
plt.xlabel('Distance ($\AA$)',fontsize=12)
plt.ylabel('Average force (kcal/mol-$\AA$)',fontsize=12)
plt.legend()


# In[ ]:




