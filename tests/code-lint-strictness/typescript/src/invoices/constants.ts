/** The provider's invoice collection. */
export const INVOICE_URL = "https://invoices.example.com/v1/invoices";

/** How long one provider read may take. */
export const READ_DEADLINE = "5 seconds";

/** How long the job waits for a settlement before it gives up. */
export const SETTLEMENT_DEADLINE = "1 minute";

/** How many reminders the job sends at once. */
export const REMINDER_CONCURRENCY = 4;

/** How long the job waits between settlement reads. */
export const POLL_INTERVAL = "2 seconds";
