from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams,PointStruct,PayloadSchemaType

from app.config import QDRANT_URL, QDRANT_API_KEY


COLLECTION_NAME = "leetcode_problems"


client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)


def create_collection():

    collections = client.get_collections()

    collection_names = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME not in collection_names:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        

        print(f"Collection '{COLLECTION_NAME}' created.")

    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")
    
    client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="difficulty",
    field_schema=PayloadSchemaType.KEYWORD
)
    client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="primary_pattern",
    field_schema=PayloadSchemaType.KEYWORD
)
    print("Difficulty index ready.")


def insert_problem(problem, embedding):

    point = PointStruct(
        id=problem["problem_id"],
        vector=embedding,
        payload={
            "problem_id": problem["problem_id"],
            "title": problem["title"],
            "difficulty": problem["difficulty"],
            "description": problem["description"],
            "tags": problem["tags"],
            "url": problem["url"],
            "primary_pattern": problem["primary_pattern"],
            "secondary_patterns": problem["secondary_patterns"],
            "reason": problem["reason"]
        }
    )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[point]
    )