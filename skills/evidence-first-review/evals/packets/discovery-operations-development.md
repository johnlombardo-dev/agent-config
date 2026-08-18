# Review packet

Review this Agent Mail port change. Report only actionable defects.

```diff
- daemon config literal: 6080
+ daemon config literal: 6110

- CLI default: http://127.0.0.1:6080
+ CLI default: http://127.0.0.1:6110

  OpenAPI server: http://127.0.0.1:6080
  launchd API port: 6080
  Tailscale Serve target: http://127.0.0.1:6080
  README quick start: 6080
  integration test server: 6110
```

The port registry reserves `6110` for the daemon and `6111` for integration tests. CLI, API schema, service plans, proxy setup, documentation, and tests must agree with that allocation without tests binding the production port.
