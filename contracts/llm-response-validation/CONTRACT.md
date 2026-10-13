---
name: llm-response-validation
message: Accept only complete, protocol-valid model responses that match exactly what was requested.
---

## Rules

Validate a model response completely before recording any result derived from it.
Treat a response that fails validation as a failed attempt, never as an answer; `llm-request-lifecycle` decides whether it is retried.

Give every question in a multi-question request a unique identifier.
Require the response to answer exactly the requested identifiers, with none missing, duplicated, or unexpected.
Accept or reject a multi-question response as a whole; never record the valid subset of a partly invalid response.
When a response reports which model produced it, reject it unless that model is the requested model or a version the requested alias is documented to resolve to.
Check every structured field against its declared type, allowed values, and range, such as a choice against its labels and a probability against zero to one.

Require a completed response with a normal stop reason before parsing structured output.
Treat a truncated, length-limited, or interrupted response, a midstream error, or a stream that carries only keep-alive signals as a failed attempt, never as a partial answer.
Parse streamed responses with a maintained parser for the streaming protocol, including event framing and multi-byte characters split across chunks.
Bound each response's received bytes and its final text length with separate declared limits.
Read a stream to its end, keeping usage and generation identifiers that arrive after the stop signal.

Keep response metadata, such as usage and model identity, on the response rather than duplicated on each answer.
Retain the validated response, its model identity, and its usage with the result derived from it.
When a result echoes the identity, value, or size of its input, compare it with the submitted input and reject any mismatch.
Before consuming a stream of assessment results, require every expected subject exactly once and a summary and status consistent with the individual results.

## Checks

Feed responses with missing, duplicate, and unexpected identifiers, a different model, an unknown label, and out-of-range probabilities, and confirm each is rejected whole.
Exercise interrupted streams, midstream errors, keep-alive-only streams, length-limited stops, and usage that arrives after the stop signal.
Can any code path record a result before every answer in its response has been validated?
Run a live request after a wire-format change; mocked responses do not establish compatibility with the provider.
