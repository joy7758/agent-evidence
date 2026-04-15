# External-Context Specimen

This directory contains one supplementary external-context specimen for the B1 line.

It belongs to the paper-facing evidence surface, not the canonical package surface.

It is not counted in B1 minimal-frozen `1 valid / 3 invalid / 1 demo`.

Its purpose is narrow: test whether the current profile and validator path still hold outside the current minimal example family while staying within one low-complexity operation accountability statement.

Current files:

- Specimen: `data_space_metadata_update.valid.json`
- Validator output: `data_space_metadata_update.validation-report.json`

Scenario note:

- one data-space / FDO catalog metadata correction
- one operation
- one accountability statement
- no workflow expansion

Validator path used for this specimen:

```bash
python3 - <<'PY' > paper/flagship/external_context/data_space_metadata_update.validation-report.json
from pathlib import Path
from agent_evidence.oap import validate_profile_file
import json

report = validate_profile_file(
    Path("paper/flagship/external_context/data_space_metadata_update.valid.json")
)
print(json.dumps(report, indent=2, sort_keys=True))
PY
```

This specimen is supplementary evidence only. It is intended for offline review and paper-facing comparison, not for changing the canonical B1 counts.
