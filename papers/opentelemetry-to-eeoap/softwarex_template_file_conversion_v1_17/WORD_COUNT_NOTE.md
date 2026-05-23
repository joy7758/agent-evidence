# Word Count Note

## Target File

`MANUSCRIPT/softwarex_template_file_draft_v1_17.md`

## Word Count

- Total words: 2155
- Approximate body words excluding title, author information, software metadata
  table, and references: 1741
- Version 1.14 total words: 2176
- Version 1.14 approximate body words: 1537
- Within SoftwareX 3000-word target: yes

## Counting Method

The count used a regular-expression tokenization command:

```bash
python - <<'PY'
from pathlib import Path
import re
path = Path("papers/opentelemetry-to-eeoap/softwarex_template_file_conversion_v1_17/MANUSCRIPT/softwarex_template_file_draft_v1_17.md")
text = path.read_text(encoding="utf-8")
words = re.findall(r"\b[\w'-]+\b", text)
print(len(words))
PY
```

The body estimate removed the title, author information, software metadata
table, and references sections from the Markdown draft. This is an approximate
count for planning only; final submission should be checked against the current
SoftwareX author guide and template instructions.

## Note on Template Discrepancy

The SoftwareX Guide for Authors page checked in version 1.17 states a 3000-word
limit. The retrieved official LaTeX template source contains older wording that
mentions 4000 words. This draft is below both values, but the discrepancy must
be rechecked before formal submission.
