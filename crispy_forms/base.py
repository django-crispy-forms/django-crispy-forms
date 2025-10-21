from __future__ import annotations

from typing import TYPE_CHECKING, Collection

if TYPE_CHECKING:
    from types import TracebackType

    from django.template import Context, Node


class KeepContext:
    """
    Context manager that receives a `django.template.Context` instance and a list of keys

    Once the context manager is exited, it removes `keys` from the context, to avoid
    side effects in later layout objects that may use the same context variables.

    Layout objects should use `extra_context` to introduce context variables, never
    touch context object themselves, that could introduce side effects.
    """

    def __init__(self, context: Context, keys: Collection[int | str | Node]) -> None:
        self.context = context
        self.keys = keys

    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        type: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        for key in list(self.keys):
            if key in self.context:
                del self.context[key]
