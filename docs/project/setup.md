# Setup

How to prepare a local machine to work on this repository: base tools, git, SSH (GitHub and the Unimore AImageLab-HPC cluster), Python, the GPU, optionally Docker for the diagrams, and VS Code. Facts about the cluster are in [cluster.md](cluster.md); daily use in [running.md](running.md).

Everything here works on **native Linux** and on **WSL2 on Windows**. Where the two differ, both are given; the differences are summed up in [Native Linux or WSL2](#native-linux-or-wsl2).

**WSL2:**

- Run everything from a WSL shell, never from PowerShell: the scripts need Linux `git`, `ssh` and `rsync`.
- Enable **systemd** (Ubuntu distros created on older WSL versions boot without it, and then services such as `snapd` and `cron` don't run, and Ubuntu release upgrades hang). Needs WSL 0.67.6 or newer (`wsl --version` in PowerShell):

  ```bash
  sudo tee /etc/wsl.conf > /dev/null <<'EOF'
  [boot]
  systemd=true
  EOF
  ```

  Then restart WSL from PowerShell with `wsl --shutdown`, open a new WSL shell, and check that `ps -p 1 -o comm=` prints `systemd`.
- WSL doesn't reboot with `sudo reboot`: restart it with `wsl --shutdown` from PowerShell, then open a new WSL shell (in VS Code: *Reconnect*).

## 1. Base tools

```bash
sudo apt update
sudo apt install make rsync openssh-client curl keychain git-lfs shellcheck
```

(Ubuntu/Debian; Ubuntu 24.04 LTS recommended, since older releases ship outdated packages. On other distributions, install the same packages with their package manager.)

**Upgrading an older Ubuntu** goes one LTS at a time (20.04 → 22.04 → 24.04): run `sudo do-release-upgrade`, restart (on WSL2: `wsl --shutdown`), and repeat. On WSL2, enable systemd first (above). When the upgrade asks whether to keep a locally modified configuration file you never edited on purpose, take the package maintainer's version. Afterwards, re-add any PPA (the upgrade disables them) and run `sudo apt autoremove`.

- `keychain` keeps SSH keys unlocked for the session ([step 3](#3-ssh-github-and-the-cluster)).
- `git-lfs` stores large binary files outside the normal git history, if the repository ever needs it.
- `shellcheck` checks the shell scripts for bugs (see [CONTRIBUTING.md](../../CONTRIBUTING.md#checks-before-committing)).

## 2. Git

### Install a current git

Distribution packages often ship an old git, and some options below need 2.37 or newer. On Ubuntu, use the official git PPA:

```bash
sudo add-apt-repository ppa:git-core/ppa
sudo apt update && sudo apt install git
git --version
```

After an Ubuntu release upgrade, the PPA is left disabled and pointing at the old release: delete its old file in `/etc/apt/sources.list.d/` (`git-core-ubuntu-ppa-<old release>.*`) and run the commands above again.

### Configure it

Once per machine:

```bash
# Identity (the same email as on GitHub)
git config --global user.name "<your name>"
git config --global user.email "<your email>"

# Pull: rebase local commits on top of the remote's instead of creating merge commits,
# stashing and restoring uncommitted changes automatically
git config --global pull.rebase true
git config --global rebase.autoStash true
git config --global merge.autoStash true

# Branches and remotes
git config --global init.defaultBranch main       # new repos start on main
git config --global push.default current          # push the current branch to the same name
git config --global push.autoSetupRemote true     # the first push sets the upstream, no -u needed
git config --global push.followTags true          # push annotated tags with their commits
git config --global fetch.prune true              # drop refs to branches deleted on the remote

# Line endings: convert CRLF to LF on commit, never the other way
git config --global core.autocrlf input

# Editor for commit messages and rebases ("nano" works too)
git config --global core.editor "code --wait"

# Diffs and conflicts
git config --global diff.algorithm histogram      # clearer diffs for moved or reordered code
git config --global diff.colorMoved zebra         # show moved lines in a different color
git config --global merge.conflictstyle zdiff3    # conflict markers include the common ancestor
git config --global rerere.enabled true           # remember conflict resolutions and reuse them

# Quality of life
git config --global commit.verbose true           # show the diff in the editor while writing a message
git config --global branch.sort -committerdate    # `git branch` lists recent branches first
git config --global help.autocorrect prompt       # "git stauts" → asks to run "git status"

# Git LFS hooks
git lfs install
```

Check with `git config --global --list`.

- **Pull with rebase:** your local commits are replayed on top of the remote's, so history stays linear. Uncommitted changes are stashed before and restored after; if restoring them conflicts, git says so and they stay in `git stash list`.
- **Line endings:** this repository's `.gitattributes` already forces LF; `core.autocrlf input` is a safety net for repositories without one.

## 3. SSH: GitHub and the cluster

Use **one key per host**: one for GitHub, one for the cluster. Each key is named after what it is for, and `~/.ssh/config` pins every host to its own key, so ssh never offers the wrong one. The compute scripts reach the cluster through the alias `ailb`. The real host and user names live only in your `~/.ssh/config`, never in the repository.

### Get the keys

**Key names.** `ssh-keygen` names a key after its algorithm (`id_rsa`, `id_ed25519`), not after what it's for, so with two keys the defaults collide and say nothing. This guide names each key `id_<type>_<host>`, e.g. `id_ed25519_github` or `id_rsa_github`: the type is the algorithm, the suffix is the host it opens. Any name works, since ssh only uses the file `IdentityFile` points to. For new keys, use **Ed25519**: the modern default, short and fast. Existing RSA keys (2048 bits or more) are fine to keep.

**New keys** (any machine):

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_github -C "<your-email>"
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_ailb   -C "<your-email>"
```

Then register each public key (`.pub`):

- **GitHub:** GitHub → Settings → SSH and GPG keys → *New SSH key*, type *Authentication key*; paste the output of `cat ~/.ssh/id_ed25519_github.pub`.
- **Cluster:** follow the cluster's documentation. Where password login is allowed: `ssh-copy-id -i ~/.ssh/id_ed25519_ailb.pub <cluster-user>@<login-host>`.

**WSL2, keys already on Windows:** WSL has its own `~/.ssh`, separate from Windows' `C:\Users\<you>\.ssh`. Copy the keys you already use into WSL (ssh refuses keys read straight from `/mnt/c`, whose permissions are too open), naming each after its host:

```bash
cp /mnt/c/Users/<you>/.ssh/<github-key>     ~/.ssh/id_<type>_github
cp /mnt/c/Users/<you>/.ssh/<github-key>.pub ~/.ssh/id_<type>_github.pub
cp /mnt/c/Users/<you>/.ssh/<cluster-key>     ~/.ssh/id_<type>_ailb
cp /mnt/c/Users/<you>/.ssh/<cluster-key>.pub ~/.ssh/id_<type>_ailb.pub
```

To tell which key is which, compare fingerprints (`ssh-keygen -lf <key>.pub`) with those listed on GitHub → Settings → SSH and GPG keys. Copy only keys in OpenSSH format (first line `-----BEGIN OPENSSH PRIVATE KEY-----`); PuTTY `.ppk` files are not needed.

### Configure `~/.ssh/config`

```
Host github.com
  User git
  IdentityFile ~/.ssh/id_<type>_github
  IdentitiesOnly yes

Host ailb
  HostName <login-host>
  User <cluster-user>
  IdentityFile ~/.ssh/id_<type>_ailb
  IdentitiesOnly yes
  ControlMaster auto
  ControlPath ~/.ssh/cm-%C
  ControlPersist 8h
  ServerAliveInterval 60
```

- `IdentitiesOnly yes` makes ssh offer each host only its own key.
- The `Control*` lines open one connection to the cluster and reuse it until it has gone unused for 8 hours (or the network drops), so the compute scripts authenticate once instead of on every command.

Make the permissions strict, or ssh refuses the files:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/config ~/.ssh/id_*_github ~/.ssh/id_*_ailb
chmod 644 ~/.ssh/*.pub
```

### Unlock everything once per session

Keys with a passphrase, and a cluster that asks for a password after the key, would mean typing passwords all the time. Instead, a working session starts with **one explicit step** that asks for everything once, and every terminal then reuses it.

**1. Terminals never ask.** In `~/.bashrc`, use `keychain` with `--noask`: each terminal joins the running SSH agent but never prompts for a passphrase.

```bash
eval "$(keychain --eval --quiet --noask)"
```

**2. List your keys in `.env`.** Copy `.env.example` to `.env` (git-ignored) and set `SSH_KEYS` to the keys to unlock, e.g. `SSH_KEYS="id_<type>_github id_<type>_ailb"`.

**3. Start each session with the session script**, from the repository:

```bash
scripts/start-session.sh
```

It:

- loads the SSH keys into the agent, asking only for the passphrases of keys not loaded yet;
- opens the shared connection to the cluster (`ssh -fN ailb`), asking for the cluster password only if no connection is open;
- checks GitHub and the cluster, and prints what is unlocked.

It is safe to rerun: whatever is already unlocked is skipped.

**How long a session lasts:**

- the keys stay unlocked until WSL or the machine restarts (on WSL2, WSL also stops by itself some time after every terminal and VS Code window is closed);
- the cluster connection stays open until it has gone unused for 8 hours (`ControlPersist`), or until the network drops; after that, rerun the script.

**Why it matters beyond convenience:** the cluster scripts run ssh non-interactively, where nobody can type a password. Without an unlocked key and an open connection they fail with `Permission denied`. Check the loaded keys with `ssh-add -l`, and the cluster connection with `ssh -O check ailb`.

**From VS Code:** the task *Start session (unlock SSH and the cluster)* runs the same script. To run it whenever VS Code opens the repository, add `"runOptions": { "runOn": "folderOpen" }` to that task in your copy of `.vscode/tasks.json` (VS Code asks once to allow automatic tasks); it then prompts on every folder open, even when you only read code.

### Check

```bash
ssh -T git@github.com    # "Hi <user>! You've successfully authenticated…"
ssh ailb hostname        # first time: confirm the host key
ssh ailb hostname        # second time: returns instantly (connection reused)
```

**If the cluster asks for a password after the key** (`ssh -v` shows `Authenticated using "publickey" with partial success`), it requires both. Scripts can't type the password, so open the shared connection by hand at the start of each working session, as described in [running.md](running.md#start-each-session).

Your cluster account is prepared once, in [step 7](#7-the-cluster-once-per-account).

## 4. Python with uv

[uv](https://docs.astral.sh/uv/) manages Python itself and every dependency. It is also a **Python version manager** (like `py` on Windows or pyenv): each version is downloaded once into `~/.local/share/uv/python` and shared by all projects. You don't need a system Python, and you should not use it.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Open a new shell afterwards (or run `source ~/.local/bin/env`) so `uv` is on the `PATH`.

### Use only uv's own Python builds

uv can run a project with two kinds of Python:

- **system Pythons:** installed by the operating system, e.g. `/usr/bin/python3.12` on Ubuntu;
- **managed Pythons:** standalone builds that uv downloads itself into `~/.local/share/uv/python`.

By default, uv uses a system Python when it matches the project's version. This project uses **managed Pythons only** (`python-preference = "only-managed"`):

- every machine (your workstation, the cluster) runs the identical Python build;
- an OS upgrade, which replaces the system Python, never changes the project's Python;
- the cluster's system Python (a different version) is never picked up by mistake.

The setting lives in two places:

- **in the repository's `pyproject.toml`:** applies to this project on every machine, with nothing to do;
- **globally, in `~/.config/uv/uv.toml`:** applies to every other uv project on the machine too. Recommended, once per machine:

  ```bash
  mkdir -p ~/.config/uv
  echo 'python-preference = "only-managed"' >> ~/.config/uv/uv.toml
  ```

Check which Python a project uses with `uv run python -c "import sys; print(sys.executable)"`: the path must be under `~/.local/share/uv/python` or the project's `.venv`.

Managing versions:

```bash
uv python install 3.12        # download a version (once)
uv python list                # installed and available versions
uv python pin 3.12            # pin a project to a version (writes .python-version)
uv self update                # update uv itself
```

You rarely need `uv python install` by hand: `uv sync` downloads the version the repository pins the first time. This repository pins an exact version, **3.12.16** (`.python-version`), so every machine runs the identical build ([PD-001](decisions/PD-001-python-and-pytorch.md)). The repository's own tooling uses the same Python: scripts run with `uv run`, and the expert-review guard hook uses the project environment's Python (`.venv/bin/python`), so `uv sync` must have been run. The cluster uses uv the same way, so local and cluster runs use the same Python build regardless of each machine's system Python.

## 5. GPU and CUDA (optional)

A local NVIDIA GPU is optional: without one, everything runs on CPU, only slower. You only need the **driver**. You don't need the CUDA toolkit, because PyTorch wheels ship their own CUDA runtime.

| | Native Linux | WSL2 on Windows |
|---|---|---|
| **Install the driver** | from the distribution, e.g. `sudo ubuntu-drivers install`, then reboot | on **Windows only**, from NVIDIA. WSL2 uses it automatically. Never install a Linux NVIDIA driver inside WSL |
| **Check it** | `nvidia-smi` | `nvidia-smi` inside WSL (it lives in `/usr/lib/wsl/lib/`) |

The driver must be recent enough for the CUDA version of the PyTorch build pinned in `pyproject.toml`: `nvidia-smi` shows the highest CUDA version the driver supports, top right.

**WSL2:** the GPU is shared with Windows. Games, browsers and other GPU-accelerated Windows apps take memory that training can't use, and their processes don't show in `nvidia-smi` inside WSL, only the total in *Memory-Usage*. Check it before a local run, and close them if memory is nearly full.

## 6. The repository

Clone it over SSH, create the environment and check it:

```bash
git clone git@github.com:<owner>/tsmerge.git
cd tsmerge
uv sync
uv run --locked pytest
uv run python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
scripts/run_local.sh hello python -m tsmerge.hello
```

- The `torch` line prints `True` when PyTorch sees the GPU.
- The last line is a complete recorded run: it should end with `completed (exit code 0)`, and its folder appears in `outputs/runs/hello/` ([running.md](running.md#running-locally)).

- Turn on the repository's git hooks, which run the checks on every commit ([CONTRIBUTING.md](../../CONTRIBUTING.md#git-hooks-the-checks-run-by-themselves)):

  ```bash
  git config core.hooksPath .githooks
  ```

- An existing clone made over HTTPS can switch to SSH: `git remote set-url origin git@github.com:<owner>/tsmerge.git`.
- **WSL2:** clone into the WSL filesystem (e.g. under `~`), **not** under `/mnt/c` or `/mnt/d`: the Windows drives are much slower for git, uv and rsync. To edit in VS Code on Windows, install the *WSL* extension and run `code .` from the repo in a WSL shell.
- **VS Code:** set it up as in [step 9](#9-vs-code).

## 7. The cluster (once per account)

Prepares your account on the Unimore cluster ([cluster.md](cluster.md)) to run this project's jobs. It needs the SSH setup of [step 3](#3-ssh-github-and-the-cluster) and the repository of [step 6](#6-the-repository).

1. **Personal values:** copy `.env.example` to `.env` (git-ignored) and fill it in: your SSH keys, the Slurm account (`susage` on the cluster lists yours), and your home and work folders on the cluster.
2. **Open the session:** `scripts/start-session.sh`.
3. **Install uv on the cluster**, once per account (a few seconds, on the login node; same installer as on your machine, [step 4](#4-python-with-uv)):

   ```bash
   ssh ailb 'curl -LsSf https://astral.sh/uv/install.sh | sh'
   ```

4. **Prepare the cluster:**

   ```bash
   scripts/cluster/setup_remote.sh
   ```

   It:

   - creates the project's folders in your cluster home and work areas, including the `data/` folder for datasets;
   - sets the cluster's uv to the same version as yours, so both read `uv.lock` the same way;
   - copies the code and builds the Python environment from `uv.lock`, as a Slurm step on the free `all_serial` partition, not directly on the shared login node (a few minutes, about 2.5 GB of downloads when packages change; no GPU);
   - refuses a `uv.lock` that doesn't match `pyproject.toml`, and while it builds, jobs refuse to start ([PD-008](decisions/PD-008-environment-integrity.md));
   - downloads into a temporary cache on the login node's local disk, deleted at the end, so no cache files pile up in your cluster home ([PD-005](decisions/PD-005-uv-cache-on-the-cluster.md)).

   Rerun it whenever `uv.lock` or your uv version changes: jobs refuse to run against an outdated environment.
5. **Check:** submit the smoke test, as in [running.md](running.md#the-cycle):

   ```bash
   scripts/cluster/submit.sh hello python -m tsmerge.hello
   ```

What each script does: [scripts/cluster/README.md](../../scripts/cluster/README.md).

## 8. Diagrams (optional)

Only needed to change or add the diagrams in [docs/project/diagrams/](diagrams/README.md): reading the docs and committing other changes work without it. The diagrams are rendered by a pinned Docker image, `minlag/mermaid-cli` (about 1 GB), that bundles everything the renderer needs ([PD-028](decisions/PD-028-diagrams.md)).

| | Native Linux | WSL2 on Windows |
|---|---|---|
| **Install Docker** | Docker Engine, from Docker's apt repository ([official steps](https://docs.docker.com/engine/install/ubuntu/)) | Docker Desktop on **Windows** ([official steps](https://docs.docker.com/desktop/features/wsl/)); never Docker Engine inside the WSL distro as well, the two conflict |
| **Use it without sudo** | `sudo usermod -aG docker $USER`, then log out and back in | nothing to do |
| **Connect it** | nothing to do | Docker Desktop → *Settings* → *Resources* → *WSL integration*: turn on this distro, then *Apply & restart* |

- **The `docker` group grants root-level privileges** to its members (Docker's own warning): add only your own user.
- **WSL2:** Docker Desktop needs WSL 2.1.5 or newer, ideally the latest (`wsl --update` from Windows). Docker Desktop must be running whenever you render.

Check it, and download the image once:

```bash
docker run --rm hello-world
scripts/render_diagrams.sh --all
```

The first render downloads the image; later renders take a few seconds per diagram.

## 9. VS Code

The repository's editor settings, tasks and debug configurations are in `.vscode/` ([PD-031](decisions/PD-031-vs-code.md)). They make the editor check code exactly as `scripts/check.sh` and the git hooks do.

### Install the extensions

Open the repository (on WSL2: from a WSL shell, `code .`), open the Extensions view, and type `@recommended`.

| Extension | What it's for | Needed |
|---|---|---|
| **Python** (`ms-python.python`) and **Pylance** (installed with it) | the interpreter, tests, code navigation | yes |
| **Python Debugger** (`ms-python.debugpy`) | the debug configurations | yes |
| **Ruff** (`charliermarsh.ruff`) | formatting and lint warnings, as in the checks | yes |
| **ShellCheck** (`timonwong.shellcheck`) | shell-script warnings as you type | when editing `scripts/` |
| **Markdown Mermaid** (`bierner.markdown-mermaid`) | diagrams in the Markdown preview | when editing diagrams |
| **WSL** (`ms-vscode-remote.remote-wsl`) | opens the repository inside WSL | on WSL2 |
| **Remote - SSH** (`ms-vscode-remote.remote-ssh`) | debugging on the cluster ([running.md](running.md#interactive-work-and-debugging-on-the-cluster)) | when needed |

- **WSL2:** extensions must be installed *in WSL*, not only on Windows: click *Install in WSL: <distro>*. Extensions installed only on Windows don't see the repository, and VS Code underlines settings it doesn't know (e.g. `"type": "debugpy"`).
- **Black** (`ms-python.black-formatter`) isn't needed and is marked unwanted: Ruff is the formatter here. If you have it for other projects, it stays inactive in this repository.

### What is already configured

Nothing to set by hand: `.vscode/settings.json` holds it.

| Setting | Effect |
|---|---|
| Interpreter: `.venv/bin/python` | everything uses the project's environment (`uv sync` first) |
| Ruff from `.venv` (`ruff.importStrategy`) | the same Ruff version as the checks, pinned by `uv.lock`, not the extension's bundled copy |
| `pyproject.toml` wins (`ruff.configurationPreference`) | personal editor settings can't change the project's rules |
| Format and sort imports on save | files are already clean when the pre-commit hook checks them |
| ShellCheck: `/usr/bin/shellcheck` | the same ShellCheck as the checks ([step 1](#1-base-tools)), with the same options from `.shellcheckrc` |
| pytest in the Testing view, LF line endings | as on the command line, and as in `.gitattributes` |

### Check it

1. **Interpreter:** the status bar (bottom right) shows Python 3.12.16 from `.venv`. If not: *Python: Select Interpreter* → `.venv/bin/python`.
2. **Ruff:** *View* → *Output* → *Ruff*: the log names the `ruff` inside `.venv`.
3. **Formatting:** add extra spaces to a line in a `.py` file and save: they disappear.
4. **Tasks and debugging:** *Terminal* → *Run Task…* → *Run locally (recorded run)*, and *Run and Debug* → *Debug a module*, both with the default `tsmerge.hello` ([running.md](running.md#from-vs-code)).

## Native Linux or WSL2

| | Native Linux | WSL2 on Windows |
|---|---|---|
| Shell | any | a WSL shell, never PowerShell |
| Where to clone | anywhere | the WSL filesystem, not `/mnt/c` or `/mnt/d` |
| NVIDIA driver | Linux driver | Windows driver only |
| SSH keys and config | `~/.ssh/` | WSL's `~/.ssh/`; keys copied from Windows, not used from `/mnt/c` |
| Editor | any (VS Code: [step 9](#9-vs-code)) | VS Code with the WSL extension, other extensions installed in WSL |
| Docker (diagrams only) | Docker Engine | Docker Desktop on Windows, with WSL integration |

## Troubleshooting

- **`Permission denied (publickey)` from GitHub:** check which key ssh offers and whether GitHub accepts it: `ssh -v -T git@github.com 2>&1 | grep -E "Offering|accepts"`. If it is accepted but still fails, the key has a passphrase and no prompt was possible (scripts, `BatchMode`): load it with `keychain`.
- **`Permission denied (password)` from the cluster:** the key was accepted but the cluster also wants a password; open the connection by hand first ([running.md](running.md#start-each-session)).
- **`do-release-upgrade` hangs** (the log shows it stuck on `snap list`): systemd isn't enabled in WSL2; see the WSL2 notes at the top.
- **`UNPROTECTED PRIVATE KEY FILE`:** the key's permissions are too open; `chmod 600` it. On WSL2, this is what happens with keys used directly from `/mnt/c`.
- **`ssh ailb` is slow every time:** the `Control*` lines aren't used; check that you edited the right `~/.ssh/config` (WSL's, on Windows).
- **`ssh ailb` asks for a password every time:** the key isn't registered on the cluster, or `IdentityFile` points to the wrong file.
- **`torch.cuda.is_available()` is `False` but `nvidia-smi` works:** the driver is probably older than the CUDA version of the PyTorch build. Update the driver; don't change the PyTorch build without a decision.
- **`nvidia-smi` not found in WSL:** update the Windows NVIDIA driver and WSL (`wsl --update` in PowerShell), then restart WSL (`wsl --shutdown`).
- **`uv: command not found`:** open a new shell, or run `source ~/.local/bin/env`.
- **`render_diagrams.sh` says Docker isn't available:** on WSL2, start Docker Desktop and check that this distro is turned on under *Resources* → *WSL integration*; on native Linux, check `systemctl status docker` and that you are in the `docker` group (`groups`).
