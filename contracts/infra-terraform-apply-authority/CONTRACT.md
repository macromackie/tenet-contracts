---
name: infra-terraform-apply-authority
message: Apply infrastructure only from the exact reviewed source and saved plan, with narrowly scoped credentials.
---

## Rules

Bind CI cloud-credential trust to the immutable repository identity and the exact default-branch subject, not to a repository name or a branch pattern.
Scope each Terraform role to its root's state key, lock key, saved-plan location, and the secret paths that root requires.
Give application release jobs no access to Terraform state.
Keep identity-and-access and bootstrap state authority out of routine workflows, and change it only through an audited operator procedure.
Grant and fetch a provider credential only for roots that use that provider.

Issue credentials only after an explicit default-branch dispatch, for the exact current default-branch source, with a successful check for that commit and a pinned workflow definition.
Apply only a saved plan produced successfully for the same root, backend, source revision, and workflow run, and verify its checksum before applying it.
Reject a saved plan older than a declared, bounded window.
Serialize applies for each root, verify state lineage and serial before applying, and keep state locking and saved-plan staleness checks enabled.
For an operator apply, verify the operator's cloud identity and the reviewed source bundle's checksum, review the saved plan, and apply that same file.
Record the source, plan, and operator provenance with the work item that authorized the change.
Do not treat a merged source change or an automation invocation as authority to change live infrastructure.

Keep plans and state private and encrypted, and never publish them as CI artifacts or commit them.
Emit provenance and operation counts in workflow output, never resource attribute values.
Supply provider credentials through the execution environment rather than through variables or data that Terraform stores in state, and keep them out of command output.

Require operator review for changes made with an account-wide provider credential; restricting state access does not restrict provider credentials.
Qualify a scoped provider credential against every operation its roots need before claiming provider isolation or switching to it.
Never fall back to a broader provider credential for an unattended change when a scoped grant is missing.

## Checks

Run `terraform fmt -check` and `terraform validate` in each changed root without production credentials.
Review each trust policy for the repository identity and subject it binds, and each role policy for the state, lock, plan, and secret paths it grants.
Confirm that the workflow requests credentials only after the dispatch, source, and check conditions pass, and that apply consumes the checksummed saved plan for the same root and revision.
Exercise a stale or mismatched saved plan and confirm that apply refuses it.
Collect operator evidence for live denial checks, identity readback, and provider qualification; passing source checks cannot establish them.
