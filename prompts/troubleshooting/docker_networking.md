# Troubleshooting: Docker Networking

When the bot runs inside Docker and the BB API runs on the host (or another machine), the container must reach the host network.

## host.docker.internal

**Windows and macOS:** Docker Desktop provides `host.docker.internal` as a hostname for the host machine.

Set:
```bash
BB_API_BASE_URL=http://host.docker.internal:8001
```
Replace `8001` with the port where the API listens.

## Linux: extra_hosts

On Linux, `host.docker.internal` is not available by default. Add it via `extra_hosts` in `docker-compose.yml`:

```yaml
services:
  bot:
    image: ...
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      - BB_API_BASE_URL=http://host.docker.internal:8001
```

`host-gateway` resolves to the host’s gateway IP from inside the container.

## Reachability Checks

From inside the running container, verify the API is reachable:

```bash
# Enter the container
docker exec -it <container_name> sh

# Test connectivity (adjust URL and port)
curl -v http://host.docker.internal:8001/api/bot/events
# Expect 401 (no auth) or 405 (wrong method) — both mean the host is reachable
# Connection refused or timeout means networking is broken
```

If `curl` is not installed, use `wget` or a simple Python script with `httpx`.
