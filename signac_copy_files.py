#!/usr/bin/env python
# coding: utf-8

# #### File to copy all the twob_smd_log.txt files 

# In[4]:


import os 
import shutil 
import signac


# In[10]:


pr = signac.get_project()

# create a folder for all the copied files 
output_dir = "log_files"
os.makedirs(output_dir, exist_ok=True)

for job in pr:
    config = job.sp.get("input_gsd_fn")[6:10]  # extract config name, eg AAAA
    seed = job.sp.get("seed") 
    fn = job.fn("twob_smd_log.txt") 
    
    # rename the file
    new_fn = f"{config}_{seed}.txt"
    output_file_path = os.path.join(output_dir, new_fn)
    
    #cope the file
    shutil.copy2(fn, output_file_path)
    print(f"Copied and renamed {fn} to {new_fn}")

print(f"all files have been processed and stored in {output_dir}")


# In[ ]:





# In[ ]:




