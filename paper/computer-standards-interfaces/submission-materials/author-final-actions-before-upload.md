# Author Final Actions Before Upload

- Enter private phone in the submission system only.
- Enter full postal address privately.
- Prepare passport-type photo outside Git if required.
- Confirm no simultaneous submission.
- Confirm funding statement.
- Confirm competing interests statement.
- Confirm ethics statement.
- Confirm Generative AI and AI-assisted technologies disclosure.
- Confirm final reference order.
- Recheck all DOI values, URLs, and access dates.
- Confirm local-only artifact wording.
- Run `make paper-demo`.
- Run targeted EEOAP tests:
  `python -m pytest tests/test_paper_case.py tests/test_operation_accountability_profile.py`
- Do not run or claim full repository pytest unless it actually passes.
- Do not move `eeoap-v0.1-paper`.
- Do not claim public GitHub Release or Zenodo DOI unless they actually exist.
- Do not include phone number, full postal address, birth date, sex/gender,
  health information, patient information, or passport-type photograph in Git.
