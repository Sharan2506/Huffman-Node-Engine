# HUFFMAN COMPRESSION AND DECOMPRESSION USING SECURITY AUTHENTICATION

An advanced, high-performance lossless data authentication and optimization project developed for the Design and Analysis of Algorithms (DAA) curriculum. This system features a custom variable-length character encoding engine, core command-line utility tools, and an interactive Streamlit graphical dashboard.

----

## Core Technologies and Implementation Language

The entire project architecture is engineered using Python 3. This implementation leveraging built-in memory management paradigms, abstract data structures, and optimized object manipulation to achieve high-performance data processing without external lower-level binary dependencies.

---

## Compression and Decompression Engine Mechanics

The backend architecture processes payloads via a deterministic, two-pass greedy optimization sequence:

- Compression Engine: Evaluates the raw input string to construct a precise character-frequency distribution. These frequencies are mapped into a binary Min-Heap structure to iteratively assemble a Huffman tree, assigning the shortest optimal prefix-free bit-strings to high-frequency characters. The final output is serialized alongside a JSON-formatted structural metadata header.
- Decompression Engine: Reconstructs the exact Huffman tree by reading the metadata headers embedded within the serialized storage payload. It parses the binary stream bit-by-bit from the root node downward, mapping the variable-length codes back to their original 8-bit characters with zero loss of data integrity.

---

## Dashboard Visualizations and Analytics

The front-end user interface utilizes dynamic data streaming powered by Pandas and Plotly to generate real-time metrics, including:

- Character Frequency Distribution Plots: Interactive bar charts visualizing individual character counts to illustrate why specific node weight assignments occur.
- Bit-Allocation Comparisons: Side-by-side analytical data visualizations contrasting standard 8-bit fixed character spacing against custom variable-length Huffman bit distributions.
- Performance and Metrics Dashboards: Real-time calculation graphs tracking file size reductions, localized space savings percentages, and precise compression ratio matrices.

---

## Project File Structure

The workspace contains both the production-grade visual application components and the foundational standalone execution scripts:

- huffman_gui.py: The primary modern user interface file containing the Streamlit framework, interactive configuration modules, and visualization logic.
- auth_secure.huff: The secure binary schema module responsible for system integrity checks, tree serialization, and validation tracking.
- huffman.py: The original independent CLI script engineered to handle file-to-file binary compression without relying on a graphical layout.
- huffman 3.py: The foundational command-line script engineered to read, validate, and restore compressed payloads back to standard text files.

---

## Local Setup and Execution

To run the interactive data dashboard application, execute the following command using the absolute directory target inside your terminal:

```powershell
streamlit run "c:\Users\Seenu\Downloads\DAA huffman\huffman_gui.py"
