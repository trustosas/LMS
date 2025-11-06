# LMS

A Library Management System (LMS) built with a Python backend and a TypeScript (React) frontend.

## Project Structure

- `/client` – React/TypeScript frontend
- `/server` – Django/Python backend

## Getting Started

### Prerequisites

- Node.js & npm
- Python (recommended: 3.8+)
- Django (installed via requirements.txt)
- Virtual environment for Python (`venv`)

### Frontend Setup

1. Navigate to the client directory:
    ```bash
    cd C:\Users\HP\Desktop\LMS\client
    ```
2. Set environment variable for API URL:
    ```bash
    echo VITE_API_URL=http://127.0.0.1:8000 > .env
    ```
3. Install dependencies and run the development server:
    ```bash
    npm install
    npm run dev
    ```
   - The frontend app will be available at `http://localhost:5173` (default Vite port).

### Backend Setup

1. Navigate to the server directory:
    ```bash
    cd C:\Users\HP\Desktop\LMS\server
    ```
2. Activate the Python virtual environment:
    ```bash
    .\venv\Scripts\Activate
    ```
3. Install backend dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the Django development server:
    ```bash
    python manage.py runserver
    ```
   - The backend API will be available at `http://127.0.0.1:8000`.

## Usage

Start both frontend and backend development servers following the steps above. By default, the frontend is configured to proxy API calls to the backend using the `VITE_API_URL` environment variable.

## Contributing

Feel free to open issues or pull requests!

## License

[MIT](LICENSE)
