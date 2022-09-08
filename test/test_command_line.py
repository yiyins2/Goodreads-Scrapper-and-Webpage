import argparse
from unittest import TestCase
from goodreads.command_line import CommandLine


class TestCommandLine(TestCase):
    def test_negative_max_books(self):
        command = CommandLine(["--max_books", "-1"])
        self.assertRaises(argparse.ArgumentError, command.check_args)

    def test_negative_max_authors(self):
        command = CommandLine(["--max_authors", "-1"])
        self.assertRaises(argparse.ArgumentError, command.check_args)

    def test_max_books_warning(self):
        command = CommandLine(["--max_books", "300"])
        self.assertWarns(Warning, command.check_args)

    def test_max_authors_warning(self):
        command = CommandLine(["--max_authors", "300"])
        self.assertWarns(Warning, command.check_args)

    def test_invalid_start_url(self):
        command = CommandLine(["--start_url", "https://illinois.edu/"])
        self.assertRaises(argparse.ArgumentError, command.check_args)

    def test_invalid_import_path(self):
        command = CommandLine(["--import_json", "xxx.json"])
        self.assertRaises(argparse.ArgumentError, command.check_args)