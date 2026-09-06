# Independent fourteen-case NC106 domain audit

PASS for the complete old and newly pruned necessary domains. The precise grid predicate, twelve affine lines, three transverse whole-cap profiles, fourteen-anchor moment cover and eighteen-element coordinate group are proved in DOMAIN_DEFINITION.md. The independently generated primary data and input hashes are in INPUTS.json. No discovery kernel or generated cache was imported or executed.

The ordered5D profile predicate has8,011 allowed triples before the new complete41 zeros and7,954 after them. The fourteen absent types act only on the twelve5D lines. They are not applied to an outer6D line on account of its numerical sum. NC106 completion predicates and first-anchor prefixes apply to the three whole-cap transverse directions, with their proper scope. All14 first-anchor cases remain nonempty.

| Case | Anchor | Full ordered old | Full ordered new | Discovery cover old | Discovery cover new | True orbits old | True orbits new |
|---:|---|---:|---:|---:|---:|---:|---:|
|0|(41,41,24)|375138|364383|25747|25038|20951|20348|
|1|(42,41,23)|210663|208332|16010|15831|11773|11642|
|2|(42,42,22)|121368|121332|9959|9957|6812|6810|
|3|(43,40,23)|87048|86814|8038|8012|4896|4883|
|4|(43,41,22)|84375|83682|7690|7613|4742|4702|
|5|(43,42,21)|49803|49803|4908|4908|2808|2808|
|6|(43,43,20)|22077|22077|2011|2011|1258|1258|
|7|(44,40,22)|45693|45567|4196|4182|2566|2559|
|8|(44,41,21)|44640|44289|4036|3997|2507|2487|
|9|(44,42,20)|26379|26379|2568|2568|1483|1483|
|10|(44,43,19)|11709|11709|1056|1056|666|666|
|11|(45,40,21)|16350|16302|3580|3564|958|950|
|12|(45,41,20)|16038|15921|3376|3337|919|912|
|13|(45,42,19)|9504|9504|2168|2168|569|569|

Totals are1,120,785 old raw grids and1,106,094 new raw grids; the respective discovery covers have95,343 and94,242 rows. The cover is not a unique orbit selector. Each orbit's actual stabilizer and the number of discovery-cover representatives were checked by forming its complete group of coordinate images. Every observed raw multiplicity equals its orbit size, and every observed cover multiplicity equals the number of images satisfying the declared cover rule. No swaps between physical columns, including the equal41 columns, were used.

The files caseNN_MODE_raw.u8 contain the full lexicographically ordered grids as9 unsigned bytes, in physical-column order a0,a1,a2,b0,b1,b2,c0,c1,c2. The cover.u8 files apply the discovery normalization. The canonical.u8 files contain the lexicographically maximal representative of each true coordinate orbit in lexicographic order. The orbit_ledger.tsv files give every representative and its raw orbit size, discovery-cover multiplicity and retention by new pruning. The features.i32le files contain19 signed32-bit little-endian integers per cover row, preserving duplicates and the ordered transverse IDs. Separately exported unique_features files are not used as the discovery domain. All data-file SHA256 values are in the pre-comparison FROZEN.json.

The complete independent run took0.557seconds and10.2MB peak resident memory. The initial unsupported macOS address-limit call stopped before reading inputs or enumerating; RUNTIME_NOTE.md records the replacement resource guard. Both computations are well within the registered180-second and1GiB budget. No alternative mathematical scheme or solver was started.

The own outputs were frozen with FROZEN.json SHA25619b3e4c9e574e97eded83a851ffd61d6c66fb83f1b5d1076ca5e171cf85cb860 before reading the new H/L outputs. The subsequent independent comparison checked every one of H's94,242 complete19-integer rows in its original order, including repeats and transverse IDs, and every old/new case count. H export SHA2566d910ef137860b100706e8f7d2d86815cabf3c88b9f7f96623609a8bd1876b25. It also matched all fourteen L old-domain counts and the separately disclosed identical old predicate/cover definitions. L did not supply a full row-byte export, so no such L byte comparison is claimed. The complete independently generated old raw domain is retained for exact coefficient replay instead. Details and hashes are in INDEPENDENT_COMPARISON.json.

This audit verifies a finite necessary integer-grid domain and source-correct pruning. It does not assert that a retained grid is geometrically realizable, that any NC106 cap exists, or that any7D branch is excluded. A separate gate governs the L integer candidate. Shared dependencies are the accepted classification/support tables and ordinary/completion results; the new grid, group, feature and comparison implementations are independent of H/L and root code.
