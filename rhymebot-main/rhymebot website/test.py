from flask import Flask, request, render_template 
  
# Flask constructor
app = Flask(__name__)   
  
# A decorator used to tell the application
# which URL is associated function
@app.route('/test.py', methods =["GET", "POST"])
def get_freq():
    if request.method == "POST":
       # getting input with freq = set_freq in HTML form
       freq = request.form.get("set_freq") # <--- do whatever you want with that value
       return "Your freq value is " + freq
    return render_template("index.html")
  
if __name__=='__main__':
   app.run()
