import gradio as gr
import pandas as pd
import joblib

# 1. LOAD THE TRAINED LOGISTIC REGRESSION MODEL
# Make sure model.pkl is in the same directory
model = joblib.load("model.pkl")

# 2. PREDICTION FUNCTION
def predict_survival(pclass, gender, age, fare, sibsp, parch, who, embarked, alone):
    # Validation: Ensure all inputs are filled to avoid errors
    if None in [pclass, gender, age, fare, sibsp, parch, who, embarked]:
        return "⚠️ Please fill in all fields before predicting."
        
    # Map Gender (male = 0, female = 1)
    sex_encoded = 0 if gender == "Male" else 1
    
    # Map 'who' features (One-Hot Encoded)
    who_man = 1 if who == "Man" else 0
    who_woman = 1 if who == "Woman" else 0
    # adult_male is 1 if who is 'Man', otherwise 0
    adult_male = 1 if who == "Man" else 0
    
    # Map Embarked features (One-Hot Encoded for Q and S)
    embarked_Q = 1 if embarked == "Queenstown" else 0
    embarked_S = 1 if embarked == "Southampton" else 0
    
    # Map Checkbox to numeric binary
    alone_encoded = 1 if alone else 0
    
    # Construct DataFrame with the exact features expected by your model
    input_data = pd.DataFrame([{
        'pclass': int(pclass),
        'sex': sex_encoded,
        'age': float(age),
        'sibsp': int(sibsp),
        'parch': int(parch),
        'fare': float(fare),
        'adult_male': adult_male,
        'alone': alone_encoded,
        'who_man': who_man,
        'who_woman': who_woman,
        'embarked_Q': embarked_Q,
        'embarked_S': embarked_S
    }])
    
    # Run Inference
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    
    # Extract confidence score based on the outcome
    confidence = probabilities[1] if prediction == 1 else probabilities[0]
    
    # Format outcome using markdown formatting (Green card for Survived, Red for Not)
    if prediction == 1:
        return f"### ✅ Survived\n**Confidence:** {confidence * 100:.2f}%"
    else:
        return f"### ❌ Did Not Survive\n**Confidence:** {confidence * 100:.2f}%"

# 3. HELPER FUNCTIONS FOR BUTTONS
def load_sample():
    # Returns a realistic passenger snapshot (e.g., 1st Class Female, Traveling with Family)
    return 1, "Female", 29, 211.3, 0, 1, "Woman", "Southampton", False

def clear_inputs():
    # Resets every user control structure to default values
    return None, None, None, None, None, None, None, None, False, ""

# 4. GRADIO BLOCKS THEME INTERFACE
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue")) as demo:
    
    # Header block
    gr.Markdown("# 🚢 Titanic Survival Prediction")
    gr.Markdown("### Predict whether a passenger would survive the Titanic disaster using Logistic Regression.")
    
    with gr.Row():
        # Left Side: Input Elements Column
        with gr.Column():
            gr.Markdown("### 📋 Passenger Attributes")
            
            pclass = gr.Dropdown(choices=[1, 2, 3], label="Passenger Class")
            gender = gr.Dropdown(choices=["Male", "Female"], label="Gender")
            age = gr.Number(label="Age")
            fare = gr.Number(label="Fare")
            sibsp = gr.Number(label="Siblings / Spouses")
            parch = gr.Number(label="Parents / Children")
            who = gr.Dropdown(choices=["Man", "Woman", "Child"], label="Who")
            embarked = gr.Dropdown(choices=["Southampton", "Cherbourg", "Queenstown"], label="Embarked")
            alone = gr.Checkbox(label="Travelling Alone", value=False)
            
            # Application Interaction Buttons
            with gr.Row():
                btn_sample = gr.Button("📋 Load Sample Passenger")
                btn_clear = gr.Button("🗑️ Clear")
                btn_predict = gr.Button("⚡ Predict Survival", variant="primary")
                
        # Right Side: Output Elements Column
        with gr.Column():
            gr.Markdown("### 🎯 Prediction Output")
            output_display = gr.Markdown(label="Results Container")
            
    # 5. BUTTON ACTION TRIGGERS
    btn_predict.click(
        fn=predict_survival, 
        inputs=[pclass, gender, age, fare, sibsp, parch, who, embarked, alone], 
        outputs=output_display
    )
    
    btn_sample.click(
        fn=load_sample, 
        inputs=[], 
        outputs=[pclass, gender, age, fare, sibsp, parch, who, embarked, alone]
    )
    
    btn_clear.click(
        fn=clear_inputs, 
        inputs=[], 
        outputs=[pclass, gender, age, fare, sibsp, parch, who, embarked, alone, output_display]
    )
    
    # Page Footer Configuration
    gr.Markdown("---")
    gr.Markdown("<center><b>Developed by Abhay Dwivedi</b><br>Machine Learning Portfolio Project</center>")

# 6. APP ENGINE LAUNCH
demo.queue().launch()