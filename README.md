# Personalized Restaurant Search

an autonomous AI agent

# How to Run?

### Create a `.env`file with the following

```OPENAI_API_KEY = "<your open ai api key>"
GOOGLE_MAPS_API_KEY = "<google maps api key>"
```

### Run the app
To install requirements: `pip install -r  requirements.txt`

To run the app: `python3 main.py`

### Endpoints

1. POST `/query` with the following body:
```
{
    "address" : "2000 Central Dr Boulder, CO",
    "dietaryRestrictions" : "peanut allergy"
}
```