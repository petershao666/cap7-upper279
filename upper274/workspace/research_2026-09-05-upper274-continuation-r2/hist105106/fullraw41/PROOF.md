# Complete raw-list coordinate and histogram extraction

The primary published coverage statement and root/L's source audit imply that the last exceptional forty-one-cap alternative in Proposition 6.2(b)/Theorem 6.3 is covered, up to affine isomorphism, by the applicable supplementary output lists. We retain the entire safe raw overcover authorized in ../../root_audit/exceptional41_raw/DECODE_GATE.md: all 34345 positive records from the frozen 180617/180716 files. The source search completeness is an explicit published premise. Decoding its outputs does not reprove that search or give a new affine classification.

The finite extraction proves that every one of these records specifies a valid forty-one-point cap, with its stated nine-cell counts and a well-defined whole directional histogram. Their histogram union has 41 elements. Their decoded normalized pointsets have 8551 distinct members; neither number is an affine isomorphism-class count. Including extra named caps and extendable caps is safe for upper-support inequalities on the source exceptional alternative.

## Coordinate templates and source controls

prepare.py reads only the literal coordinate strings in the four primary Java cap functions. It executes no Java code, macros or PostScript. The source file hashes are frozen in SOURCE_INPUTS.json. The three eight-intersection sources use profile plus zero-based numeric switch index; General9 prints the actual named code or profile:index string, which is used directly in its cap(profile,code) branch. Adjacent quoted numeric strings are concatenated as data. No general expression evaluation is used.

Each template gives three colon-separated groups of four-coordinate points, with first coordinates 2,0,1. The first coordinate is discarded exactly as in the Java construction; the remaining three coordinates are (x3,x4,x5). The template group sizes must equal the profile digits. Empty groups are retained. The earlier verified one-record SC fixture is a disclosed starting point for this mathematical format; the full extraction uses a separate all-format data parser.

The raw files contain temporary subprogram blocks introduced by a double-hyphen program tag inside a surrounding program section. An unprefixed program header sets the surrounding program, while a prefixed tag overrides only its next block. After that block's Cap configurations line, parsing returns to the surrounding program. The first parser detected an inconsistent twelve-field record after a temporary antiprism sub-block and stopped before point decoding. FORMAT_RESOLUTION_01.json preserves this source-context issue and its resolution. No row was discarded or reassigned by a cap-validity heuristic. The corrected parser independently checks that General9 headers have intersection size nine and all other headers have intersection size eight; each block's explicit output count must match its declared Cap configurations value.

This procedure gives exactly 33549 SC records, 60 General9 records, 432 cube8 records, and 304 antiprism8 records. Every explicit numeric output is consumed and mapped to an original file, line, block header and shape. RAW_BLOCKS.json preserves the whole block ledger, including zero-output blocks.

## Four distinct transformation rules

All arithmetic below is in F3. Transformations act only on the two left-section groups outside the common eight- or nine-point intersection. The common intersection is retained in place; the two bottom-section groups are untransformed. The equality of the two template intersection sets and invariance under the selected transformation are checked for every used template/transformation combination.

For SC, the primary methods mapRSC/mapMSC are at lines 4535-4572 of the SC Java source. On p=(a,b,c),

    Rsc(p)=(2c,2b,a),  Msc(p)=(c,b,a).

The applied transformation is Msc^m Rsc^r, with r in 0..3 and m in 0..1. The ten raw fields are r,m,leftProfile,leftIndex,bottomProfile,bottomIndex,free00,free10,free01,free11. The source print statement and exact placement proof are additionally documented in ../exceptional41_decoder/DECODER_PROOF.md.

For cube8, mapPerm/mapMTimes3 are at lines 1082-1150 of its Java source. The permutation r in 0..5 selects component orders

    abc, acb, bac, bca, cab, cba.

After this permutation, multiply the three components by

    1+(floor(m/4) mod 2), 1+(floor(m/2) mod 2), 1+(m mod 2),

