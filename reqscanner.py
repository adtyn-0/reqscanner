import os
import ast
import sys
import pathlib
import importlib.util
import pkg_resources

# Root path
PROJECT_DIR = pathlib.Path(__file__).resolve().parent

# Installed pip packages
installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

# Import alias → PyPI name
alias_map = {
    "PIL": "pillow",
    "cv2": "opencv-python",
    "sklearn": "scikit-learn",
    "bs4": "beautifulsoup4",
    "yaml": "PyYAML",
    "decouple": "python-decouple",
    "rest_framework": "djangorestframework",
    "rest_framework_simplejwt": "djangorestframework-simplejwt",
    "corsheaders": "django-cors-headers",
    "ImageTk": "pillow",
    "PyAutoGUI": "pyautogui",
    "pyautogui": "pyautogui",
    "np": "numpy",
    "pd": "pandas",
    "sns": "seaborn",
    "plt": "matplotlib",
    "dt": "datetime",
    "jwt": "PyJWT",
    "flask_sqlalchemy": "flask_sqlalchemy",
    "flask_login": "flask_login",
    "flask_wtf": "flask_wtf",
    "wtforms": "wtforms",
    "dotenv_values": "python-dotenv",
    "httpx": "httpx",
    "httpcore": "httpcore",
    "requests_ntlm": "requests_ntlm",
    "sqlparse": "sqlparse",
    "pytz": "pytz",
    "cv": "opencv-python",
    "crypt": "cryptography",
    "PyJWT": "PyJWT",
    "mpl": "matplotlib",
    "lgb": "lightgbm",
    "xgb": "xgboost",
    "qiskit": "qiskit",
    "aer": "qiskit-aer",
    "sk": "scikit-learn",
    "sym": "sympy",
    "alt": "altair",
    "py": "pyyaml",
    "pycryptodome": "pycryptodome",
    "dotenv": "python-dotenv",
    "jax": "jax",
}


def extract_imports(path):
    imports = set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=path)
    except SyntaxError:
        return imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return imports


def gather_all_imports(root):
    found = set()
    for dirpath, _, files in os.walk(root):
        if 'venv' in dirpath or '__pycache__' in dirpath:
            continue
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(dirpath, file)
                found |= extract_imports(full_path)
    return found


def is_third_party(module):
    try:
        spec = importlib.util.find_spec(module)
        if spec and spec.origin:
            stdlib_path = os.path.dirname(os.__file__)
            return not spec.origin.startswith(stdlib_path)
    except:
        pass
    return False


def generate_requirements(imports):
    result = {}
    for mod in imports:
        package_name = alias_map.get(mod, mod).lower()
        if package_name in installed and is_third_party(mod):
            result[package_name] = installed[package_name]
        else:
            reason = []
            if package_name not in installed:
                reason.append("not installed or stdlib/internal")
            joined = ", ".join(reason) if reason else "unknown"
            print(f"Skipped: {mod} -> {package_name} ({joined})")
    return result


def write_requirements(reqs, file="requirements.txt"):
    with open(file, "w", encoding="utf-8") as f:
        for pkg, ver in sorted(reqs.items()):
            f.write(f"{pkg}=={ver}\n")
    print(f"\nSaved {len(reqs)} packages to {file}")


if __name__ == "__main__":
    print(f"Scanning: {PROJECT_DIR}\n")
    all_imports = gather_all_imports(PROJECT_DIR)
    matched = generate_requirements(all_imports)
    write_requirements(matched)
