# Word Count Note

## Method

Word count was computed with a simple Python regular-expression token count:

```bash
python - <<'PY'
from pathlib import Path
import re
path = Path("papers/opentelemetry-to-eeoap/softwarex_article_v1_9/softwarex_article_draft_v1_9.md")
text = path.read_text(encoding="utf-8")
words = re.findall(r"\b[\w'-]+\b", text)
print("total_words", len(words))
start = text.find("## Abstract")
end = text.find("## References")
body = text[start:end] if start != -1 and end != -1 else text
body_words = re.findall(r"\b[\w'-]+\b", body)
print("approx_excluding_metadata_and_references", len(body_words))
PY
```

## Result

- Total words: `2939`
- Approximate words excluding metadata table and references:
  `2520`
- Article body sections estimate: `2520`

## Interpretation

The v1.9 draft appears within the SoftwareX 3000-word target when excluding the
metadata table and references. The estimate is conservative but not an official
venue word count. A v1.10 self-review should still check section balance,
remove unnecessary repetition, and preserve the narrow claim boundary.
