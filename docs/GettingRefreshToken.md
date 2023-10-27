## Getting your refresh token:
One of the most challenging parts of this project is authentication, it uses Apple's App Attest in place of a captcha. As far as I'm aware there's no work around without jailbreaking your phone / using a modified version of the app. I'm planning on waiting for Lapse's Android version to try to reverse engineer it there and hopefully they'll use another authentication method.

### How to get your refresh token (Windows-Iphone):
* Log out of the app
* Install [MitMProxy](https://mitmproxy.org/) **Make sure to install all certificates required. [Certificates](https://docs.mitmproxy.org/stable/concepts-certificates/)**
* Start MitMWeb ignoring the host `register.appattest.apple.com` using `mitmweb --ignore-hosts register.appattest.apple.com`
* Get your computer's ip address. Open your terminal and write `ipconfig`
* On your phone go to Settings -> Network -> <Your network> -> info -> proxy -> manual and enter the proxy information.
* Open the Lapse app and sign in.
* Watch your proxies API calls for the second call to `https://auth.production.journal-api.lapse.app/verify` and inspect it.
* Go to the Response tab, and set `view` to `json`
* Copy the refresh token from the response.