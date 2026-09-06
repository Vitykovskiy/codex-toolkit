DOCUMENTS = {
    "a-1": {"organization_id": "org-a", "text": "Synthetic A"},
    "b-1": {"organization_id": "org-b", "text": "Synthetic B"},
}
ACTORS = {"alice": {"organization_id": "org-a"}, "bob": {"organization_id": "org-b"}}


def handle_request(method, path, actor):
    """HTTP adapter supplies an authenticated actor from trusted middleware."""
    if actor is None:
        return 401, {"error": "authentication required"}
    if method != "GET" or not path.startswith("/documents/"):
        return 404, {"error": "not found"}
    document_id = path.removeprefix("/documents/")
    document = DOCUMENTS.get(document_id)
    if document is None:
        return 404, {"error": "not found"}
    return 200, document
