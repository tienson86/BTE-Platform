"""Ten Gods Core Engine exceptions."""


class TenGodsEngineError(Exception):
    """Base error for Ten Gods Core Engine."""


class TenGodsValidationError(TenGodsEngineError):
    """Invalid chart or input."""


class TenGodsLoaderError(TenGodsEngineError):
    """Hidden stem or rule loader failure."""
