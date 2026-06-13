# Mac + WSL GPU workflow

## Roles

- Mac: writing, VS Code, GitHub, literature, Codex planning, small tests.
- WSL GPU: training, large analysis, MLflow, DVC cache, large data.

## SSH from Mac to WSL GPU

Use the Mac SSH config:

```sshconfig
Host wslgpu
  HostName <GPU_MACHINE_IP_OR_TAILSCALE_NAME>
  User <YOUR_WSL_USERNAME>
  Port 22
  IdentityFile ~/.ssh/id_ed25519
  ServerAliveInterval 60
  ServerAliveCountMax 5
```

Then connect:

```bash
ssh wslgpu
```

## Push/pull code

Use GitHub as the source of truth:

```bash
# Mac
cd ~/projects/bioinfo-scientist-paper
git push

# WSL GPU
cd ~/projects/bioinfo-scientist-paper
git pull
```

## Sync large artifacts when needed

```bash
rsync -avP wslgpu:~/projects/bioinfo-scientist-paper/results/ ./results/
```

Prefer MLflow/DVC for systematic tracking.
