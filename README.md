# keel marketplace

The list of plugins [keel](https://github.com/MiladNalbandi/keel-v2) can install. It holds **no plugin code**, only pointers to each plugin's repo
and releases.

> **Status: early.** The entries are here; the signed index and keel's Plugins page come with keel 0.20
> ([the plan](https://github.com/MiladNalbandi/keel-v2/tree/main/docs/plugins/04-marketplace.md)).

## How it works

```
 plugin repo (a tag)            this repo                               keel
 ───────────────────            ─────────                               ────
 builds db-1.4.0.kplug   ──▶    sync: checks sha256, signature, lint
 signs it, releases it          adds the version to v1/index.json  ──▶  reads the index (signed),
                                signs the index (GitHub Pages)          shows the Plugins page,
                                                                        installs after you say yes
```

```
publishers/   who publishes: name, public keys, verified or not
plugins/      one file per plugin: id, publisher, repo, title, summary, category, tags
revoked.yml   versions that must never be installed
tools/        check.py: the checks a pull request must pass
```

## Add your plugin

1. Make your plugin from [keel-plugin-template](https://github.com/MiladNalbandi/keel-plugin-template).
2. Open a pull request here with `publishers/<you>.yml` (your **public** key) and `plugins/<id>.yml`.
3. The checks pass and a maintainer merges. Your plugin shows as **community**. After a review it can become
   **verified**.

Private keys and tokens never go into this repo. Release signing keys live in GitHub Actions secrets.

## License

MIT
