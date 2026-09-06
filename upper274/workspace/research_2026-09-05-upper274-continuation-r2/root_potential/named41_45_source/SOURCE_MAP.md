# Primary source map: canonical 45 and named 41A-E

Status: explicit primary vector sources located; literal five-coordinate point tables have not yet been decoded or accepted. This source-only task executes no external PostScript, Java, or macros and no cap-family search or LP.

The complete arXiv source archive was retrieved from `https://arxiv.org/src/2206.09719v1`. Its local copy is `arxiv_source.tar`, SHA256 `5f6aa7b3086bfde22d6942b2eccf74b99caa4a882c1c3c26a87bf0635c04540f`. Only the relevant TeX and EPS members were read/extracted. Archive member names were never used as the sole evidence of mathematical identity: the primary TeX explicitly binds each inclusion to its caption and definition.

Primary article: H. (M.) R. Thackeray, [The cap set problem: 41-cap 5-flats, arXiv:2206.09719v1](https://arxiv.org/html/2206.09719v1). The source TeX is `CapSetProblem5S41.tex`, 48,338 bytes. Exact per-file SHA256 values and absolute paths are recorded in `SOURCE_MAP.json`.

| Requested input | Exact archive member | Bytes | TeX identification | Filled four-cubic circle paths |
|---|---|---:|---|---:|
| Canonical 45-cap | Fig03EPS.eps | 63,152 | lines 198-199; Figure 3, label fign5s45m0 | 45 |
| 41A | Fig04EPS.eps | 60,343 | lines 206-207; Figure 4, label fign5s41A | 41 |
| 41B | Fig06EPS.eps | 60,480 | lines 220-221; Figure 6, label fign5s41B | 41 |
| 41C | Fig07EPS.eps | 60,614 | lines 226-227; Figure 7, label fign5s41C | 41 |
| 41D | Fig08EPS.eps | 60,405 | lines 232-233; Figure 8, label fign5s41D | 41 |
| 41E | Fig09EPS.eps | 60,204 | lines 238-239; Figure 9, label fign5s41E | 41 |

Theorem 4.3, TeX line 347, states affine uniqueness of the 45-cap with Figure 3 as representative. Lemma 3.1(e)-(f), especially lines 202 and 210, supplies the named A-E identities. Figure 2 is another 45-cap; the explicit affine transformation at line 194 maps it to Figure 3. Its `Fig02EPS.eps` source (61,940 bytes) is retained only as an optional independent geometric cross-check. Previously accepted Delta and F-I sources were not redecoded, and no exceptional-list completeness analysis was performed.

## Coordinate data format

These are explicit vector diagrams, not ASCII arrays of five field coordinates. They are Cairo 1.16.0 EPSF-3.0, `Clean7Bit`, with a planar bounding box `0 0 263 181`. Black point markers have the command shape `u v m`, then four cubic-Bezier `c` segments, then `f`; the same circle is subsequently stroked with `S`. Every requested file has exactly the expected number of four-cubic filled-circle paths, listed above. A parser must count the filled paths once and must not count their duplicate stroke as another point. Grid lines, arrows and letter outlines are separate path data.

The decimal EPS positions describe the planar rendering, not elements of F3. Literal five-coordinate decoding requires matching each marker to the figure's five-coordinate grid convention. The plot's outer section positions and its internal projected three-dimensional grids must be interpreted from the primary diagram; coordinates cannot safely be assigned merely by sorting all dots by screen position. Any resulting field coordinates should use residues 0,1,2, with displayed -1 mapped to 2. Coordinate order and any globally chosen affine relabelling must be stated explicitly.

## Finite extraction plan

1. Read only numeric path geometry and isolate the 45+5*41=250 filled point-marker paths. Compute their centers from opposite circle extrema, preserving original decimals as exact rationals and requiring the four cubic segments to form the expected symmetric marker. Execute no EPS program.
2. Independently inspect the labelled primary figures and grid strokes to establish a single unambiguous planar-grid-to-five-coordinate map for each diagram. Declare the coordinate order, each three-level ordering and the within-section projected basis. Record each original marker center next to its decoded coordinate. If any marker or grid interpretation is ambiguous, stop rather than choose a decoding because it happens to pass a cap test.
3. After that mapping is explicit, extract six finite point lists only. Verify 45 distinct points and 990 unordered pairs for Figure 3; verify 41 distinct points and 820 pairs for each A-E figure. Check the known 45-cap directional spectrum as a consistency check. This later extraction needs its own registered gate; it is not performed by the present source map.
4. Root independently checks the point coordinates against the primary figures using visual inspection or a separate path parser. Only after that acceptance may a separately authorized all-four-deletions family be enumerated. No 45-minus-four computation is included here.

This resolves source availability. The remaining issue is exact coordinate decoding, not missing primary files. No mathematical novelty, new cap record, or complete universal 41-cap spectrum is claimed.
