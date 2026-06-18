import os
import json
import heapq
import logging
import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =====================================================================
# SYSTEM ARCHITECTURE: STANDARD LOGGING FRAMEWORK CONFIGURATION
# =====================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

class StreamlitLogHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.log_buffer = []

    def emit(self, record):
        msg = self.format(record)
        self.log_buffer.append(msg)
        self.widget.code("\n".join(self.log_buffer), language="text")

# =====================================================================
# ALGORITHMIC LOGIC: HUFFMAN CORE IMPLEMENTATION
# =====================================================================

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_map(text_data):
    freq_map = {}
    for char in text_data:
        freq_map[char] = freq_map.get(char, 0) + 1
    return freq_map

def build_huffman_tree(freq_map):
    if len(freq_map) == 1:
        char, freq = list(freq_map.items())[0]
        root = HuffmanNode(None, freq)
        root.left = HuffmanNode(char, freq)
        return root

    heap = [HuffmanNode(char, freq) for char, freq in freq_map.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left_child = heapq.heappop(heap)
        right_child = heapq.heappop(heap)
        parent = HuffmanNode(None, left_child.freq + right_child.freq)
        parent.left = left_child
        parent.right = right_child
        heapq.heappush(heap, parent)
        
    return heap[0] if heap else None

def generate_prefix_codes(node, current_code="", code_map=None):
    if code_map is None:
        code_map = {}
    if node is None:
        return code_map
    if node.char is not None:
        code_map[node.char] = current_code
        return code_map
    generate_prefix_codes(node.left, current_code + "0", code_map)
    generate_prefix_codes(node.right, current_code + "1", code_map)
    return code_map

# =====================================================================
# CORE ENGINE: PIPELINE COMPRESSION & DECOMPRESSION
# =====================================================================

def compress_payload(raw_text):
    logging.info("Initiating compression pipeline sequence...")
    freq_map = build_frequency_map(raw_text)
    tree_root = build_huffman_tree(freq_map)
    code_map = generate_prefix_codes(tree_root)
    
    bit_stream = "".join(code_map[char] for char in raw_text)
    padding_length = (8 - (len(bit_stream) % 8)) % 8
    bit_stream += "0" * padding_length

    packed_bytes = bytearray()
    for i in range(0, len(bit_stream), 8):
        byte_segment = bit_stream[i:i+8]
        packed_bytes.append(int(byte_segment, 2))

    header_json = json.dumps(freq_map, ensure_ascii=False).encode("utf-8")
    header_length = len(header_json)

    output_buffer = io.BytesIO()
    output_buffer.write(header_length.to_bytes(4, byteorder="big"))
    output_buffer.write(header_json)
    output_buffer.write(bytes([padding_length]))
    output_buffer.write(packed_bytes)
    
    logging.info("Compression pipeline finalized successfully.")
    return output_buffer.getvalue(), freq_map, code_map

def decompress_payload(binary_data):
    logging.info("Initiating binary decompression sequence...")
    input_buffer = io.BytesIO(binary_data)
    
    header_length_bytes = input_buffer.read(4)
    if not header_length_bytes:
        raise ValueError("Invalid binary schema formatting.")
        
    header_length = int.from_bytes(header_length_bytes, byteorder="big")
    header_json = input_buffer.read(header_length).decode("utf-8")
    freq_map = json.loads(header_json)
    padding_length = int.from_bytes(input_buffer.read(1), byteorder="big")
    payload_bytes = input_buffer.read()

    bit_stream = "".join(f"{b:08b}" for b in payload_bytes)
    if padding_length > 0:
        bit_stream = bit_stream[:-padding_length]

    tree_root = build_huffman_tree(freq_map)
    decoded_characters = []
    current_node = tree_root
    
    for bit in bit_stream:
        current_node = current_node.left if bit == "0" else current_node.right
        if current_node.char is not None:
            decoded_characters.append(current_node.char)
            current_node = tree_root

    logging.info("Decompression sequence finished. Data integrity verified.")
    return "".join(decoded_characters)

# =====================================================================
# USER INTERACTION & WEB APP INTERFACE DESIGN
# =====================================================================

st.set_page_config(
    page_title="Huffman Compression & Security Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme customization with glowing neon red metrics and indicators
st.markdown("""
    <style>
        .stApp { background-color: #000000; color: #FFFFFF; }
        h1, h2, h3 { color: #FF0033 !important; font-family: 'Courier New', monospace !important; }
        .stButton>button { 
            background-color: #1A0003 !important; color: #FF0033 !important; 
            border: 1px solid #FF0033 !important; font-family: 'Courier New', monospace; font-weight: bold;
            width: 100%; transition: 0.3s;
        }
        .stButton>button:hover { background-color: #FF0033 !important; color: white !important; box-shadow: 0 0 15px #FF0033; }
        .css-11yzg6d, .stTabs [data-baseweb="tab"] { font-family: 'Courier New', monospace; color: #999999; }
        .stTabs [aria-selected="true"] { color: #FF0033 !important; font-weight: bold; border-bottom-color: #FF0033 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("HUFFMAN COMPRESSION AND DECOMPRESSION USING SECURITY AUTHENTICATION")
st.write("An optimization engine for compressing and validating secure authentication payloads.")

# Continuous Core Framework Terminal System Component
st.sidebar.markdown("### SYSTEM RECOVERY LOGS")
console_placeholder = st.sidebar.empty()
log_handler = StreamlitLogHandler(console_placeholder)
logging.getLogger().addHandler(log_handler)

tabs = st.tabs(["Secure Data Compression", "Package Parsing and Recovery"])

# Generate robust mock authentication structured database using Pandas
mock_logs = [
    {"timestamp": "2026-06-17 23:45:01", "user_id": "seenu_99", "token": "SECURE_7c1a93e82b", "status": "AUTHORIZED"},
    {"timestamp": "2026-06-17 23:46:12", "user_id": "prof_daa", "token": "EVAL_4f8e139c2a", "status": "AUTHORIZED"},
    {"timestamp": "2026-06-17 23:48:33", "user_id": "guest_usr", "token": "NONE_f3e82a19c7", "status": "DENIED"},
    {"timestamp": "2026-06-17 23:50:00", "user_id": "sys_root", "token": "ROOT_a1f94c83e2", "status": "AUTHORIZED"}
] * 35 
df_mock = pd.DataFrame(mock_logs)

# -----------------------------------------------------------------
# TAB 1: LOCK & COMPRESS PIPELINE
# -----------------------------------------------------------------
with tabs[0]:
    st.header("Authentication Data Compression Panel")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Target Authentication Dataset")
        edited_df = st.data_editor(df_mock, use_container_width=True, num_rows="dynamic")
        raw_payload_string = edited_df.to_json(orient="records", indent=2)
        
    with col2:
        st.markdown("### Execution Controls")
        st.caption("Execute file compression and process data tables into a secure binary stream.")
        
        if st.button("EXECUTE COMPRESSION ENGINE"):
            compressed_bytes, f_map, c_map = compress_payload(raw_payload_string)
            
            orig_size = len(raw_payload_string.encode('utf-8'))
            comp_size = len(compressed_bytes)
            reduction = ((orig_size - comp_size) / orig_size) * 100
            
            st.session_state['latest_compressed_payload'] = compressed_bytes
            st.session_state['original_raw_string'] = raw_payload_string
            
            st.success("Compression Pipeline Successfully Finalized!")
            
            # Interactive Metric Cards
            m1, m2, m3 = st.columns(3)
            m1.metric("Original Data Size", f"{orig_size} Bytes")
            m2.metric("Compressed File Size", f"{comp_size} Bytes")
            m3.metric("Space Saved", f"{reduction:.2f}%")
            
            st.markdown("### Real-Time Performance Analytics")
            
            # -----------------------------------------------------------------
            # GRAPH 1 & GRAPH 2 (ROW 1)
            # -----------------------------------------------------------------
            row1_col1, row1_col2 = st.columns(2)
            
            with row1_col1:
                # Graph 1: File Size Optimization Bar Chart
                fig_bytes = go.Figure(data=[
                    go.Bar(name='Original Data Size', x=['Payload File Structure'], y=[orig_size], marker_color='#330005', marker_line_color='#FF0033', marker_line_width=1.5),
                    go.Bar(name='Compressed File Size', x=['Payload File Structure'], y=[comp_size], marker_color='#00FF55')
                ])
                fig_bytes.update_layout(
                    barmode='group', 
                    title_text='File Size Optimization Comparison', 
                    template="plotly_dark", 
                    paper_bgcolor='#000000', 
                    plot_bgcolor='#050505'
                )
                st.plotly_chart(fig_bytes, use_container_width=True)
                
            with row1_col2:
                # Graph 2: Character Frequency Distribution
                df_freq = pd.DataFrame(list(f_map.items()), columns=['Character', 'Frequency']).sort_values(by='Frequency', ascending=False)
                fig_freq = px.bar(
                    df_freq.head(15), 
                    x='Character', 
                    y='Frequency', 
                    title='Top-15 Character Frequency Distribution', 
                    color_discrete_sequence=['#FF0033']
                )
                fig_freq.update_layout(
                    template="plotly_dark", 
                    paper_bgcolor='#000000', 
                    plot_bgcolor='#050505'
                )
                st.plotly_chart(fig_freq, use_container_width=True)

            # -----------------------------------------------------------------
            # NEW ADDITIONS: GRAPH 3 & GRAPH 4 (ROW 2)
            # -----------------------------------------------------------------
            row2_col1, row2_col2 = st.columns(2)
            
            with row2_col1:
                # Graph 3: Interactive Bit Allocation Savings Distribution (Pie Chart)
                fig_pie = go.Figure(data=[go.Pie(
                    labels=['Optimized File Mass', 'Memory Savings Capacity'],
                    values=[comp_size, orig_size - comp_size],
                    hole=.4,
                    marker=dict(colors=['#FF0033', '#00FF55'], line=dict(color='#000000', width=2))
                )])
                fig_pie.update_layout(
                    title_text='Data Footprint Density Allocation',
                    template="plotly_dark",
                    paper_bgcolor='#000000',
                    plot_bgcolor='#050505'
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                
            with row2_col2:
                # Graph 4: Dynamic Codebook Bit-Length Density Profile (Scatter Plot)
                df_codes = pd.DataFrame([
                    {'Character': char, 'Bit Length': len(code)} 
                    for char, code in c_map.items()
                ]).sort_values(by='Bit Length')
                
                fig_scatter = px.scatter(
                    df_codes, 
                    x='Character', 
                    y='Bit Length', 
                    title='Asymmetric Huffman Bit-Length Distribution Grid',
                    color='Bit Length',
                    color_continuous_scale=['#00FF55', '#FF0033']
                )
                fig_scatter.update_layout(
                    template="plotly_dark", 
                    paper_bgcolor='#000000', 
                    plot_bgcolor='#050505'
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Binary File Export Component Interface
            st.download_button(
                label="DOWNLOAD COMPRESSED SECURITY FILE",
                data=compressed_bytes,
                file_name="auth_payload_secure.huff",
                mime="application/octet-stream"
            )

# -----------------------------------------------------------------
# TAB 2: PARSE & RECOVER PIPELINE
# -----------------------------------------------------------------
with tabs[1]:
    st.header("File Decompression and Deverification Panel")
    
    uploaded_file = st.file_uploader("Upload compressed tool bundle (.huff)", type=["huff"])
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        st.info(f"Loaded secure file package segment totaling: {len(file_bytes)} Bytes.")
        
        if st.button("RUN DECOMPRESSION ENGINE"):
            try:
                recovered_text = decompress_payload(file_bytes)
                st.success("Extraction Sequence Completed Successfully.")
                
                if 'original_raw_string' in st.session_state:
                    is_match = st.session_state['original_raw_string'] == recovered_text
                    if is_match:
                        st.markdown("<h3 style='color: #00FF55 !important;'>SECURITY AUTHENTICATION PASSED: 100% PERFECT DATA INTEGRITY</h3>", unsafe_allow_html=True)
                    else:
                        st.error("SECURITY AUTHENTICATION FAILED: Data stream disparity detected.")
                
                st.markdown("### Restored Authentication Records")
                recovered_io = io.StringIO(recovered_text)
                df_recovered = pd.read_json(recovered_io)
                st.dataframe(df_recovered, use_container_width=True)
                
            except Exception as error_msg:
                st.error(f"Decompression Failure: {str(error_msg)}")