# Finite canonical 45-cap extraction from published maps

Root explicitly authorized this replacement for Figure 3 point decoding. Input is the primary Remark immediately after Theorem 4.3 of arXiv:2206.09719v1, printed page 12, giving

`T(x1,x2,x3,x4,x5)=(x1-x2+1,x2+1,x5,x3,x4)`

and

`R(x1,x2,x3,x4,x5)=(-x1,x3,-x2,x4+x5,-x4+x5)`.

The formulas are directly present at lines 356-357 of the frozen primary `CapSetProblem5S41.tex`. The Remark's transitivity statement motivates the finite orbit, but no assumption that the origin lies in the drawn representative is required: if the independently computed orbit of the origin has 45 points and passes every cap pair check, it is a valid canonical 45-cap, and the accepted affine uniqueness theorem applies regardless of its exact diagram-coordinate identity.

Before computing, declare a domain of at most all 243 points of F3^5. Starting at zero, repeatedly apply T and R until closed; record a parent and generating map for each discovered point. Check that both maps are invertible on the full finite space, output all distinct orbit points, verify all 990 unordered pairs, and recompute all 121 projective hyperplane profiles. The expected consistency spectrum is 55 directions (18,18,9) and 66 directions (15,15,15); do not infer validity from the spectrum alone.

Budget at most 60 seconds, one worker, 256 MiB. Terminal an explicit coordinate list plus exact witness/check record, or rejection if size/cap checks fail. This is extraction/replication of a published input, not a new construction or a new global bound. No EPS execution, no A-E extraction in this gate, no four-point deletion enumeration, and no LP. Root independently computes the same source-defined orbit using a separate representation before acceptance.
