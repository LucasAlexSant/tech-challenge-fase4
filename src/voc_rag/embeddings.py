"""Geração de embeddings para documentos e perguntas."""


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Retorna um vetor por texto usando o modelo definido em config.EMBEDDING_MODEL."""
    raise NotImplementedError
