import os
import subprocess
from pathlib import Path

inbox = "/Prodigal/"
lstbox ="/indv_HKseq_names/"
outbox = "/HK_seqs/"

for filename in os.listdir(inbox):
    if filename.endswith(".faa"):
        subprocess.run(["bash", "seqtk_run", os.path.join(inbox,filename), Path(lstbox), Path(outbox)])
