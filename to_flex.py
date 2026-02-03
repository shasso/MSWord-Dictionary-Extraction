#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
to_flex.py
~~~~~~~~~
A minimal module that demonstrates how to create a single dictionary entry
using the ``entry`` helper from ``utils.py`` and wrap it in a well‑formed XML
container.

The function ``convert_to_flex`` builds a dummy entry with one sense,
prints the raw XML returned by ``entry`` and then prints the complete XML
document that encloses the entry.
"""

# The utils module is expected to provide an ``entry`` function that returns an
# XML fragment for a single dictionary entry.
# Example signature (in utils.py):
#     def entry(word: str, senses: list[str]) -> str:
#         ...


import os
from bailis_extraction.utils import entry


def convert_to_flex() -> None:
    """
    Create a dummy dictionary entry with a single sense, print the entry XML,
    and then print the entry wrapped inside a well‑formed ``<dictionary>`` XML
    container.
    """
    # Dummy data – you can replace these with real values later.
    dummy_word = "example"
    dummy_definition = "placeholder definition"
    dummy_gram_info = "noun"
    dummy_bib = "bailis"

    # Build the entry XML using the helper from utils.py.
    entry_xml, entry_tree = entry(dummy_word, dummy_definition, dummy_gram_info, dummy_bib)

    # Print the raw entry (useful for debugging).
    print("Raw entry XML:")
    print(entry_xml)

    # Use the raw entry XML (already well‑formed) for inclusion in the wrapper.
    pretty_entry = entry_xml

    # Wrap the pretty entry in a top‑level container to produce a complete XML document.
    full_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    {pretty_entry}
    """

    print("\nFull XML document:")
    print(full_xml)


if __name__ == "__main__":
    convert_to_flex()