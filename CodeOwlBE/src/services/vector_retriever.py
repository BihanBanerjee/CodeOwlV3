from typing import List, Dict, Any
from src.utils.qdrant_client import qdrant_client
from src.db.embedding_service import EmbeddingService


class VectorRetriever:
    """Retrieves code data from Qdrant vector collections"""
    def __init__(self):
        self.embedding_service = EmbeddingService()
    
    def get_code_graphs_by_files(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """Retrieve code graph for specific files"""
        if not file_paths:
            return []
        
        # Create a query from file paths
        query_text = f"Code from files: {', '.join(file_paths)}"
        query_vector = self.embedding_service.embed_text(query_text)

        # Search in code_graphs collection
        results = qdrant_client.search(
            collection_name="code_graphs",
            query_vector=query_vector,
            limit=len(file_paths) * 2, # Get more results than files.
        )

        # Extract payloads 
        code_graphs = [hit.payload for hit in results]
        return code_graphs
    
    def get_import_files_by_files(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        '''Retrieve import files for specific files'''
        if not file_paths:
            return []
        
        # Create a query from file paths
        query_text = f"Import files from files: {', '.join(file_paths)}"
        query_vector = self.embedding_service.embed_text(query_text)

        # Search in import_files collection
        results = qdrant_client.search(
            collection_name="import_files",
            query_vector=query_vector,
            limit=len(file_paths) * 2, # Get more results than files.
        )

        # Extract payloads 
        import_files = [hit.payload for hit in results]
        return import_files
    
    def get_related_learnings(self, limit: int = 5) -> List[Dict[str, Any]]:
        '''Retrieve recent learnings (past reviews)'''
        # Use generic query to get recent learnings
        query_text = "Code review feedback and learnings"
        query_vector = self.embedding_service.embed_text(query_text)

        results = qdrant_client.search(
            collection_name="learnings",
            query_vector=query_vector,
            limit=limit
        )

        learnings = [hit.payload for hit in results]
        return learnings
    
    def format_for_ai(
            self,
            code_graphs: List[Dict[str, Any]],
            import_files: List[Dict[str, Any]],
            learnings: List[Dict[str, Any]],
    ) -> str:
        """Format retrieved data into markdown for AI consumption"""
        sections = []

        # Code Graphs Section
        if code_graphs:
            sections.append("## Code Structure\n")
            for graph in code_graphs:
                sections.append(f"**File:** {graph.get('file_path', 'Unknown')}")
                sections.append(f"- Functions: {', '.join(graph.get('functions', []))}")
                sections.append(f"- Classes: {', '.join(graph.get('classes', []))}")
                sections.append(f"- Complexity: {graph.get('node_count', 0)} nodes, {graph.get('edge_count', 0)} edges\n")

        # Import Files Section
        if import_files:
            sections.append("## Import Dependencies\n")
            for imp in import_files:
                sections.append(f"**File:** {imp.get('file_path', 'Unknown')}")
                sections.append(f"- Imports: {', '.join(imp.get('imports', []))}\n")

        # Learnings Section
        if learnings:
            sections.append("## Past Review Learnings\n")
            for learning in learnings:
                sections.append(f"**Commit:** {learning.get('commit_message', 'N/A')}")
                sections.append(f"- Bot Comment: {learning.get('bot_comment', 'N/A')}")
                if learning.get('has_user_feedback'):
                    sections.append(f"- User Feedback: {learning.get('user_feedback', 'N/A')}")
                sections.append("")

        return "\n".join(sections)