# Agent config

Reusable Codex instructions and agent skills. The installer keeps this
repository as the source of truth and links its files into the locations read by
agents.

## Install from GitHub

```bash
curl -fsSL https://raw.githubusercontent.com/johnlombardo-dev/agent-config/main/install.sh | bash
```

This downloads a persistent copy to `~/.local/share/agent-config` before
creating the symlinks. Running the command again installs the latest `main`
archive and backs up the previous copy.

From an existing checkout, run:

```bash
./install.sh
```

## Installed links

- `AGENTS.md` → `~/.codex/AGENTS.md`
- Each `skills/<name>/` directory containing `SKILL.md` →
  `~/.agents/skills/<name>`

Edit the files in this repository, then rerun the installer after adding or
renaming a skill.

## Backups and cleanup

Existing files and skill directories are moved to:

```text
~/.local/state/agent-config/backups/<timestamp>/
```

Previous repository copies installed by the one-liner are moved to:

```text
~/.local/state/agent-config/checkouts/<timestamp>/repository/
```

The installer also moves broken links from `~/.agents/skills` into the backup
directory when they point into this repository's `skills` directory. It leaves
unrelated broken links alone.

## Add a skill

```text
skills/
└── skill-name/
    ├── SKILL.md
    └── optional supporting files
```

Then run `./install.sh` again.
