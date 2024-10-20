import openai

# Set up the OpenAI client (replace with your actual API key)
openai.api_key = ""


def generate_unemployment_premium_and_risk_profile(job_name: str, company: str, industry: str, income: float) -> dict:
    """
    This function generates an estimated insurance premium for unemployment and a risk profile based on job details.
    The response is structured to return only the premium and risk profile in a simple format: 'Premium, RiskProfile'.
    """
    # Prepare the message prompt for OpenAI API
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert insurance premium evaluator centered to evaluate the risk of informal earners. Based on the provided job details, "
                "company, industry, and monthly income, generate an estimated unemployment insurance premium "
                "and a risk profile for an individual."
            )
        },
        {
            "role": "user",
            "content": (
                f"Job Name: {job_name}\n"
                f"Company: {company}\n"
                f"Industry: {industry}\n"
                f"Income: {income}\n"
                "Please provide the response in the following format: 'Premium, RiskProfile'. "
                "For example, '60.0, Medium Risk'."
            )
        }
    ]

    # Use your original response call
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=50
    )

    # Extract the content from the response
    response_content = response.choices[0].message.content.strip()

    # Split the response into premium and risk profile
    premium, risk_profile = response_content.split(',')

    return {
        "Estimated monthly unemployment insurance premium": premium.strip(),
        "Risk profile": risk_profile.strip()
    }


def main():
    print("Unemployment Insurance Premium and Risk Profile Generator\n")

    # Input job details
    job_name = input("Enter the job title: ")
    company = input("Enter the company name: ")
    industry = input("Enter the industry: ")
    income = float(input("Enter the monthly income (in ZAR): "))

    # Generate the unemployment insurance premium and risk profile
    try:
        result = generate_unemployment_premium_and_risk_profile(job_name, company, industry, income)

        # Extract and display the results
        premium = result.get("Estimated monthly unemployment insurance premium", "N/A")
        risk_profile = result.get("Risk profile", "N/A")

        print(f"\nEstimated Monthly Unemployment Insurance Premium: R{premium}")
        print(f"Risk Profile: {risk_profile}")
    except Exception as e:
        print("Error during premium generation:", str(e))


if __name__ == "__main__":
    main()
