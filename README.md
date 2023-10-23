# lapsepy
A Python3 API Wrapper for the social media app Lapse.


## How to install:
* You can install `lapsepy` through PyPi using `pip install lapsepy`

## Getting your refresh token:
One of the most challenging parts of this project is authentication, it uses Apple's App Attest in place of a captcha. As far as I'm aware there's no work around without jailbreaking your phone / using a modified version of the app. I'm planning on waiting for Lapse's Android version to try to reverse engineer it there.

### How to get your refresh token (IOS):
* Log out of the app
* Install a proxy like [MitMProxy](https://mitmproxy.org/) (but don't enable it) **Make sure to install all certificates required. [Certificates](https://docs.mitmproxy.org/stable/concepts-certificates/)**
* Open the Lapse app and enter your phone number and wait for the text with your verification code **Do not enter verification code yet.**.
* Go to Settings -> Network -> <Your network> -> info -> proxy -> manual -> enter proxy information.
* Enter your verification code.
* Watch your proxies API calls for the second call to `https://auth.production.journal-api.lapse.app/verify` and inspect it.
* Go to the Response tab, and set `view` to `json`
* Copy the refreshToken line.


## How to use examples:
1. Clone the repository `git clone https://github.com/quintindunn/lapsepy.git`
2. OPTION 1: Set your refresh token in your environment variable as `REFRESH_TOKEN`<br>
OPTION 2: In the examples replace the `os.getenv("REFRESH_TOKEN")` with `"YOUR_REFRESH_TOKEN"`
3. Run the file.
