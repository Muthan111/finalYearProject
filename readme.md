# Activate the Scripts
myenv/Scripts/Activate  

# Install the required packages
pip install -r requirements.txt

# Start the server
uvicorn src.main:app --reload