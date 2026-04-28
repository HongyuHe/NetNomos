# NetNomos

NetNomos is a scalable and expressive rule-mining framework for network data.

It mines logical formulas from datasets such as NetFlow records, PCAP traces, and pre-aggregated telemetry. Users define the input data, the predicate search space, and the rule-learning strategy through configuration files.

You provide:

- a **dataset schema**, which tells NetNomos how to load, window, and annotate the data
- a **grammar**, which defines the logic predicates NetNomos is allowed to construct
- a **rule learner**, which combines predicates into candidate rules

The Python package is `netnomos`. The shorter CLI alias is `netn`.

## 1. Introduction

### What NetNomos Does

NetNomos supports declarative rule mining over network datasets, including:

- NetFlow records
- PCAP traces
- pre-aggregated telemetry

Small example datasets are provided under [`./data/`](data/), including:

- [CIDDS NetFlow records](data/cidds_wk2_normal_10k.csv)
- [Netflix PCAP trace](data/netflix.pcap)
- [MAWI PCAP trace](data/mawi_2025july19_tcp100k.pcap)
- preprocessed datacenter logs from [MetaDC](data/metadc_test_10racks_5ctx.csv) [[IMC '22](https://dl.acm.org/doi/10.1145/3517745.3561430)]

The typical workflow is:

1. Describe the dataset using a schema JSON file.
2. Describe the allowed predicate space using a grammar JSON file.
3. Run `netn mine ...`.
4. Inspect the generated predicates, learned rules, and semantic mappings in the run directory.

### Key Concepts

#### Dataset Schema

The dataset schema defines how NetNomos interprets and preprocesses input data. It specifies:

- where the data is loaded from
- which fields are available and what types they have
- semantic roles such as `size`, `time`, `sequence`, `src`, and `dst`
- preprocessing steps such as filtering, mapping, casting, and hex parsing
- context windows for packet-local or time-local reasoning
- derived variables such as interarrival statistics

#### Grammar

The grammar defines the predicate space that NetNomos may explore. It specifies:

- which fields may appear in predicates
- which operators are allowed
- how constants are selected
- whether predicates are simple comparisons, scalar terms, addition terms, or quantified window predicates

#### Rule Learning

NetNomos currently provides two rule learners:

- `hitting-set`: enumerates disjunctive rules from evidence sets
- `tree`: learns implication-style rules using entropy-based decision trees

## Citation

```tex
@inproceedings{he2026netnomos,
  author    = {Hongyu H{\`e} and Minhao Jin and Maria Apostolaki},
  title     = {{Making Logic a First-Class Citizen in Network Data Generation with {ML}}},
  booktitle = {23rd USENIX Symposium on Networked Systems Design and Implementation (NSDI 26)},
  year      = {2026},
}
```

## 2. Installation & Setup

### Requirements

- Python `>=3.10`
- [`uv`](https://docs.astral.sh/uv/) for dependency management and command execution

### Setup

```bash
git clone <your-repo-url>
cd NetNomos
uv sync
```

Verify the CLI:

```bash
uv run netnomos --help
#* Or just use the alias:
uv run netn --help
```

Expected repository locations:

- dataset specs: `examples/datasets/`
- grammar specs: `examples/grammars/`
- sample inputs: `data/`
- mining outputs: `runs/`

## 3. CLI Usage

### `netn --help`

```text
usage: netn [-h] [--log-level LOG_LEVEL] COMMAND ...

Inspect specs, prepare datasets, mine rules, validate rule sets, interpret saved artifacts, and run entailment queries.

positional arguments:
  COMMAND               Subcommand to run
    show-dataset        Print a dataset schema JSON file.
    show-grammar        Print a grammar JSON file.
    prepare             Load and materialize a dataset.
    mine                Generate predicates and learn rules.
    validate            Validate a mined or saved rule set against data.
    interpret           Render rules into human-readable formulas.
    entails             Check whether a query is entailed by a rule set.

options:
  -h, --help            show this help message and exit
  --log-level LOG_LEVEL
                        Logging verbosity for diagnostic messages written to
                        stderr. (default: INFO)

Examples:
  netn mine --dataset-spec examples/datasets/cidds.json --grammar-spec examples/grammars/network_flow.json --input data/cidds_wk2_normal_10k.csv
  netn mine --dataset-spec examples/datasets/pcap_tcp.json --grammar-spec examples/grammars/pcap_window.json --input data/netflix.pcap
  netn entails --dataset-spec examples/datasets/cidds.json --grammar-spec examples/grammars/network_flow.json --rules runs/<run>/rules.json --query "Packets * 65535 >= Bytes"
```

### Subcommands

| Command | Purpose | Typical output |
| --- | --- | --- |
| `show-dataset` | Print a dataset schema JSON file after model validation. | Schema JSON on stdout |
| `show-grammar` | Print a grammar JSON file after model validation. | Grammar JSON on stdout |
| `prepare` | Load data, apply preprocessing, build context windows, and derived variables. | Prepared schema summary JSON |
| `mine` | Generate predicates and learn rules. | Run summary JSON and saved artifacts |
| `validate` | Validate saved or freshly mined rules against data. | Satisfaction statistics JSON |
| `interpret` | Render rules into readable formulas. | One interpreted rule per line |
| `entails` | Ask whether a formula satisfies learned theory. | `{"entailed": true/false}` |

### Flag reference

#### Global flags

| Flag | Commands | Default | Purpose | Example |
| --- | --- | --- | --- | --- |
| `--log-level` | all | `INFO` | Controls stderr diagnostics from dataset loading, mining, warnings, and early stopping. | `uv run netn --log-level DEBUG prepare ...` |

#### Dataset and grammar selection

| Flag | Commands | Default | Purpose | Example |
| --- | --- | --- | --- | --- |
| `--dataset-spec` | all except `show-grammar` | required | Path to a dataset schema JSON file. | `--dataset-spec examples/datasets/cidds.json` |
| `--grammar-spec` | `show-grammar`, `mine`, `validate`, `interpret`, `entails` | required | Path to a grammar JSON file. | `--grammar-spec examples/grammars/network_flow.json` |
| `--input` | `prepare`, `mine`, `validate`, `interpret`, `entails` | schema default | Overrides `source.path` from the dataset spec. | `--input data/netflix.pcap` |
| `--limit` | `prepare`, `mine`, `validate`, `interpret`, `entails` | `None` | Loads only the first N raw rows or packets before preprocessing. Useful for smoke tests. | `--limit 200` |

#### Mining and artifact control

| Flag | Commands | Default | Purpose | Example |
| --- | --- | --- | --- | --- |
| `--learner` | `mine`, `validate`, `interpret`, `entails` | `hitting-set` | Selects the learning backend when the command needs to mine rules. | `--learner tree` |
| `--stall-timeout` | `mine`, `validate`, `interpret`, `entails` | `None` | Stops the hitting-set learner after this many seconds without a new rule. Partial results are returned and saved. Ignored by `tree`. | `--stall-timeout 60` |
| `--runs-dir` | `mine`, `validate`, `interpret`, `entails` | `runs` | Directory where mined artifacts and cache metadata are stored. | `--runs-dir tmp/runs` |
| `--rules` | `validate`, `interpret`, `entails` | `None` | Uses an existing `rules.json` artifact instead of mining a fresh rule set. | `--rules runs/<run>/rules.json` |
| `--query` | `entails` | required | Formula string to check against a theory. | `--query "Packets * 65535 >= Bytes"` |

### Example commands

#### Inspect specs

```bash
uv run netn show-dataset --dataset-spec examples/datasets/pcap_tcp.json
uv run netn show-grammar --grammar-spec examples/grammars/pcap_window.json
```

#### Prepare data

```bash
uv run netn prepare \
  --dataset-spec examples/datasets/pcap_tcp.json \
  --input data/netflix.pcap \
  --limit 10
```

#### Mine rules for the shipped datasets

CIDDS flow records:

```bash
uv run netn mine \
  --dataset-spec examples/datasets/cidds.json \
  --grammar-spec examples/grammars/network_flow.json \
  --input data/cidds_wk2_normal_10k.csv
```

Netflix PCAP:

```bash
uv run netn mine \
  --dataset-spec examples/datasets/pcap_tcp.json \
  --grammar-spec examples/grammars/pcap_window.json \
  --input data/netflix.pcap
```

MAWI PCAP:

```bash
uv run netn mine \
  --dataset-spec examples/datasets/pcap_tcp.json \
  --grammar-spec examples/grammars/pcap_window.json \
  --input data/mawi_2025july19_tcp100k.pcap
```

MetaDC aggregated statistics:

```bash
uv run netn mine \
  --dataset-spec examples/datasets/metadc.json \
  --grammar-spec examples/grammars/metadc_agg.json \
  --input data/metadc_test_10racks_5ctx.csv
```

Example of stall-aware early stopping:

```bash
uv run netn mine \
  --dataset-spec examples/datasets/cidds.json \
  --grammar-spec examples/grammars/network_flow.json \
  --input data/cidds_wk2_normal_10k.csv \
  --limit 200 \
  --stall-timeout 60
```

If the search stalls, NetNomos:

- logs a warning on stderr
- returns the rules found so far
- records `search_stopped_early`, `stop_reason`, and `stall_timeout_seconds` in `fit_metadata`

#### Validate, interpret, and query saved artifacts

```bash
uv run netn validate \
  --dataset-spec examples/datasets/cidds.json \
  --grammar-spec examples/grammars/network_flow.json \
  --input data/cidds_wk2_normal_10k.csv \
  --rules runs/<run>/rules.json
```

```bash
uv run netn interpret \
  --dataset-spec examples/datasets/cidds.json \
  --grammar-spec examples/grammars/network_flow.json \
  --input data/cidds_wk2_normal_10k.csv \
  --rules runs/<run>/rules.json
```

```bash
uv run netn entails \
  --dataset-spec examples/datasets/cidds.json \
  --grammar-spec examples/grammars/network_flow.json \
  --input data/cidds_wk2_normal_10k.csv \
  --rules runs/<run>/rules.json \
  --query "Packets * 65535 >= Bytes"
```

### Where outputs go

Every mining run creates a directory under `runs/`:

```text
runs/<timestamp>_<dataset-name>_<grammar-name>/
```

Important files in each run directory:

| File | Meaning |
| --- | --- |
| `dataset_spec.json` | Resolved dataset spec used for the run |
| `grammar_spec.json` | Resolved grammar spec used for the run |
| `fields.json` | Prepared field metadata after windows and derived variables |
| `derived_variables.json` | Derived-variable definitions and provenance |
| `configured_exclude_fields.json` | Columns removed by the dataset spec's `exclude_fields` denylist |
| `excluded_fields.json` | Columns auto-removed because of `NaN` or empty values |
| `manifest.json` | Run summary including dataset, grammar, source type, rule counts, and `fit_metadata` |
| `predicates.jsonl` | Raw generated predicates with AST and provenance |
| `interpreted_predicates.clj` | Human-readable predicate forms using semantic labels such as `p50` and `top1` |
| `rules.json` | Raw learned rules with AST, provenance, and support |
| `interpreted_rules.clj` | Human-readable rule forms |
| `semantic_values.json` | Mapping from semantic labels to raw values for reproducibility |

Evidence caches are stored separately under:

```text
runs/.cache/evidence/
```

## 4. Dataset Schema Specification

Dataset schema files are `DatasetSpec` JSON documents. They define how NetNomos should interpret raw input data before predicate generation.

### Top-level schema fields

| Field | Meaning | Valid values | Effect |
| --- | --- | --- | --- |
| `name` | Logical dataset name. | any string | Used in run directory names and manifests |
| `description` | Human-readable summary. | any string | Documentation only |
| `source` | Input source description. | `SourceSpec` object | Chooses CSV or PCAP loading |
| `fields` | Explicit field metadata. | list of `FieldSpec` | Controls types, roles, constants, and enum labels |
| `include_fields` | Allowlist after preprocessing. | list of field names | Keeps only the listed columns |
| `exclude_fields` | Denylist after preprocessing. | list of field names | Removes columns after `include_fields` |
| `entity_keys` | Entity-level metadata. | list of field names | Currently metadata only |
| `grouping_keys` | Group-level metadata. | list of field names | Currently metadata only |
| `ordering_keys` | Preferred ordering metadata. | list of field names | Documentation and config consistency |
| `preprocessing` | Ordered source transformations. | list of `PreprocessStepSpec` | Rewrites, filters, maps, and casts raw input |
| `context_window` | Sliding-window specification. | `ContextWindowSpec` or `null` | Builds `_ctx0`, `_ctx1`, ... columns |
| `derived_variables` | Derived columns computed after loading or windowing. | list of `DerivedVariableSpec` | Adds new fields such as interarrival statistics |

### `source`

`source` is a `SourceSpec` object:

| Field | Meaning | Valid values | Effect |
| --- | --- | --- | --- |
| `type` | Physical input format. | `auto`, `csv`, `pcap` | Chooses the loader |
| `path` | Default input path. | string or `null` | Used when `--input` is omitted |
| `csv_read_options` | Extra options passed to `pandas.read_csv`. | JSON object | CSV-specific loading tweaks |

`source.type = "auto"` is the recommended setting when the same logical schema should handle both raw PCAPs and legacy CSV exports. NetNomos infers the loader from the file suffix:

- `.csv` -> CSV loader
- `.pcap`, `.pcapng`, `.cap` -> PCAP loader

### `fields`

Each entry in `fields` is a `FieldSpec` object.

| Field | Meaning | Valid values | Effect |
| --- | --- | --- | --- |
| `name` | Canonical field name used everywhere else. | string | Referenced by grammars and artifacts |
| `source_name` | Original column name before renaming. | string or `null` | Lets a schema normalize raw source names |
| `value_type` | Storage and comparison type. | `integer`, `real`, `categorical`, `boolean`, `string` | Controls predicate generation, constant profiling, and solver lowering |
| `roles` | Semantic tags. | list of role names | Restricts selectors and numeric compatibility |
| `bounds` | Optional numeric range metadata. | `{lower, upper}` or `null` | Informational today, available for future checks |
| `domain` | Explicit categorical domain. | list or `null` | Used by `domain` constant selection and solver typing |
| `constants` | Field-specific reusable constants. | list of `FieldConstantSpec` | Drives `field_constants` selectors and arithmetic terms |
| `enum_labels` | Mapping from raw values to human-readable labels. | object | Used in interpreted predicates and rules |
| `context_family` | Base field family for windowed columns. | string or `null` | Usually auto-filled after windowing |
| `context_index` | Position inside the context window. | integer or `null` | Usually auto-filled after windowing |

#### `value_type`

Use `value_type` to tell NetNomos how a field should behave:

| Value | Use for | Notes |
| --- | --- | --- |
| `integer` | counters, sizes, IDs encoded as integers, timestamps encoded as integers | Can participate in numeric predicates |
| `real` | durations, rates, floating-point measurements | Can participate in numeric predicates |
| `categorical` | enums such as protocol classes, mapped subnets, port classes | Treated symbolically |
| `boolean` | true/false flags | Generates equality predicates |
| `string` | raw text or high-cardinality identifiers | Treated symbolically |

#### `roles`

Roles connect dataset meaning to grammar selectors.

Supported roles in the current schema model:

- `src`
- `dst`
- `proto`
- `time`
- `sequence`
- `measurement`
- `identifier`
- `window`
- `count`
- `size`
- `flag`
- `derived`

Roles matter because they affect:

- selector matching in grammars
- which numeric fields are considered comparable
- whether arithmetic predicates are allowed between two fields

Example:

- `Bytes` and `MTU` should both carry the `size` role if you want `Bytes + Header <= MTU`
- `Duration` should carry `time`, which prevents meaningless predicates like `Bytes <= Duration`

#### `constants`

`constants` is a list of `FieldConstantSpec` objects:

| `kind` | Meaning | Typical use |
| --- | --- | --- |
| `assignment` | Symbolic equality constants | mapped subnets, mapped ports, class IDs |
| `limit` | Numeric thresholds | zero payload, MTU-like bounds |
| `scalar` | Multipliers for `SCALAR` predicates | `Packets * 65535 <= Bytes` |
| `addition` | Additive offsets for `ADDITION` predicates | `tcp.seq + 1 = tcp.seq_next` |

Example:

```json
{
  "name": "Packets",
  "value_type": "integer",
  "roles": ["count"],
  "constants": [
    {
      "kind": "scalar",
      "values": [65535],
      "description": "Maximum payload size per packet"
    }
  ]
}
```

#### `enum_labels`

`enum_labels` maps raw values to readable names in interpreted outputs.

Example:

```json
{
  "name": "SrcPortClass",
  "value_type": "integer",
  "constants": [
    {"kind": "assignment", "values": [80, 443, 70000, 71000, 72000]}
  ],
  "enum_labels": {
    "80": "http",
    "443": "https",
    "70000": "well_known",
    "71000": "registered",
    "72000": "dynamic"
  }
}
```

### Variable selection

`include_fields` and `exclude_fields` operate after preprocessing.

- `include_fields` keeps only the listed columns
- `exclude_fields` removes columns from the post-include set

After field selection, NetNomos automatically removes selected columns that still contain `NaN` or empty values. It:

- logs a warning on stderr
- records denylist-driven removals in `configured_exclude_fields.json`
- records incomplete-column removals in `excluded_fields.json`
- records the same information in `manifest.json`

### Preprocessing

Each preprocessing step is a `PreprocessStepSpec`.

Supported `kind` values:

| Kind | Meaning |
| --- | --- |
| `rename` | Rename columns |
| `drop` | Drop columns |
| `cast` | Cast columns to a dtype such as `int64` |
| `parse_hex` | Parse hexadecimal strings like `0x0012` into integers |
| `fillna` | Replace missing values |
| `map_values` | Value-to-value lookup mapping |
| `map_rules` | Rule-based mapping using equality, ranges, prefixes, regexes, and defaults |
| `filter_equals` | Keep rows where a column equals a value |
| `filter_in` | Keep rows where a column belongs to a set |
| `filter_present` | Keep rows where a column is present and non-empty |
| `sort` | Sort rows by one or more columns |

Important `PreprocessStepSpec` fields:

| Field | Meaning |
| --- | --- |
| `columns` | Source columns affected by the step |
| `target_column` | Output column name for mapping steps |
| `mapping` | Explicit lookup table for `map_values` |
| `rules` | Ordered rule list for `map_rules` |
| `value` | Filter or fill value |
| `dtype` | Target dtype for `cast` |
| `by` | Sort key override for `sort` |

Mapping rules support:

- `equals`
- `in`
- `range`
- `prefix`
- `regex`
- `default`

### Context windows

`context_window` is a `ContextWindowSpec`:

| Field | Meaning | Effect |
| --- | --- | --- |
| `size` | Number of rows or packets per window | creates `_ctx0 ... _ctxN` columns |
| `stride` | Step size between windows | controls overlap |
| `partition_by` | Group keys | prevents windows from crossing entity boundaries |
| `order_by` | Sort order inside each partition | ensures stable window order |
| `column_template` | Output naming template | defaults to `{name}_ctx{index}` |

Example:

```json
{
  "size": 3,
  "stride": 1,
  "partition_by": ["ip.src", "ip.dst", "tcp.srcport", "tcp.dstport"],
  "order_by": ["frame.time_epoch", "frame.number"],
  "column_template": "{name}_ctx{index}"
}
```

### Derived variables

Each `derived_variables` entry is a `DerivedVariableSpec`.

| Field | Meaning |
| --- | --- |
| `name` | Output column name |
| `operation` | Derived operation to apply |
| `inputs` | Source fields consumed by the operation |
| `value_type` | Output type |
| `roles` | Semantic tags for the derived field |
| `literal` | Reserved for literal-driven derivations |
| `numerator` | Explicit numerator for `ratio` |
| `denominator` | Explicit denominator for `ratio` |
| `description` | Free-text metadata |

Supported `operation` values:

- `copy`
- `sum`
- `min`
- `max`
- `avg`
- `std`
- `diff`
- `ratio`
- `count_nonzero`
- `exists`
- `forall`

Example from the shared PCAP schema:

```json
{
  "name": "interarrival_std",
  "operation": "std",
  "inputs": ["interarrival_01", "interarrival_12"],
  "value_type": "real",
  "roles": ["time", "measurement", "derived"]
}
```

## 5. Grammar Specification

Grammar files are `GrammarSpec` JSON documents. They define the search space of predicates and quantifier projections.

### Top-level grammar fields

| Field | Meaning | Effect |
| --- | --- | --- |
| `name` | Grammar name | Used in run directory names and manifests |
| `description` | Human-readable summary | Documentation only |
| `max_clause_size` | Maximum disjunct size for the hitting-set learner | Limits rule complexity |
| `max_rules` | Maximum number of rules to keep before pruning | Caps search size |
| `predicate_templates` | Allowed predicate-generation patterns | Builds propositional candidates |
| `quantifier_templates` | Allowed quantified window patterns | Builds projected quantifier predicates |

### Operators

Supported comparison operators:

- `=`
- `!=`
- `>`
- `>=`
- `<`
- `<=`

These operators are accepted both in grammar files and in formula strings passed to `entails`.

### Variable selectors

Selectors are used in `lhs`, `rhs_field`, term templates, and quantifier templates.

`VariableSelectorSpec` fields:

| Field | Meaning | Interaction with dataset schema |
| --- | --- | --- |
| `names` | Explicit field allowlist | Matches exact `FieldSpec.name` values |
| `regex` | Regex-based allowlist | Matches field names after preprocessing/windowing |
| `types` | Allowed value types | Matches `FieldSpec.value_type` |
| `roles` | Required semantic roles | Matches `FieldSpec.roles` |
| `derived_only` | Restrict to derived or non-derived fields | Matches the `derived` role |
| `context_family` | Restrict to a window family such as `tcp.seq` | Matches `FieldSpec.context_family` |
| `window_only` | Restrict to context-window columns | Matches fields with a `context_family` |
| `exclude` | Explicit denylist | Removes fields after the positive filters |

Example:

```json
{
  "roles": ["size"],
  "window_only": true
}
```

This selects windowed fields that are tagged as `size`, such as `frame.len_ctx0` or `tcp.len_ctx2`.

### Constant selectors

`ConstantSelectorSpec` controls where constants come from.

| Field | Meaning | Valid values |
| --- | --- | --- |
| `mode` | Constant source | `explicit`, `domain`, `profile`, `field_constants` |
| `values` | Explicit values for `explicit` | list |
| `kinds` | Constant kinds for `field_constants` | any subset of `assignment`, `limit`, `scalar`, `addition` |
| `top_k` | Number of categorical values for `profile` | integer |
| `quantiles` | Numeric quantiles for `profile` | list of floats in `[0, 1]` |

Mode behavior:

| Mode | Meaning |
| --- | --- |
| `explicit` | Use `values` exactly as written |
| `domain` | Use explicit field domains or observed categorical values |
| `profile` | Use numeric quantiles or categorical top-k values from the prepared data |
| `field_constants` | Reuse constants from the dataset schema |

`profile` mode also drives semantic labels:

- numeric constants are labeled `p25`, `p50`, `p75`, `p90`, ...
- categorical profile constants are labeled `top1`, `top2`, ...

Those labels appear in:

- `interpreted_predicates.clj`
- `interpreted_rules.clj`
- `semantic_values.json`

### Term templates

`lhs_term` and `rhs_term` are `TermTemplateSpec` objects.

Supported `kind` values:

| Kind | Meaning | Example |
| --- | --- | --- |
| `field` | Plain field reference | `Bytes` |
| `constant` | Plain literal term | `1500` |
| `scalar` | Field multiplied by a constant | `Packets * 65535` |
| `addition` | Field plus another field or constant | `Bytes + Header`, `tcp.seq + 1` |

`TermTemplateSpec` fields:

| Field | Meaning |
| --- | --- |
| `kind` | Term shape |
| `field` | Primary field selector |
| `other_field` | Secondary field selector for `addition` |
| `constant` | Constant selector for `constant`, `scalar`, or `addition` |
| `allow_same_field` | Allows `X + X` or `X op X` when meaningful |
| `description` | Free-text metadata |

### Predicate templates

Each `predicate_templates` entry is a `PredicateTemplateSpec`.

| Field | Meaning | Notes |
| --- | --- | --- |
| `name` | Template name | Appears in predicate provenance |
| `lhs` | Left-hand field selector | Used in simple field-field or field-constant predicates |
| `operators` | Allowed comparators | Must be a non-empty list |
| `rhs_field` | Right-hand field selector | Use for variable-variable predicates |
| `rhs_constant` | Right-hand constant selector | Use for variable-constant predicates |
| `lhs_term` | Left-hand term template | Use for arithmetic predicates |
| `rhs_term` | Right-hand term template | Use for arithmetic predicates |
| `allow_same_field` | Allows comparisons like `X <= X` when desired | Defaults to `false` |
| `description` | Free-text metadata | Optional |

Valid shapes:

- `lhs` + `rhs_field`
- `lhs` + `rhs_constant`
- `lhs_term` + `rhs_term`
- `lhs_term` + legacy `rhs_field` or `rhs_constant` via compatibility conversion

#### Variable-variable example

```json
{
  "name": "numeric-pairs",
  "lhs": {"roles": ["size"]},
  "operators": ["<=", ">="],
  "rhs_field": {"roles": ["size"]}
}
```

Possible generated predicates:

- `Bytes <= MTU`
- `frame.len_ctx0 >= tcp.len_ctx1`

#### Variable-constant example

```json
{
  "name": "zero-payload",
  "lhs": {
    "names": ["tcp.len_ctx0", "tcp.len_ctx1", "tcp.len_ctx2"]
  },
  "operators": ["=", "!="],
  "rhs_constant": {
    "mode": "field_constants",
    "kinds": ["limit"]
  }
}
```

Possible generated predicates:

- `tcp.len_ctx0 = 0`
- `tcp.len_ctx2 != 0`

#### `SCALAR` example

```json
{
  "name": "packet-capacity",
  "lhs_term": {
    "kind": "scalar",
    "field": {"names": ["Packets"]},
    "constant": {
      "mode": "field_constants",
      "kinds": ["scalar"]
    }
  },
  "operators": ["<=", ">="],
  "rhs_term": {
    "kind": "field",
    "field": {"names": ["Bytes"]}
  }
}
```

Possible generated predicates:

- `Packets * 65535 <= Bytes`
- `Packets * 65535 >= Bytes`

#### `ADDITION` examples

Field plus field:

```json
{
  "name": "frame-budget",
  "lhs_term": {
    "kind": "addition",
    "field": {"names": ["Bytes"]},
    "other_field": {"names": ["Header"]}
  },
  "operators": ["<="],
  "rhs_term": {
    "kind": "field",
    "field": {"names": ["MTU"]}
  }
}
```

Field plus constant:

```json
{
  "name": "seq-offset",
  "lhs_term": {
    "kind": "addition",
    "field": {
      "context_family": "tcp.seq",
      "window_only": true
    },
    "constant": {
      "mode": "field_constants",
      "kinds": ["addition"]
    }
  },
  "operators": ["="],
  "rhs_term": {
    "kind": "field",
    "field": {
      "context_family": "tcp.seq",
      "window_only": true
    }
  }
}
```

Possible generated predicates:

- `Bytes + Header <= MTU`
- `tcp.seq_ctx0 + 1 = tcp.seq_ctx1`

### Quantifier templates

Each `quantifier_templates` entry is a `QuantifierTemplateSpec`.

| Field | Meaning | Notes |
| --- | --- | --- |
| `name` | Template name | Appears in predicate provenance |
| `quantifier` | Quantifier kind | `forall` or `exists` |
| `selector` | Context-family selector | Usually points at windowed numeric families |
| `operators` | Allowed comparators | Same operator set as predicate templates |
| `constant` | Constant selector | Often `profile` |
| `aggregator_projection` | Optional projection hint | Accepted by the schema; current v1 lowering derives the projection automatically |
| `description` | Free-text metadata | Optional |

NetNomos projects monotone quantified window predicates into finite predicates:

- `forall X[k] >= c` -> `min(X_*) >= c`
- `exists X[k] >= c` -> `max(X_*) >= c`
- equality and inequality forms fall back to finite conjunction or disjunction

Example:

```json
{
  "name": "payload-forall",
  "quantifier": "forall",
  "selector": {
    "context_family": "tcp.len",
    "window_only": true
  },
  "operators": [">=", "<="],
  "constant": {
    "mode": "profile",
    "quantiles": [0.25, 0.5, 0.75]
  }
}
```

Possible generated predicate:

- `min(tcp.len_ctx0, tcp.len_ctx1, tcp.len_ctx2) >= p50`

### How grammars interact with dataset schemas

The grammar does not operate on raw files directly. It operates on the prepared schema. That means:

- selectors see post-rename, post-preprocessing field names
- `window_only` only works if the dataset defines `context_window`
- `context_family` only works on windowed fields
- `field_constants` only works when the dataset schema declares matching constants
- role-based numeric comparisons only work if the dataset fields are tagged consistently
- profiled constants are computed from the prepared dataset, not from the raw source

### Example rule shapes

A learned rule is built from generated predicates. Examples you should expect in artifacts:

- `Bytes > Mtu`
- `Packets * 65535 >= Bytes`
- `frame.len_ctx0 <= p50 or tcp.len_ctx2 = 0`
- `(tcp.seq_ctx0 + 1) = tcp.seq_ctx1`

Interpreted artifacts use:

- `enum_labels` for categorical readability
- `semantic_values.json` for profiled constants such as `p50` and `top1`

## Shipped example specs

- CIDDS: `examples/datasets/cidds.json` + `examples/grammars/network_flow.json`
- Netflix PCAP: `examples/datasets/pcap_tcp.json` + `examples/grammars/pcap_window.json`
- MAWI PCAP: `examples/datasets/pcap_tcp.json` + `examples/grammars/pcap_window.json`
- MetaDC: `examples/datasets/metadc.json` + `examples/grammars/metadc_agg.json`
