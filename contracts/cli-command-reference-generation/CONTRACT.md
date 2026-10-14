---
name: cli-command-reference-generation
message: Declare each command once in a model that drives both the CLI parser and its published reference.
---

## Rules

Declare every command, subcommand, argument, option, default value, and help text once, in one command model.
Build the executable's argument parser from that model.
Generate the published command reference from the same model.
Do not maintain a second command catalogue, such as a hand-written reference page or a separate list of commands, options, or defaults.
Declare the defaults the program applies, such as the default server address, in the model rather than in runtime code.
Take the version the program reports and the version recorded in the reference from one declaration.

Keep network clients, credential storage, update checks, filesystem reads, and command execution out of the command model.
Resolve the content a parsed argument points to, such as a file or standard input, in runtime code after parsing.
Limit the model's dependencies to declaring and serializing commands.
Generate the reference with a generator that depends only on the model, without building or running the full program.
Publish the reference as data with a declared schema, so documentation consumers read it without depending on the program or its build toolchain.
Fail checks when a committed copy of the reference differs from the model's current output.

Preserve command names, argument names, defaults, help text, version metadata, and the reference schema when refactoring the model, unless a product change explicitly changes them.

## Checks

Generate the reference and compare it with the program's help and version output for representative commands.
Review the generator's dependency closure, and confirm it excludes the full program and network, credential, filesystem, and execution libraries.
Search the repository for command names, options, or defaults declared outside the model.
After changing the model, diff the generated reference and confirm each changed name, default, or help line comes from an intended product change.
Build each reference consumer without the program's build toolchain.
