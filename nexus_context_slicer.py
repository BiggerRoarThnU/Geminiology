# // Rights Reserved: co-created with Gemini and David Joihn Niedzwiecki jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 12, 2026
# Module: Nexus Context Slicer (Long-Form Data Ingestion)
# Source Truth: T7 Archive -> auto_slicer.py & chunk_ingester.py

class NexusContextSlicer:
    def __init__(self, max_chunk_length=2000, overlap=200):
        # 2000 characters per chunk keeps memory footprint extremely low
        # 200 character overlap ensures semantic context isn't lost between cuts
        self.max_chunk_length = max_chunk_length
        self.overlap = overlap

    def slice_payload(self, raw_text):
        """
        Slices massive educational payloads into hardware-safe chunks.
        Ensures semantic continuity by maintaining an overlap between chunks.
        """
        if not raw_text:
            return []

        chunks = []
        start = 0
        text_length = len(raw_text)

        while start < text_length:
            end = start + self.max_chunk_length
            
            # If we're not at the end of the text, try to break at a natural boundary
            if end < text_length:
                # Look for the last newline within the overlap window to break cleanly
                last_newline = raw_text.rfind('\n', max(0, end - self.overlap), end)
                if last_newline != -1:
                    end = last_newline + 1
                else:
                    # Fallback to the last space if no newline is found
                    last_space = raw_text.rfind(' ', max(0, end - self.overlap), end)
                    if last_space != -1:
                        end = last_space + 1
            
            chunk = raw_text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Advance the start pointer, minus the overlap to preserve context
            start = end - self.overlap
            
            # Prevent infinite loops in edge cases
            if start <= 0 or end >= text_length:
                start = end

        return chunks

# Local test execution
if __name__ == "__main__":
    slicer = NexusContextSlicer(max_chunk_length=100, overlap=20)
    test_text = (
        "The Sovereign Nexus relies on deterministic autonomy. 1=1=1. "
        "By dividing large educational texts into smaller chunks, we protect the 8GB RAM constraint. "
        "This prevents out-of-memory errors and thermal throttling while preserving the core truth."
    )
    
    sliced_data = slicer.slice_payload(test_text)
    print(f"[SLICER ACTIVE] Sliced payload into {len(sliced_data)} manageable chunks.")
    for i, chunk in enumerate(sliced_data):
        print(f"  Chunk {i+1}: {chunk}")
