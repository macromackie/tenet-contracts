# Choosing a boundary

| Structure | Reason to introduce it |
| --- | --- |
| Function | A coherent operation deserves a name. |
| Module or file | One responsibility can be understood separately. |
| Nested folder | Related modules form a subsystem with a small entry point. |
| Package or crate | Enforce a dependency, runtime, ownership, or actual reuse boundary. |

A report subsystem can separate input validation, label metrics, and summary construction behind one entry point.
Callers should not need to know which file implements each operation. In Rust, keep child modules private and expose
only the functions used outside the subsystem.

A run coordinator should keep deadlines, cancellation, state transitions, and retries together. Extract pure encoding
or trace bookkeeping when it has a clear input and result. Do not split each state transition into a package that needs
the entire coordinator passed back to it.

A provider adapter with real callers can justify a package. A second provider imagined for later does not justify a
registry or plugin loader. Consistency means using the same roles and conventions, not forcing every folder to have
the same number of layers.

Keep one owner for a durable fact. A runtime can return a final report containing results and their summary; the CLI
should render that snapshot rather than recompute from an earlier status poll. In a local resumable runner, checkpoints
own completed work and exported JSONL is a projection. Neither needs a generic event bus or a second database.

Prefer a small domain result shared by callers over exposing provider response objects throughout the system. Keep raw
provider evidence at its diagnostic boundary when needed. Do not introduce a new DTO at every hop when the existing
type already expresses the same meaning.

For example, an audit result with optional `grade`, `error`, and `score` permits both success and failure, or neither.
Give the outcome an explicit graded/failed variant. Retain raw provider evidence separately, derive summaries from
completed results, and validate a saved report once before passing it to the audit. The benefit is fewer decisions
for the CLI, not a new general-purpose result framework.
