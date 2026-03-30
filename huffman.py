import heapq
from collections import Counter
import PyPDF2  # Our new PDF library!

# 1. Define the Node structure for our Huffman Tree
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# 2. Build the Tree
def build_huffman_tree(text):
    frequency_map = Counter(text)
    
    priority_queue = []
    for char, freq in frequency_map.items():
        heapq.heappush(priority_queue, HuffmanNode(char, freq))
        
    while len(priority_queue) > 1:
        left_node = heapq.heappop(priority_queue)
        right_node = heapq.heappop(priority_queue)
        
        merged_freq = left_node.freq + right_node.freq
        parent_node = HuffmanNode(None, merged_freq)
        
        parent_node.left = left_node
        parent_node.right = right_node
        
        heapq.heappush(priority_queue, parent_node)
        
    return priority_queue[0]

# 3. Generate the 0s and 1s (DFS Traversal)
def generate_codes(node, current_code="", codes_dict=None):
    if codes_dict is None:
        codes_dict = {}
        
    if node is None:
        return codes_dict
        
    # If it's a leaf node (has a character), save the binary code
    if node.char is not None:
        codes_dict[node.char] = current_code
        
    # Go left (add 0) and go right (add 1)
    generate_codes(node.left, current_code + "0", codes_dict)
    generate_codes(node.right, current_code + "1", codes_dict)
    
    return codes_dict

# 4. Compress the Actual Text!
def compress_text(text, codes_dict):
    compressed_string = ""
    for char in text:
        # Replace every letter with its new binary code
        compressed_string += codes_dict[char]
    return compressed_string

# 5. Decompress the Binary String back to Text
def decompress_text(compressed_string, root_node):
    decompressed_string = ""
    current_node = root_node
    
    for bit in compressed_string:
        # Go left for '0', right for '1'
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right
            
        # DAA Concept: Check if we reached a leaf node (no children)
        if current_node.left is None and current_node.right is None:
            decompressed_string += current_node.char # Found the letter!
            current_node = root_node                 # Reset back to the top of the tree
            
    return decompressed_string

# 6. Extract Text from PDF (NEW!)
def extract_text_from_pdf(pdf_path):
    extracted_text = ""
    try:
        # Open the PDF file in 'read binary' mode
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            # Loop through every page and grab the text
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text
        return extracted_text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

# --- THE PRESENTATION DASHBOARD ---
if __name__ == "__main__":
    # Make sure this matches the name of the PDF you put in your folder!
    pdf_filename = "sample.pdf"  
    
    print(f"--- Extracting text from {pdf_filename} ---")
    pdf_text = extract_text_from_pdf(pdf_filename)
    
    if not pdf_text:
        print("Could not extract text. Make sure 'sample.pdf' is in your DAA folder and has readable text!")
    else:
        print("Text extracted successfully! Compressing now...\n")
        
        # Run the Algorithm
        root_node = build_huffman_tree(pdf_text)
        huffman_codes = generate_codes(root_node)
        compressed_data = compress_text(pdf_text, huffman_codes)
        
        # Calculate Compression Ratio
        # 1 standard character = 1 byte (8 bits)
        original_size_bits = len(pdf_text) * 8 
        compressed_size_bits = len(compressed_data)
        
        # Calculate how much space we saved
        space_saved = 100 - ((compressed_size_bits / original_size_bits) * 100)
        
        print(f"📊 RESULTS DASHBOARD:")
        print(f"Original Text Size:   {original_size_bits} bits")
        print(f"Compressed Text Size: {compressed_size_bits} bits")
        print(f"Space Saved:          {space_saved:.2f}%\n")
        
        print("Verifying data integrity...")
        decompressed_data = decompress_text(compressed_data, root_node)
        
        if pdf_text == decompressed_data:
            print("✅ SUCCESS! The PDF text was compressed and completely recovered without data loss!")
        else:
            print("❌ ERROR! Data was lost during compression.")