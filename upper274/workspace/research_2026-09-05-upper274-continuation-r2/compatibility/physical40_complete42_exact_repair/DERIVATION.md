peter，The final floating vector determines only potential values and unscaled case coefficients. All floating whole-bound variables and floating support-bound variables are discarded before integer recovery. Each scale is fixed in SCOPE.md; rounding uses NumPy rint on these existing coefficients and potentials. The resulting integers are then evaluated without floating inequalities.

peter，For every physical leaf function g on a complete accepted histogram family H, set B_g=max_{h∈H}〈g,h〉. The physical18 pair bound is the maximum of〈g_left,h_a〉+〈g_right,h_b〉over every accepted ordered pair; the conditional18 bound is the maximum over every accepted conditional state. This recomputation is performed independently for each of the three40 tiers. Function IDs400,401,402 all refer to mathematical size40; they attach respectively to column1 of NC106 anchors(43,40,23),(44,40,22),(45,40,21).

peter，For a nonempty first-anchor case t of a tier m, let X(M) be its exact local feature vector, F the forced feature totals, θ_m its main potential, and t_1,t_2,t_3 the transverse profiles. Let the physical child terms include the appropriate independent leaf or main functions and any accepted ordered-pair/conditional18 functions. Compute

K_t = min_M [〈q_t,X(M)〉 − θ_m(t_1) − θ_m(t_2) − θ_m(t_3) + Σ child_values(M)],

B_t = θ_m(t) + 〈q_t,F〉 + Σ child_bounds − D_m K_t.

peter，Here D_m=40 for each size40 tier and D_106=121. The full first-anchor cover gives B_m=max_t B_t. Empty cases use their frozen complete coverage status and contribute no maximum candidate. The three40 bounds are recomputed first, then supplied in their respective physical NC106 columns; every NC106 case minimum and its whole maximum B_106 is recomputed afterward. The original fixedH3 upper inequalities remain present with their original signs and forced values.

peter，Finally, on the complete frozen outer domain for minimum profile(106,106,63) with its two NC106 sections, compute

K_out = min_M [〈q_out,X_out(M)〉 + Φ_106(t_0(M)) + Φ_106(t_1(M))],

U_out = 〈q_out,F_out〉 + 2B_106,

gap = 364K_out − U_out.

peter，The ordinary18 bans and the Q67-minimum condition remain separate predicates in the unchanged outer domain. No minimum-only closure is used as an ordinary ban. A strictly positive gap would yield the scoped contradiction after independent raw verification. Every recovered gap is negative, so this argument yields no exclusion at the tested coefficient vector.

peter，Implementation dependencies are explicit: run.py reuses the frozen producer domain constructors, accepted lower-dimensional inputs, and allocation order; verify.py is the unchanged shared-kernel author checker and is not run because no positive candidate exists. Root/P independent raw checker implementations are separate. RESULT.json and TERMINAL_FROZEN.json bind the checkpoint, source/layout hashes, all five exact signed gaps, corrected three40/NC106 bounds, outer minima, and integer safety ceilings. No discovery cache or nominal floating bound was accepted as an exact inequality.
