# Choose a local check

Start with a public behavior and the mistake a check should expose. Bind the check locally with
Tenet 0.17.0 or later. With an earlier release, invoke the checker through the project's test command.

| Recipe                     | Bind it when                                           | Exercise it                                                                                                                                                                                             |
| -------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Consumer agreement         | Two public operations promise the same interpretation. | Supply the same boundary input to both. Verify what each consumer does with the interpretation. Break one consumer in a temporary copy and check that its example fails.                                |
| Input provenance           | A value can come from several sources.                 | State the policy for absent, empty, and ordinary nonempty input. Give the sources distinct payloads and check the winning value and its reported origin. Try an incorrect fallback with a falsey value. |
| Inspection preserves state | An operation promises to describe existing state.      | Declare the fields that must survive. Compare their values before and after a real call. Try a direct assignment and a write through a helper.                                                          |
| Output round-trip          | Another supported program consumes the output.         | Use the real consumer with delimiters, empty fields, and significant whitespace. Assert the fields it recovers. Report an unavailable consumer as unresolved.                                           |

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

## Repair and rerun

Name the executable claim under `checks` in the contract. Bind a reviewed project command
in `checks/NAME.json` beside the contract. Run `tenet check --local CONTRACT/NAME`; read the
case, evidence, and replay command. Apply a project-approved safe fixer for mechanical edits.
For behavior failures, repair the implementation and replay the same case. Run all local checks
after the repair, including those established earlier. Leave any broader unanswered question visible in the review.
