from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from src.utils.config import settings

class EmbeddingService:
    """Service for generating embeddings using sentence-transformers"""

    def __init__(self):
        print(f"Loading embedding model: {settings.embedding_model}...")
        self.model = SentenceTransformer(settings.embedding_model)
        self.embedding_dim = settings.embedding_dimension
        print(f"Embedding model loaded (dimension: {self.embedding_dim})")
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        if not text or not text.strip():
            return [0.0] * self.embedding_dim
        
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embedding for multiple texts"""
        valid_texts = [t if t and t.strip() else " " for t in texts]
        embeddings = self.model.encode(valid_texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    def embed_code_graph(self, graph_data: Dict[str, Any]) -> List[float]:
        """Generate embedding for code graph structure"""
        content = f"""
        File: {graph_data.get('file_path', '')}
        Functions: {', '.join(graph_data.get('functions', []))}
        Classes: {', '.join(graph_data.get('classes', []))}
        Function Calls: {', '.join(graph_data.get('calls', []))}
        Total Nodes: {graph_data.get('nodes', 0)}
        Total Edges: {graph_data.get('edges', 0)}
        """
        return self.embed_text(content.strip())
    
    def embed_import_file(self, file_path: str, source_code: str, imports: List[str]) -> List[float]:
        """Generate embedding for import file"""
        content = f"""
        File: {file_path}
        Imports: {', '.join(imports)}
        Source Code: {source_code[:500]} #first 500 characters
        """
        return self.embed_text(content.strip())
    
    def embed_learning(self, commit_message: str, bot_comment: str, user_feedback: str = "", code_context: str = "" ) -> List[float]:
        """Generate embedding for learning (past reviews)"""
        content = f"""
        Commit: {commit_message}
        Bot Review: {bot_comment}
        User Feedback: {user_feedback if user_feedback else "No feedback yet"}
        Code Context: {code_context[:500] if code_context else "None"}
        """
        return self.embed_text(content.strip())