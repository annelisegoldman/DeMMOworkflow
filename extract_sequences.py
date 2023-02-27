import subprocess
from pathlib import Path
import re

# Define base directory, and directories for (1) input files (.faa from Prodigal), (2) .lst files containing protein names, and (3) output file for extracted HK sequences. Can use subdirectories of the basedir (as given here), or change these to be hardcoded paths
basedir= "path/to/basedir"
inbox= "/inbox"
lstbox= "/lstbox"
outbox= "/outbox"

faa_dir = Path(basedir).joinpath(inbox)
lst_dir = Path(basedir).joinpath(lstbox)
out_dir = Path(basedir).joinpath(outbox)

for f in faa_dir.iterdir():
    # For faa files in inbox, extract MAG ID
    if f.name.endswith('faa'):
        faa_id = re.search('[0-9]+(?=\.faa)', f.name).group(0)
  
        # Find corresponding .lst file for each MAG ID
        for lst_file in lst_dir.glob('FAA_ID%s.SLURM*.lst' % faa_id):

        # Spawns bash script for running seqtk to extract HK sequences from each file 
            subprocess.run(["bash", "seqtk_run", f, lst_file, out_dir,faa_id])