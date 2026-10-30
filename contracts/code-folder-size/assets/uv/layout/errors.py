"""Invalid layout declarations that cannot produce a trustworthy check."""


class LayoutRejected(ValueError):
    """The layout policy does not describe bounded repository source roots."""
