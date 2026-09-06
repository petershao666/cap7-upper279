peter，Internal identifiers400,401,402 are function IDs for three different functions on size40 caps. They are never dimensions or cap cardinalities. The legacy producer fields m and, for some leaf metadata, case_dimension_size carry these IDs. Independent replay and user-facing interpretation must use the explicit mapping below.

| function_id | mathematical_size | ambient_dimension | whole_directions | refinement_directions | physical NC106 parent |
|---|---:|---:|---:|---:|---|
|400|40|5|121|40|(43,40,23), column1|
|401|40|5|121|40|(44,40,22), column1|
|402|40|5|121|40|(45,40,21), column1|
|106|106|6|364|121|Both actual outer106 sections, through a universal bound|

For count/empty-case records, m=400/401/402 means the indicated40 proof tier. For local-support records, m is the actual lower section size16/17/18/41/42, while case_dimension_size=400/401/402 identifies its parent40 function tier. The leaf's m and its parent's internal ID have different meanings. A normalized terminal export will add explicit function_id or parent_function_id and mathematical_size fields, preserving all original frozen values separately.

The main histogram nodes already include mathematical_size and tier_parent, and the top-level tier_mapping records every40 function's physical use. All three retain40-point type tuples; their coefficients and bounds are independently optimized. This schema clarification adds no mathematical constraint and changes no running or frozen code.
