import logging


def configure_logging() -> None:
    # TODO: Add structured logging handlers and request correlation IDs.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
