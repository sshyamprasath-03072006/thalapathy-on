from flask import Flask, render_template_string, request
import subprocess

app = Flask(__name__)

# HTML Template for the Web UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>THALAPATHYON</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            color: white;
            background-color: #121212; /* Dark theme background */
            overflow-x: hidden;
            margin: 0;
            padding: 0;
        }
        /* Background video styling */
        #background-video {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: -1;
        }
        /* Title Grid */
        .title-grid {
            display: grid;
            place-items: center;
            height: 100px;
            background-color: #000000; /* Black background for title */
            text-align: center;
        }
        h1 {
            font-size: 3em;
            color: white; /* White color for heading */
        }
        /* Container for code input */
        .container {
            max-width: 900px;
            margin-top: 20px;
            background-color: rgba(0, 0, 0, 0.5); /* 50% transparent background */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        /* Code box */
        .form-control {
            background-color: #333;
            color: white;
            border: 1px solid #444;
            opacity: 0.7;
            transition: opacity 0.3s ease;
        }
        .form-control:focus {
            opacity: 1;
            border-color: #ffffff; /* White border color on focus */
            outline: none;
        }
        /* Button Styling */
        .btn {
            background-color: #000;
            color: white;
            border: 1px solid #444;
            font-size: 1.2em;
            width: 100%;
            transition: background-color 0.3s;
        }
        .btn:hover {
            background-color: #444;
        }
        /* Output section */
        .alert {
            margin-top: 30px;
            background-color: #1d1d1d;
            color: white; /* White output text */
        }
    </style>
</head>
<body>
    <!-- Background video -->
    <video id="background-video" autoplay muted loop>
        <source src="/static/GOAT.mp4" type="video/mp4">
    </video>

    <!-- Title Section -->
    <div class="title-grid">
        <h1>THALAPATHYON</h1>
    </div>

    <div class="container">
        <form method="POST" action="/" id="code-form">
            <div class="mb-3">
                <label for="code" class="form-label">Write your Thalapathy-on code here...</label>
                <textarea name="code" id="code" class="form-control" rows="20">{{ request.form['code'] if request.form.get('code') else '' }}</textarea>
            </div>
            <div class="row mb-3">
                <div class="col-12">
                    <button type="submit" class="btn">Run Code</button>
                </div>
            </div>

            {% if output %}
            <div class="alert" id="output">
                <h4>Output:</h4>
                <pre>{{ output }}</pre>
            </div>
            {% endif %}
        </form>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>

    <!-- Auto scroll to output section -->
    <script>
        // Function to scroll smoothly to the output section
        function scrollToOutput() {
            setTimeout(function() {
                const outputElement = document.getElementById('output');
                if (outputElement) {
                    outputElement.scrollIntoView({ behavior: 'smooth' });
                }
            }, 100);  // Slight delay to allow page to load content
        }

        // Scroll automatically after the form is submitted and output is rendered
        window.onload = function() {
            if (document.getElementById('output')) {
                scrollToOutput();
            }
        };

        // Add event listener to form submission to trigger scroll after submission
        document.getElementById('code-form').addEventListener('submit', scrollToOutput);
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    if request.method == 'POST':
        code = request.form.get('code', '')

        # Replace "Thalapathy-on" syntax with Python syntax
        translated_code = (code
            .replace('verithanam', 'print')
            .replace('oruvaati_mudivu_panita', 'if')
            .replace('en_pecha_nane_kekamatan', 'else')
            .replace('inga_jeikuravan_thopaan', 'for')
            .replace('thokuravan_jeipan', 'while')
            .replace('all_is_well', 'def ')
            .replace('na_thanda_leo-', 'try')
            .replace('leo_das', 'except')
            .replace('a_lion_is_always_a_lion', 'exit'))

        # Write the translated code to a temporary file
        with open('temp_code.py', 'w') as temp_file:
            temp_file.write(translated_code)

        try:
            result = subprocess.run(['python', 'temp_code.py'], capture_output=True, text=True)
            output = result.stdout + result.stderr
        except Exception as e:
            output = str(e)

    return render_template_string(HTML_TEMPLATE, output=output)

if __name__ == '__main__':
    app.run(debug=True)
