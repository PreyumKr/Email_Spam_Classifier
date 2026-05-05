# Email Spam Classifier

Simple Streamlit app wrapping a saved Naive Bayes spam classifier.

## Prerequisites

- Docker installed and running
- (Optional) A GHCR account and a Personal Access Token (PAT) for pushing images

## Build (local)

Build the image from the repository root and tag it `latest`:

```bash
docker build -t ghcr.io/preyumkr/email-spam-classifier:latest .
```

You may add an additional semver tag:

```bash
docker tag ghcr.io/preyumkr/email-spam-classifier:latest ghcr.io/preyumkr/email-spam-classifier:1.0
```

## Push to GitHub Container Registry (GHCR)

Login (use PAT as password):

```bash
docker login ghcr.io -u preyumkr
```

Push the `latest` tag:

```bash
docker push ghcr.io/preyumkr/email-spam-classifier:latest
```

## Run the container (detached)

- Default (host port 8501 -> container port 8501):

```bash
docker run -d --name email-spam -p 8501:8501 ghcr.io/preyumkr/email-spam-classifier:latest
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

```yaml
services:
	app:
		image: ghcr.io/preyumkr/email-spam-classifier:latest
		container_name: email-spam
		ports:
			- "8501:8501"
		restart: unless-stopped
```

Start detached:

```bash
docker compose up -d
```

## Troubleshooting

- If `docker run` fails with a `COPY` file not found error during build, make sure a `models/` directory exists in the build context and is not listed in `.dockerignore`.
- If the container exits immediately, inspect logs: `docker logs <container>`.
- If Streamlit is not reachable from host, ensure you published the correct host port and that the container app binds to `0.0.0.0` (the Dockerfile uses that flag by default).

---

If you want, I can add a small `run.sh` helper or a `docker-compose.yml` to the repo—which would you prefer?

