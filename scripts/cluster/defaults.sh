# shellcheck shell=bash
# shellcheck disable=SC2034  # the variables are used by the scripts that source this file
# Project-wide cluster settings: decisions, not personal values (those live in .env).
# Sourced by common.sh. Change them only together with the decision they implement.
#
# Every Slurm option the scripts set is here; job.sbatch hardcodes none.
# Each scalar value can be overridden for one submission with an environment variable:
#   CLUSTER_TIME=04:00:00 scripts/cluster/submit.sh ...
# Any other sbatch option goes in SBATCH_OPTS.

# --- Where jobs run ---

# Partition for GPU work (docs/project/decisions/PD-002).
CLUSTER_PARTITION=${CLUSTER_PARTITION:-all_usr_prod}

# The partition's GPU models, sorted into two explicit lists (PD-004). Every model in
# the partition must be in exactly one; submit.sh checks this before every submission.

# Allowed: jobs may run on these (--constraint). Whether to also exclude L40S and A40
# is PQ-002.
CLUSTER_GPU_FEATURES=(
  gpu_1080_8G
  gpu_2080_11G
  gpu_2080Ti_11G
  gpu_RTX5000_16G
  gpu_RTX6000_24G
  gpu_RTX_A5000_24G
  gpu_A40_45G
  gpu_L40S_45G
)

# Excluded, each with its reason.
CLUSTER_GPU_EXCLUDED=(
  gpu_RTXPro6000B_96G # Blackwell: no kernels in this PyTorch build (PD-001)
)

# --- What each job gets ---

# One run per job, on one node (PD-003).
CLUSTER_NODES=${CLUSTER_NODES:-1}
CLUSTER_NTASKS=${CLUSTER_NTASKS:-1}

# GPUs per job (--gres=gpu:N).
CLUSTER_GPUS=${CLUSTER_GPUS:-1}

# Time limit per job (--time). Billing counts only the time actually used, but longer
# limits can wait longer in the queue. The partition allows up to 24:00:00.
CLUSTER_TIME=${CLUSTER_TIME:-01:00:00}

# CPUs and memory are deliberately not set: the cluster's default per GPU applies
# (6 CPU cores and 18 GB of RAM), which fits this project's models.
# Set them for one job with SBATCH_OPTS="--cpus-per-task=… --mem=…".
