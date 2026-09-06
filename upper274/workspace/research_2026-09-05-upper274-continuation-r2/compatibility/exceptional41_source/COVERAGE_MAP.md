# Exceptional41 source-to-list coverage audit

## Verdict

**GO for a separately gated finite-list extraction; STOP before accepting a complete41 histogram packet.** The published source explicitly supplies completeness up to isomorphism for the last alternative of Proposition6.2(b). H9's earlier extraction of only named F/G/H/I representatives did not exhaust that alternative. The relevant local full5D output carrier is `Dim5_41_CapsFound.txt`, interpreted with its companion Arguments file and the search-format source. The files named `*_ListOfCaps.xlsx` contain4D building blocks, not complete5D41 point sets.

No list has been executed, expanded into all caps, independently checked, or promoted to a usable histogram family in this task. The exact number of distinct decoded5D caps/histograms remains unestablished.

## Primary source and coverage chain

Frozen primary source: hist105106/h13/source_article.html, arXiv2206.09719v1. At id S6.Thmtheorem2, Proposition6.2(b) concerns41caps without20201 or18185 directions that have an18176 or18167 direction. Its last alternative is a complete cap with a saddled-cube intersection between the indicated18-section and another18-,17-,or16-section. The parenthetical sentence explicitly states completeness up to isomorphism of its supplementary lists for this alternative and permits repeated representatives of one isomorphism class.

Section5 explains the algorithmic list semantics: for each3-flat count matrix, normalize the left4D section and bottom4D section, enumerate compatible shared3D section symmetries, then list fillings of the four unfilled3D cells. Proposition6.2(b)'s proof sends each count matrix to contradiction, an earlier hyperplane case, or one of the listed cap alternatives, and points to the supplementary files for full search results. Therefore the source-level coverage is real; it is not inferred merely from a filename.

The companion `Dim5_41_CapsFoundArguments.txt` ends by assigning the remaining non-excluded configurations to45-minus4 or the complete saddled-cube alternative, while treating named caps and Delta-minus1 earlier. Use the complete union of outputs under the source's preceding-case restrictions; do not identify the exceptional family with just F/G/H/I, and do not silently discard non-sc blocks without checking their reductions in Arguments.

## Exact file roles and sizes

All local paths below are under hist105106/h9.

* `Dim5_41_CapsFound.txt`,49600bytes:5D output summary. It has77 `(sc)` blocks, including repeated count matrices and blocks with exclusions. Entries are either explicit output tuples or compressed ranges/subset families. At least18 late blocks say that their actual configurations lie among the displayed families. Thus expanding the displayed families gives an overcover; their raw expansion count must not be equated with the reported number of actual caps.
* `Dim5_41_CapsFoundArguments.txt`,13968bytes: reductions and interpretation of output configurations, with some named point diagrams. It is not itself a complete point list.
* `ChecksForCompletenessOfLists.xlsx`,3207818bytes:18 sheets, each keyed by a nine-entry3-flat count. They compare explicit10-field output rows with the compressed families for selected late sc blocks. Sheet names and dimensions are exported in INVENTORY.json. This checks selected list compression, not the entire exceptional family by itself.
* `SetDim5Cap43_8sc_ListOfCaps.xlsx`,210918bytes:12 sheets of4D input caps with a fixed common saddled cube. Sheet profiles and counts are819:4,828:35,837:14,846:11,855:9,818:219,827:275,836:237,845:216,817:806,826:1011,835:993. Rows are zero-based code index,4-coordinate point-string, and matching Java return-string. These numbers count normalized4D building blocks, not exceptional41caps.
* `SetDim5Cap43_8cu_ListOfCaps.xlsx`,34528bytes; `SetDim5Cap43_8sa_ListOfCaps.xlsx`,53737bytes; `SetDim5Cap43_9asifsa_ListOfCaps.xlsx`,40736bytes:other4D building-block catalogues for the shared3D shape. They are not whole5D41 lists.
* `SetDim5Cap43_8sc_ExclPtCounts.java`,620817bytes, and `Mod3Vector.java`,4098bytes:read-only decoding specification, including the identical indexed4D point strings, symmetry maps and printed tuple order. Neither was compiled or executed.

The original arXiv ancillary index also names the raw output files

    Dim5_41_180617_SetDim5Cap43_9And8_ExclPtCounts_Data.txt
    Dim5_41_180716_SetDim5Cap43_9And8_ExclPtCounts_Data.txt

corresponding to the physical18/6/17 and18/7/16 branches of Proposition6.2(b). They are not in the inspected local H9 directory. Their raw byte sizes and complete contents were not established: direct web opens returned cache-miss. Do not invent their record counts or assume their contents from their filenames. The frozen ancillary link index is the provenance for these exact filenames. The analogous170717 and170816 files belong to Proposition6.2(c)'s reduction rather than being needed as extra exceptional classes once(b) is covered.

## Coordinate reconstruction of an sc output row

The Java print statement at lines597–606 establishes the ten fields:

    r, m, leftProfile, leftIndex, bottomProfile, bottomIndex,
    cap00, cap10, cap01, cap11.

Indices are zero-based. The two4D code strings are split by colon into the layers whose first4D coordinate is2,0,1, representing-1,0,1. Within each layer semicolon-separated points have four comma-separated residues; discard the layer coordinate to obtain z=(x3,x4,x5). The common shared cap occupies(x1,x2)=(2,2). The left code supplies cells(2,0),(2,1), and the bottom code supplies(0,2),(1,2), with the common cap counted once.

For the left code's non-shared cells apply M^m composed with R^r, where

    R(z0,z1,z2)=(2*z2,2*z1,z0), r in{0,1,2,3},
    M(z0,z1,z2)=(z2,z1,z0), m in{0,1}.

These formulas are read from Java mapRSC and mapMSC at lines4535–4571. The four final fields then fill the cells(0,0),(1,0),(0,1),(1,1), in that order. Each integer p is an uncentred base3 point index, decoded as(floor(p/9),floor(p/3) mod3,p mod3), by strArray/base3IndexUncentred. Empty strings or '-' denote empty cells in summaries. Parenthesized choices, inclusive index ranges and '(k of ...)' require explicit expansion. One cannot always treat each tab-separated field as one point list: e.g. '(3,6)' denotes alternatives when the cell size is one, whereas '3,6' is a two-point cell when its required size is two.

The printed3-flat matrix is organized as three physical columns, each listed top-to-bottom, with x1 labels-1,0,1 and x2 labels1,0,-1. The source read operations at lines185–218 and233–245 fix this interpretation independently of the informal diagram layout.

## Safe next finite input and remaining obstacle

A separately registered extraction can either acquire the two raw(b)-branch outputs and decode their records, or expand the entire local CapsFound summary using the matching source/catalogue semantics. Every decoded object must be checked for41 distinct points, all pair completions, its stated3-flat count and every retained preceding-case restriction. Overgenerated invalid configurations may be discarded by these exact checks; valid extra caps may remain in a necessary overcover. The complete-exception claim must retain the primary source's entire case coverage, including reductions to earlier named/deletion families.

The present source audit establishes a meaningful new coverage bridge, but leaves an explicit terminal obstacle: no complete decoded and independently verified exceptional41 packet yet exists here. It does not justify injecting the4D workbook rows directly into a41-cap support model. H21 and all frozen stages remain unchanged.
