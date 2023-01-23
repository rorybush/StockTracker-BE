import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyABF_dh8WSnwqCmlX01PiQ7hiOFhleX4Bc",
    "authDomain": "southcoders-be.firebaseapp.com",
    "projectId": "southcoders-be",
    "databaseURL": "",
    "storageBucket": "southcoders-be.appspot.com",
    "messagingSenderId": "851060036490",
    "appId": "1:851060036490:web:4b2a072e7b5fd2d504ee73",
    "measurementId": "G-7R5FPYEH2F"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

email = "test67867sdfsdf@gmail.com"
password = "123456AAAAAA@"

# user = auth.create_user_with_email_and_password(email, password)

# print(user)


# user = auth.sign_in_with_email_and_password(email, password)

# info = auth.get_account_info(user['idToken'])

# print(info)
# print(user["localId"])

# auth.send_email_verification(user["idToken"])

# auth.send_password_reset_email(email)
