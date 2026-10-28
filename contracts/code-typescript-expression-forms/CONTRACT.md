---
name: code-typescript-expression-forms
message: Destructure same-name TypeScript reads, use shorthand properties, expression-bodied arrows, template strings, `replaceAll`, `===`, and `for (;;)`, and convert or parse values with comparisons, `Boolean`, `Number`, or `String`.
requires-tenet: 0.11.0
---

## Rules

Read an object's property into a variable of the same name by destructuring it, such as `const { usage } = response.data`, never `const usage = response.data.usage`.
This holds for `const` and `let`, for a property named by a string literal, such as `response.data['usage']`, and for an assignment, written `({ cursor } = page)`.
An optional chain, a private field, `super`, and an annotated declaration, such as `const writeEvent: EventSink = sinks.writeEvent`, keep the plain read.
A variable named differently from its property, such as `const total = invoice.amount`, and an array element read by index or by destructuring are outside this rule.

Build every string that joins text with a value or with other text as a template literal, such as `` `Invoice ${invoice.id} is due` ``, never with `+`.
This holds for every `+` with a string operand, whether the other operand is a literal, a variable, or a call, such as `title + suffix` on two strings.
Write a long text, such as a prompt, as one literal whose source lines break exactly where the text does, never as literals joined with `+`.
Appending to a string with `+=` is outside this rule, but its right side follows it, such as `` frame += `${line}\n` ``, never `frame += line + '\n'`.

Never convert a value with an operator, such as `!!invoice`, `+digits`, `digits * 1`, `digits - 0`, `'' + count`, or `label += ''`.
Turn a string, number, or optional boolean into a boolean as `code-typescript-boolean-conditions` requires.
Call `Boolean(invoice)` only on a value whose type is an object, array, or function that may be `null` or `undefined`, such as the result of `invoices.find((invoice) => isOverdue({ invoice }))`.
Convert a value to a number with `Number(digits)` and to a string with `String(count)`, never with a template that holds only the value, such as `` `${count}` ``.
Parse decimal text the same way, `Number(digits)`, after taking the digits out of any longer text, never with `parseFloat`, `Number.parseFloat`, or a `parseInt` that reads base 10.
Parse text in another base with `Number.parseInt` and its radix, such as `Number.parseInt(byte, HEX_RADIX)`, never with the global `parseInt`.
Never use a bitwise operator, such as `position | 0`, `flags & MASK`, or `~name.indexOf('-')`, and test whether a string holds some text with `includes`, such as `name.includes('-')`.

Give an arrow function that only returns a value an expression body, such as `(line) => ({ amount: line.amount })`, never a block holding only `return`.
Write each property whose value is a same-name variable in shorthand, such as `{ invoice }`, never `{ invoice: invoice }`, and list functions as `code-typescript-object-literal-functions` requires.

Replace every match with `replaceAll`, such as `title.replaceAll('-', '_')`, never with `replace` and a regular expression flagged `g`, and call `replace` only to change the first match.
Pass `replaceAll` plain text as a string, never as a regular expression such as `/-/gv`, and keep a regular expression for a pattern, such as `/\s+/gv`.
Give every regular expression the `v` flag, such as `/\s+/gv` or `new RegExp(pattern, 'v')`, so that its syntax is strict and its character classes read Unicode.

Compare with `===` and `!==`, never with `==` or `!=`, even against `null`.
Write a loop that runs until its body leaves as `for (;;)`, never as `while (true)` or `do { ... } while (true)`.
Never test a condition that is constant as written, such as `if (true)`, `while (1)`, or `if (isReady || true)`.

Configure the repository's lint to reject each form these rules forbid wherever a tool supports it, and suppress a finding only as `code-lint-suppressions` allows.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.

Violation: `const usage = response.data.usage` and, in a loop over pages, `cursor = page.cursor` read a same-name property without destructuring it.
Allowed: `const { usage } = response.data`, `({ cursor } = page)` in a loop that advances `cursor`, and `const total = invoice.amount`.
Violation: `const label = 'Invoice ' + invoice.id`, and a prompt written as `'Review the invoice, ' +` with `'then list each overdue line.'` on the next line.
Allowed: `` const label = `Invoice ${invoice.id}` `` and `const prompt = 'Review the invoice, then list each overdue line.'` on one line.
Violation: `const hasInvoice = !!found`, `const amount = +digits`, and `const count = digits * 1` convert with operators.
Violation: `` const label = `${count}` `` converts a lone value with a template that joins nothing.
Allowed: `const hasNote = invoice.note !== ''`, `const hasInvoice = Boolean(found)` after `const found = invoices.find((invoice) => isOverdue({ invoice }))`, `const amount = Number(digits)`, and `const label = String(count)`.
Violation: `parseInt(digits, DECIMAL_RADIX)`, `Number.parseInt(digits)`, and `Number.parseFloat(digits)` parse decimal text.
Allowed: `const quantity = Number(digits)` and `const value = Number.parseInt(byte, HEX_RADIX)`.
Violation: `invoices.map((invoice) => { return invoice.total; })` wraps a lone `return` in a block.
Allowed: `invoices.map((invoice) => invoice.total)` and `lines.map((line) => ({ amount: line.amount }))`.
Violation: `return { invoice: invoice, total }` writes a same-name property in full.
Allowed: `return { invoice, total }` and `return { owner: account }`.
Violation: `title.replace(/-/gv, '_')` and `title.replaceAll(/-/gv, '_')` replace plain text through a global regular expression.
Allowed: `title.replaceAll('-', '_')`, `title.replaceAll(/\s+/gv, ' ')`, and `title.replace('-', '_')` to change only the first dash.
Violation: `title.replaceAll(/\s+/g, ' ')` omits the `v` flag, and `const page = offset | 0` truncates a number with a bitwise operator.
Allowed: `title.replaceAll(/\s+/gv, ' ')` and `const page = Math.trunc(offset)`.
Violation: `invoice.currency == account.currency` compares with `==`.
Allowed: `invoice.currency === account.currency`.
Violation: `while (true)` wraps a loop that reads pages until the last one, and `if (true)` tests a fixed condition.
Allowed: `for (;;)` wraps the same loop, which returns after reading the last page.

## Checks

Run the repository's lint from the repository root, and confirm that it rejects `const usage = response.data.usage`, `'Invoice ' + id`, literals joined with `+` across lines, and `!!invoice`.
Confirm that the same run rejects `` `${count}` ``, `{ invoice: invoice }`, `title.replace(/-/gv, '_')`, `/\s+/g`, `offset | 0`, `Number.parseInt(digits, 10)`, `total == limit`, and `while (true)`.
For each `+` a change adds whose operands are both variables or calls, is either operand a string, which the lint cannot see without types?
For each `Boolean(x)` a change adds, including one the lint's fix wrote, is `x` an object, array, or function that may be `null` or `undefined`?
For each long text a change adds, is it one literal whose source lines break exactly where the text does?
For each `Number.parseInt` a change adds, does its radix name a base other than 10, which the lint cannot see through a constant?
For each `replace` call a change adds, is changing only the first match what the code needs?
