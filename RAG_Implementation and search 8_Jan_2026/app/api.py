from fastapi import APIRouter, HTTPException
from RAG.retrival.search import similarity_search
from RAG.vector_store.vector_store import get_qdrant_client, COLLECTION_NAME

router = APIRouter()


@router.get("/search")
def search(query: str):
    """
    Search top 3 most relevant chunks for a given query.
    """
    try:
        results = similarity_search(query, top_k=3)

        return {
            "query": query,
            "top_k": 3,
            "results": results
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/chunks")
def get_all_chunks():
    """
    Return all chunks stored in Qdrant (debug / inspection endpoint).
    """
    try:
        client = get_qdrant_client()

        points, _ = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=1000
        )

        client.close()

        return {
            "total_chunks": len(points),
            "chunks": [
                {
                    "chunk_id": p.payload.get("chunk_id"),
                    "text": p.payload.get("text")
                }
                for p in points
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch chunks: {str(e)}"
        )
