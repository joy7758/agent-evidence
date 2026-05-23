# Template Source Note

## Official Guide Checked

- Guide URL:
  `https://www.sciencedirect.com/journal/softwarex/publish/guide-for-authors`
- Checked date: 2026-05-23
- Result: reachable through the web tool.

The guide states that SoftwareX submissions consist of a short descriptive paper
and an open-source software distribution with support material. It also states
that submissions are accepted only if they follow journal-specific templates,
with Word and LaTeX Original software publication templates linked from the
guide.

## Template Files Retrieved

Retrieved into this directory:

- `softwarex-osp-template.docx`
  - Source URL:
    `https://legacyfileshare.elsevier.com/promis_misc/softwarex-osp-template.docx`
  - Type: DOCX, Office Open XML Document
  - Role: official Original software publication template source
  - Modified: no
- `softwarex-osp-template.tex`
  - Source URL:
    `https://legacyfileshare.elsevier.com/promis_misc/softwarex-osp-template.tex`
  - Type: LaTeX source
  - Role: official Original software publication template source
  - Modified: no

The retrieved LaTeX template source contains upstream trailing whitespace. A
local `TEMPLATE_SOURCE/.gitattributes` entry disables whitespace checks for that
official source file so it can remain byte-for-byte unmodified in this support
directory.

## Important Note

The SoftwareX Guide for Authors page checked in this task states a 3000-word
limit for the short descriptive paper. The retrieved official LaTeX template
contains older template wording that mentions a 4000-word limit. Version 1.17
uses the current guide-page limit of 3000 words for the draft readiness
assessment and records this discrepancy as a formal-submission blocker to
recheck before submission.

## Conversion Status

This directory includes official template source files, a Markdown
template-compatible manuscript draft, and a conservative LaTeX draft. No binary
DOCX manuscript output was created.
