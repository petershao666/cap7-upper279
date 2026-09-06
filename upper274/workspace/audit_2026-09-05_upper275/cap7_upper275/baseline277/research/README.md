# Optional discovery code

None of these programs is required to verify the proof. They use numerical optimization to propose inequalities and perform integer recovery checks; only the complete verifiers establish the released certificate on the full matrix family.

The executed discovery used Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, and Numba 0.65.1. These are recorded in `requirements.txt`. The solver is SciPy's bundled HiGHS interface. Different solver releases can return different valid coefficients or fail to recover the same candidate.

From the release directory:

```bash
python3 -m pip install -r research/requirements.txt
python3 research/prepare_outputs.py
python3 research/discover_near112.py
python3 research/extremal.py
python3 research/nested108.py
```

The first command after installation seeds `research/outputs/new_certificate.json` with the two recorded ordinary exclusion stages. It never overwrites an existing output file. The subsequent programs regenerate candidates for the near-112 lemma, extremal cases, and the final nested-histogram branch. Newly generated files go under `outputs/`, not into the verified release's `certificate.json`.

To discover the ordinary stages from scratch, start with an empty `research/outputs/` directory, omit `prepare_outputs.py`, and run `python3 research/search_stage.py ordinary` twice. Each invocation freezes its previous stages and writes a new stage. The released stages contain 60 and 2 certificates. An invocation with `branches` also tries completion-status splits and preserves partial branch proposals. A returned `None` is a discovery failure, **not** an exact feasibility certificate or proof of existence.

`probe.py` compares sorted-only and labelled completed-column models. Example:

```bash
python3 research/probe.py 106 106 66
```

`nested108.py` jointly searches for a function on thirty noncompletion types, inner six-dimensional inequalities bounding its global histogram sum, and an outer seven-dimensional inequality. It reconstructs integer coefficients and checks positive gaps on its discovery arrays. The release's exact verifiers use the full canonical matrix family, not this discovery representation.

The discovery code reduces beta by cyclic rotations and may retain only endpoints of the labelled-deletion values, which suffice for its affine objectives. These speedups are **not trusted by the proof**: the full Python and C++ verifiers enumerate all ordered beta/gamma columns and check every compatible original-40-section label.

`recorded/` preserves the actual discovery output and logs. The recorded `extremal_certificate.json` intentionally lacks the final 00 branch, because it was found separately by `nested108.py`. The released root `certificate.json` merges these results, supplies that branch, and adds a constant 100,000 to the recorded histogram function to make it nonnegative. With a shift s, inner K changes by −3s, the histogram bound by +364s, outer K by +2s, and its summed bound by +728s. All contradiction gaps are unchanged. The complete verifiers check the shifted data directly.

This code does not guarantee further improvements, and its outputs are not automatically promoted into the proof. The exact mathematical scope, frozen stage dependencies, signed coefficients, and exhaustive case coverage must remain checked for any subsequent release.
