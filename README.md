# HUFFMAN COMPRESSION AND DECOMPRESSION USING SECURITY AUTHENTICATION

An advanced, high-performance lossless data authentication and optimization project developed for the Design and Analysis of Algorithms (DAA) curriculum. This system features a custom variable-length character encoding engine wrapped inside a streamlined Streamlit visual dashboard.

---

## Key Features

- Optimal Prefix Coding Engine: Implements a greedy algorithmic approach utilizing a binary Min-Heap data structure to dynamically assign variable-length paths based on character frequency.
- High-Impact Visualization Dashboard: Built using Streamlit, Plotly, and Pandas to deliver real-time data analysis, frequency charts, and interactive compression metrics.
- Secure Binary Serialization: Packages compression trees and encrypted structures safely into a specialized .huff binary schema integrated with JSON-based metadata headers.
- Bit-Level Integrity Verification: Employs precise recovery validation to ensure 100% accurate, lossless reconstruction of compressed data payloads.

---

## Technical Architecture and Metrics

The compression algorithm fundamentally optimizes standard data structures, achieving localized payload reductions between 40% to 55% depending on character entropy.

| Module Components | Core Responsibility | Technologies Used |
| :--- | :--- | :--- |
| Algorithmic Backend | Greedy frequency distribution and tree parsing | Python 3, Min-Heaps |
| Data Analytics | Dynamic file structure tracking and mapping | Pandas, NumPy |
| Visual Interface | Real-time compression visualizer charts | Streamlit, Plotly |
| Storage Layer | Secure, structured recovery checkpoints | .huff Binary Schema |

---

## Project File Structure

- huffman_gui.py: The main execution script powering the graphical user interface, stream charts, and data logic panels.
- auth_secure.huff: The production-grade binary module managing secure node storage and file integrity tracking.

---

## Local Setup and Execution

Since this app operates completely independently of strict workspace constraints, you can launch the dashboard using an absolute path directly from your terminal:

```powershell
streamlit run "c:\Users\Seenu\Downloads\DAA huffman\huffman_gui.py"