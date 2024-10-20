# Sisonke
"We are Together"

## Links

* Presentation: https://www.canva.com/design/DAGUBwsU7xw/jLJiSlqAgIWHgHCwRI3iSg/edit?utm_content=DAGUBwsU7xw&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
* Demo: _>(Optional) Link to a live demo.<_
* Other: _>(Optional) Any links you want to share. Make sure you add a description to the link.<_

## How it works

**Sisonke Insurance Solution Overview:**  

Sisonke Insurance aims to **democratize access to unemployment insurance** by leveraging accessible technology, particularly WhatsApp, to offer coverage for informal sector workers—who are typically excluded from traditional UIF systems. This innovative model allows users to easily enroll, contribute, and make claims through a **WhatsApp-based platform**.  

The solution operates as follows:  
1. **User Onboarding and Risk Pooling:** Users receive personalized quotes and are added to risk pools based on their profile.  
2. **Monthly Contributions:** Payments are deducted automatically from an open wallet, ensuring seamless participation.  
3. **Claim Verification:** In the event of job loss, claims are validated either by previous employers or alternative verification methods, such as community-based checks or transaction monitoring.  
4. **Payouts:** Approved claims are paid directly into an **ILP wallet** (Interledger Protocol), ensuring fast and secure transfers.  

Sisonke's approach bridges the gap for **5 million informal workers** in South Africa, many of whom lack access to traditional financial services or unemployment insurance. By using familiar technology, the solution empowers workers to build financial security without the typical barriers of formal employment or banking requirements.

### How to Run the Project

Our project consists of two APIs: one built with Flask and another with Express. To get started, you'll need to install the required dependencies for both.

1. **Flask API Setup:**
   - From the root directory of the project, install the Python dependencies by running:
     ```bash
     pip install -r requirements.txt
     ```

2. **Express API Setup:**
   - Navigate to the Express app directory:
     ```bash
     cd express_app
     ```
   - Install the Node.js dependencies using:
     ```bash
     npm install
     ```

### Running the Applications

- **Flask API**: From the root directory, start the Flask API by running:
  ```bash
  python -m flask_app.app
  ```

- **Express API**: Navigate to the Express app directory and start the server:
  ```bash
  cd express_app
  npm run start
  ```

### Running TigerBeetle

TigerBeetle is not included in our repository, but you can install it separately. Once installed, you can run the TigerBeetle instance with the following command:
```bash
./tigerbeetle start --addresses=3000 --development 0_0.tigerbeetle
```

### Twilio Integration

Our app integrates with Twilio, but due to security reasons, we haven't included our authentication and secret keys in the repository. If you'd like to see the service in action, please visit us at **Table AZ Team 27** during the event, and we'll be happy to provide the keys and give you a demo. It’s also a great opportunity to say hello!

### Database Requirements

If you wish to use the database functionality, ensure that you have **SQLite** installed. The database should be placed in the `database` directory within the project structure.

## Team members

[Jason Joannou](https://github.com/Jason-Joannou)
[Darryl Nyamayaro](https://github.com/Darryldn9)
Shaun Brick 
Johan Brits

### Learnings
During this hackathon, I gained valuable experience working with TigerBeetle, a high-performance financial accounting database. I also learned how to integrate OpenAI's language model into a Twilio chatbot, enabling intelligent and interactive conversations. Additionally, I explored new ways to rethink and reimagine how OpenPayments grants can be utilized within fintech solutions, broadening my understanding of financial APIs and payment ecosystems.

### Achievements
One of the most significant achievements from this hackathon was successfully implementing a WhatsApp chatbot that integrates with OpenAI's language translation capabilities. This allowed the chatbot to handle multiple languages and provide insurance quotes with dynamic pricing. I also implemented TigerBeetle for efficient accounting operations and successfully integrated the OpenPayments API to set up a recurring payments system, which automatically debits users at the end of each month.

### What Comes Next?
Looking ahead, I plan to further enhance the TigerBeetle integration for more robust financial management capabilities. I also aim to improve user management by creating better pooling functionalities using databases. Additionally, refining the job validation claim process and developing a more sophisticated AI model for risk profiling are key goals for future iterations of the project.
