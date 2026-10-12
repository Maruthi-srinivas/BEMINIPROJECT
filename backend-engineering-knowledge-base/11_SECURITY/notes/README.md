# D12 note paths

Canonical note files match `inventory.json` `note_path` values: `d12-tNNN-<slug>.md` (for example `d12-t001-authentication-vs-authorization.md`).

If duplicate copies exist as `d12-<slug>.md` without the topic id prefix, delete the duplicates and keep only the `d12-tNNN-*` files.

Regenerate all D12 artifacts:

```powershell
python ..\..\_generators\generate_d12_security.py
```

Or from repo root:

```powershell
.\materialize_d12.ps1
```