respectively, with m in 0..7. The ten raw fields otherwise have the same roles as SC. No rotational power interpretation is substituted for the permutation index.

For antiprism8, mapR/mapM are at lines 1334-1373 of its Java source. They are

    R(p)=(2a,b+c,2b+c),  M(p)=(a,b,2c),

and the source applies M^m R^r, with r in 0..7 and m in 0..1. These are different from the SC maps. Its ten raw fields have the same roles as the other eight-intersection formats.

General9 uses the same displayed R and M as antiprism8 and additionally uses the two affine maps at lines 1465-1504 of its Java source:

    T1(p)=(a+2b+1,b+1,c),  T2(p)=(a+2c+1,b,c+1).

The composition read from the nested calls at lines 316-320 is

    M^m R^r T2^t2 T1^t1,

with t1,t2 in 0..2, r in 0..7, and m in 0..1. Its twelve raw fields are t1,t2,r,m,leftProfile,leftCode,bottomProfile,bottomCode,free00,free10,free01,free11. The printed left/right codes are the code strings, not indices into the code-name array; the statement at lines 690-702 determines this distinction.

## Nine physical cells

Writing L0,L1,L2 for the left template and B0,B1,B2 for the bottom template, and F for the appropriate composition above, the physical cells are:

| (x1,x2) | Last three coordinates |
| --- | --- |
| (2,2) | L0 |
| (2,0) | F(L1) |
| (2,1) | F(L2) |
| (0,2) | B1 |
| (1,2) | B2 |
| (0,0) | free00 |
| (1,0) | free10 |
| (0,1) | free01 |
| (1,1) | free11 |

Every free-cell integer v is the printed base3IndexUncentred value, which Mod3Vector.java defines as 9a+3b+c. Thus it decodes as (floor(v/9),floor(v/3) mod 3,v mod 3), including v=0. An empty field means an empty set. The stored grid uses row values x1=2,0,1 and column values x2=2,0,1, exactly matching the source's left-column-first serialization.

## Full finite checking and independence

prepare.py writes every row as forty-one sorted point IDs, with encoding 81*x1+27*x2+9*x3+3*x4+x5. The new C++ checker independently reconstructs those coordinates from the IDs. For every row it checks the range, strict point order and distinctness, all nine stated cell counts, and all 820 unordered pairs p,q, requiring that -p-q is absent. This is equivalent to the cap property in characteristic three. No record is skipped after any failure.

The checker enumerates the 121 projective normals in F3^5 by fixing the first nonzero coordinate to one. It computes each normal's three level sizes directly and records their sorted triple. Every resulting histogram sums to 121 and satisfies the exact moment identities sum(E2)=81*binom(41,2)=66420 and sum(E3)=27*binom(41,3)=287820. In total, 28162900 point-pair checks and 4155745 directional checks pass. The bound of twenty on any four-dimensional section is the already accepted lower-dimensional input; every recorded type is checked against that domain.

The producer froze FROZEN.json before reading L's generated output. L independently read workbook coordinate data and independently derived the shape transformations, then used its own checker. After both freezes, all 34345 rows agree exactly on original-file order, nine-cell grids and every sorted point ID. Apart from the producer's extra leading count line, the point-row payloads are byte-identical. L also independently reports exact agreement of each row's histogram and the complete 41-element histogram set. INDEPENDENT_COMPARISON.json records the freezes, hashes and shared primary-input boundary; this is more than agreement between two wrappers of one decoder kernel.

HISTOGRAMS.json supplies the complete type order, 41 histogram vectors, and an explicit point representative for each. ROW_LEDGER.tsv links every source line to its point hash and histogram ID; point hashes are SHA256 of the 41 sorted point IDs serialized as bytes. ROW_METADATA.jsonl retains the original printed fields. These artifacts cover the raw overcover and therefore, conditional on the published source-to-exceptional-family coverage premise, supply an upper-support family for that exceptional alternative. They are not by themselves a universal forty-one-family list, a new classification theorem, or a seven-dimensional exclusion. The remaining named/deletion families are root's separate integration responsibility.
