import joblib
import os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import streamlit as st
import pandas as pd
import plotly.express as px

MODEL_PATH = "disease_model.pkl"

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            return None
    return None

model = load_model()

def save_patient_history(
    name,
    age,
    gender,
    bmi,
    health_score,
    diabetes_score,
    heart_score,
    overall_score
):

    os.makedirs(
        "data",
        exist_ok=True
    )

    history_file = "data/patient_history.csv"

    new_data = pd.DataFrame({
    "Date": [datetime.now().strftime("%Y-%m-%d %H:%M")],
    "Name": [name],
    "Age": [age],
    "Gender": [gender],
    "BMI": [bmi],
    "Health Score": [health_score],
    "Diabetes Risk": [diabetes_score],
    "Heart Risk": [heart_score],
    "Overall Score": [overall_score]
})

    if os.path.exists(history_file):

        try:
            old_data = pd.read_csv(history_file)

            updated_data = pd.concat(
                [old_data, new_data],
                ignore_index=True
            )

            updated_data.to_csv(
                history_file,
                index=False
            )

        except Exception:
            new_data.to_csv(
                history_file,
                index=False
            )

    else:
        new_data.to_csv(
            history_file,
            index=False
        )

def generate_pdf(
    name,
    age,
    gender,
    bmi,
    health_score,
    diabetes_score,
    heart_score,
    overall_score
):

    filename = "health_report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Health Digital Twin AI Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Patient Name: {name}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Age: {age}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Gender: {gender}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"BMI: {bmi}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Health Score: {health_score}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Diabetes Risk: {diabetes_score}%",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Heart Disease Risk: {heart_score}%",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Overall Health Score: {overall_score}",
            styles["BodyText"]
        )
    )

    doc.build(content)

    return filename

st.set_page_config(
    page_title="Health Digital Twin AI",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Health Digital Twin AI")
st.subheader("AI-Powered Health Risk Intelligence Platform")

st.markdown("---")

st.header("Patient Profile")

name = st.text_input("Patient Name")

age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    value=25
)

gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

height = st.number_input(
    "Height (cm)",
    min_value=50,
    max_value=250,
    value=170
)

weight = st.number_input(
    "Weight (kg)",
    min_value=20,
    max_value=300,
    value=70
)

bp = st.number_input(
    "Blood Pressure",
    min_value=50,
    max_value=250,
    value=120
)

sugar = st.number_input(
    "Blood Sugar",
    min_value=50,
    max_value=400,
    value=100
)

cholesterol = st.number_input(
    "Cholesterol",
    min_value=50,
    max_value=400,
    value=180
)

heart_rate = st.number_input(
    "Heart Rate",
    min_value=30,
    max_value=200,
    value=72
)

if st.button("Generate Health Report"):

    if not name.strip():

        st.error("Please enter a patient name before generating a report.")

    else:

        bmi = round(
            weight / ((height / 100) ** 2),
            2
        )

        health_score = max(
            0,
            round(100 - abs(bmi - 22) * 2)
        )

        # Diabetes Risk Prediction

        diabetes_score = 0

        if age > 45:
            diabetes_score += 30

        if bmi > 30:
            diabetes_score += 30

        if sugar > 140:
            diabetes_score += 40

        # Heart Disease Risk

        heart_score = 0

        if age > 50:
            heart_score += 30

        if cholesterol > 200:
            heart_score += 35

        if bp > 140:
            heart_score += 35

        # Overall Health Status

        overall_score = round(
            (health_score +
             (100 - diabetes_score) +
             (100 - heart_score)) / 3
        )

        # AI Disease Prediction (computed once, stored with the rest of the report)

        ai_prediction = None

        if model is not None:
            try:
                ai_prediction = model.predict(
                    [[age, bmi, sugar, bp]]
                )[0]
            except Exception:
                ai_prediction = None

        save_patient_history(
            name,
            age,
            gender,
            bmi,
            health_score,
            diabetes_score,
            heart_score,
            overall_score
        )

        # Persist everything the sections below need, so it survives reruns
        # (e.g. when Streamlit reruns the whole script after a download click)

        st.session_state["report"] = {
            "name": name,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "bp": bp,
            "sugar": sugar,
            "cholesterol": cholesterol,
            "heart_rate": heart_rate,
            "bmi": bmi,
            "health_score": health_score,
            "diabetes_score": diabetes_score,
            "heart_score": heart_score,
            "overall_score": overall_score,
            "ai_prediction": ai_prediction
        }

