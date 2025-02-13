import ast
import os

import importlib.metadata


def get_installed_packages() -> set:
    """Get installed packages inside .venv using importlib.metadata."""
    installed = {pkg.metadata["Name"].lower() for pkg in importlib.metadata.distributions()}
    return installed


def get_imported_modules(project_path) -> set:
    """Scan all Python files in the project for imported modules, ignoring .venv."""
    imported_modules = set()

    for root, _, files in os.walk(project_path):
        # Skip the virtual environment directory
        if ".venv" in root:
            continue

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"Scanning {file_path}...")
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        tree = ast.parse(f.read(), filename=file_path)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imported_modules.add(alias.name.split(".")[0])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    imported_modules.add(node.module.split(".")[0])
                except SyntaxError:
                    print(f"Skipping {file_path} due to syntax error.")

    return imported_modules

def analyze_dependencies(project_path) -> tuple[set, set, set]:
    installed_packages = get_installed_packages()
    imported_modules = get_imported_modules(project_path)

    used_dependencies = installed_packages.intersection(imported_modules)
    unused_dependencies = installed_packages - imported_modules
    missing_dependencies = imported_modules - installed_packages

    return used_dependencies, unused_dependencies, missing_dependencies


if __name__ == "__main__":
    project_directory = os.path.dirname(os.path.abspath(__file__))
    used, unused, missing = analyze_dependencies(project_directory)

    print("\nUsed Dependencies:\n", used)
    print("\nUnused Dependencies:\n", unused)
    print("\nMissing Dependencies:\n", missing)
