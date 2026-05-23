# Word Count Note

## Target File

`papers/opentelemetry-to-eeoap/softwarex_template_metadata_update_v1_21/MANUSCRIPT/softwarex_template_metadata_update_draft_v1_21.md`

## Results

- Total words: 2114
- Approximate body words excluding title, author information, metadata table,
  and references: 1715
- Version 1.17 total words: 2155
- Version 1.17 approximate body words: 1741
- Within SoftwareX 3000-word target: yes

## Counting Method

Total words were counted with:

```bash
python - <<'PY'
from pathlib import Path
import re
path = Path("papers/opentelemetry-to-eeoap/softwarex_template_metadata_update_v1_21/MANUSCRIPT/softwarex_template_metadata_update_draft_v1_21.md")
text = path.read_text(encoding="utf-8")
words = re.findall(r"\b[\w'-]+\b", text)
print(len(words))
PY
```

Approximate body words were estimated by counting from `# Highlights` through
the text before `# References`. This excludes title, author information,
SoftwareX metadata table, and references, while preserving abstract, main body,
declarations, limitations, and artifact availability text.

## Comparison

Version 1.21 is slightly shorter than version 1.17 because the metadata update
replaced some TODO explanatory wording with confirmed author metadata and a
shorter conflict-of-interest TODO.
