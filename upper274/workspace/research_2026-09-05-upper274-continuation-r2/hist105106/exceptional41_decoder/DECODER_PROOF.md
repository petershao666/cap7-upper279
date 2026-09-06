# Exact SC record-to-point formulas

This is a decoder proof and one-record format check. It does not establish that the raw lists exhaust any exceptional family; L/root separately own that coverage audit. No downloaded Java or spreadsheet macro was executed.

The authoritative decoder source is ../h9/SetDim5Cap43_8sc_ExclPtCounts.java with ../h9/Mod3Vector.java. The former contains all coordinate templates as literal strings in its cap(profile,index) switch, so no spreadsheet evaluation is necessary for decoding this record. The static strings are read as data, not executed as code. Exact source hashes are in ONE_RECORD.json.

## Field order and indices

The print statement at Java lines 597-606 writes ten tab-separated fields:

    r, m, left_profile, left_index, bottom_profile, bottom_index,
    free00, free10, free01, free11

Empty free-cell sets are empty fields and must not be removed when splitting. The left and bottom loops begin at zero (lines 180-181 and 229-231), and the cap switch begins with case zero (lines 637 onward). Both indices are therefore zero-based. They are not spreadsheet row numbers.

A cap template has three colon-separated groups. Each point in a group is a four-coordinate tuple. Its first component is the local slicing coordinate, successively 2,0,1; the last three are the actual (x3,x4,x5). The Java constructor reads components 1,2,3, discarding component 0 (lines 186-218 and 234-255). The profile digits give the three group sizes, for example 828 means sizes 8,2,8.

## Physical coordinates and transformations

We work in residues 0,1,2, with 2 representing -1. Let L0,L1,L2 be the last-three-coordinate groups in the left template, and B0,B1,B2 those of the bottom template. The source labels cap_ab use a=x1 and b=x2, as its comments and hasExclPtCount dot products explicitly confirm (lines 188-218, 237-255, and 4594 onward).

The mapRSC method at lines 4535-4553 is the linear map

    R(a,b,c)=(2c,2b,a) mod 3.

The mapMSC method at lines 4554-4572 is

    M(a,b,c)=(c,b,a).

The nested call at lines 226-227 applies R repeatedly r times first and M repeatedly m times second. It is M^m R^r, not R^r M^m. Only the left two groups outside the common eight-cap are transformed. The common group cap22 is not reassigned in the r,m loops, and the bottom groups are loaded after the transformations without being transformed. The resulting nine physical cells are:

| Physical cell (x1,x2) | Last three coordinates |
| --- | --- |
| (2,2) | L0 |
| (2,0) | M^m R^r L1 |
| (2,1) | M^m R^r L2 |
| (0,2) | B1 |
| (1,2) | B2 |
| (0,0) | decoded free00 |
| (1,0) | decoded free10 |
| (0,1) | decoded free01 |
| (1,1) | decoded free11 |

The first eight-point template groups agree for the selected left/bottom templates. The actual common eight-point set is invariant under the selected M^m R^r; this is checked directly in the decoder. The formulas themselves follow the source and require no conjecture about a symmetry group.

The strArray method at lines 4728-4735 prints base3IndexUncentred values. Mod3Vector.java lines 110-121 show that a three-coordinate vector (a,b,c) is encoded as 9a+3b+c. Thus a printed value v in 0..26 decodes to (floor(v/9),floor(v/3) mod 3,v mod 3). It is not an index into a search-candidate array.

The printed grid at lines 132-135 serializes the left physical column first, then the other two physical columns. To avoid visual-transpose ambiguity, ONE_RECORD.json defines its stored grid explicitly: rows are x1=2,0,1, and columns x2=2,0,1. That array matches the three semicolon groups of the raw header directly.

## One explicit check

The raw source is ../../root_audit/exceptional41_raw/Dim5_41_180716_SetDim5Cap43_9And8_ExclPtCounts_Data.txt. Line 734 identifies the active SetDim5Cap43_8sc_ExclPtCounts block; line 826 gives grid 8,2,8;5,2,0;5,3,8. Exactly one record, line 831, is decoded. It has r=3, m=1, left profile 828 at index 7, bottom profile 855 at index 8, and free00/free10/free01/free11 of sizes 2,3,0,8. This tests a nonidentity rotation, reflection, and an empty field.

The resulting forty-one points are in ONE_RECORD_POINTS.tsv. Direct arithmetic verifies forty-one distinct points, all 820 unordered pairs, the advertised nine-cell grid, and all 121 projective directions. Both exact directional moments are also checked. ONE_RECORD.json contains the full histogram and source literals with their Java line numbers.

No second raw record or complete raw batch was decoded. This format is specific to SC. Root's broader safe raw overcover includes General9, cube8 and antiprism8 outputs; their coordinate/template/transform formats require separate source proofs or an explicit approved reduction. They cannot be omitted because this SC example succeeds. Full-list coverage, completeness of source computations, and eventual universal forty-one support remain outside this format-check claim.
