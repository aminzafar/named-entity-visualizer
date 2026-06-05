import streamlit as st
import spacy
from spacy import displacy


@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")


nlp = load_model()

st.set_page_config(page_title="Named Entity Visualizer", layout="centered")
st.title("Named Entity Visualizer")
st.markdown("Paste any text to highlight people, organizations, locations, dates, and more!")

text = st.text_area("Input Text", height=250, placeholder="Paste your text here...")

if st.button("Analyze", type="primary"):
    if not text.strip():
        st.warning("Please enter some text first.")
    
    else:
        doc = nlp(text)
        
        st.subheader("Highlighted Entities")
        
        html = displacy.render(doc, style="ent", page=False)
        
        st.markdown(html, unsafe_allow_html=True)
        st.divider()

        if doc.ents:
            st.subheader("Entities Found")

            entity_dict = {}
            for ent in doc.ents:
                if ent.label_ not in entity_dict:
                    entity_dict[ent.label_] = set()
                entity_dict[ent.label_].add(ent.text)

            for label, entities in sorted(entity_dict.items()):
                st.markdown(f"**{label}** — {', '.join(sorted(entities))}")
        
        else:
            st.info("No named entities detected in this text.")
    