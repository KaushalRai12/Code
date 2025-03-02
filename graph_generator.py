import matplotlib.pyplot as plt
import os
from collections import Counter

def generate_graph(results):
    """Generates a bar chart for document classification counts"""

    # Count document categories
    category_counts = Counter([doc['document_type'] for doc in results])

    # Prepare data for the bar chart
    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    # Create a bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(categories, counts)
    plt.xlabel("Document Categories")
    plt.ylabel("Number of Documents")
    plt.title("Document Classification Overview")
    plt.xticks(rotation=45, ha="right")

    # Ensure static folder exists
    static_folder = "static"
    os.makedirs(static_folder, exist_ok=True)

    # Save graph as an image
    graph_path = os.path.join(static_folder, "classification_graph.png")
    plt.savefig(graph_path, bbox_inches="tight")
    plt.close()
