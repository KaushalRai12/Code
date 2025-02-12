import requests
import json

def test_connection():
    # API endpoint for local Ollama instance
    url = "http://localhost:11434/api/generate"
    
    # Request payload
    payload = {
        "model": "llama2",
        "prompt": "Who are you?",
        "stream": False
    }
    
    try:
        # Send POST request to Ollama
        response = requests.post(url, json=payload)
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            print("Connection successful!")
            print("\nModel response:")
            print(result['response'])
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Connection failed! Make sure Ollama is running locally.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print("Testing connection to local Llama 2 model...")
    test_connection()
