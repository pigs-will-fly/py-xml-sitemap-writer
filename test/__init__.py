"""
Generic helper functions
"""
from typing import Iterator


def urls_iterator(count: int = 10, prefix: str = 'page_', host: str = 'http://example.net') -> Iterator[str]:
    """
    Returns URLs iterator
    """
    for idx in range(1, count + 1):
        yield f'{host}/{prefix}_{idx}.html'
