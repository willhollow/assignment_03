"""
process_file.py — Part 2: one file of package descriptions, uploaded.

A Streamlit app that accepts an uploaded text file with one package description
per line, shows the total for every line, and writes the parsed packages to a
JSON file in the `data/` folder — `data/packaging1.txt` in, `data/packaging1.json`
out.

New here: an uploaded file arrives as **bytes**, not text, so it has to be
decoded before it can be split into lines. And a text file usually ends with a
newline, so the last "line" is empty and must be skipped rather than parsed.

Run it:  Run and Debug -> "Streamlit Run: Current File"   (see README Reference #1)
Test it: pytest tests/test_streamlit.py -k process_file
"""

import json

import streamlit as st

from packaging_parser import calc_total_units, get_unit, parse_packaging


st.title("Process File of Packages")

package_file = st.file_uploader(
    "Upload a package file:",
    type="txt",
    key="package_file",
)

if package_file:
    package_text = package_file.read().decode("utf-8")
    package_lines = package_text.splitlines()

    parsed_packages = []
    for line in package_lines:
        line = line.strip()
        if not line:
            continue
        package = parse_packaging(line)
        parsed_packages.append(package)
        total = calc_total_units(package)
        unit = get_unit(package)
        st.info(f"{line} ➡️ Total 📦 Size: {total} {unit}")

    json_filename = f"data/{package_file.name.replace('.txt', '.json')}"
    with open(json_filename, "w") as file:
        json.dump(parsed_packages, file)

    st.success(f"{len(parsed_packages)} packages written to {json_filename}")
