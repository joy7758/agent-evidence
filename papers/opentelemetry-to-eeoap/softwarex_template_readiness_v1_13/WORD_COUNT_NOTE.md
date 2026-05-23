# Word Count Note

## Method

Word count will be computed with a simple Python regular-expression token count:

```bash
python - <<'PY'
from pathlib import Path
import re
path = Path("papers/opentelemetry-to-eeoap/softwarex_template_readiness_v1_13/softwarex_article_draft_v1_13_readiness.md")
text = path.read_text(encoding="utf-8")
words = re.findall(r"\b[\w'-]+\b", text)
print("total_words", len(words))
start = text.find("## Abstract")
end = text.find("## References")
body = text[start:end] if start != -1 and end != -1 else text
print("approx_body_excluding_metadata_and_references", len(re.findall(r"\b[\w'-]+\b", body)))
PY
```

## Result

- version 1.13 total words: `2258`
- version 1.13 approximate body words excluding metadata table and references:
  `1835`

## Comparison With Version 1.11

- version 1.11 total words: `2590`
- version 1.11 approximate body words: `2190`
- version 1.13 total word change: `-332`
- version 1.13 approximate body word change: `-355`

## Interpretation

The version 1.13 readiness draft remains within the SoftwareX 3000-word target.
It is shorter than version 1.11 while adding clearer release-readiness,
metadata, artifact availability, source-layout, and frozen-package wording.
