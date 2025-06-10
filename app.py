from flask import Flask, request

app = Flask(__name__)

clinics = {
    "1": "Sunrise Clinic",
    "2": "Green Valley Hospital",
    "3": "Downtown Health Center"
}

# Temporary queue (you can later save this to file/database)
queue = []

@app.route('/ussd', methods=['POST'])
def ussd():
    session_id = request.form.get('sessionId')
    service_code = request.form.get('serviceCode')
    phone_number = request.form.get('phoneNumber')
    text = request.form.get('text')

    inputs = text.strip().split('*')

    if text == "":
        response = "CON Welcome to QuickQ\n"
        response += "1. Sunrise Clinic\n"
        response += "2. Green Valley Hospital\n"
        response += "3. Downtown Health Center"
    
    elif len(inputs) == 1:
        choice = inputs[0]
        if choice in clinics:
            response = f"CON You chose {clinics[choice]}\nPlease enter your full name:"
        else:
            response = "END Invalid clinic selected. Please try again."
    
    elif len(inputs) == 2:
        clinic_choice = inputs[0]
        user_name = inputs[1]
        clinic_name = clinics.get(clinic_choice, "Unknown")

        queue.append({
            "name": user_name,
            "clinic": clinic_name,
            "phone": phone_number
        })

        response = f"END Hi {user_name}, you’ve joined the queue at {clinic_name}. Estimated wait: 15 minutes."

    else:
        response = "END Invalid input. Please try again."

    return response

if __name__ == '__main__':
    app.run(port=5000)