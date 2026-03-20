import io
import importlib.util
import pathlib
import unittest
from contextlib import redirect_stderr
from unittest.mock import patch

MODULE_PATH = (
    pathlib.Path(__file__).resolve().parent.parent
    / "skills"
    / "convert-sc-design-hblab"
    / "scripts"
    / "read_sheet.py"
)
MODULE_SPEC = importlib.util.spec_from_file_location("read_sheet_under_test", MODULE_PATH)
read_sheet = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(read_sheet)


class ResolveSheetNameTests(unittest.TestCase):
    def test_resolve_sheet_name_uses_gid_when_provided(self):
        metadata = {
            "sheets": [
                {"properties": {"sheetId": 7, "title": "First"}},
                {"properties": {"sheetId": 12, "title": "Target"}},
            ]
        }

        sheet_name = read_sheet.resolve_sheet_name(
            metadata,
            sheet_name="Ignored",
            gid="12",
        )

        self.assertEqual(sheet_name, "Target")

    def test_resolve_sheet_name_falls_back_to_first_sheet(self):
        metadata = {
            "sheets": [
                {"properties": {"sheetId": 7, "title": "First"}},
                {"properties": {"sheetId": 12, "title": "Target"}},
            ]
        }

        sheet_name = read_sheet.resolve_sheet_name(
            metadata,
            sheet_name="",
            gid="",
        )

        self.assertEqual(sheet_name, "First")

    def test_resolve_sheet_name_exits_when_gid_is_missing(self):
        metadata = {
            "sheets": [
                {"properties": {"sheetId": 7, "title": "First"}},
            ]
        }

        with redirect_stderr(io.StringIO()):
            with patch.object(read_sheet.sys, "exit", side_effect=SystemExit) as exit_mock:
                with self.assertRaises(SystemExit):
                    read_sheet.resolve_sheet_name(
                        metadata,
                        sheet_name="",
                        gid="12",
                    )

        exit_mock.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
