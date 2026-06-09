"""Tests for history manager undo/redo functionality."""

import unittest
from PIL import Image

from image_editor.core.history_manager import HistoryManager, Command


class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        self.history = HistoryManager(max_history=5)
        self.image = Image.new("RGB", (100, 100), color=(255, 0, 0))

    def test_reset(self):
        self.history.reset(self.image)
        self.assertFalse(self.history.is_dirty)
        self.assertFalse(self.history.can_undo)
        self.assertFalse(self.history.can_redo)

    def test_push_and_undo(self):
        self.history.reset(self.image)
        img2 = Image.new("RGB", (100, 100), color=(0, 255, 0))
        cmd = Command("edit", img2)
        self.history.push(cmd)
        self.assertTrue(self.history.can_undo)
        result = self.history.undo()
        self.assertIsNotNone(result)
        self.assertTrue(self.history.can_redo)

    def test_max_history(self):
        self.history.reset(self.image)
        for i in range(10):
            img = Image.new("RGB", (10, 10), color=(i, i, i))
            self.history.push(Command(f"edit{i}", img))
        count = 0
        while self.history.undo():
            count += 1
        self.assertLessEqual(count, 5)

    def test_is_dirty_after_edit(self):
        self.history.reset(self.image)
        self.assertFalse(self.history.is_dirty)
        img2 = Image.new("RGB", (100, 100), color=(0, 255, 0))
        self.history.push(Command("edit", img2))
        self.history._current_image = img2
        self.assertTrue(self.history.is_dirty)

    def test_set_clean(self):
        self.history.reset(self.image)
        img2 = Image.new("RGB", (100, 100), color=(0, 255, 0))
        self.history.push(Command("edit", img2))
        self.history._current_image = img2
        self.assertTrue(self.history.is_dirty)
        self.history.set_clean(img2)
        self.assertFalse(self.history.is_dirty)


if __name__ == "__main__":
    unittest.main()
