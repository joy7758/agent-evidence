# Word Count Note

## Method

Word count was computed with a simple Python regular-expression token count:

```bash
python - <<'PY'
from pathlib import Path
import re
path = Path("papers/opentelemetry-to-eeoap/softwarex_article_v1_11/softwarex_article_draft_v1_11.md")
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

- v1.11 total words: `2590`
- v1.11 approximate words excluding metadata table and references: `2190`
- v1.11 article body sections estimate: `2190`

## Comparison With v1.9

- v1.9 total words: `2939`
- v1.9 approximate body words: `2520`
- v1.11 total word change: `-349`
- v1.11 approximate body word change: `-330`

## Interpretation

The v1.11 draft remains within the SoftwareX 3000-word target. It is shorter
than v1.9 while adding clearer software-package framing, usage flow, and
release-blocker disclosure. This is still a draft-stage count, not an official
venue word count.
