# TikTok CSV Manager

Since TikTok Affiliate outreach involves managing large datasets and extracting usernames from various sources, TikTok CSV Manager is a powerful, local-first Streamlit application designed to streamline these workflows. It offers a modern, intuitive interface for creating, editing, splitting, and processing CSV files specifically tailored for TikTok affiliate management.

## Features

- **📂 File Manager**: Upload existing CSVs or create new ones from scratch with custom columns.
- **✍️ Advanced Data Editor**: Interactive spreadsheet interface to edit cells, filter rows, rename columns, and drop unnecessary data.
- **📦 Batch Splitter**: Automatically split large CSV files into smaller, manageable chunks based on row count (perfect for daily outreach limits).
- **🔍 Username Extractor**: intelligent tool to extract clean `@usernames` from unstructured text dumps.
- **🎨 Modern UI**: User-friendly dark mode interface with responsive design.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/MyTikTok_CSV_Manager.git
    cd MyTikTok_CSV_Manager
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the application locally using Streamlit:

```bash
streamlit run app.py
```

The application will open automatically in your comprehensive web browser at `http://localhost:8501`.

## Project Structure

- `app.py`: Main application file containing the Streamlit frontend and logic.
- `requirements.txt`: List of Python dependencies.
- `mytiktok_csv_manager.py`: (Legacy) Original CLI script for reference.

## Technologies Used

- [Streamlit](https://streamlit.io/) - For the interactive web interface.
- [Pandas](https://pandas.pydata.org/) - For efficient data manipulation.

## License

MIT License
