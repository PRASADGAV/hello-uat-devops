"""Minimal application used for the DevOps UAT dry run."""


def get_message() -> str:
    """Return the application's expected greeting."""
    return "Hello from the DevOps UAT environment!"


def main() -> None:
    """Print the greeting to standard output."""
    print(get_message())


if __name__ == "__main__":
    main()
