from pathlib import Path

import docker

BASE_PATH = Path("/home/pierre/PycharmProjects/pfe/rapport")  # Change this to your project folder
LATEX_FOLDER = BASE_PATH / "src"
DOCKERFILE_PATH = BASE_PATH
OUTPUT_FOLDER = BASE_PATH / "output"


def build_container(client, dockerfile_path):
    """Build the Docker container from the provided Dockerfile."""
    print(f"Building Docker image from {dockerfile_path}...")
    try:
        image, logs = client.images.build(path=str(dockerfile_path), tag="latex-compiler")
        for log in logs:
            print(log.get('stream', '').strip())
        print("Docker image built successfully.")
        return image
    except docker.errors.BuildError as e:
        print(f"Error during build: {e}")
        return None


def compile_latex(folder_path, output_path, client):
    """Compile LaTeX by running a Docker container with the LaTeX files."""
    folder_path = folder_path.resolve()
    output_path = output_path.resolve()
    if not folder_path.is_dir():
        print(f"Error: The folder {folder_path} does not exist.")
        return
    tex_file = folder_path / "main.tex"
    if not tex_file.exists():
        print(f"Error: main.tex not found in {folder_path}.")
        return
    output_path.mkdir(exist_ok=True)
    try:
        print(f"Compiling LaTeX in {folder_path}...")
        container = client.containers.run(
            image="latex-compiler",
            command="pdflatex -output-directory /output /app/main.tex",
            volumes={
                str(folder_path): {'bind': '/app', 'mode': 'rw'},
                str(output_path): {'bind': '/output', 'mode': 'rw'}
            },
            remove=True
        )
        print("LaTeX compilation finished.")
        print(f"Output PDF is located in {output_path / 'main.pdf'}")
    except docker.errors.ContainerError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    client = docker.from_env()
    if build_container(client, DOCKERFILE_PATH):
        compile_latex(LATEX_FOLDER, OUTPUT_FOLDER, client)
    client.close()
