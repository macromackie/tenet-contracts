---
name: llm-confidence-routing
message: Keep raw model answers and confidence separate from routing, and never treat confidence as calibrated correctness.
---

## Rules

Store each model answer's raw choice, and any confidence or probabilities it carries, exactly as obtained, in a record separate from any routed outcome.
Do not write routed outcomes, thresholds, or inferred reasons into the raw answer record.
Return the same raw answer representation from every kind of question the system asks.
Keep raw answers and routed outcomes in separate fields of machine-readable output, and label them separately in human-readable output.

Apply minimum confidence through one routing policy that the caller owns and that depends only on the raw answer and a declared threshold.
Apply the same declared minimum confidence to every answer that contributes to one decision.
Route an answer below the minimum confidence to uncertain, keeping its chosen label and exact confidence.
Keep an explicit uncertain answer uncertain at every threshold, including zero.
Record low confidence and explicit model uncertainty as distinct routing reasons, without inventing an explanation for the model's choice.
Routing must not change the raw answer or send another request.

Interpret each answer only as an answer to the question asked about the evidence supplied, and keep any part of the original requirement it did not ask about open.
Routing an uncertain answer to more evidence, another representation, or a fuller review does not settle the original question; it stays unresolved until a later answer settles it.

Do not average per-subject confidences or scores into the confidence of a combined decision.
Do not present a probability, a confidence, or an average of them as the correctness rate of the system.
Treat model confidence as neither an error bound nor a calibrated probability of correctness.
Support any claim about error rates or calibration with separate evaluation evidence and the population it measured; changing a confidence threshold does not create that evidence.

## Checks

Run the same inputs at two confidence thresholds and confirm that the raw answers in the output are identical.
Exercise an explicit uncertain answer and a low-confidence answer, and confirm each stays unresolved with its own reason and unchanged raw values.
Confirm that routing sends no additional request.
Does any report, summary, or document present confidence or averaged scores as measured accuracy?
Inspect any claimed error rate, calibration, or stopping guarantee for the evaluation evidence behind it.
