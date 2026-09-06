# Independent complete raw41 point decoder audit

## Exact completed domain and result

Every one of the34345 explicit positive output records in the two primary18/6/17 and18/7/16 ancillary files has been decoded. The four format totals are33549 saddled-cube,60 General9,432 cube and304 square-antiprism records. No row was omitted, repaired into a different configuration, or discarded as invalid. Every source block's printed Cap configurations total matches its actual number of rows.

The decoded records give8551 distinct normalized point sets and41 distinct direction histograms. These are point-set/histogram counts, not affine-isomorphism class counts. The packet is a necessary overcover for the primary theorem's exceptional41 alternative, together with the source's reductions to earlier named/deletion alternatives; it is not a new proof of the source's original search completeness or a full41-cap classification. Independent producer comparison and root coverage integration are still required before acceptance.

## Coordinate sources and independent implementation

For all8-section formats, this decoder reads the workbook columnsA/B directly: columnA is the zero-based code index; columnB is the4-coordinate point string. It does not read the producer's extracted Java literal tables or generated pointsets. Workbook ZIP/XML relationships map sheet names to worksheet files explicitly. Semicolon-separated points are grouped by colon into levels2,0,1 of the first4D coordinate. Residues and layer labels are checked.

The17-point bottom sections used in48 General9 records come from the9asifsa workbook. Three named18-coordinate inputs,918/981F,918/981I and972/981I, have no equivalent table in the inspected workbook families and are read as static strings from the primary General9 Java source. Root explicitly authorized this shared input boundary. The same primary mathematical data may be used by the other decoder; implementation independence does not imply independent source data.

Transformations are implemented by independent homogeneous4-by-4 matrix multiplication and binary matrix exponentiation overF3. This differs from applying the Java array-transform routines point by point. All resulting affine maps are tested as permutations of the27 inner points and as setwise stabilizers of the shared3D cap. The source Java is read only and never compiled or executed.

Let z=(x3,x4,x5). Saddled-cube maps are R(z)=(2z2,2z1,z0), M(z)=(z2,z1,z0), with map M^m R^r. General9/square-antiprism maps use R(z)=(2z0,z1+z2,2z1+z2), M(z)=(z0,z1,2z2). General9 additionally applies T1(z)=(z0+2z1+1,z1+1,z2) and T2(z)=(z0+2z2+1,z1,z2+1), in the total order M^m R^r T2^t2 T1^t1. Cube maps first permute coordinates in the explicitly listed order012,021,102,120,201,210, then independently multiply coordinates by1 or2 according to the three bits of m. Each format's own allowed parameter ranges are checked.

These maps apply to the left4D section's two non-shared cells. The common cell(x1,x2)=(2,2) is included once; the bottom4D section supplies cells(0,2) and(1,2). The four final free-cell fields give cells(0,0),(1,0),(0,1),(1,1). An inner index p is decoded in most-significant-first base3 as(p//9,p//3 mod3,p mod3). Final point indices use81*x1+27*x2+9*x3+3*x4+x5.

The raw printed3-by-3 count uses BOTH physical-axis label orders(2,0,1). This corrects the informal diagram-order sentence in the earlier source-only COVERAGE_MAP.md; the raw source's n[8],n[6],n[7] serialization is explicit. The decoder asserts its reconstructed matrix equals each raw header exactly in this order.

## Exact checks

The Python decoder checks that every row gives exactly41 distinct residue tuples, the required common3D cap and all nine stated cell counts. It writes CHECK_INPUT.txt and a row ledger retaining original source file, line, block and shape.

A new C++ verifier independently reconstructs all five coordinates from point indices. It checks every unordered pair against the precomputed completion-(p+q), for28162900 pair tests total. It independently reconstructs every raw3-by-3 matrix. It enumerates all121 normalized nonzero5D dual vectors directly and computes every direction's three occupation counts, for4155745 direction histograms total. The verifier asserts the known maximum4D section size20 and the two exact directional identities sumE2=81*C(41,2)=66420 and sumE3=27*C(41,3)=287820. All operations are bounded integer arithmetic; the checker was compiled with undefined-behavior sanitizer and no sanitizer recovery.

All rows passed. Python decoding took2.018950seconds; the complete C++ check took0.581081seconds. These are finite verification timings, not mathematical progress measures. The packager additionally checked each raw block's recorded excluded profile conditions against the computed histogram. These exclusions retain their source case scope and are not promoted to ordinary bans.

## Frozen outputs and comparison contract

ROWS.jsonl gives every decoded sorted point set, original line identity and point SHA256. Point hashes are SHA256 of compact JSON for the lexicographically sorted5-tuples. ROW_LEDGER.jsonl gives every original row's point hash and deterministic histogram ID. HISTOGRAM_PACKET.json supplies the full40-type order, all41 histogram vectors and an explicit41-point representative for each. Histogram IDs are the lexicographic order of the full histogram vectors.

No H producer decoder, new generated point table, histogram file or result was read before this freeze. Root mentioned an earlier one-record format example; it was not imported into this implementation or used as verification evidence. Shared dependencies are the original raw records, published coverage theorem, workbook/static named-coordinate data and transformation specification. Root must compare independent outputs and integrate the complete case coverage before promoting this input. No LP or seven-dimensional claim occurs in this audit.
