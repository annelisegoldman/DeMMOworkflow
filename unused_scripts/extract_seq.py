import os
import subprocess
from pathlib import Path

inbox = "/home/alg18/Prodigal/"
lst_dir = "/home/alg18/indv_HKseq_names/"
outbox = "/home/alg18/HK_seqs/"

for filename in os.listdir(inbox):
    if filename.endswith(".faa"):
        subprocess.run(["bash", "/home/alg18/DeMMOworkflow/seqtk_run", os.path.join(inbox,filename), lst_dir, Path(outbox)])
