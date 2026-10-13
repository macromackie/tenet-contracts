---
name: llm-request-lifecycle
message: Retry transient model request failures within one owned budget, never to obtain a preferred answer.
---

## Rules

Disable retries in provider client libraries and every other layer except the request's one retry owner, as `code-execution-lifecycle` requires.
Give each logical request a declared maximum number of attempts and one deadline that all its attempts share.
Use the same provider, model, parameters, and input for every attempt of a logical request.

Retry only transient failures, such as dropped connections, timeouts, rate limiting, temporary provider errors, and responses that fail validation.
Do not retry permanent failures, such as rejected credentials, invalid requests, or an unsupported model.
Accept the first valid answer, even an uncertain or unfavorable one, and never retry, resample, change parameters, or switch models to obtain a different one.
Honor the provider's rate-limit and retry-after signals across every request that shares the limit.

Make every caller in a process that shares a provider rate limit draw from one declared concurrency limit.
Count a hedged duplicate request as an attempt, and send it only when a spare concurrency slot exists.
Cancel every active attempt when the caller cancels or abandons the request.

Send each request to the explicitly selected provider and model, using only that provider's credential.
Fall back to another model or provider only under a declared policy, as a separate logical request recorded with the model that answered.
Record each logical request's attempts, failures, response identifiers, and usage outside the prompt sent to the model.
Count the accepted response's usage once, and record cancelled or abandoned attempts as unknown usage, never as zero.

## Checks

Count the layers that can retry one model request and confirm that only the declared owner does.
Simulate transient failures, permanent errors, rate-limit signals, and invalid responses, and confirm that attempts stop within the declared count and deadline.
Return a valid unfavorable or uncertain answer on the first attempt and confirm that no further request is sent.
Cancel a request with attempts in flight and confirm that every attempt stops and that its usage is not recorded as zero.
Inspect the recorded attempts of one logical request and confirm that they share one provider, model, parameter set, input, and deadline.
