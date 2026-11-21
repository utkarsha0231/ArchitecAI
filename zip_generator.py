import re
import io
import zipfile


def extract_files(ai_output):
    """
    Extract multiple files from AI-generated markdown code.
    Supports filename headings and fenced code blocks.
    """

    files = {}

    if isinstance(ai_output, dict):
        ai_output = str(ai_output)

    text = str(ai_output).strip()

    # Pattern: ### main.py / **main.py** / `main.py`
    pattern = r'(?im)^\s{0,3}(?:#{1,6}\s+|\*\*)?([A-Za-z0-9_./\\-]+\.[A-Za-z0-9]+)(?:\*\*|`)?\s*$'
    matches = list(re.finditer(pattern, text))

    if matches:
        for i, match in enumerate(matches):
            filename = match.group(1).strip().replace("\\", "/")

            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

            section = text[start:end]

            code_match = re.search(
                r"```(?:[a-zA-Z0-9_+-]*)\s*\n(.*?)```",
                section,
                re.DOTALL
            )

            if code_match:
                code = code_match.group(1).strip()
                if code:
                    files[filename] = code

    # Fallback: if no files found, use first code block as main.py
    if not files:
        code_blocks = re.findall(
            r"```(?:python)?\s*\n(.*?)```",
            text,
            re.DOTALL
        )

        if code_blocks:
            files["main.py"] = code_blocks[0].strip()

        else:
            # Plain Python output fallback
            if text and ("import " in text or "def " in text or "class " in text):
                files["main.py"] = text

    # Ensure main.py exists
    if "main.py" not in files:
        python_files = [
            name for name in files
            if name.endswith(".py")
        ]

        if python_files:
            files["main.py"] = files[python_files[0]]

    return files


def create_project_zip(ai_output, project_name="ArchitecAI_Generated_Project"):
    """
    Create a ZIP containing AI-generated project files.
    Returns ZIP data as BytesIO.
    """

    files = extract_files(ai_output)

    # Default files if AI output is incomplete
    if "README.md" not in files:
        files["README.md"] = f"""# {project_name}

This project was generated using ArchitecAI.

## How to run

1. Install Python.
2. Install dependencies using:

    pip install -r requirements.txt

3. Run the project using:

    python main.py
"""

    if "requirements.txt" not in files:
        files["requirements.txt"] = "streamlit\npandas\n"

    # Create ZIP in memory
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(
        zip_buffer,
        mode="w",
        compression=zipfile.ZIP_DEFLATED
    ) as zip_file:

        for filename, content in files.items():

            # Avoid unsafe paths
            filename = filename.replace("\\", "/").lstrip("/")

            if ".." in filename.split("/"):
                continue

            zip_file.writestr(filename, content)

        # Add README if missing
        if "README.md" not in files:
            zip_file.writestr("README.md", "# Generated Project")

    zip_buffer.seek(0)

    return zip_buffer


# Compatibility aliases
generate_project_zip = create_project_zip
build_project_zip = create_project_zip