# Email Spam Classifier

Simple Streamlit app wrapping a saved Naive Bayes spam classifier.

## Prerequisites

- Docker installed and running
- (Optional) A GHCR account and a Personal Access Token (PAT) for pushing images

**Note on PyTorch:** Two requirement files are provided:
- `requirements.txt` — PyTorch CPU version (default)
- `requirements-gpu.txt` — PyTorch GPU version (CUDA 13.2)

## Build (local)

Build the image from the repository root. By default, it uses the CPU version:

```bash
docker build -t ghcr.io/preyumkr/email-spam-classifier:latest .
```

For GPU support (CUDA 13.2), use the `--build-arg` flag:

```bash
docker build --build-arg PYTORCH_VARIANT=gpu -t ghcr.io/preyumkr/email-spam-classifier:latest-gpu .
```

## Run the container (detached)

- Default (host port 8501 -> container port 8501):

```bash
docker run -d --name email-spam -p 8501:8501 ghcr.io/preyumkr/email-spam-classifier:latest
# then open http://localhost:8501
```

- Map any host port to the container's Streamlit port (container listens on 8501):

```bash
# host port 8080 mapped to container port 8501
docker run -d --name email-spam -p 8080:8501 ghcr.io/preyumkr/email-spam-classifier:latest
# then open http://localhost:8080
```

Notes:

- `-p <host_port>:<container_port>` — left is host, right is container.
- Use `-d` to run detached (background). Omit `-d` to run in foreground and see logs directly.

## Run GPU image with GPU access

**Prerequisites for GPU:**
- NVIDIA GPU available on host
- NVIDIA Container Runtime installed (for `--gpus` flag support)

**Setup NVIDIA Container Runtime** (one-time setup):

```bash
# On Ubuntu/Debian

# 1. Download and configure the new, secure GPG keyring
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

# 2. Add the official, stable production repository
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# 3. Update apt and install the official modern package
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# 4. Restart the Docker daemon to complete the installation
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# 5. Verify installation
docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi

# If you see the NVIDIA driver and GPU info, you're good to go!
```

**Run GPU container** (with GPU access):

```bash
# Using --gpus flag (recommended)
docker run -d --name email-spam-gpu -p 8501:8501 --gpus all \
  ghcr.io/preyumkr/email-spam-classifier:latest-gpu
# then open http://localhost:8501
```

Flags explained:
- `--gpus all` — Give container access to all GPUs. Use `--gpus '"device=0"'` for specific GPU.
- Use `--gpus '"device=0,2"'` for multiple specific GPUs.
- Other flags same as CPU version.

## Useful commands

```bash
docker ps                        # list running containers and port mappings
docker logs -f email-spam         # stream logs from the container
docker exec -it email-spam /bin/bash  # open shell in running container (or /bin/sh)
docker stop email-spam
docker rm email-spam
```

## docker-compose (optional)

Create a `docker-compose.yml` to run detached and restart automatically:

**CPU version:**

```yaml
services:
	app:
		image: ghcr.io/preyumkr/email-spam-classifier:latest
		container_name: email-spam
		ports:
			- "8501:8501"
		restart: unless-stopped
```

**GPU version** (requires NVIDIA Container Runtime):

```yaml
services:
	app:
		image: ghcr.io/preyumkr/email-spam-classifier:latest-gpu
		container_name: email-spam-gpu
		ports:
			- "8501:8501"
		restart: unless-stopped
		deploy:
			resources:
				reservations:
					devices:
						- driver: nvidia
						  count: all
						  capabilities: [gpu]
```

Start detached:

```bash
docker compose up -d
```

## Troubleshooting

- If `docker run` fails with a `COPY` file not found error during build, make sure a `models/` directory exists in the build context and is not listed in `.dockerignore`.
- If the container exits immediately, inspect logs: `docker logs <container>`.
- If Streamlit is not reachable from host, ensure you published the correct host port and that the container app binds to `0.0.0.0` (the Dockerfile uses that flag by default).
- **GPU container not using GPU**: 
  - Check NVIDIA Container Runtime is installed: `docker run --rm --gpus all nvidia/cuda:12.2.0-runtime-ubuntu22.04 nvidia-smi`
  - Verify container has GPU access: `docker exec <container> nvidia-smi`
  - Ensure you used `--gpus all` or `--gpus '"device=0"'` flag when running
- **GPU docker-compose not working**: Ensure Docker Compose v1.28.0+ is installed (older versions don't support GPU syntax)

---

If you want, I can add a small `run.sh` helper or a `docker-compose.yml` to the repo—which would you prefer?

