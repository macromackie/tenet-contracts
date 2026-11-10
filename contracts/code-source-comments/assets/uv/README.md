# Source comment check

Name `assets/ast-grep/rules` of this contract under `ruleDirs` in the repository's ast-grep configuration, so the
ordinary lint reports each prose comment. The rule set covers TypeScript, TSX, Python, and Rust:

- `prose-comments-<language>` reports, as an error, every comment that is neither a tool directive nor a reason
  comment. The Python rule also reports a string that stands alone as a statement, such as a docstring.
- `reason-comments-<language>` reports, at the `info` severity, each `Why:` line comment inside a function body. It
  fails no scan; the checker below counts its reports.

Copy `source-comments.json` into the repository as `.config/source-comments.json`, set `sourceRoots`, and set
`maximumReasonComments` to the count the repository allows. Run from the repository root, replacing the installed
contract path:

```bash
uv run --script .contracts/034-code-source-comments/assets/uv/check-source-comments.py \
  --root . --config .config/source-comments.json
```

The script requires Python 3.14 or later, has no package dependencies, and runs `ast-grep` from the path with the
rule set beside it, `../ast-grep/sgconfig.yml`. It reports each prose comment, and, when the reason comments under the
source roots outnumber the maximum, each reason comment. `source-comments.schema.json` describes the policy.

Run the rules' own cases with:

```bash
ast-grep test --skip-snapshot-tests --config .contracts/034-code-source-comments/assets/ast-grep/sgconfig.yml
```

A directive passes only in the forms the rule notes list. To allow another tool's directive, copy the rule into the
repository's own rule folder and add the directive's opening word to its pattern.

These rules report the doc comments that the doc comment coverage contracts require, so a scope adopts one family or
the other. The command reports every finding and exits unsuccessfully. It changes no files.
