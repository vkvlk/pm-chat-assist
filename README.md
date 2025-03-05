# MS Project AI Assistant

This project is a Streamlit-based AI assistant designed to help users with project scheduling questions in MS Project. The assistant leverages AI models to provide actionable insights and optimize project timelines.

## Features

- Upload project schedule data in Excel format.
- Analyze project schedules for holiday and weekend impacts.
- Detect scheduling inconsistencies and suggest optimizations.
- Maintain a chat history with the last 10 messages for context.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/pm-chat-assist.git
   cd pm-chat-assist
   ```

2. Create and activate a virtual environment:

   ```sh
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   ```

3. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

4. Create a .env file in the root directory with your OpenRouter API key:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```

## Usage

1. Run the Streamlit app:

   ```sh
   streamlit run app.py
   ```

2. Open your web browser and navigate to the provided URL (usually `http://localhost:8501`).

3. Upload your project schedule data in Excel format using the sidebar.

4. Enter your OpenRouter API key in the sidebar.

5. Select the AI model you want to use.

6. Ask questions about your project schedule in the chat input.

## Project Structure

- app.py: Main application file.
- config.py: Configuration settings.
- dataset.py: Data loading and processing utilities.
- llm.py: AI model querying logic.
- models.py: Data models.
- requirements.txt: List of required Python packages.
