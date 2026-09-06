# Fixed decoding of the primary five-coordinate grid

The primary PDF was visually inspected on printed pages 6-9, containing Figures 3,4,6,7,8,9 (Figure 5/Delta was not extracted). The axes are explicit: outer columns give x1=-1,0,1 left to right; outer rows give x2=-1,0,1 bottom to top. Within each cell, x3 increases diagonally down-left, x4 increases horizontally right, and x5 increases upwards across the three small grids. The same labelled convention and repeated grid are used in all six requested diagrams.

The raw EPS uses downward-increasing planar y before its final page-flip matrix. The central grid origin marked O in Figure 3 is at planar center approximately (96.754,85.414). The repeating projected step is u=720/127 EPS units (approximately 5.669291); the within-grid x4 and x5 steps are 3u, the projected x3 step is u in each of its two planar components, and the outer-cell step is 10u. These ratios are visible in the grid strokes and are independent of which dots are occupied.

Fix the following decoding model before reading A-E as field point sets. For signed coordinates s1,...,s5 in {-1,0,1}, the expected marker center is

`X=96.754+u*(10*s1-s3+3*s4)`

`Y=85.414+u*(-10*s2+s3-3*s5)`.

The origin constants are the primary Figure 3 origin marker's extrema midpoint; they are not fitted to a cap test. The EPS rounds path coordinates to three decimals. Allow absolute error at most 1/100 EPS unit in each planar coordinate, far below the grid spacing. Require exactly one of the 243 fixed grid locations to match every marker. This is geometric decoding of a labelled grid, not a search over point assignments.

The 243 model locations are pairwise distinct. Indeed 3*s4-s3 takes every integer from -4 through 4 exactly once. The three possible outer x1 intervals are disjoint, so X determines s1,s3,s4. Once s3 is known, Y determines s2,s5 by their separated step sizes. No collision can be hidden by the stated tolerance.

Read only the path shape `moveto + four cubic curves + fill`. Its four quarter endpoints and control-point extrema must have the expected circular symmetry and radius approximately 2.126. Retain the original path location and exact rational extrema midpoint. A later stroke of the same marker is ignored. Map the recovered signed coordinates modulo three in order (x1,x2,x3,x4,x5).

As a fixed calibration check, the decoded Figure 3 points must exactly equal the independently extracted published T/R orbit, without any affine search, permutation search or post-hoc coordinate change. If they do not, stop and report the conflict. After that check, apply the same fixed map to A-E and verify their point and histogram properties. Passing a cap test alone is never used to choose the mapping.
