Audio Summarizer UI
A web-based application built with Gradio and Azure AI to summarize audio content from uploaded WAV files, microphone recordings, or URLs. The application uses Azure OpenAI to process and generate summaries of audio data based on user-defined prompts.
Table of Contents

About the Project
Features
Getting Started
Prerequisites
Installation


Usage
Contributing
License
Contact
Acknowledgments

About the Project
This project provides a user-friendly interface for summarizing audio files (in WAV or MP3 format) using Azure's AI services and OpenAI's language models. Users can upload audio files, record audio directly, or provide a URL to an audio file. The application processes the audio, encodes it to base64, and sends it to Azure OpenAI for summarization based on customizable system and user prompts.
Built With

Python 3.8+
Gradio for the web interface
Azure AI Projects for AI processing
Azure Identity for authentication
python-dotenv for environment variable management
Requests for HTTP requests

Features

Upload WAV/MP3 files for summarization
Record audio directly from the microphone
Summarize audio from a provided URL
Customizable system and user prompts for tailored summarization
Integration with Azure OpenAI for robust audio analysis
Clean and intuitive Gradio-based UI

Getting Started
Prerequisites

Python 3.8 or higher
An Azure account with access to Azure AI Projects and OpenAI services
A valid Azure endpoint and model deployment for OpenAI
pip (Python package manager)

Installation

Clone the repository:git clone https://github.com/samir72/audio-summarizer-ui.git


Navigate to the project directory:cd audio-summarizer-ui


Create a virtual environment (optional but recommended):python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:pip install -r requirements.txt


Set up environment variables:Create a .env file in the project root and add the following:AC_PROJECT_ENDPOINT=your_azure_project_endpoint
AC_MODEL_DEPLOYMENT=your_openai_model_deployment

Replace your_azure_project_endpoint and your_openai_model_deployment with your Azure AI project endpoint and model deployment name, respectively.
Ensure Azure credentials:The application uses DefaultAzureCredential for authentication. Ensure you have configured your Azure credentials (e.g., via Azure CLI or environment variables). Refer to Azure Identity documentation for details.

Usage

Run the application:python app.py


Open the Gradio interface in your browser (the URL will be displayed in the terminal, typically http://127.0.0.1:7860).
Choose one of the following options:
Upload a WAV or MP3 file.
Record audio using your microphone.
Enter a URL to a publicly accessible audio file.


Optionally, customize the System Prompt and User Prompt to guide the summarization process.
Click Summarize to process the audio and view the generated summary.

Example

System Prompt: "You are an AI assistant tasked with summarizing customer inquiries from audio recordings."
User Prompt: "Summarize the key points of the audio content."
Output: A concise text summary of the audio content.

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/YourFeature).
Commit your changes (git commit -m 'Add YourFeature').
Push to the branch (git push origin feature/YourFeature).
Open a Pull Request.

Please adhere to the Code of Conduct and review the Contributing Guidelines.
License
Distributed under the MIT License. See LICENSE for more information.
Contact
Your Name - syedamirhusain@gmail.com
Project Link: https://github.com/samir72/audio-summarizer-ui
Acknowledgments

Gradio for the easy-to-use UI framework
Azure AI for powerful AI capabilities
OpenAI for advanced language models
Best-README-Template for README inspiration
