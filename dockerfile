# Use an official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app/src

# Copy the current directory contents into the container
COPY . /app

# Delete the ressources folder, as it will be mounted into the container
RUN rm -rf /app/src/ressources

# Install necessary Python packages (streamlit)
RUN pip install --no-cache-dir streamlit pyyaml streamlit_code_editor

# Create a non-root user and switch to it
RUN useradd -m myuser
USER myuser

# Expose port (Streamlit default port)
EXPOSE 8501

# Run the Streamlit app with the specified command
CMD ["streamlit", "run", "app.py", "--theme.base=dark", "--theme.primaryColor=#ea0a8e"]
