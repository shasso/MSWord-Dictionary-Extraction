#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""to_flex.py
~~~~~~~~~~
Final clean implementation: InputDriver + GADriver + CLI + pretty XML output.
"""

from __future__ import annotations

import argparse
import abc
import csv
import os
from typing import Iterator, Tuple, Optional

import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

import bailis_extraction.utils as utils


class InputDriver(abc.ABC):
    @abc.abstractmethod
    def generate_entries(self) -> Iterator[Tuple[str, object]]:
        """Yield tuples `(xml_string, ElementTree)` for each entry."""


class GADriver(InputDriver):
    """CSV driver for Giwargiz Aghassi format.

    Expects a CSV with header containing `English` and one or more columns
    starting with `Assyrian` (case-insensitive). For each non-empty Assyrian
    cell we call `utils.entry(aii_lexeme, en_definition, gram_info, bib)`.
    """

    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def generate_entries(self) -> Iterator[Tuple[str, object]]:
        with open(self.csv_path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                en_definition = (row.get("English") or "").strip()
                gram_info = "noun"
                bib = "Giwargis_Aghassi"

                for key, value in row.items():
                    if not key:
                        continue
                    if key.lower().startswith("assyrian") and (value or "").strip():
                        aii_lexeme = value.strip()
                        xml_string, tree = utils.entry(aii_lexeme, en_definition, gram_info, bib)
                        yield xml_string, tree


def build_dictionary_tree(entries: Iterator[Tuple[str, object]]) -> ET.Element:
    """Return an `<dictionary>` element containing all parsed `<entry>` children."""
    root = ET.Element("dictionary")
    for xml_string, _tree in entries:
        if not xml_string or not xml_string.strip():
            continue
        try:
            entry_elem = ET.fromstring(xml_string)
        except Exception:
            entry_elem = ET.fromstring(xml_string.strip())
        root.append(entry_elem)
    return root


def write_pretty_xml(root: ET.Element, out_path: str) -> None:
    """Write a pretty-printed XML document (UTF-8) with declaration."""
    rough = ET.tostring(root, encoding="utf-8")
    reparsed = minidom.parseString(rough)
    pretty_bytes = reparsed.toprettyxml(indent="  ", encoding="utf-8")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(pretty_bytes)


def write_raw_entries(entries: Iterator[Tuple[str, object]], out_path: str) -> None:
    """Append raw entry fragments to `out_path`, one entry per line (UTF-8)."""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "a", encoding="utf-8") as fh:
        for xml_string, _tree in entries:
            if not xml_string:
                continue
            fh.write(xml_string)
            fh.write("\n")


def convert_from_driver(driver: InputDriver, out_path: str, pretty: bool = True) -> None:
    entries = driver.generate_entries()
    if pretty:
        root = build_dictionary_tree(entries)
        write_pretty_xml(root, out_path)
    else:
        write_raw_entries(entries, out_path)


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="Convert input to FLEX LIFT entries")
    parser.add_argument("--driver", "-d", choices=["ga"], default="ga",
                        help="Input driver type (ga = Giwargiz Aghassi CSV)")
    parser.add_argument("--input", "-i",
                        default=os.path.join("data", "Giwargiz Aghassi Small Dictionary.csv"),
                        help="Input file path for the driver")
    parser.add_argument("--output", "-o",
                        default=getattr(utils, "file_path", os.path.join("data", "output.lift")),
                        help="Output XML file path")
    parser.add_argument("--raw", action="store_true",
                        help="Write raw entries one-per-line instead of a pretty XML document")
    args = parser.parse_args(argv)

    if args.driver == "ga":
        driver = GADriver(args.input)
    else:
        raise SystemExit(f"Unknown driver: {args.driver}")

    print(f"Driver={args.driver} input={args.input} output={args.output} raw={args.raw}")
    convert_from_driver(driver, args.output, pretty=not args.raw)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
