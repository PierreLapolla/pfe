# Use the official LaTeX image from Docker Hub
FROM texlive/texlive

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the src directory into the container
COPY src /app

# Run pdflatex on the main LaTeX file
RUN pdflatex main.tex
