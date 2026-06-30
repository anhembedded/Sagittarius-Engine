import ast
import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path
from typing import List, Dict, Any

class CodeVisitor(ast.NodeVisitor):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.items = []

    def visit_ClassDef(self, node: ast.ClassDef):
        docstring = ast.get_docstring(node)
        self.items.append({
            'type': 'class',
            'name': node.name,
            'filepath': self.filepath,
            'docstring': docstring,
            'lineno': node.lineno
        })
        self.generic_visit(node)

    def _extract_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        args = []
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {ast.unparse(arg.annotation)}"
            args.append(arg_str)

        returns = ""
        if node.returns:
            returns = f" -> {ast.unparse(node.returns)}"

        return f"({', '.join(args)}){returns}"

    def visit_FunctionDef(self, node: ast.FunctionDef):
        docstring = ast.get_docstring(node)
        signature = self._extract_signature(node)
        self.items.append({
            'type': 'function',
            'name': node.name,
            'signature': signature,
            'filepath': self.filepath,
            'docstring': docstring,
            'lineno': node.lineno
        })
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        docstring = ast.get_docstring(node)
        signature = self._extract_signature(node)
        self.items.append({
            'type': 'async_function',
            'name': node.name,
            'signature': signature,
            'filepath': self.filepath,
            'docstring': docstring,
            'lineno': node.lineno
        })
        self.generic_visit(node)

def parse_codebase(src_dir: str) -> List[Dict[str, Any]]:
    print(f"Parsing codebase in {src_dir}...")
    extracted_items = []
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    tree = ast.parse(content)
                    visitor = CodeVisitor(filepath)
                    visitor.visit(tree)
                    extracted_items.extend(visitor.items)
                except Exception as e:
                    print(f"Error parsing {filepath}: {e}")

    print(f"Extracted {len(extracted_items)} items from codebase.")
    return extracted_items

def generate_embeddings(items: List[Dict[str, Any]], model_name: str = 'all-MiniLM-L6-v2'):
    print(f"Loading embedding model {model_name}...")
    model = SentenceTransformer(model_name)

    texts_to_embed = []
    for item in items:
        # Create a rich text representation for embedding
        text = f"{item['type']} {item['name']}"
        if 'signature' in item and item['signature']:
            text += item['signature']
        if item['docstring']:
            text += f"\nDocstring: {item['docstring']}"
        texts_to_embed.append(text)

    print(f"Generating embeddings for {len(texts_to_embed)} items...")
    embeddings = model.encode(texts_to_embed, show_progress_bar=True)
    return np.array(embeddings, dtype=np.float32)

def build_kb(src_dir: str, output_dir: str):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 1. Parse Codebase
    items = parse_codebase(src_dir)

    if not items:
        print("No items found to index. Exiting.")
        return

    # Assign IDs to items
    for i, item in enumerate(items):
        item['id'] = i

    # 2. Generate Embeddings
    embeddings = generate_embeddings(items)

    # 3. Build FAISS Index
    dimension = embeddings.shape[1]
    print(f"Building FAISS index with dimension {dimension}...")
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # 4. Save metadata and index
    index_path = os.path.join(output_dir, "codebase.index")
    faiss.write_index(index, index_path)

    metadata_path = os.path.join(output_dir, "metadata.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2)

    print(f"Knowledge Base successfully built!")
    print(f"- Index saved to: {index_path}")
    print(f"- Metadata saved to: {metadata_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build an AI-ready Knowledge Base for the codebase.")
    parser.add_argument("--src", type=str, default="src", help="Source directory to parse")
    parser.add_argument("--out", type=str, default="docs/kb", help="Output directory for KB files")

    args = parser.parse_args()
    build_kb(args.src, args.out)
