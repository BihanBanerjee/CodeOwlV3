import uuid
from typing import List, Dict, Any
from qdrant_client.models import PointStruct

from src.utils.qdrant_client import qdrant_client
from src.db.embedding_service import EmbeddingService

class VectorIndexer:
    """Indexes code data into Qdrant vector collections"""
    def __init__(self):
        self.embedding_service = EmbeddingService()
    
    def index_code_graph(self, file_path: str, graph_data: Dict[str, Any]) -> str:
        """Index code graph structure into Qdrant"""
        embedding = self.embedding_service.embed_code_graph(graph_data)

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                'type': 'code_graph',
                'file_path': file_path,
                'functions': graph_data.get('functions', []),
                'classes': graph_data.get('classes', []),
                'calls': graph_data.get('calls', []),
                'node_count': graph_data.get('nodes', 0),
                'edge_count': graph_data.get('edges', 0)
            },
        )

        qdrant_client.upsert(collection_name='code_graphs', points=[point])
        return point.id
    
    def index_import_file(self, file_path: str, source_code: str, imports: List[str]) -> str:
        """Index import file into Qdrant"""
        embedding = self.embedding_service.embed_import_file(file_path, source_code, imports)

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                'type': 'import_file',
                'file_path': file_path,
                'source_code': source_code[:1000], # Store first 1000 characters
                'imports': imports,
                'import_count': len(imports),
            },
        )

        qdrant_client.upsert(collection_name='import_files', points=[point])
        return point.id
    
    def index_learning(self, commit_msg: str, bot_comment: str, user_feedback:str = "", code_context: str = "") -> str:
        """Index learning (past review feedback) into Qdrant"""
        embedding = self.embedding_service.embed_learning(
            commit_message=commit_msg,
            bot_comment=bot_comment,
            user_feedback=user_feedback,
            code_context=code_context,
        )

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                'type': 'learning',
                'commit_message': commit_msg,
                'bot_comment': bot_comment,
                'user_feedback': user_feedback if user_feedback else None,
                'has_user_feedback': bool(user_feedback),
                'code_context': code_context[:1000] if code_context else "",
            },
        )

        qdrant_client.upsert(collection_name='learnings', points=[point])
        return point.id