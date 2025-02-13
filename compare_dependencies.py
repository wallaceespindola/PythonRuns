import ast
import importlib.metadata
import os

# Set PROJECT_DIR to the script's directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(PROJECT_DIR, ".venv")


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


def compare_dependencies() -> None:
    """Compare installed vs imported dependencies."""
    installed_packages = get_installed_packages()
    imported_modules = get_imported_modules(PROJECT_DIR)

    used_dependencies = installed_packages.intersection(imported_modules)
    unused_dependencies = installed_packages - imported_modules
    missing_dependencies = imported_modules - installed_packages

    print("\n📌 Dependency Comparison:\n")
    print("✅ Used Dependencies (Installed & Imported):")
    print(sorted(used_dependencies))

    print("\n❌ Unused Dependencies (Installed but NOT used):")
    print(sorted(unused_dependencies))

    print("\n⚠️ Missing Dependencies (Used but NOT installed):")
    print(sorted(missing_dependencies))


if __name__ == "__main__":
    compare_dependencies()
