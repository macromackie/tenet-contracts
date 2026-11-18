# Choose a local check

Start with a public behavior and the mistake a check should expose. Bind the check locally with
Tenet 0.17.0 or later. With an earlier release, invoke the checker through the project's test command.

| Recipe                     | Bind it when                                           | Exercise it                                                                                                                                                                                             |
| -------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Consumer agreement         | Two public operations promise the same interpretation. | Supply the same boundary input to both. Verify what each consumer does with the interpretation. Break one consumer in a temporary copy and check that its example fails.                                |
| Input provenance           | A value can come from several sources.                 | State the policy for absent, empty, and ordinary nonempty input. Give the sources distinct payloads and check the winning value and its reported origin. Try an incorrect fallback with a falsey value. |
| Inspection preserves state | An operation promises to describe existing state.      | Declare the fields that must survive. Compare their values before and after a real call. Try a direct assignment and a write through a helper.                                                          |
| Output round-trip          | Another supported program consumes the output.         | Use the real consumer with delimiters, empty fields, and significant whitespace. Assert the fields it recovers. Report an unavailable consumer as unresolved.                                           |

## Choose a boundary that exists in the project

- When a stored reference names a relative path, place the owner in a different directory from the caller. Resolve the reference from each location and inspect the object the public API actually opens.
- When several owners can reuse a declaration, construct two distinguishable owners in both orders. After constructing the second, invoke both and inspect their metadata.
- When an API accepts a caller-owned stream, exercise a supplied stream, an absent stream, and a stream whose operation fails. Check the documented result, error and ownership policy for each.
- When rendering makes some fields optional, remove each optional section and check that the required fields survive. For encoded output, pass empty, delimiter-containing and whitespace-containing fields through the real supported reader and compare the result with the original values.

Write down the expected behavior from the public interface before creating fixtures. If a project has no supported reader for a format, record that limit. For a required reader missing from the test environment, return an unresolved check with its name.

## Combine an AST check with a behavior check

The [Python inspection rule](./ast-grep/rules/inspection-writes.yml) matches simple and augmented assignments to
`self.field` inside `describe_*` methods. Copy the rule into your project and run
`ast-grep scan --rule checks/inspection-writes.yml src/`. Bind that command to a local check
such as `no-direct-field-write`. Include both the rule and the Python sources in its inputs.

Run the included examples with `ast-grep test --config ast-grep/sgconfig.yml --skip-snapshot-tests` from this resource directory. Qualify the rule on a small project copy. A read in `describe_mode` should pass. An assignment to
`self.mode` there should fail. A method that intentionally updates state should remain valid.
Move the write into a helper and call it from `describe_mode`. A second check should call
`describe_mode` and compare state before and after. That check owns the observable guarantee,
including changes through the helper. Other forms such as writes through containers also need behavioral coverage.

## Qualify a checker

With Tenet 0.18.0 or later, run `tenet check --qualify CONTRACT/CHECK` when introducing or changing a checker. Start with an example of a correct public behavior. Change its implementation to violate one claim, then try a separate implementation that preserves the same public behavior. A checker for a reusable declaration can exercise two independent consumers, introduce a write to shared metadata, and try a harmless change to how that metadata is copied. Inspect the observed outcome on each example before adopting the check.

## Repair and rerun

Name the executable claim under `checks` in the contract. Bind a reviewed project command
in `checks/NAME.json` beside the contract. Run `tenet check --local CONTRACT/NAME`; read the
case, evidence, and replay command. Apply a project-approved safe fixer for mechanical edits.
For behavior failures, repair the implementation and replay the same case. Run all local checks
after the repair, including those established earlier. Leave any broader unanswered question visible in the review.

After the last edit, run `tenet check --final` with Tenet 0.18.0 or later. Inspect the semantic and local results on the version you intend to submit. Use the reported replay when a required claim is still open. If you edit again, repeat the final check.
