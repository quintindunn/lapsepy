![LapsePy](https://github.com/quintindunn/lapsepy/blob/main/icon.png?raw=true)
<div align = "center">
	<img src = "https://img.shields.io/pypi/v/lapsepy?label=PYPI%20Version">
	<img src = "https://img.shields.io/pypi/l/lapsepy">
	<img src = "https://img.shields.io/github/stars/quintindunn/lapsepy?label=GitHub%20Stars">
</div>

## Install
```pip install lapsepy```

## [Getting Started](https://github.com/quintindunn/lapsepy/blob/main/docs/GettingStarted.md)

## Features:
* Modify your bio, display name, date of birth, emojis, and username. Many past what's allowed on the app!
* Upload any image to your darkroom and make it develop at any time!
* Get your friends feed, and download images.

## Getting your refresh token:
One of the most challenging parts of this project is authentication, it uses Apple's App Attest in place of a captcha. As far as I'm aware there's no work around without jailbreaking your phone / using a modified version of the app. I'm planning on waiting for Lapse's Android version to try to reverse engineer it there.

### How to get your refresh token (Windows-Iphone):
#### Method 1 (Semi automated):
* Follow the instructions on my [LapsePyRefreshTokenSniffer](https://github.com/quintindunn/LapseRefreshTokenSniffer/) project.
#### Method 2 (Completely manual):
* Log out of the app
* Install [MitMProxy](https://mitmproxy.org/) **Make sure to install all certificates required. [Certificates](https://docs.mitmproxy.org/stable/concepts-certificates/)**
* Start MitMWeb ignoring the host `register.appattest.apple.com` using `mitmweb --ignore-hosts register.appattest.apple.com`
* Get your computer's ip address. Open your terminal and write `ipconfig`
* On your phone go to Settings -> Network -> <Your network> -> info -> proxy -> manual and enter the proxy information.
* Open the Lapse app and sign in.
* Watch your proxies API calls for the second call to `https://auth.production.journal-api.lapse.app/verify` and inspect it.
* Go to the Response tab, and set `view` to `json`
* Copy the refresh token from the response.


## How to use examples:
1. Clone the repository `git clone https://github.com/quintindunn/lapsepy.git`
2. OPTION 1: Set your refresh token in your environment variable as `REFRESH_TOKEN`<br>
OPTION 2: In the examples replace the `os.getenv("REFRESH_TOKEN")` with `"YOUR_REFRESH_TOKEN"`
3. Run the file.
