# Changelog

## [1.0.0] - 2026-07-31

### Added
- Initial release
- `speckit.switch.list` — list all specs with branch and active status
- `speckit.switch.set` — switch to spec via git checkout + auto-unlock lifecycle
- Avoids `feature.json` conflicts by doing `git checkout` first
- `--local-only` flag for branchless specs
