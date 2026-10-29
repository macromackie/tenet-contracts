import { Schema } from "effect";

/** A record this repository owns, declared as a schema class. */
export class Account extends Schema.Class<Account>("Account")({ id: Schema.String }) {}
