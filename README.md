Subway Locator App for Kuala Lumpur, Malaysia

This web application allows users to locate Subway branches in Kuala Lumpur, Malaysia. The application consists of three main components:

1. Data Scraping (./web_scrap/main.py):

   - Run `main.py` to scrape Subway location details from the map and store them in the SQLite database (`subway.db`).

2. Backend API (./backend/main.py):

   - After scraping the data, start the FastAPI backend by running:
     ```
     uvicorn backend.main:app --reload
     ```
   - This will launch the FastAPI server, providing endpoints to access Subway branch data.

3. Frontend Web App (.frontend/main.py):
   - Open a new terminal and run the Streamlit app using:
     ```
     streamlit run ./app/main_streamlit.py
     ```
   - This will start the Streamlit application, allowing users to interact with the API and visualize Subway outlets on a map.

Prerequisites:

- Python 3.11.5
- Pip (Python package installer)

Setup:

1. Create and Activate Virtual Environment:

   - Open a terminal and navigate to the project directory.
   - Create a virtual environment:
     ```bash
     python3 -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       .\venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

2. Install Dependencies:

   - Install the required Python packages by running the following command in your terminal:
     ```bash
     pip install -r requirements.txt
     ```

3. Create .env file:

   - Create a `.env` file in the project root directory and add the following environment variables:
     ```
     OPENAI_API_KEY=sk-CCECECCILCOEICONNWEICNECIENCICWCN
     ```

4. Scrape Subway Data:

   - Run the data scraping script to populate the database:
     ```bash
     python ./web_scrap/main.py
     ```

5. Run FastAPI Backend:

   - Start the FastAPI server:
     ```bash
     uvicorn backend.main:app --reload
     ```

6. Run Streamlit Frontend:
   - Open a new terminal (while keeping the virtual environment activated) and run the Streamlit app:
     ```bash
     streamlit run ./frontend/main.py
     ```

Access the Application:

- Once the FastAPI server is running, the API documentation will be available at `http://127.0.0.1:8000/docs`. You can interact with the API using this Swagger UI.
- Open the Streamlit app at `http://localhost:8501` to visualize Subway outlets on the map and explore the application features.

Feel free to reach out for any questions or issues!
