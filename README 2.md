# Introduction 
- The architecture of this chatbot based on Rasa, by the way built by own 's architecture.

# Install and Run
- Installing the necessary and dependent library by command:
    - For Backend:  cd backend && pip install -r requirements.txt
    - **(OPTIONAL)** For Frontend: cd frontend && npm i(npm>=6.14.12 && nodejs>=v14.16.1)  
- Running the process by following command:
    - Terminal 1: pip install -e . && cd backend && python app.py
    - Terminal 2: cd frontend && npm start


# Notes:
- In folder `backend`, file `app.log` logged all errors when API go wrong.
- In folder `frontend`, if folder `node_modules` is missing or get something wrong when running(error is raised compatible version), remove it and install by **(OPTIONAL)**