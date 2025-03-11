# from flask import Flask, render_template, request, url_for
# import pandas as pd
# # Import your existing modules
# from weather_module import get_weather
# from skin_color import get_closest_color_name
# from face_shape import detect_face_shape

# app = Flask(__name__)

# # Load your dataset from Excel
# dataset = pd.read_excel('products_combined.xlsx')

# # Route for the homepage (form)
# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/register')
# def register():
#     return render_template('registration_form.html')

# # Route to handle form submission and display recommendations
# @app.route('/submit', methods=['POST'])
# def submit():
#     if request.method == 'POST':
#         # Get the user inputs from the form
#         name = request.form['name']
#         email = request.form['email']
#         location = request.form['location']
#         occasion = request.form['occasion']
#         gender = request.form['gender']
#         image = request.files['image']

#         # Process the inputs through your modules
#         weather_info = get_weather(location)  # Get real-time weather info
#         skin_color = get_closest_color_name(image)  # Extract skin tone from the uploaded image
#         face_shape = detect_face_shape(image)  # Detect face shape from the image

#         # Filter outfits from the dataset based on the features
#         recommendations = filter_outfits(dataset, weather_info, skin_color, face_shape, occasion, gender)

#         # Render the result page with the filtered recommendations
#         return render_template('result.html', name=name, email=email, recommendations=recommendations)

# # Function to filter outfits based on user data (weather, skin tone, face shape, occasion, gender)
# def filter_outfits(dataset, weather_info, skin_color, face_shape, occasion, gender):
#     # Convert columns to lowercase to avoid case sensitivity
#     dataset['weather'] = dataset['weather'].str.lower()
#     dataset['skin_color'] = dataset['skin_color'].str.lower()
#     dataset['face_shape'] = dataset['face_shape'].str.lower()
#     dataset['occasion'] = dataset['occasion'].str.lower()
#     dataset['gender'] = dataset['gender'].str.lower()
    

#     # Filter the dataset based on the extracted features
#     filtered_outfits = dataset[
#         (dataset['weather'] == weather_info.lower()) &
#         (dataset['skin_color'] == skin_color.lower()) &
#         (dataset['face_shape'] == face_shape.lower()) &
#         (dataset['occasion'] == occasion.lower()) &
#         (dataset['gender'] == gender.lower())
#     ]

#     # Convert the filtered DataFrame to a list of dictionaries for rendering
#     return filtered_outfits.to_dict(orient='records')

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request
import pandas as pd
from weather_module import get_weather
from face_shape import detect_face_shape, process_uploaded_image
from skin_color import calculate_dominant_color, get_closest_color_name

app = Flask(__name__)

# Step 1: Check if the dataset is loaded
try:
    dataset = pd.read_excel('products_combined.xlsx')
    print("Step 1: Dataset loaded successfully!")
    print(dataset.head())  # Show first few rows of the dataset for verification
except Exception as e:
    print("Step 1 Error: Unable to load dataset:", e)

@app.route('/')
def home():
    # Render the index page with a welcome message or button to start
    print("Step 2: User reached the home page.")
    return render_template('index.html')

@app.route('/register')
def register():
    # Step 3: User has reached the registration form page
    print("Step 3: User reached the registration form page.")
    return render_template('registration_form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get the user inputs from the form
        name = request.form['name']
        email = request.form['email']
        location = request.form['location']
        occasion = request.form['occasion']
        gender = request.form['gender']
        image = request.files['image']

        uploaded_image = request.files['image']  

        # Convert the uploaded image to a format OpenCV can use
        image = process_uploaded_image(uploaded_image)

        # Step 4 Check: Verify if the form data is captured correctly
    print(f"Step 4: Form Data - Name={name}, Email={email}, Location={location}, Occasion={occasion}, Gender={gender}")

        # Step 5: Call the weather module and print the result
    try:
        weather_info, temperature = get_weather(location)
        print(f"Step 5: Weather info - {weather_info}, Temperature - {temperature}")
    except Exception as e:
        print("Step 5 Error: Unable to get weather information:", e)
        return render_template('registration_form.html', message="Error fetching weather info")

    if weather_info == "No City Found":
        print("Step 5 Error: No City Found")
        return render_template('registration_form.html', message="No City Found")

        # Step 6: Call face shape detection module and print the result
    try:
        face_shape = detect_face_shape(image)
        print(f"Step 6: Detected Face Shape - {face_shape}")
    except Exception as e:
        print("Step 6 Error: Unable to detect face shape:", e)
        face_shape = "Unknown"

        # Step 7: Call skin tone detection module and print the result
    try:
        dominant_color = calculate_dominant_color(image)
        skin_tone = get_closest_color_name(dominant_color)
        print(f"Step 7: Detected Skin Tone - {skin_tone}")
    except Exception as e:
            print("Step 7 Error: Unable to detect skin tone:", e)
            skin_tone = "Unknown"

    
        # Step 8: Filter the dataset based on user input and modules' results
    try:
            recommendations = filter_outfits(dataset, occasion, weather_info, skin_tone, face_shape, gender)
            print(f"Step 8: Filtered Recommendations: {len(recommendations)} items found.")
    except Exception as e:
            print("Step 8 Error: Filtering outfits failed:", e)
            recommendations = []

        # Step 9: Render the result page and pass recommendations
    print("Step 9: Rendering the result page.")
    return render_template('result.html', name=name, email=email, weather=weather_info, recommendations=recommendations)

def filter_outfits(dataset, occasion, weather_info, skin_tone, face_shape, gender):
    # Step 8: Logic for filtering the dataset based on user inputs
   
        print(f"Step 8: Filtering dataset for: Weather={weather_info}, Skin tone={skin_tone}, Face shape={face_shape}, Occasion={occasion}, Gender={gender}")
        filtered_outfits = dataset[
            (dataset['occasion'].str.lower() == occasion.lower()) &
            (dataset['weather'].str.lower() == weather_info.lower()) &
            (dataset['skin_color'].str.lower() == skin_tone.lower()) &
            (dataset['face_shape'].str.lower() == face_shape.lower()) &
            (dataset['gender'].str.lower() == gender.lower())
        ]
        return filtered_outfits.to_dict(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
