# Reproducibility Summary for Reviewers

The scoped reproduction command is:

```bash
make paper-demo
```

Expected visible output:

```text
PASS valid evidence bundle
FAIL tampered output hash mismatch
```

Expected failure code:

```text
references_digest_mismatch
```

Targeted tests:

```text
tests/test_paper_case.py
tests/test_operation_accountability_profile.py
```

Expected targeted-test result from the current verified state:

```text
19 passed, 1 warning
```

Full repository pytest success is not claimed.

The paper_case artifact does not perform dependency installation. It is scoped
to local review of the EEOAP paper case, validator path, valid PASS, tampered
FAIL, references_digest_mismatch, and targeted EEOAP tests.
