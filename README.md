# Real-Time Disaster Management Dashboard

This project is a Streamlit-based dashboard designed to provide real-time disaster management capabilities. It leverages AI, data visualization, and document analysis to assist in disaster response and decision-making.

## Features

* **Real-Time Data Visualization:** Displays disaster-related messages and data in an interactive dashboard.
* **AI-Powered Analysis:** Integrates the DeepSeek API (via OpenAI library) to analyze disaster-related information and provide intelligent responses.
* **Severity Categorization:** Categorizes disaster messages based on severity levels (high, medium, low).
* **Interactive Charts:** Generates interactive charts and graphs to visualize disaster data.
* **PDF Document Analysis:** Allows users to upload or provide URLs to PDF documents for analysis and response guidance.
* **Disaster Response Steps:** Provides step-by-step guidance for different disaster types (wildfire, earthquake, flood).
* **Voice Recognition (Local):** Includes voice recognition capabilities for hands-free interaction (Note: This feature is only available when running the application locally).

## Getting Started

### Prerequisites

* Python 3.7+
* Pip (Python package installer)

### Installation

1.  Clone the repository:

    ```bash
       git clone (https://github.com/khuramhanif/Real-TimeDisasterManagement.git)
    ```

2.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

* **API Key:**
    * This application requires an API key for the DeepSeek API.
    * **Hugging Face Spaces:** If deploying to Hugging Face Spaces, add your API key as a secret named `API_KEY` in the Space settings.
    * **Local Development:** If running locally, set the API key as an environment variable named `API_KEY`.
    * **Google Colab:** If running on Google Colab, add your API key as a Colab secret named `API_KEY`.

### Running the Application

* **Hugging Face Spaces:** The application will automatically run when pushed to a Hugging Face Space.
* **Local Development:** Run the Streamlit application using:

    ```bash
    streamlit run app.py
    ```

## Usage

1.  **Generate Random Messages:** Click the "Generate Random Messages" button to populate the dashboard with sample disaster messages.
2.  **Chatbot:** Use the chatbot to ask questions about disaster management, and it will provide responses based on the uploaded PDF document (if available).
3.  **Voice Recognition:** Click "Start Voice Recognition" to use voice commands (local only).
4.  **Disaster Response Steps:** Select a disaster type to view response steps and related YouTube links.

## Deployment

* This application can be deployed on Hugging Face Spaces for easy sharing and access.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bug fixes or feature requests.


## Contact

Khuram Hanif (https://www.linkedin.com/in/khuram-hanif/)
khuramhanif42@gmail.com
