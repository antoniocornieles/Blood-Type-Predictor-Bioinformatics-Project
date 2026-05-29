import streamlit as st
from Bio import SeqIO
import pandas as pd
from io import StringIO
import plotly.express as px

st.set_page_config(page_title="ABO-H Phenotyper", page_icon="🧬", layout="wide")
st.title("🧬 ABO-H Phenotyper")
st.markdown("**Bioinformatics Research Tool** — Predict ABO blood type phenotype from genetic data with H antigen insights")

# ====================== SIDEBAR ======================
st.sidebar.header("About")
st.sidebar.info(
    "This tool predicts ABO blood type by analyzing key variants in the ABO gene.\n\n"
    "Useful for transfusion research, resolving serological discrepancies, and population genetics."
)

input_method = st.sidebar.radio("Input Method",
    ["Key SNPs (Recommended)", "FASTA Sequence"])

# ====================== CORE PREDICTION ======================
def predict_abo(del261="Absent", c526="C", c703="G", c796="C", c803="G"):
    is_o = del261 == "Present"
    has_a = (c526 == "G" or c703 == "A")
    has_b = (c796 == "A" or c803 == "C")

    if is_o and not (has_a or has_b):
        return "O", "High", "Full H antigen remains"
    elif has_a and has_b:
        return "AB", "Low", "Both A and B antigens expressed"
    elif has_a:
        return "A", "Medium", "A antigen expressed"
    elif has_b:
        return "B", "Medium", "B antigen expressed"
    return "Unknown", "Unknown", "Could not determine phenotype"

def show_results(phenotype, h_level, explanation, input_summary):
    col1, col2 = st.columns([2, 1])

    with col1:
        st.success(f"**Predicted Blood Type: {phenotype}**")
        st.metric("H Antigen Level", h_level)
        st.info(explanation)

    with col2:
        # Antigen Expression Visualization
        fig = px.bar(
            x=["H Antigen", "A Antigen", "B Antigen"],
            y=[90 if phenotype == "O" else 30,
               85 if phenotype in ["A", "AB"] else 5,
               85 if phenotype in ["B", "AB"] else 5],
            color=["H", "A", "B"],
            title="Estimated Surface Antigen Expression"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Input Summary")
    st.json(input_summary)

# ====================== KEY SNPs INPUT ======================
if input_method == "Key SNPs (Recommended)":
    st.subheader("Enter Key ABO Variants")
    col1, col2 = st.columns(2)

    with col1:
        del261 = st.selectbox("261delG (O allele marker)", ["Absent", "Present"])
        c796 = st.selectbox("796C>A", ["C", "A"])
        c803 = st.selectbox("803G>C", ["G", "C"])

    with col2:
        c526 = st.selectbox("526C>G", ["C", "G"])
        c703 = st.selectbox("703G>A", ["G", "A"])

    if st.button("🔬 Predict Blood Type", type="primary"):
        phenotype, h_level, explanation = predict_abo(del261, c526, c703, c796, c803)
        show_results(phenotype, h_level, explanation, {
            "261delG": del261,
            "526C>G": c526,
            "703G>A": c703,
            "796C>A": c796,
            "803G>C": c803
        })

# ====================== FASTA INPUT ======================
elif input_method == "FASTA Sequence":
    st.subheader("Upload ABO Gene Sequence (Exon 6/7)")
    uploaded = st.file_uploader("Choose FASTA file", type=["fasta", "fa", "txt"])

    if uploaded:
        try:
            content = uploaded.getvalue().decode("utf-8")
            sequences = list(SeqIO.parse(StringIO(content), "fasta"))

            if sequences:
                seq = str(sequences[0].seq).upper()
                st.success(f"✅ Sequence loaded: {len(seq):,} base pairs")

                if st.button("🔬 Analyze Sequence", type="primary"):
                    # Placeholder: In real version you'd align and call variants
                    # For now we use default (you can improve this later)
                    phenotype, h_level, explanation = predict_abo()
                    show_results(phenotype, h_level, explanation, {
                        "Input": "FASTA Sequence",
                        "Length": f"{len(seq):,} bp",
                        "Note": "Key variant extraction under development"
                    })
        except Exception as e:
            st.error(f"Failed to read file: {e}")

# ====================== FOOTER ======================
st.caption("ABO-H Phenotyper v1.0 • Portfolio Project • Built with Biopython + Streamlit")
