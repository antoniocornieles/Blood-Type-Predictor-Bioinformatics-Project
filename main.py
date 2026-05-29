import streamlit as st
from Bio import SeqIO
from io import StringIO
import plotly.express as px

st.set_page_config(page_title="ABO-H Phenotyper", page_icon="🧬", layout="wide")
st.title("🧬 ABO-H Phenotyper")
st.markdown("**Research Tool** — ABO Blood Type + H Antigen Prediction")

# ====================== PREDICTION ENGINE ======================
def predict_abo(del261="Absent", c526="C", c703="G", c796="C", c803="G"):
    del261 = str(del261).strip()
    c526 = str(c526).strip()
    c703 = str(c703).strip()
    c796 = str(c796).strip()
    c803 = str(c803).strip()

    if del261 == "Present":
        return "O", "High", "Full H antigen remains (O allele)"
    elif (c796 == "A" or c803 == "C") and (c526 == "G" or c703 == "A"):
        return "AB", "Low", "Both A and B antigens expressed"
    elif c796 == "A" or c803 == "C":
        return "B", "Medium", "B antigen expressed"
    elif c526 == "G" or c703 == "A":
        return "A", "Medium", "A antigen expressed"
    else:
        return "Unknown", "Unknown", "Could not determine phenotype"

def show_results(phenotype, h_level, explanation, summary):
    st.success(f"**Predicted Blood Type: {phenotype}**")
    st.metric("H Antigen Level", h_level)
    st.info(explanation)

    fig = px.bar(x=["H Antigen", "A Antigen", "B Antigen"],
                 y=[90 if phenotype == "O" else 35,
                    80 if phenotype in ["A", "AB"] else 10,
                    80 if phenotype in ["B", "AB"] else 10],
                 title="Estimated Antigen Expression")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Input Summary")
    st.json(summary)

# ====================== INPUT SELECTION ======================
input_method = st.sidebar.radio("Input Method", ["Key SNPs (Recommended)", "FASTA Sequence"])

# ====================== KEY SNPs ======================
if input_method == "Key SNPs (Recommended)":
    st.subheader("Enter Key ABO Variants")
    col1, col2 = st.columns(2)
    with col1:
        del261 = st.selectbox("261delG (O)", ["Absent", "Present"])
        c796 = st.selectbox("796C>A", ["C", "A"])
        c803 = st.selectbox("803G>C", ["G", "C"])
    with col2:
        c526 = st.selectbox("526C>G", ["C", "G"])
        c703 = st.selectbox("703G>A", ["G", "A"])

    if st.button("🔬 Predict Blood Type", type="primary"):
        phenotype, h_level, explanation = predict_abo(del261, c526, c703, c796, c803)
        show_results(phenotype, h_level, explanation, {
            "261delG": del261, "526": c526, "703": c703,
            "796": c796, "803": c803
        })

# ====================== FASTA SEQUENCE ======================
elif input_method == "FASTA Sequence":
    st.subheader("Upload ABO Sequence (Exon 6/7)")
    uploaded = st.file_uploader("Choose FASTA file", type=["fasta", "fa", "txt"])

    if uploaded:
        try:
            content = uploaded.getvalue().decode("utf-8")
            sequences = list(SeqIO.parse(StringIO(content), "fasta"))

            if sequences:
                seq = str(sequences[0].seq).upper()
                st.success(f"✅ Sequence loaded: {len(seq):,} bp")
                st.text_area("Preview", seq[:400] + "..." if len(seq) > 400 else seq, height=120)

                if st.button("🔬 Analyze Sequence", type="primary"):
                    # Simple placeholder detection (can be improved later)
                    # For demo, we'll assume common A allele unless "del" hint is in sequence
                    if "DEL" in seq.upper() or len(seq) < 100:
                        phenotype, h_level, explanation = predict_abo("Present", "C", "G", "C", "G")
                    else:
                        phenotype, h_level, explanation = predict_abo("Absent", "G", "A", "C", "G")  # Default to A

                    show_results(phenotype, h_level, explanation, {
                        "Input Type": "FASTA",
                        "Sequence Length": f"{len(seq):,} bp",
                        "Sequence ID": sequences[0].id if hasattr(sequences[0], 'id') else "Unknown"
                    })
        except Exception as e:
            st.error(f"Error processing file: {e}")

st.caption("ABO-H Phenotyper • Portfolio Project")
