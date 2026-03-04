import random
import string

try:
    from captcha.image import ImageCaptcha
    HAS_CAPTCHA_LIB = True
except ImportError:
    HAS_CAPTCHA_LIB = False

def generate_math_captcha():
    """Generates a simple math text-based captcha (no dependencies required)."""
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-', '*'])
    
    if operator == '+':
        answer = num1 + num2
    elif operator == '-':
        # Ensure positive result for simplicity
        if num1 < num2:
            num1, num2 = num2, num1
        answer = num1 - num2
    else:
        answer = num1 * num2
        
    question = f"What is {num1} {operator} {num2}?"
    return question, str(answer)

def generate_text_string(length=6):
    """Generates a random alphanumeric string for a captcha."""
    characters = string.ascii_letters + string.digits
    captcha_text = ''.join(random.choice(characters) for _ in range(length))
    return captcha_text

import os

def generate_image_captcha(text=None, filename="captcha.png", output_dir="."):
    """
    Generates an image captcha and saves it to a file. 
    Requires the 'captcha' library (pip install captcha).
    """
    if not HAS_CAPTCHA_LIB:
        print("The 'captcha' library is not installed.")
        print("To generate image captchas, please install it by running: pip install captcha")
        return None, None
        
    if text is None:
        text = generate_text_string()
        
    image = ImageCaptcha(width=280, height=90)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create the full path to save the image
    filepath = os.path.join(output_dir, filename)
    
    # Save the image to the specified path
    image.write(text, filepath)
    print(f"Image captcha generated and saved as: {filepath}")
    
    return text, filepath

if __name__ == "__main__":
    print("=== Demo 1: Math Text Captcha ===")
    question, correct_answer = generate_math_captcha()
    print(f"Question: {question}")
    
    # Simulate user input
    user_input = input("Enter your answer: ")
    if user_input.strip() == correct_answer:
        print("Success! You verified you are human.")
    else:
        print(f"Failed. The correct answer was {correct_answer}.")
        
    print("\n=== Demo 2: Image Captcha ===")
    if HAS_CAPTCHA_LIB:
        expected_text, img_file = generate_image_captcha()
        print(f"Please open '{img_file}' to view the captcha.")
        user_input = input("Enter the text seen in the image: ")
        
        if user_input.strip() == expected_text:
            print("Success! Captcha solved correctly.")
        else:
            print(f"Failed. The correct text was '{expected_text}'.")
    else:
        generate_image_captcha() # This will print the install instructions
