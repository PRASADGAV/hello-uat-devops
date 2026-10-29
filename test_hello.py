"""One basic pytest test for hello.py."""

from hello import get_message


def test_get_message() -> None:
    """The application returns the expected greeting."""
    assert get_message() == "Hello from the DevOps UAT environment!"
