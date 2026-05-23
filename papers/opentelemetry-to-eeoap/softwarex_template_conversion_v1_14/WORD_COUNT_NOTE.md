# Word Count Note

## Method

Word count will be computed with a Python regular-expression token count:

```bash
python - <<'PY'
from pathlib import Path
import re
path = Path("papers/opentelemetry-to-eeoap/softwarex_template_conversion_v1_14/softwarex_template_style_draft_v1_14.md")
text = path.read_text(encoding="utf-8")
words = re.findall(r"\b[\w'-]+\b", text)
print("total_words", len(words))
start = text.find("# Abstract")
end = text.find("# References")
body = text[start:end] if start != -1 and end != -1 else text
metadata_start = text.find("# Software metadata table")
metadata_end = text.find("# Highlights")
metadata = text[metadata_start:metadata_end] if metadata_start != -1 and metadata_end != -1 else ""
body_words = len(re.findall(r"\b[\w'-]+\b", body))
metadata_words = len(re.findall(r"\b[\w'-]+\b", metadata))
print("approx_body_excluding_title_authors_metadata_and_references", max(body_words - metadata_words, 0))
PY
```

## Result

- version 1.14 total words: `2176`
- version 1.14 approximate body words excluding title, authors, metadata table,
  and references: `1537`

## Comparison With Version 1.13

- version 1.13 total words: `2258`
- version 1.13 approximate body words: `1835`
- version 1.14 total word change: `-82`
- version 1.14 approximate body word change: `-298`

## Interpretation

The version 1.14 template-style draft remains within the SoftwareX 3000-word
body target. It is shorter than version 1.13 because author and metadata fields
were separated from the main body and the draft was mapped into SoftwareX-style
sections.
