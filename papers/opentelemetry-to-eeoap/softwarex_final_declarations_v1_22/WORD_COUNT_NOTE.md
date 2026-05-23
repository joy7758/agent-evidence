# Word Count Note

## Target File

`papers/opentelemetry-to-eeoap/softwarex_final_declarations_v1_22/MANUSCRIPT/softwarex_final_declaration_draft_v1_22.md`

## Results

- Total words: 2129
- Approximate body words excluding title, author information, metadata table,
  and references: 1730
- Version 1.21 total words: 2114
- Version 1.21 approximate body words: 1715
- Within SoftwareX 3000-word target: yes

## Counting Method

Total words were counted with:

```bash
python - <<'PY'
from pathlib import Path
import re
path = Path("papers/opentelemetry-to-eeoap/softwarex_final_declarations_v1_22/MANUSCRIPT/softwarex_final_declaration_draft_v1_22.md")
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

Version 1.22 is slightly longer than version 1.21 because the conflict of
interest TODO was replaced with the final author-confirmed declaration.
