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
            byte = padded_encoded_text[i:i + 8]
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

        print(f" Success! yay done, File compressed to: {output_path}")
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

        print(f" Success! File decompressed to: {output_path}")

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
    TARGET_ACTION = "compress"
    TARGET_FILE = r"C:\Users\Seenu\Downloads\sample.txt"

    if TARGET_ACTION == "compress":
        print("Creating a fresh, exceptionally lengthy sample text file for compression testing...")

        test_content = (
            "================================================================================\n"
            "DESIGN AND ANALYSIS OF ALGORITHMS: A COMPREHENSIVE GUIDE TO LOSSLESS COMPRESSION\n"
            "================================================================================\n\n"
            "INTRODUCTION TO THE GREEDY ALGORITHMIC PARADIGM\n"
            "In computer science, algorithms are systematically designed to solve complex computational problems. "
            "Among the various foundational design paradigms—such as Divide and Conquer, Dynamic Programming, "
            "Backtracking, and Branch and Bound—the Greedy Paradigm stands out for its elegant simplicity and operational efficiency. "
            "A greedy algorithm constructs a solution piece by piece, systematically choosing the next piece that offers the most "
            "obvious and immediate benefit. This localized strategy is fundamentally known as making a locally optimal choice. "
            "The core philosophy underlying greedy algorithms is the structural assumption that a sequence of locally optimal choices "
            "will ultimately lead to a globally optimal solution.\n\n"
            "However, it is critical to note that greedy algorithms do not always yield the absolute optimal global result. "
            "For a greedy approach to be mathematically proven correct, the underlying problem structure must satisfy two "
            "essential algorithmic properties: the Greedy Choice Property and the Optimal Substructure Property. The Greedy Choice "
            "Property states that a globally optimal solution can be arrived at by making locally optimal, shortsighted choices without "
            "ever having to reconsider past choices. The Optimal Substructure Property establishes that an optimal solution to the "
            "overall large-scale problem contains within it the optimal solutions to all its smaller subproblems.\n\n"
            "THE FOUNDATIONAL MECHANICS OF HUFFMAN CODING\n"
            "A quintessential, universally celebrated manifestation of the greedy paradigm is Huffman Coding, an elegant method designed "
            "by David Huffman in 1952 for lossless data compression. Lossless data compression algorithms reduce the physical storage "
            "footprint of a file while guaranteeing that the original source data can be perfectly, flawlessly reconstructed down to the "
            "exact bit during decompression. This contrasts sharply with lossy compression techniques, which permanently discard redundant "
            "visual or auditory data to minimize space, as frequently observed in JPEG or MP3 formats.\n\n"
            "The core computational problem that Huffman Coding addresses is variable-length character encoding. In standard computer systems, "
            "textual datasets are represented using fixed-length encoding schemes. For example, standard ASCII characters each consume "
            "exactly 8 bits (1 byte) of storage space, regardless of how frequently those individual characters appear within a given document. "
            "In a traditional 8-bit system, the highly common character 'e' or a blank space character ' ' takes up the exact same amount of "
            "physical space as the rarely utilized character 'z' or 'q'. This structural rigidity represents a massive algorithmic "
            "inefficiency when processing large volumes of data.\n\n"
            "Huffman Coding removes this inefficiency by introducing a variable-length character assignment framework. The foundational "
            "principle is remarkably intuitive yet mathematically profound: characters that appear with a high frequency throughout the "
            "source text are assigned shorter binary sequences, while characters that appear with a low frequency are assigned longer "
            "binary sequences. By systematically varying the bit length of individual character codes based on empirical frequency metrics, "
            "the cumulative size of the processed text stream is drastically optimized.\n\n"
            "THE GREEDY INITIALIZATION AND MIN-HEAP MECHANICS\n"
            "The computational implementation of Huffman Coding is broken down into a series of highly structured phases. The algorithm "
            "begins by executing a preliminary pass over the raw input text to compute a comprehensive frequency map. This frequency mapping "
            "process reads every symbol sequentially, accumulating an integer tally of occurrences for each character. If the input data "
            "contains n total characters and an alphabet size of C unique characters, constructing this frequency dictionary requires linear "
            "time complexity, mathematically denoted as O(n).\n\n"
            "Once the frequency dictionary is completed, the algorithm shifts to its core greedy phase. To build an optimal prefix-free "
            "binary tree, the algorithm utilizes a Priority Queue data structure, implemented via a binary Min-Heap. The Min-Heap is an essential "
            "algorithmic tool because it allows for the retrieval and removal of the element with the absolute smallest value in logarithmic time. "
            "Every unique character from the frequency dictionary is encapsulated within a custom TreeNode object, which tracks the individual "
            "character symbol and its associated weight or frequency count.\n\n"
            "During the heapification process, all unique character nodes are inserted into the Min-Heap. The initial construction of this "
            "heap structure takes O(C) time, where C represents the count of unique symbols. After initialization, the algorithm enters a continuous "
            "iterative loop to build the Huffman Tree. The loop executes exactly C - 1 times, performing a greedy merge operation during each iteration.\n\n"
            "THE STEP-BY-STEP TREE CONSTRUCTION LOOP\n"
            "Within the greedy merge loop, the algorithm performs the following exact actions:\n"
            "1. It pops the absolute lowest-frequency node from the Min-Heap. Let this be designated as Left_Child.\n"
            "2. It pops the next lowest-frequency node from the Min-Heap. Let this be designated as Right_Child.\n"
            "3. It creates a brand-new internal parent node. This parent node does not contain any character symbol. Instead, its internal frequency "
            "weight is calculated as the exact mathematical sum of Left_Child's frequency and Right_Child's frequency.\n"
            "4. The algorithm assigns Left_Child as the left branch of the new parent node, and Right_Child as the right branch.\n"
            "5. Finally, this newly constructed parent node is pushed back into the Min-Heap structure.\n\n"
            "This iterative loop perfectly exemplifies the greedy paradigm. At every single structural step, the algorithm completely disregards "
            "the overall structure of the eventual tree, choosing instead to execute the immediate, locally optimal task: merging the two smallest available weights. "
            "Because extracting a node from a Min-Heap requires O(log C) time, and this operation is performed inside a loop running C times, the total "
            "time complexity for constructing the structural Huffman Tree is asymptotically bounded by O(C log C).\n\n"
            "PREFIX CODES AND THE MATHEMATICAL DFS TRAVERSAL\n"
            "Once the loop terminates, exactly one master node remains inside the priority queue. This remaining node is the root node of the fully realized Huffman Tree. "
            "This binary tree structure maps paths from the root down to individual leaf nodes, where each leaf node represents a unique character from our initial alphabet.\n\n"
            "To extract the actual binary bit sequences for each character, the algorithm executes a structured tree traversal, typically implemented via a recursive Depth-First Search (DFS) function. "
            "The algorithm begins at the root node and descends down through the branches. By convention, whenever the traversal moves down a left edge, a binary bit of '0' "
            "is appended to the current path sequence. Conversely, whenever the traversal moves down a right edge, a binary bit of '1' is appended to the sequence.\n\n"
            "When the DFS function encounters a terminal leaf node, it creates an entry in a code map dictionary, linking that node's character symbol to the compiled string of binary bits. "
            "This generation process produces a set of unique prefix codes. A prefix code (more accurately called a prefix-free code) ensures that no binary code assigned to "
            "a character is a prefix of any other character's binary code. For example, if the character 'e' is assigned the binary code '01', no other character in the "
            "entire codebook will have a code that begins with '01', such as '010' or '011'. This prefix-free guarantee is absolutely vital because it removes any possible ambiguity "
            "during the decompression process, allowing a continuous stream of bits to be parsed linearly without needing explicit delimiters.\n\n"
            "BIT-PACKING, STREAM PADDING, AND METADATA OVERHEAD\n"
            "After generating the prefix codes, the algorithm translates the human-readable source text into a packed binary bitstream. This step cycles through the original text file "
            "character by character, replacing each symbol with its corresponding variable-length binary code.\n\n"
            "However, physical computer storage media operate exclusively on 8-bit byte structures. A raw binary string like '101101' cannot be saved directly to disk "
            "because its length is 6 bits, not an even multiple of 8. To resolve this hardware interface limitation, a bit-packing wrapper handles the data formatting. "
            "The algorithm counts the remaining bits and computes an integer value representing extra padding. It appends trailing '0' bits to the end of the stream until "
            "its length is perfectly divisible by 8. Furthermore, an 8-bit padding details byte is prepended to the absolute top of the compressed payload so that the "
            "decompressor knows exactly how many filler bits to discard at the end of the file.\n\n"
            "Moreover, because a Huffman tree is custom-tailored to the specific character distribution of its unique input file, the compressed `.huff` file layout must include a metadata header. "
            "If the decompression engine does not possess the exact frequency counts or tree structure used during compression, it cannot interpret the bitstream. "
            "Therefore, our custom file format encodes a 4-byte length header followed by a serialized JSON dictionary containing the frequency mapping data. "
            "During compression, this metadata overhead introduces a fixed size penalty. As inputs grow into large-scale files, this fixed header penalty becomes entirely negligible, "
            "allowing the true efficiency of the variable-length bit distribution to shine.\n\n"
            "SUMMARY OF ASYMPTOTIC RUNTIME COMPLEXITIES\n"
            "To summarize the mathematical efficiency of this project from a DAA perspective:\n"
            "- Frequency Mapping Phase: O(n) time, where n is the total number of characters in the input file.\n"
            "- Min-Heap Initialization: O(C) time, where C is the count of unique alphabet symbols.\n"
            "- Greedy Tree Merging Phase: O(C log C) execution time through iterative priority adjustments.\n"
            "- Code Extraction via DFS Traversal: O(C) time to traverse the binary tree paths.\n"
            "- Bitstream Translation Phase: O(n) time to pack and map symbols into raw bytes.\n"
            "- Total Compression Complexity: O(n + C log C). Because the alphabet size C is bounded by a fixed constant in standard character sets (like 256 for extended ASCII), the runtime scales completely linearly as O(n) for real-world large datasets.\n"
            "- Total Space Complexity: O(C) auxiliary memory required to hold the heap nodes and structural dictionaries.\n\n"
            "This complete pipeline achieves optimal lossless data compression, perfectly showcasing the practical power of the greedy choice property in software engineering applications.\n"
            "================================================================================\n"
        )

        # We duplicate the textbook string 8 times over to make it truly lengthy (~60,000+ bytes)
        test_content = test_content * 8

        with open(TARGET_FILE, 'w', encoding='utf-8') as f:
            f.write(test_content)

    # --- RUN ENGINE ---
    creator = HuffmanCompressor()

    if TARGET_ACTION == "compress":
        print(f"Starting compression on: {TARGET_FILE}")
        creator.compress(TARGET_FILE)

    elif TARGET_ACTION == "decompress":
        print(f"Starting decompression on: {TARGET_FILE}")
        creator.decompress(TARGET_FILE)