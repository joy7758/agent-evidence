# Template Finalization Plan

## Current Template Source Status

Version 1.17 retrieved official SoftwareX Original software publication template
source files:

- `softwarex-osp-template.docx`
- `softwarex-osp-template.tex`

They are stored under:

`papers/opentelemetry-to-eeoap/softwarex_template_file_conversion_v1_17/TEMPLATE_SOURCE/`

## Current Markdown Template Draft Status

Version 1.17 created:

`MANUSCRIPT/softwarex_template_file_draft_v1_17.md`

It is under the 3000-word target and organized by SoftwareX template-like fields.

## Current LaTeX Draft Status

Version 1.17 created:

`MANUSCRIPT/softwarex_template_file_draft_v1_17.tex`

LaTeX compilation was not attempted.

## DOCX Binary Submission Draft Status

A binary DOCX manuscript draft was not created. The official DOCX template was
stored as a source reference only.

## Requirements for Final DOCX Route

- Confirm reliable DOCX tooling.
- Populate author, affiliation, support email, metadata table, references, and
  declarations.
- Verify layout manually or through rendered inspection.
- Confirm no fabricated DOI/release URL.
- Use final public artifact availability wording.

## Requirements for Final LaTeX Route

- Confirm LaTeX dependencies.
- Populate final metadata and references.
- Compile to PDF.
- Check warnings, missing references, and formatting.
- Confirm word count against current SoftwareX guide.
- Preserve official template structure.

## Recommended Route

Primary route: LaTeX.

Reason: LaTeX is version-control friendly, reviewable in diffs, and easier to
audit in a repository workflow. DOCX can remain a secondary route if SoftwareX
submission workflow or author preference requires it.

## Required Checks Before Final Template File

1. Author/support metadata collected.
2. Release metadata strategy resolved.
3. Public release/DOI/tag decisions completed if required for submission.
4. Final references updated.
5. Declarations finalized.
6. LaTeX compile or DOCX render check passes.
7. Final scoped pytest and validator checks pass.
8. Final support package checksum and clean-clone verification pass.
