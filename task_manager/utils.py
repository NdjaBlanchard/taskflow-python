import uuid

def generate_id():
    """Generate an unique ID for each task"""
    return str(uuid.uuid4())