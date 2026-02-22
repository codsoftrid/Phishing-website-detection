from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)



model = pickle.load(open('phishing_lr.pkl', 'rb')) 
vector = pickle.load(open('vectorizer.pkl', 'rb'))
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        url = request.form['url'].strip()

        if not url:
            return render_template("index.html", predict="⚠️ Please enter a URL!")

       
       
        cleaned_url = re.sub(r'^https?://', '', url)
       
        cleaned_url = cleaned_url.strip('/')

        
        print("Cleaned URL:", cleaned_url)

       
        predict_raw = model.predict(vector.transform([cleaned_url]))[0]

        if predict_raw.lower() == 'bad':
            predict = "🚫 This is a Phishing website !!"
        elif predict_raw.lower() == 'good':
            predict = "✅ This is a legitimate and safe website."
        else:
            predict = f"⚠️ Unknown output: {predict_raw}"

        return render_template("index.html", predict=predict)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