if "report" in st.session_state:

    r = st.session_state["report"]

    name = r["name"]
    age = r["age"]
    gender = r["gender"]
    bmi = r["bmi"]
    health_score = r["health_score"]
    diabetes_score = r["diabetes_score"]
    heart_score = r["heart_score"]
    overall_score = r["overall_score"]
    bp = r["bp"]
    sugar = r["sugar"]
    cholesterol = r["cholesterol"]
    heart_rate = r["heart_rate"]
    ai_prediction = r["ai_prediction"]

    st.success(f"Patient: {name}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("BMI", bmi)

    with col2:
        st.metric("Health Score", health_score)




    # BMI Category

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal Weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    st.info(f"📊 BMI Category: {category}")

    # Health Risk

    if health_score >= 80:
        st.success("🟢 Low Health Risk")
    elif health_score >= 60:
        st.warning("🟡 Moderate Health Risk")
    else:
        st.error("🔴 High Health Risk")

    st.markdown("---")

    # Diabetes Risk Prediction

    st.subheader("🤖 Diabetes Risk Prediction")

    if diabetes_score < 30:
        st.success(
            f"🟢 Low Diabetes Risk ({diabetes_score}%)"
        )

    elif diabetes_score < 70:
        st.warning(
            f"🟡 Moderate Diabetes Risk ({diabetes_score}%)"
        )

    else:
        st.error(
            f"🔴 High Diabetes Risk ({diabetes_score}%)"
        )

    st.markdown("---")

    # Heart Disease Risk

    st.subheader("❤️ Heart Disease Risk")

    if heart_score < 30:
        st.success(
            f"🟢 Low Heart Disease Risk ({heart_score}%)"
        )

    elif heart_score < 70:
        st.warning(
            f"🟡 Moderate Heart Disease Risk ({heart_score}%)"
        )

    else:
        st.error(
            f"🔴 High Heart Disease Risk ({heart_score}%)"
        )

    st.markdown("---")

    # AI Disease Prediction

    st.subheader("🤖 AI Disease Prediction")

    if model is None:
        st.warning(
            "AI prediction model is not available right now. "
            "Make sure 'disease_model.pkl' is present in the app directory."
        )
    elif ai_prediction is None:
        st.warning(
            "AI prediction could not be computed for this patient."
        )
    elif ai_prediction == 1:
        st.error(
            "⚠️ AI Model: High Disease Risk Detected"
        )
    else:
        st.success(
            "✅ AI Model: Low Disease Risk"
        )

    st.markdown("---")

    # Health Recommendations

    st.subheader("💡 Health Recommendations")

    recommendations = []

    if bmi > 25:
        recommendations.append(
            "Maintain a balanced diet and increase physical activity."
        )

    if sugar > 140:
        recommendations.append(
            "Monitor blood sugar regularly and reduce sugar intake."
        )

    if cholesterol > 200:
        recommendations.append(
            "Reduce saturated fats and increase fiber-rich foods."
        )

    if heart_rate > 100:
        recommendations.append(
            "Consult a healthcare professional regarding elevated heart rate."
        )

    if not recommendations:
        recommendations.append(
            "Your health indicators look good. Maintain your healthy lifestyle."
        )

    for rec in recommendations:
        st.write("✅", rec)

    st.markdown("---")

    st.subheader("🥗 Smart Diet Recommendation Engine")

    if bmi < 18.5:

        st.success("📈 Weight Gain Diet Plan")
        st.write("🍳 Breakfast: Eggs, Milk, Oats")
        st.write("🍚 Lunch: Rice, Chicken, Vegetables")
        st.write("🥜 Snacks: Nuts, Peanut Butter")
        st.write("🍲 Dinner: Protein-rich meals")

    elif bmi < 25:

        st.success("⚖️ Balanced Diet Plan")

        st.write("🥣 Breakfast: Oats, Fruits")
        st.write("🥗 Lunch: Lean Protein, Salad")
        st.write("🍎 Snacks: Fruits")
        st.write("🍛 Dinner: Vegetables and Protein")

    else:

        st.warning("📉 Weight Loss Diet Plan")

        st.write("🥣 Breakfast: Oats and Green Tea")
        st.write("🥗 Lunch: Salad and Grilled Chicken")
        st.write("🍏 Snacks: Apple and Nuts")
        st.write("🥦 Dinner: Soup and Vegetables")

    st.markdown("### 🚫 Foods To Avoid")

    avoided_any = False

    if sugar > 140:
        avoided_any = True
        st.write("❌ Sugary Drinks")
        st.write("❌ Excess Sweets")
        st.write("❌ Soft Drinks")

    if cholesterol > 200:
        avoided_any = True
        st.write("❌ Fried Foods")
        st.write("❌ Processed Meat")
        st.write("❌ Fast Food")

    if bmi > 25:
        avoided_any = True
        st.write("❌ Excess Calories")
        st.write("❌ Junk Food")
        st.write("❌ Late Night Snacking")

    if not avoided_any:
        st.write("✅ No specific foods to avoid based on current indicators.")

    st.markdown("---")
    st.markdown("---")

    # Overall Health Status

    st.subheader("🏥 Overall Health Status")

    st.metric(
        "Health Digital Twin Score",
        f"{overall_score}/100"
    )

    # Health Grade System

    if overall_score >= 90:
        grade = "A+"
    elif overall_score >= 80:
        grade = "A"
    elif overall_score >= 70:
        grade = "B"
    elif overall_score >= 60:
        grade = "C"
    else:
        grade = "D"

    st.subheader("🏆 Health Grade")

    if grade == "A+":
        st.success(f"🌟 Grade: {grade}")
    elif grade == "A":
        st.success(f"✅ Grade: {grade}")
    elif grade == "B":
        st.info(f"👍 Grade: {grade}")
    elif grade == "C":
        st.warning(f"⚠️ Grade: {grade}")
    else:
        st.error(f"🚨 Grade: {grade}")

    st.markdown("---")

    if overall_score >= 85:
        st.success("🌟 Excellent Health")
    elif overall_score >= 70:
        st.info("👍 Good Health")
    elif overall_score >= 50:
        st.warning("⚠️ Moderate Health")
    else:
        st.error("🚨 Poor Health")

    st.markdown("---")

    # Dashboard

    st.subheader("📈 Health Metrics Dashboard")

    data = pd.DataFrame({
        "Metric": [
            "Blood Pressure",
            "Blood Sugar",
            "Cholesterol",
            "Heart Rate"
        ],
        "Value": [
            bp,
            sugar,
            cholesterol,
            heart_rate
        ]
    })

    fig = px.bar(
        data,
        x="Metric",
        y="Value",
        title="Health Metrics"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    pdf_file = generate_pdf(
        name,
        age,
        gender,
        bmi,
        health_score,
        diabetes_score,
        heart_score,
        overall_score
    )

    with open(pdf_file, "rb") as f:

        st.download_button(
            label="📄 Download Health Report",
            data=f,
            file_name="Health_Report.pdf",
            mime="application/pdf"
        )

else:

    st.info(
        "Fill in the patient profile above and click Generate Health Report to see results."
    )

st.markdown("---")

st.header("📋 Patient History")

history_file = "data/patient_history.csv"

history_df = None

if os.path.exists(history_file):

    try:
        history_df = pd.read_csv(history_file)

        st.dataframe(
            history_df,
            use_container_width=True
        )

    except Exception:
        st.warning(
            "No patient history available."
        )

else:
    st.info(
        "No patient history yet. Generate a report to start building history."
    )

st.markdown("---")

st.header("📈 Health Trends Analytics")

if history_df is not None and len(history_df) > 1:

    history_df["Date"] = pd.to_datetime(
        history_df["Date"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average BMI",
            round(history_df["BMI"].mean(), 2)
        )

    with col2:
        st.metric(
            "Average Health Score",
            round(history_df["Health Score"].mean(), 2)
        )

    with col3:
        st.metric(
            "Average Overall Score",
            round(history_df["Overall Score"].mean(), 2)
        )

    bmi_fig = px.line(
        history_df,
        x="Date",
        y="BMI",
        markers=True,
        title="BMI Trend Over Time",
    )

    st.plotly_chart(
        bmi_fig,
        use_container_width=True,
    )

    health_fig = px.line(
        history_df,
        x="Date",
        y="Health Score",
        markers=True,
        title="Health Score Trend"
    )

    st.plotly_chart(
        health_fig,
        use_container_width=True
    )

    overall_fig = px.line(
        history_df,
        x="Date",
        y="Overall Score",
        markers=True,
        title="Overall Health Trend"
    )

    st.plotly_chart(
        overall_fig,
        use_container_width=True
    )

else:

    st.info(
        "Generate more reports to view trends."
    )