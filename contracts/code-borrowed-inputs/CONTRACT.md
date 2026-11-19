---
name: code-borrowed-inputs
message: Preserve caller-owned values across operations that promise to leave their inputs unchanged.
---

## Rules

Apply this rule to each public operation whose interface promises to preserve a caller-owned input.
On both success and error, leave that input and its reachable contents in their original observable state.
Keep this promise when another reference points to the same contents or a helper receives part of the input.
Exclude inputs whose interface explicitly transfers ownership or allows the operation to change them.

## Checks

Keep a separate snapshot of an input before the call and inspect the caller's original reference after it.
For an operation that returns sorted entries, supply an out-of-order list and check both the sorted result and the order visible through a second reference to the input.
Confirm the check catches a helper sorting a shallow copy's shared inner list in place and accepts sorting a private copy of that list.
Exercise an error after the operation has begun and compare the caller's contents with the original snapshot.
