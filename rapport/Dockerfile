# Use the official LaTeX image from Docker Hub
FROM texlive/texlive

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the src directory into the container
COPY src /app

# Run pdflatex on the main LaTeX file
RUN pdflatex -interaction=nonstopmode main.tex

# Ensure that the main.aux file exists before running bibtex
RUN test -f main.aux && bibtex main || echo "Skipping bibtex as main.aux not found"

# Run pdflatex multiple times to resolve cross-references
RUN pdflatex -interaction=nonstopmode main.tex
RUN pdflatex -interaction=nonstopmode main.tex
