import tiktoken
from typing import List, Dict


class ChunkingService:
    @staticmethod
    def count_tokens(text: str) -> int:
        try:
            encoding = tiktoken.get_encoding("cl100k_base")
            tokens = encoding.encode(text)
            return len(tokens)
        except:
            return len(text.split())

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 1024,
        chunk_overlap: int = 204
    ) -> List[Dict]:
        chunks = []
        encoding = tiktoken.get_encoding("cl100k_base")

        sentences = text.split(". ")
        current_chunk = ""
        current_tokens = 0
        char_start = 0

        for i, sentence in enumerate(sentences):
            sentence_tokens = ChunkingService.count_tokens(sentence)

            if current_tokens + sentence_tokens <= chunk_size:
                current_chunk += sentence + ". "
                current_tokens += sentence_tokens
            else:
                if current_chunk:
                    chunks.append({
                        "text": current_chunk.strip(),
                        "char_start": char_start,
                        "char_end": char_start + len(current_chunk),
                        "token_count": current_tokens
                    })
                    char_start += len(current_chunk)

                overlap_sentences = []
                overlap_tokens = 0
                for j in range(max(0, len(sentences) - i - 1), len(sentences)):
                    if j == i:
                        continue
                    sent = sentences[j]
                    sent_tokens = ChunkingService.count_tokens(sent)
                    if overlap_tokens + sent_tokens <= chunk_overlap:
                        overlap_sentences.append(sent)
                        overlap_tokens += sent_tokens

                current_chunk = ". ".join(overlap_sentences) + ". " + sentence + ". "
                current_tokens = overlap_tokens + sentence_tokens

        if current_chunk:
            chunks.append({
                "text": current_chunk.strip(),
                "char_start": char_start,
                "char_end": char_start + len(current_chunk),
                "token_count": current_tokens
            })

        return chunks
