import openai
import os
from dotenv import load_dotenv

def test_openai_connection():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    
    # Initialize the OpenAI client
    client = openai.OpenAI(api_key=api_key)
    
    try:
        # Test connection with a simple prompt
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who are you?"}
            ]
        )
        
        print("Connection successful!")
        print("\nModel response:")
        print(response.choices[0].message.content)
        
    except openai.AuthenticationError:
        print("Authentication Error: Please check your OpenAI API key")
    except openai.APIConnectionError:
        print("Connection Error: Unable to connect to OpenAI API")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print("Testing connection to OpenAI API...")
    test_openai_connection()
