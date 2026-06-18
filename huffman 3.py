import heapq
import os
import json

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Overriding __lt__ ensures the priority queue compares nodes by frequency
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCompressor:
    def __init__(self):
        self.reverse_mapping = {}

    def _build_frequency_map(self, text):
        frequency = {}
        for char in text:
            if char not in frequency:
                frequency[char] = 0
            frequency[char] += 1
        return frequency

    def _build_priority_queue(self, frequency_map):
        heap = []
        for key in frequency_map:
            node = HuffmanNode(key, frequency_map[key])
            heapq.heappush(heap, node)
        return heap

    def _build_tree(self, heap):
        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)

            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(heap, merged)
        return heapq.heappop(heap)

    def _make_codes_helper(self, root, current_code, codes):
        if root is None:
            return

        if root.char is not None:
            codes[root.char] = current_code
            return

        self._make_codes_helper(root.left, current_code + "0", codes)
        self._make_codes_helper(root.right, current_code + "1", codes)

    def _make_codes(self, root):
        codes = {}
        self._make_codes_helper(root, "", codes)
        return codes

    def _get_encoded_text(self, text, codes):
        encoded_text = ""
        for char in text:
            encoded_text += codes[char]
        return encoded_text

    def _pad_encoded_text(self, encoded_text):
        extra_padding = 8 - (len(encoded_text) % 8)
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def _get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print("Error: Padded text formatting failed.")
            exit(1)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    def compress(self, path):
        if not os.path.exists(path):
            print(f"Error: The input file '{path}' does not exist. Please check the path.")
            return

        filename, file_extension = os.path.splitext(path)
        output_path = filename + ".huff"

        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()
            text = text.rstrip()

        if not text:
            print("Error: File is empty.")
            return

        frequency_map = self._build_frequency_map(text)
        heap = self._build_priority_queue(frequency_map)
        tree_root = self._build_tree(heap)
        codes = self._make_codes(tree_root)

        encoded_text = self._get_encoded_text(text, codes)
        padded_encoded_text = self._pad_encoded_text(encoded_text)
        b_array = self._get_byte_array(padded_encoded_text)

        # Save frequency map as metadata to rebuild the tree during decompression
        metadata = json.dumps(frequency_map)
        metadata_bytes = metadata.encode('utf-8')
        metadata_length = len(metadata_bytes)

        with open(output_path, 'wb') as output:
            output.write(metadata_length.to_bytes(4, byteorder='big'))
            output.write(metadata_bytes)
            output.write(bytes(b_array))

        print(f" Success!!!!! yayyyy File compressed to: {output_path}")
        self._calculate_metrics(path, output_path)

    def _remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text_length = len(padded_encoded_text) - extra_padding

        encoded_text = padded_encoded_text[:encoded_text_length]
        return encoded_text

    def _decode_text(self, encoded_text, variable_codes):
        reverse_mapping = {v: k for k, v in variable_codes.items()}
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in reverse_mapping:
                character = reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, input_path):
        if not os.path.exists(input_path):
            print(f"Error: The file '{input_path}' does not exist.")
            return

        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_decompressed.txt"

        with open(input_path, 'rb') as file:
            metadata_length = int.from_bytes(file.read(4), byteorder='big')
            metadata_bytes = file.read(metadata_length)
            frequency_map = json.loads(metadata_bytes.decode('utf-8'))

            bit_string = ""
            byte = file.read(1)
            while len(byte) > 0:
                binary_value = bin(ord(byte))[2:]
                binary_value = binary_value.rjust(8, '0')
                bit_string += binary_value
                byte = file.read(1)

        heap = self._build_priority_queue(frequency_map)
        tree_root = self._build_tree(heap)
        codes = self._make_codes(tree_root)

        encoded_text = self._remove_padding(bit_string)
        decompressed_text = self._decode_text(encoded_text, codes)

        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(decompressed_text)

        print(f" Success!!!!!!!! yayyyy File decompressed to: {output_path}")

    def _calculate_metrics(self, orig_path, comp_path):
        orig_size = os.path.getsize(orig_path)
        comp_size = os.path.getsize(comp_path)
        
        ratio = (1 - (comp_size / orig_size)) * 100
        space_saving = orig_size - comp_size

        print("\n=== DAA PERFORMANCE EMPIRICAL METRICS ===")
        print(f"• Original File Size    : {orig_size} bytes")
        print(f"• Compressed File Size  : {comp_size} bytes")
        print(f"• Physical Storage Saved: {space_saving} bytes")
        print(f"• Compression Ratio     : {ratio:.2f}%")
        print("=========================================\n")


if __name__ == "__main__":
    # --- HARDCODED TEST CONFIGURATION FOR DECOMPRESSION ---
    # Step 1: Set action strictly to decompress
    TARGET_ACTION = "decompress" 
    
    # Step 2: Point directly to the compressed binary .huff file location
    TARGET_FILE = r"C:\Users\Seenu\Downloads\sample.huff"
    
    # --- RUN ENGINE ---
    creator = HuffmanCompressor()

    if TARGET_ACTION == "compress":
        print(f"Starting compression on: {TARGET_FILE}")
        creator.compress(TARGET_FILE)
        
    elif TARGET_ACTION == "decompress":
        print(f"Starting decompression on: {TARGET_FILE}")
        creator.decompress(TARGET_FILE)