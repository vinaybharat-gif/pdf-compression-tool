import streamlit as st
import PyPDF2
from huffman import build_huffman_tree, generate_codes, compress_text, decompress_text

# 1. CHANGE THE BROWSER TAB LOGO (Must be the first Streamlit command!)
st.set_page_config(page_title="Huffman Compressor", page_icon="⚡")

# 2. COLORFUL TITLE WITH NEW LOGO
st.markdown("<h1 style='text-align: center; color: #00E676;'>✂️🔨Huffman File Compressor</h1>", unsafe_allow_html=True)

# 3. COLORFUL DESCRIPTION BOX
st.info("✨ **DAA Project:** Upload a PDF or Text file below to compress its text using the **Huffman Coding algorithm**. Watch the data shrink in real-time!")

# 4. THE "IMPRESS" SIDEBAR
with st.sidebar:
    st.header("👩‍🏫 Project Details")
    st.success("**Algorithm:** Huffman Coding")
    st.info("**Approach:** Greedy Algorithm")
    st.warning("**Time Complexity:** O(N log N)")
    st.error("**Space Complexity:** O(N)")

# 5. Create a File Uploader Box (UPDATED FOR PDF & TXT)
uploaded_file = st.file_uploader("Choose a PDF or Text file", type=["pdf", "txt"])

# 6. What happens when a file is uploaded? (UPDATED LOGIC)
if uploaded_file is not None:
    pdf_text = ""
    try:
        # Check if it is a PDF file
        if uploaded_file.name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pdf_text += text
                    
        # Check if it is a Text file
        elif uploaded_file.name.endswith('.txt'):
            pdf_text = uploaded_file.read().decode("utf-8")
            
    except Exception as e:
        st.error(f"Error reading file: {e}")

    # Create a big "Compress" button
    if st.button("🚀 Run Compression Algorithm"):
        if not pdf_text.strip():
            st.error("Could not find any readable text in this file. Please try a different one!")
        else:
            with st.spinner("Building Huffman Tree and Compressing..."):
                # Run your exact algorithm
                root_node = build_huffman_tree(pdf_text)
                huffman_codes = generate_codes(root_node)
                compressed_data = compress_text(pdf_text, huffman_codes)
                
                # Calculate the math
                original_bits = len(pdf_text) * 8
                compressed_bits = len(compressed_data)
                space_saved = 100 - ((compressed_bits / original_bits) * 100)
                
                # Display a beautiful dashboard
                st.subheader("📊 Compression Results")
                col1, col2, col3 = st.columns(3)
                col1.metric(label="Original Size", value=f"{original_bits} bits")
                col2.metric(label="Compressed Size", value=f"{compressed_bits} bits")
                col3.metric(label="Space Saved", value=f"{space_saved:.2f} %")
                
                # Verify Decompression
                st.subheader("🔒 Data Integrity Check")
                decompressed_data = decompress_text(compressed_data, root_node)
                
                if pdf_text == decompressed_data:
                    st.success("✅ SUCCESS! Text was decompressed perfectly. 0% Data Loss.")
                else:
                    st.error("❌ ERROR! Data mismatch detected.")
                    
                # Optional: Show a tiny peek at the binary string
                with st.expander("Click to peek at the raw compressed binary data"):
                    st.write(compressed_data[:1000] + "...")
                
                # --- NEW DOWNLOAD BUTTON START ---
                st.divider()
                st.subheader("💾 Download Compressed Data")
                st.info("Note: The downloaded file contains the raw compressed binary data saved as a readable Text file (.txt).")
                
                # Create the download button
                st.download_button(
                    label="⬇️ Download Compressed File",
                    data=compressed_data,
                    file_name="compressed_text.txt",
                    mime="text/plain"
                )
                # --- NEW DOWNLOAD BUTTON END ---
