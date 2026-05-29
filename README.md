# Blood-Type-Predictor-Bioinformatics-Project
Dabbling in a new branch and or field within the realm of bioinformatics. This time we are attempting to use code to predict blood type.

# 🧬 ABO-H Phenotyper

**A bioinformatics tool to predict ABO blood type phenotype from genetic data.**

Built as a portfolio project combining genetics, bioinformatics, and interactive visualization.

![Cover](cover.png)

## ✨ Features

- Predict ABO blood type (A, B, AB, O) using key genetic variants
- H antigen expression insights (biochemical context)
- Support for **Key SNPs** and **FASTA sequence** upload
- Interactive antigen expression visualization
- Educational explanations for research/transfusion context

## Why This Matters

DNA-based blood typing is especially useful when:
- Patient received recent blood transfusions
- Serological testing shows discrepancies
- Studying rare subgroups or population genetics

## How to Use

### Option 1: Key SNPs (Recommended)
Enter the 5 critical positions in the ABO gene.

### Option 2: FASTA Upload
Upload a sequence covering exon 6/7 of the ABO gene.

## Tech Stack

- **Python** + **Streamlit**
- **Biopython** (sequence parsing)
- **Plotly** (visualizations)

## Installation

```bash
git clone https://github.com/yourusername/abo-h-phenotyper.git
cd abo-h-phenotyper
pip install streamlit biopython pandas plotly
streamlit run app.py
