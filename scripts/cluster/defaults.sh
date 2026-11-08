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

# Partition for GPU work (docs/engineering/decisions/ED-0002).
CLUSTER_PARTITION=${CLUSTER_PARTITION:-all_usr_prod}

# The partition's GPU models, sorted into two explicit lists (ED-0004). Every model in
# the partition must be in exactly one; submit.sh checks this before every submission.

# Allowed: jobs may run on these (--constraint): every GPU except Blackwell (ED-0027).
# On all_usr_prod, a list asking for more than 24 GB is refused: keep at least one model
# of 24 GB or less in it. For one submission, CLUSTER_GPU_SUBSET="<features>" narrows it
# to a subset (e.g. one family, for strictly comparable hardware).
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
  gpu_RTXPro6000B_96G # Blackwell: no kernels in this PyTorch build (ED-0001)
)

# --- GPU jobs (the default) or CPU-only jobs (ED-0022) ---

# CLUSTER_PROFILE=cpu scripts/cluster/submit.sh … submits a CPU-only job: no GPU request,
# no GPU list, no GPU check. By default it runs on all_serial: the login nodes, but
# through Slurm, free of charge, at most 4 h, without taking cores from GPU jobs. For
# heavy or long CPU work, set CLUSTER_CPU_PARTITION=all_usr_prod (billed, up to 24 h).
CLUSTER_PROFILE=${CLUSTER_PROFILE:-gpu}
CLUSTER_CPU_PARTITION=${CLUSTER_CPU_PARTITION:-all_serial}

# --- What each job gets ---

# One run per job, on one node (ED-0003).
CLUSTER_NODES=${CLUSTER_NODES:-1}
CLUSTER_NTASKS=${CLUSTER_NTASKS:-1}

# GPUs per job (--gres=gpu:N).
CLUSTER_GPUS=${CLUSTER_GPUS:-1}

# CPU cores per job (--cpus-per-task). 6 is what each GPU reserves by default anyway, so
# asking explicitly costs nothing extra, and programs can read it from
# SLURM_CPUS_PER_TASK (e.g. for data-loader workers).
CLUSTER_CPUS=${CLUSTER_CPUS:-6}

# Time limit per job (--time). Billing counts only the time actually used, but longer
# limits can wait longer in the queue. The partition allows up to 24:00:00.
CLUSTER_TIME=${CLUSTER_TIME:-01:00:00}

# Warning before the time limit (--signal): Slurm sends TERM to the job script ("B:") 120
# seconds before killing the job, so job.sbatch can record "timeout" in run.json and stop
# the command cleanly. Without it, a timed-out run would stay "running" forever.
# Consequences: a run effectively gets CLUSTER_TIME minus 2 minutes, and sacct shows such
# runs as FAILED (signal 15) rather than TIMEOUT: run.json is the reliable record (ED-0006).
CLUSTER_SIGNAL=${CLUSTER_SIGNAL:-B:TERM@120}

# Never requeue a job (--no-requeue). A requeued job would run again in the same run
# folder, mixing two executions in one record. The cluster doesn't requeue by default
# (JobRequeue = 0, checked 2026-11-02); this keeps it so if its configuration changes.
CLUSTER_REQUEUE=${CLUSTER_REQUEUE:-false}

# Memory is deliberately not set: the cluster's default applies (3 GB per CPU core, so
# 18 GB with 6 cores), which fits this project's models.
# Set it for one job with SBATCH_OPTS="--mem=…".
