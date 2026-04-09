# ACM/acmart Mapping Plan

## Front Matter

- Title:
  `paper/tosem_en/00_title_abstract_keywords.md`
- Abstract:
  `paper/tosem_en/00_title_abstract_keywords.md`
- CCS concepts placeholder:
  not drafted yet; add during template conversion
- Keywords:
  `paper/tosem_en/00_title_abstract_keywords.md`

## Body Structure Mapping

- Introduction:
  `paper/tosem_en/01_introduction.md`
- Contributions and scope boundary:
  currently a standalone markdown section in `paper/tosem_en/02_contributions_and_scope.md`
  likely destination:
  merge into the end of the Introduction section or keep as a short early section depending on template fit
- Method:
  `paper/tosem_en/04_methods_profile_and_validator.md`
- Evaluation:
  `paper/tosem_en/05_evaluation.md`
- Related Work:
  `paper/tosem_en/06_related_work.md`
- Discussion / Threats:
  `paper/tosem_en/07_discussion_limits_threats.md`
- Conclusion:
  `paper/tosem_en/08_conclusion.md`

## Artifact Availability / Data Availability Note

- Current source:
  `submission/artifact-availability.md`
- Likely placement:
  dedicated unnumbered note near the end matter, footnote-style artifact statement, or appendix-side availability note depending on venue-specific template expectations

## Merge / Split Notes

- `02_contributions_and_scope.md` will likely need partial merging into the Introduction to avoid an overly short standalone journal section
- `04_methods_profile_and_validator.md` already contains method subsections and can likely map directly into one major numbered section
- `05_evaluation.md` likely maps directly into one major numbered section, with table insertions retained
- `07_discussion_limits_threats.md` may remain one combined section, or its threat-validity subsections may be visually nested under a broader discussion section in the final LaTeX structure
- Figure insertion markers and table insertion markers in markdown will need conversion into acmart figure/table environments during the LaTeX phase

## Packaging Note

This mapping is intentionally structural. It does not generate LaTeX, author metadata, bibliography blocks, or ACM-specific macros yet. Its purpose is to reduce ambiguity before template conversion starts.
