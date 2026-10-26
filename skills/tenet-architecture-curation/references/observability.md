# Observability

A useful diagnostic answers: which operation, which stage or attempt, what happened, how long it took, and what can
happen next. Emit these facts at meaningful ownership boundaries. Keep a stable run or request identity across them.
Use common stage and error vocabulary instead of translating the same event differently in every adapter.

Keep domain decisions readable. Put transport tracing, redaction, and serialization in small boundary helpers rather
than threading a logger through pure transformations. Record enough detail to diagnose failures, with bounded payloads
and histories. Exclude credentials and avoid persisting source or request bodies by default when metadata suffices.

Authoritative results and checkpoints must surface write failures. Optional status summaries and cosmetic progress
must not determine execution success. A quiet provider is not evidence of progress: show elapsed time or last activity
honestly. Keep diagnostic evidence separate from generated prose used to make a terminal status easier to read.

Reports and terminal summaries should consume the same completed snapshot. Include partial results and failures so an
operator can distinguish an incomplete run from a poor score. Inspect one saved report against the terminal output after
changing this path; adding more log lines is not a substitute for a consistent data flow.
