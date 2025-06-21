#!/bin/bash
#SBATCH --job-name=Robust_CCG_Net5
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --mem=64gb
#SBATCH --time=60:00:00
#SBATCH --constraint=chip_type_6148g

set -e

module load anaconda3/2023.09-0 gurobi/10.0.1
source activate gurobi_10

srun python3 robust_Main.py

