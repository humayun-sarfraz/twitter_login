from flask import Flask, redirect, request, session, render_template
import tweepy

# Flask app configuration
app = Flask(__name__)
app.secret_key = "Und3YkdQQ0xJN0JCc0FCNS1oYzY6MTpj1aQ"  # Replace with a secure secret key

# Twitter API credentials
consumer_key = "sCp27dgYP9HbtpaulCuQree3y4"
consumer_secret = "jx48AGmG0Zr9YLhDgmG385DqRssg1NxKGcpLWtH9I7F6LAOawWF"
callback_url = "http://127.0.0.1:5000/callback"  # Update with your callback URL

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    try:
        redirect_url = auth.get_authorization_url()
        session['request_token'] = auth.request_token
        return redirect(redirect_url)
    except tweepy.TweepyException as e:
        return f"Failed to authenticate: {e}"

@app.route("/callback")
def callback():
    verifier = request.args.get('oauth_verifier')
    auth.request_token = session['request_token']

    try:
        auth.get_access_token(verifier)
        api = tweepy.API(auth)
        # Retrieve authenticated user's profile data
        user = api.verify_credentials()
        #tweets = api.user_timeline(screen_name=user.screen_name, count=10)  # Adjust count as needed
        #print(tweets)
        return render_template("profile.html", user=user)
    
    except tweepy.TweepyException as e:
        return f"Failed to retrieve profile data: {e}"

if __name__ == "__main__":
    app.run(debug=True)
