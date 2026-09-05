# Execution notes

Both complete verifier outputs are included. They agree on all 155 local cases,
all spectral checks, all stage sizes, and the root contradiction.

The certificate excludes 280 points and proves an upper bound of 279.
It does not assert that 279 points can be attained.

C++ uses signed 64-bit integers. For each local polynomial, bounding
T by 9*m^3, E2 by 3*m^2, E3 by m^3, and each spectral function
by the largest absolute value in its table gives a conservative absolute
bound of 34,161,577,632,000 on every such expression and its sum over
directions (m=20 in dimension six, m=45 in dimension seven). This is
below 2^63-1. Python uses arbitrary-precision integers.

The source classification theorems are listed in README.md. Their original
computations are not rerun; every additional finite certificate in this
package is exhaustively verified.
