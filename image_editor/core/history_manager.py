"""Undo/redo history management using the Command pattern."""

from dataclasses import dataclass
from typing import Optional, List
from PIL.Image import Image


@dataclass
class Command:
    """Represents a single reversible edit operation."""
    name: str
    pre_image: Image


class HistoryManager:
    """Manages a finite stack of image editing commands."""

    def __init__(self, max_history: int = 20):
        self.max_history = max_history
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []
        self._clean_image: Optional[Image] = None
        self._current_image: Optional[Image] = None

    @property
    def can_undo(self) -> bool:
        return len(self._undo_stack) > 0

    @property
    def can_redo(self) -> bool:
        return len(self._redo_stack) > 0

    @property
    def is_dirty(self) -> bool:
        if self._current_image is None or self._clean_image is None:
            return False
        return self._current_image.tobytes() != self._clean_image.tobytes()

    def reset(self, image: Image) -> None:
        """Reset history with a fresh image (e.g., after opening or saving)."""
        self._undo_stack.clear()
        self._redo_stack.clear()
        self._clean_image = image.copy()
        self._current_image = image.copy()

    def push(self, command: Command) -> None:
        """Push a new command onto the undo stack."""
        self._undo_stack.append(command)
        self._redo_stack.clear()

        # Enforce max history
        if len(self._undo_stack) > self.max_history:
            self._undo_stack.pop(0)

        self._current_image = command.pre_image

    def undo(self) -> Optional[Image]:
        """Undo the last command and return the previous image state."""
        if not self.can_undo:
            return None
        command = self._undo_stack.pop()
        self._redo_stack.append(command)
        self._current_image = command.pre_image
        return command.pre_image

    def redo(self) -> Optional[Image]:
        """Redo the last undone command.
        
        Returns the image AFTER the redone command was applied.
        Since we only store pre_image, the caller must have the 
        post_image state already or re-apply the operation.
        """
        if not self.can_redo:
            return None
        # We return the command info; caller re-applies operation
        return self._redo_stack[-1]

    def pop_redo(self) -> Optional[Command]:
        """Pop and return the redo command for actual redo use."""
        if not self.can_redo:
            return None
        return self._redo_stack.pop()

    def set_clean(self, image: Image) -> None:
        """Mark the current image state as saved/clean."""
        self._clean_image = image.copy()
