import os
import subprocess
from pathlib import Path

inbox = "/Users/emilyfulk/Downloads/demmo_faa_errors"
outbox = "/Users/emilyfulk/Downloads/demmo_faa_errors"

for filename in os.listdir(inbox):
    if filename.endswith(".faa"):
        subprocess.run(["bash", "seqtk_run", os.path.join(inbox,filename), Path(outbox)])
