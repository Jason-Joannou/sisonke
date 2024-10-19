import os
import base64
from typing import Dict, Any, List
import re
from openai import OpenAI
import json

# Set up the OpenAI client
client = OpenAI(
)

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_item_condition(image_paths: List[str]) -> Dict[str, Any]:
    # Encode all images to base64
    encoded_images = [encode_image(path) for path in image_paths]

    # Prepare the messages for the API request
    messages = [
        {
            "role": "system",
            "content": "You are an expert insurance claims evaluator . Provide your analysis in a structured JSON format without any markdown formatting."
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": (
                    "Analyze the attached images of an product and provide the following information:"
                    "\n1. Brand and model (if identifiable) as accurately as possible down to the year and model"
                    "\n2. Condition score (0-100, where 100 is perfect condition)"
                    "\n3. Estimated current market value (in ZAR)"
                    "\n4. Estimated repair or replacement cost (in ZAR)"
                    "\n5. Detailed description of visible damage or missing parts"
                    "\n6. Overall assessment summary"
                    "\nEnsure your response is in valid JSON format without any additional formatting or code blocks."
                )}
            ] + [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}} for img in encoded_images]
        }
    ]

    # Make a request to the OpenAI model
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500
    )

    # Get the response content
    content = response.choices[0].message.content

    # Try to extract JSON from the content
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    # If JSON extraction fails, return the raw content
    return {"raw_response": content}

def analyze_item_condition_service(image_paths: List[str]) -> tuple[bool, Dict[str, Any], Dict[str, Any]]:
    try:
        result = analyze_item_condition(image_paths)

        # Extract data into variables
        brand = result.get('brand', 'Unknown')
        model = result.get('model', 'Unknown')
        condition_score = result.get('condition_score', 0)
        estimated_market_value = result.get('estimated_market_value', 0)
        estimated_repair_cost = result.get('estimated_repair_cost', 0)
        damage_description = result.get('damage_description', {})
        visible_damage = damage_description.get('visible_damage', 'None noted')
        missing_parts = damage_description.get('missing_parts', 'None noted')
        overall_assessment = result.get('overall_assessment', 'No assessment available')

        # Store variables in a dictionary
        variables = {
            'brand': brand,
            'model': model,
            'condition_score': condition_score,
            'estimated_market_value': estimated_market_value,
            'estimated_repair_cost': estimated_repair_cost,
            'visible_damage': visible_damage,
            'missing_parts': missing_parts,
            'overall_assessment': overall_assessment
        }

        return True, variables, result
    except Exception as e:
        return False, {}, {'error': str(e)}

if __name__ == "__main__":
    image_paths = [
        "/Users/darrylnyamayaro/Documents/UCT Notes and stuff/interledger/Interledger Hackathon ChatGPT/samsung.png",
        "/Users/darrylnyamayaro/Documents/UCT Notes and stuff/interledger/Interledger Hackathon ChatGPT/samsung2.png"#,
        #"/Users/darrylnyamayaro/Documents/UCT Notes and stuff/interledger/Interledger Hackathon ChatGPT/offwhite3.png"
    ]
    success, variables, raw_result = analyze_item_condition_service(image_paths)

    if success:
        print("Analysis completed successfully!")
        print("\nExtracted Variables:")
        for key, value in variables.items():
            print(f"{key}: {value}")

        print("\nRaw JSON Result:")
        print(json.dumps(raw_result, indent=2))
    else:
        print("Analysis failed.")
        print("Error:", raw_result['error'])