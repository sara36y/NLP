import streamlit as st
from translation import BilingualTranslationPipeline
import time
import os

# Set up Streamlit page
st.set_page_config(
    page_title="Bilingual Translation System",
    page_icon="🌐",
    layout="wide"
)


# Create translation pipeline with selected direction
@st.cache_resource
def load_pipeline(direction):
    pipeline = BilingualTranslationPipeline(direction)
    pipeline.setup_resources()
    pipeline.load_data()
    pipeline.load_model()
    return pipeline


# User interface
def main():
    # Application title
    st.title("🌐 Bilingual Translation System")

    # Select translation direction
    direction = st.radio(
        "Select translation direction:",
        ["Arabic to English", "English to Arabic"],
        index=0,
        horizontal=True
    )

    # Convert the selection to model format
    model_direction = 'ar-en' if direction == "Arabic to English" else 'en-ar'

    # Load translation model
    with st.spinner("Loading translation model..."):
        pipeline = load_pipeline(model_direction)

    # Application tabs
    tab1, tab2 = st.tabs(["Translation", "System Information"])

    with tab1:
        # Input text based on selected direction
        input_label = "Arabic text" if model_direction == 'ar-en' else "English text"
        input_placeholder = "Enter text to translate..."

        st.subheader(f"Enter {input_label}")
        input_text = st.text_area(
            "input_text",
            height=150,
            placeholder=input_placeholder,
            label_visibility="collapsed"
        )

        # Control buttons
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            translate_btn = st.button("Translate", use_container_width=True)
        with col2:
            clear_btn = st.button("Clear", use_container_width=True)

        if clear_btn:
            input_text = ""
            st.experimental_rerun()

        if translate_btn and not input_text:
            st.warning("Please enter text for translation")

        # Display results
        if translate_btn and input_text:
            with st.spinner("Processing translation..."):
                start_time = time.time()
                result = pipeline.translate_text(input_text)
                elapsed_time = time.time() - start_time

            st.success("Translation completed successfully!")

            # Results columns
            col1, col2 = st.columns(2)

            with col1:
                st.subheader(input_label)
                st.text_area(
                    "original_text",
                    value=result['original'],
                    height=200,
                    disabled=True,
                    label_visibility="collapsed"
                )

            with col2:
                output_label = "English text" if model_direction == 'ar-en' else "Arabic text"
                st.subheader(output_label)
                st.text_area(
                    "translated_text",
                    value=result['translated'],
                    height=200,
                    disabled=True,
                    label_visibility="collapsed"
                )

            # Translation details expander
            with st.expander("Translation Details"):
                st.write(f"**Processing time:** {elapsed_time:.2f} seconds")
                st.write(f"**Cleaned input text:** {result['cleaned']}")

    with tab2:
        st.header("System Information")

        st.subheader("About This Application")
        st.write("""
        This bilingual translation system provides high-quality translations between Arabic and English. 
        It utilizes state-of-the-art machine learning models fine-tuned on extensive language datasets.
        """)

        st.subheader("Technical Specifications")
        st.write("""
        - **Base Model:** Helsinki-NLP MarianMT
        - **Translation Directions:** Arabic ↔ English
        - **Text Processing:** Advanced cleaning and normalization
        - **Performance:** Optimized for accuracy and speed
        """)

        st.subheader("Usage Instructions")
        st.write("""
        1. Select translation direction
        2. Enter text in the input box
        3. Click the Translate button
        4. View results in the output section
        """)


if __name__ == "__main__":
    # Ensure the visualizations directory exists
    os.makedirs('visualizations', exist_ok=True)
    main()
