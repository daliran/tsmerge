# EQ-014 — Can the cluster's compute nodes reach the internet?

- **Status:** open
- **Opened:** 2026-11-02

## Why it matters

- Online services from inside a job depend on it: experiment tracking such as wandb ([ED-033](../decisions/ED-033-training-curves.md), whose "Revisit if" names it), and downloading datasets or pretrained weights while a job runs.
- Today nothing needs it: environments are built on a login node, and datasets are uploaded beforehand ([ED-020](../decisions/ED-020-dataset-location.md)).

## Options

- **A. Test it once:** a short CPU job that tries an HTTPS request to a public site and records the result. About a minute, free on `all_serial` (though `all_serial` runs on the login nodes, which may differ from the GPU nodes: the test would also need one short job on `all_usr_prod`, billed: a fraction of a standard hour).
- **B. Ask the HPC helpdesk.**
- **C. Assume no:** design anything online to run offline in jobs and sync from your machine.

## Hypotheses

Not established yet:

- The cluster's data-transfer node isn't reachable from outside the Unimore network, a sign of restrictive networking ([ED-024](../decisions/ED-024-large-transfers.md)); compute nodes may have no outbound access either.

## Evidence so far

- None direct.

## Next action

Decide when something first needs internet access inside a job (wandb, downloads); until then, option C holds by default.
