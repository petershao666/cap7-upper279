# Rechecking the frozen final proof

Run from `/Users/hengshao/Desktop/math`. Python 3 and a C++17 compiler supporting signed 128-bit integers are sufficient for the final raw checks. No optimizer, random seed, network access, or paid service is needed.

The fast exact global integration check is:

```sh
python3 research_2026-09-05-upper274-continuation-r2/root_audit/global274/verify.py
```

It verifies input hashes, exact root/profile/state arithmetic, inherited certificate gaps, and complete closure. It reads a frozen pre-274 registry copy, so later bookkeeping changes cannot invalidate its intended historical dependency binding. It does not pretend to rerun the inherited large finite domains.

For a fresh replay of the final three lower40 tiers and the outer domain, compile `root_audit/three40_complete42/verify.cpp` with `-O2 -std=c++17 -fsanitize=undefined`. Run the resulting executable with the immutable `root_audit/three40_complete42/input.txt` on standard input and direct new output to a fresh temporary directory. Require exit zero, empty standard error, and all 133 `CASE` lines identical to the frozen `verify.log`; the final elapsed time may differ. The expected totals are 7,701,024 raw rows and 2,570,134 normalized cover rows. The outer gap is 148,616,699,075.

For the independent NC106 replay, compile `root_potential/three40_complete42_nc106_verify/replay_raw.cpp` with C++17, without disabling assertions. Its two arguments are the immutable `root_potential/three40_complete42_nc106_verify/REPLAY_INPUT.txt` and the directory `root_potential/complete41_domain_audit`. Direct the new JSON output to the same fresh temporary directory. Require exit zero and all 14 case records identical to the frozen `RAW_VERIFICATION.json`; elapsed time and peak memory may differ. Expected raw total: 1,106,094.

Support data and transcription are checked by root's `three40_complete42/export.py` and P's `three40_complete42_nc106_verify/prepare_exact.py`; both are standard-library Python except that the latter imports only its own pure-data reader. Their immutable source/support outputs and inputs are hash-bound by the root finalizers. To rerun output-writing helpers, use a separate verification copy with the same relative layout; do not overwrite the historical frozen reports, whose hashes are part of the proof record.

The exact support families, Table 1 restrictions, first-anchor orders, coefficient vectors, physical-column assignments, upper-only signs, all case bounds, and attaining witnesses are explicit JSON. `PROOF.md` supplies the map from arbitrary caps to each complete finite domain and the final contradiction. A replay validates these certificates subject to the recorded published low-dimensional theorems; it does not independently re-prove those publications' classification searches.
