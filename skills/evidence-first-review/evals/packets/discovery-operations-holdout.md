# Review packet

Review this container deployment change. Report only actionable defects.

```diff
  application default: PORT=8080
  Dockerfile: EXPOSE 8080
- compose service: "3000:3000"
+ compose service: "8080:3000"
  healthcheck: curl -f http://127.0.0.1:3000/health
  operator guide: open http://127.0.0.1:8080
```

The process listens on its configured container port. The host must expose it at `8080`, and the health check must probe the actual listener inside the container.
