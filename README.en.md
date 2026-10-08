# AstrBot Himeko Public Configuration Guide

[中文](README.md) | English

This is a **sanitized configuration-guide repository intended for public release** for the [Himeko Companion plugin](https://github.com/fushuyiliu/astrbot_plugin_himeko); it is independently reviewed as a public-release candidate. It helps users prepare AstrBot, select a model, follow the plugin installation order, and review privacy boundaries.

It is not a production-configuration backup or a one-click deployment bundle. This repository contains—and must never contain—real owner IDs, model keys, platform tokens, server addresses, chat records, databases, logs, attachments, or backups.

## Relationship with the plugin repository

| Repository | Responsibility | Never contains |
| --- | --- | --- |
| This `astrbot_config_himeko` repository | General AstrBot setup steps, public templates, and compatibility notes | Real runtime configuration or credentials |
| [Plugin repository `astrbot_plugin_himeko`](https://github.com/fushuyiliu/astrbot_plugin_himeko) | Installable Himeko interaction, owner memory, reminder, and attachment plugin | Platform tokens, model keys, or real owner data |

The repositories do not use Git submodules, automatic synchronization, directory copying, or a shared runtime directory. They coordinate only through installation instructions and version compatibility.

## Installation order

1. Install AstrBot using the [official AstrBot documentation](https://docs.astrbot.app/) and start it through WebUI.
2. Configure your message platform and model provider in AstrBot WebUI. Model choice, model keys, and platform credentials remain only in your own AstrBot environment.
3. Read [Compatibility](COMPATIBILITY.md) and confirm that the AstrBot version meets the plugin requirement.
4. Install `astrbot_plugin_himeko` from the plugin repository, then manually enter the owner ID and desired feature switches in the plugin's WebUI settings.
5. Complete a first-interaction and deletion test with fictional content before using real private-chat data.

## Using public templates

[`templates/astrbot_plugin_himeko.config.example.json`](templates/astrbot_plugin_himeko.config.example.json) shows only plugin configuration fields and safe defaults.

- Prefer AstrBot's plugin-configuration WebUI. Never commit your completed configuration file back to this repository.
- Keep `owner_id` blank until you enter the exact sender ID in your own AstrBot administration UI.
- Every sensitive capability starts disabled. Verify ordinary interaction first, then enable memory, reminders, and attachments one at a time if needed.
- Do not put a model key in an example file. AstrBot's AI configuration manages models.

## Privacy checklist

Before committing any change, confirm:

- No `cmd_config.json`, real `*_config.json`, `.env`, certificate, private key, token, or password is present.
- No IP/domain, owner ID, phone number, email address, chat record, attachment, log, SQLite database, or backup is present.
- Examples contain only blank strings, fictional values, or clear placeholders.
- Documentation does not promise unverified mobile, cloud, or performance outcomes.

Run:

```powershell
python tools/audit_public_config_repo.py . --history .
```

An automated scan is only an aid; manually review every file before publishing.

## Known boundaries

- This repository does not replace AstrBot's official documentation or modify AstrBot itself.
- It does not automatically install the plugin, start a service, upload configuration, or connect to any platform.
- Deleting this repository does not delete AstrBot configuration, model-provider records, or message-platform data on your machine. Handle each separately under its own documentation.

## Contribution and security

Read [CONTRIBUTING.md](CONTRIBUTING.md) before contributing. Follow [SECURITY.md](SECURITY.md) for security reports; never include secrets or private chat content in a public issue.

Original text and templates are available under the [MIT License](LICENSE). See [NOTICE.md](NOTICE.md) for the AstrBot, plugin-repository, and dependency boundaries.
