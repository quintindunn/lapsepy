![LapsePy](https://github.com/quintindunn/lapsepy/blob/main/icon.png?raw=true)
<div align = "center">
	<img src = "https://img.shields.io/pypi/v/lapsepy?label=PYPI%20Version">
	<img src = "https://img.shields.io/pypi/l/lapsepy">
	<img src = "https://img.shields.io/github/stars/quintindunn/lapsepy?label=GitHub%20Stars">
</div>

## Install
```pip install lapsepy```

## [Getting Started](https://github.com/quintindunn/lapsepy/blob/main/docs/GettingStarted.md)

## State of the project:
I created this library as a tiny sideproject and had a lot of fun doing it, as of 1/21/2024 I will continue maintaining the preexisting code as long as there aren't any major changes in the Lapse APIs. However, I've added many of the features that are available on the app, though there are still many unimplemented features. I don't plan on adding these, and if I do they most likely won't be added at any consistent invervals. If there's a specific feature you want, make an issue and I'll see what I can do though there is no guarantees. If you have the ability to add these features yourself, please make a pull request and I will review them and most likely add them.

## Contributing:
As I'm bringing this project to a close I'm not going to go too indepth with this explenation on how to reverse engineer the API, though I will give a brief overview. Here are a few key points to know:
* Lapse uses a GraphQL (GQL) API to send and retrieve data, in my code I didn't write any custom GQL queries, and only uses the quieres extracted from API calls.
* In the code the GQL queries are built in a "factory", the home for these queries are `lapsepy/journal/factory/*`, they're seperated into different files dependent on what the queries accomplish. Queries are built as a class, inheriting from `lapsepy.journal.factory.BaseGQL`. When you instantiate the `BaseGQL` you pass in the `operation_name` and the `query`. While the query can be custom made (so can the operation name, though I'd weight against doing so), as I said I used exact queries from the sniffed API calls.
* To sniff API calls you'll need to use some sort of proxy, I used [MitMProxy](https://mitmproxy.org/), I ran it using this command to filter out other network traffic, though a more specific command could be used to only listen to traffic from the common APIs: `mitmweb --ignore-hosts register.appattest.apple.com --ignore-hosts api.mixpanel.com --ignore-hosts firebaselogging-pa.googleapis.com --ignore-hosts api.onesignal.com --ignore-hosts app-measurement.com`. Viewing the queries in `JSON` mode is from my experience the easiest way to decipher it.
* After you create your GQL queries the next step in the chain is creating the wrapper in the `lapsepy.journal.journal` file. First you want to make a new instance of the GQL class you just created, to actually send the data however you need to convert it to a dictionary. Then you will want to execute `Journal._sync_journal_call`, passing in the query.
* After you have your wrapper in the `lapsepy.journal.journal` you'll need to write the wrapper in the `lapsepy.lapse.lapse` file, call the `Lapse.journal.*` method, with the `*` being the method you just created in the previous step. Run checks to make sure the call worked, and if it doesn't run the appropriate exception.
* Finally, you need to write an example for it, keep your examples short, and simple. In your examples do not hard code the refresh token, but instead use `os.getenv("REFRESH_TOKEN")` for a more dynamic approach.

### A few side notes.
* Try to keep your code up to a fair level of quality. I will provide a bit of support if need be, however I cannot promise a load of it.
* **DO NOT LEAK YOUR REFRESH TOKEN**, Lapse isn't the most safe of apps, and if you leak your token as far as I know it cannot be reset. Your token is persistent even if you log out, and log back in.
* If you need to contact me reguarding this project make an issue and I will try to get back to you in a timely fashion. If it is a security voulnerability, or more private matter please contact me in any of the ways depicted [here](https://github.com/quintindunn/quintindunn/blob/main/README.md).

## Support:
* If you need support or need to contact me reguarding this project make an issue and I will try to get back to you in a timely fashion. If it is a security voulnerability, or more private matter please contact me in any of the ways depicted [here](https://github.com/quintindunn/quintindunn/blob/main/README.md).
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
