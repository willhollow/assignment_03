"""Process a series of package files and keep a running total across reruns."""

import json

import streamlit as st

from packaging_parser import parse_packaging


st.title("Process Package Files")

if "files_processed" not in st.session_state:
    st.session_state.files_processed = 0
    st.session_state.packages_processed = 0
    st.session_state.history = []

package_file = st.file_uploader("Upload package file:", type="txt", key="package_file")
process_clicked = st.button("Process file", key="process")

if process_clicked and package_file is not None:
    package_text = package_file.read().decode("utf-8")
    package_lines = package_text.splitlines()

    parsed_packages = []
    for line in package_lines:
        line = line.strip()
        if not line:
            continue
        parsed_packages.append(parse_packaging(line))

    json_filename = f"data/{package_file.name.replace('.txt', '.json')}"
    with open(json_filename, "w") as file:
        json.dump(parsed_packages, file)

    st.session_state.files_processed += 1
    st.session_state.packages_processed += len(parsed_packages)
    st.session_state.history.append(f"{len(parsed_packages)} packages written to {json_filename}")

left, right = st.columns(2)
with left:
    st.metric("Files processed", st.session_state.files_processed)
with right:
    st.metric("Packages processed", st.session_state.packages_processed)

for message in st.session_state.history:
    st.info(message)
