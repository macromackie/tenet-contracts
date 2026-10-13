---
name: infra-terraform-state-ownership
message: Keep one state owner per resource and preserve data and physical identities through ownership transfers.
---

## Rules

Keep exactly one live Terraform state owner for every resource.
Never apply a root that declares a resource another state already owns, and never recreate an existing resource to change its owner.
Manage persistent resources in Terraform, manage deployed code and its runtime bindings through application releases, and give each resource attribute exactly one owner.
Do not treat a data source or cached lookup that reads a resource as ownership of it.
Manage secret containers in Terraform without declaring their secret values or versions, and leave the values to their operators.

Preserve physical names, resource identifiers, state lineage, secret values, database roles, stored contents, migration histories, and deletion guards such as `prevent_destroy` when ownership moves.
Record each reviewed address change as a state move, such as a `moved` block, that keeps the same physical resource; an address rename does not authorize recreation.

Freeze every writer of the affected states and privately back up both states before a transfer.
Compare resource identifiers and addresses, transfer ownership, then verify the resulting states before any apply.
Preserve each existing state's lineage while state writes advance its serial.
Record a new backend's fresh lineage and initial serial, and compare managed attributes and outputs rather than recomputed metadata.
Transfer existing resources into a newly extracted root before its first apply; an empty destination state must never recreate existing resources.
Apply nothing in a destination root until its plan proposes no replacement, deletion, secret version change, or credential change for transferred resources.
Retire the obsolete source, workflow mappings, and grants only after verifying that the former state manages zero instances of the transferred resources.

## Checks

Run `terraform fmt -check` and `terraform validate` in each changed root without production credentials.
List the resources in each affected state and confirm that no resource appears in more than one state.
Compare source, backend, and resource identities against operator inventories and state backups; static validation cannot prove that data was preserved.
For an ownership transfer, confirm that the first destination plan proposes no replacement, deletion, secret version change, or credential change.
