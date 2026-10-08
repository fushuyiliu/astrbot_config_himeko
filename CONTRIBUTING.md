# Contributing

- Submit only sanitized instructions and fictional or blank example values.
- Never submit an exported `cmd_config.json`, completed plugin configuration, key, token, platform identifier, chat record, attachment, log, database, or backup.
- Keep the repository independent from the plugin repository: no submodule, runtime copy, or automatic synchronization.
- Update [COMPATIBILITY.md](COMPATIBILITY.md) when an installation step, supported AstrBot range, or plugin schema changes.
- Run `python tools/audit_public_config_repo.py . --history .` and manually inspect the changed files before opening a pull request.

By contributing, you agree that your contribution may be distributed under the MIT License.
