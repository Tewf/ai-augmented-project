# Checks run from the root

**Date:** 2026-11-03
**Type:** fact
**Source:** `python3 -m unittest discover -s checks`

The tests of a task sit in `checks/` and are found by unittest discovery from the project root.
A module that a test imports sits at the root.
