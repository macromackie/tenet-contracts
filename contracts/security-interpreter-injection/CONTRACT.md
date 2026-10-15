---
name: security-interpreter-injection
message: Pass untrusted input to interpreters only as bound data, never as code, commands, query text, templates, or type-constructing serialized objects.
---

## Rules

Treat as untrusted any input from outside the process's trust boundary, including request data, uploaded files, messages, third-party responses, model output, and stored values that came from them.
An interpreter is anything that runs its input: a language's evaluate or execute facility, a shell, a query language, a template engine, and a deserializer that can construct arbitrary types.

Never pass untrusted input to a language's evaluate or execute facility, a dynamic import, or reflection that selects a type, function, or module by name.
Map untrusted names to code through an explicit allowlist of known handlers.
Run external commands with an argument list and no shell, and never interpolate untrusted input into a shell command string.
Place untrusted arguments after an end-of-options marker, such as `--`, wherever the command would otherwise read one as an option.
Bind untrusted values as query parameters, and never build query text by concatenating or formatting them.
Choose untrusted identifiers, such as a sort column or a table name, from an explicit allowlist, because parameters cannot bind identifiers.
Render templates only from trusted template source, and pass untrusted input as template variables with the engine's escaping enabled.
Escaping or filtering untrusted input does not satisfy these rules where the interpreter accepts parameters, argument lists, or variables.

Deserialize untrusted bytes only with a parser that produces plain data, such as a JSON parser or a YAML loader restricted to standard types.
Never deserialize untrusted bytes with a format or loader that can construct arbitrary types or run code on load, such as native object serialization, object-constructing YAML loaders, or model checkpoint formats that execute code.
Load code-bearing artifacts, such as plugins, serialized objects, and executable model files, only from sources verified by digest or signature.

A feature whose purpose is to run code that a user or model wrote may run it inside an isolated sandbox that holds no credentials or network access its author does not already have.

Violation: query text built as `"SELECT total FROM orders WHERE id = '" + orderId + "'"` from a request parameter.
Allowed: query text `SELECT total FROM orders WHERE id = ?` with the order identifier bound as a parameter.
Violation: a shell command string that interpolates an uploaded file's name.

## Checks

Search changed code for evaluate and execute facilities, dynamic imports, shell invocations, query construction, template rendering, and deserialization, and trace each input to its source.
Send a value containing quotes, shell metacharacters, template delimiters, and a leading `-` through each changed entry point, and confirm that it arrives as literal data.
For each deserialization of external bytes, name the format and confirm that it cannot construct arbitrary types.
Confirm that each loaded plugin or executable model file is verified by digest or signature before it loads.
