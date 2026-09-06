# Exact extraction of the published 45 and 41A-E inputs

The primary source identity and all figure-caption mappings are in `SOURCE_MAP.md` and `SOURCE_MAP.json`. Two subsequent finite extraction gates were explicitly approved by root and registered before their computations: `ORBIT45_GATE.md` and `EPS_AE_GATE.md`. The following results are replication/input verification of published representatives, not new constructions or a classification claim.

## Formula-defined 45-cap

The frozen primary TeX gives T and R at lines 356-357, in the Remark following Theorem 4.3. `extract_orbit45.py` evaluates those displayed affine formulas directly on residue tuples. It first checks that each map permutes all 243 points of F3^5. Starting from zero, it closes a queue under T and R, preserving a parent point and generator for every newly reached point. The final set has 45 distinct points and is closed under both maps. Since the maps are permutations of a finite set, the forward-closed set is also closed under their inverses. The parent witnesses prove reachability, so it is exactly the generated group orbit of zero.

Every one of the 990 unordered pairs has its third line point outside this set. Thus the output is an actual 45-cap independently of any assumption about the origin's placement in Figure 3. The accepted affine uniqueness theorem for 45-caps makes it a canonical representative suitable for later deletion-family computations, once independently accepted. The full nonzero-normal count gives 55 directions of type (18,18,9) and 66 of type (15,15,15).

`ORBIT45_POINTS.json` supplies all coordinates, point indices and parent witnesses. Root independently generated the same orbit by a matrix/ordered-index implementation. `ORBIT45_COMPARISON.json` records exact equality of the two 45-point sets; root's points were read only after P's independent points had been generated and hashed.

## Direct named-figure decoding

The labelled primary PDF figures were visually read before extraction. `EPS_GEOMETRY.md` declares the fixed coordinate rule and its geometric origin. It uses the outer x1/x2 grid and the internal x3/x4/x5 projection, with positive x3 down-left, positive x4 right, and positive x5 up. It fixes u=720/127, origin (96.754,85.414), and the equations

`X=96.754+u*(10*x1-x3+3*x4)`,

`Y=85.414+u*(-10*x2+x3-3*x5)`,

where the signed xi range over {-1,0,1}. The 243 projected grid locations are distinct, and their spacing is far larger than the declared 1/100 planar tolerance.

`extract_eps_ae.py` reads numeric EPS path text without executing any PostScript program. It recognizes a filled marker as one moveto and four cubic segments followed by fill; it checks the four quarter-circle endpoints, closure and marker radius. It computes the exact rational midpoint of opposite extrema, then requires a unique match to the predeclared 243-location grid. The duplicate stroke is not counted. Every one of the six figures has the expected number of markers. The largest planar matching error is exactly 143/63500, below 1/100.

As a calibration fixed in advance, Figure 3 decoded by this rule is required to equal the independently computed T/R orbit exactly. It does, without any affine search or coordinate adjustment. The same rule then gives five sets of 41 distinct points from Figures 4,6,7,8,9, identified respectively as A,B,C,D,E by the primary captions and definitions. Each set passes all 820 unordered pair checks. Every histogram is computed using all 242 nonzero normals and exact division by two; in each A-E set every hyperplane section has size at most 18, agreeing with the primary named-family property.

`EPS_POINTS.json` contains all six finite point tables and all 250 marker-to-coordinate witnesses. A witness gives the source EPS line and byte offset, exact rational observed and expected centers, signed coordinates and residue coordinates. This permits root to compare each finite field point directly with the primary diagram through an independently read grid. Passing a cap test was not used to select or tune a coordinate assignment.

## Independence and limitations

Root's independent T/R orbit already matches P exactly. Root's independent A-E figure/coordinate audit is a separate remaining acceptance step. Shared source data consist of the published formulas and vector diagrams; no root orbit or A-E coordinate output was imported before P's extraction. The EPS decoder and orbit generator are independently written local code. Poppler was used only to render the primary PDF for visual reading, not to execute the EPS inputs.

There is no four-point deletion enumeration, LP, new cap-record claim, or proof of a global upper bound in these artifacts. The complete classification cover for all 41-caps still requires separate integration of all its stated alternatives; these six representatives fill only the declared input slots.
