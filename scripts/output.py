"""Write a library check's findings and summary to the standard streams, and end its process."""

import sys
from enum import IntEnum
from typing import NoReturn


# jscpd:ignore-start -- duplication -- Standalone checkers must carry their own output protocol.
class ExitStatus(IntEnum):
    """The statuses that the library's check scripts end with."""

    VALID = 0
    INVALID = 1


def report_findings(*, lines: list[str]) -> None:
    """Write each finding, the program's result, on its own line of standard output."""
    for line in lines:
        print(line)


def report_summary(*, line: str) -> None:
    """Write the closing summary to standard error, so standard output holds only findings."""
    print(line, file=sys.stderr)


# jscpd:ignore-end


def finish(*, status: ExitStatus) -> NoReturn:
    """End the process with the given status."""
    sys.exit(status)
