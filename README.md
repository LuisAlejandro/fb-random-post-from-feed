<p align='center'>
  <img src="https://github.com/LuisAlejandro/fb-random-post-from-feed/blob/develop/branding/banner.svg">
  <h3 align="center">Facebook random post from feed</h3>
  <p align="center">GitHub Action for posting a random article from an atom feed to a facebook page</p>
</p>

---

Current version: 0.1.1

## 🎒 Prep Work
1. Get a facebook permanent access token (explained below) using a facebook account that owns the page where you want to post messages.
2. Find the ID of the page that you want to post messages in (explained below).
3. Find the atom feed URL that contains the posts that you wish to share.

## 🖥 Workflow Usage

Configure your workflow to use `LuisAlejandro/fb-random-post-from-feed@0.1.1`,
and provide the atom feed URL you want to use as the `FEED_URL` env variable.

Provide the access token for your Facebook app as the
`FACEBOOK_ACCESS_TOKEN` env variable, set your facebook page ID as
`FACEBOOK_PAGE_ID` (as secrets). Remember, to add secrets go to your repository
`Settings` > `Secrets` > `Actions` > `New repository secret`
for each secret.

For example, create a file `.github/workflows/schedule.yml` on
a github repository with the following content:

```yml
name: Publish random post of feed hourly
on:
  schedule:
    - cron: '0 * * * *'
jobs:
  fbpost:
    runs-on: ubuntu-20.04
    steps:
      - uses: LuisAlejandro/fb-random-post-from-feed@0.1.1
        env:
          FACEBOOK_ACCESS_TOKEN: ${{ secrets.FACEBOOK_ACCESS_TOKEN }}
          FACEBOOK_PAGE_ID: ${{ secrets.FACEBOOK_PAGE_ID }}
          FEED_URL: ${{ secrets.FEED_URL }}
```

Publish your changes, activate your actions if disabled and enjoy.

## ❗ Important notes

* The action is designed to pick random posts published within the last year. You can modify this
interval by setting a `MAX_POST_AGE` env variable with an integer value in days. For example, to pick posts
from the last month set `MAX_POST_AGE: 30`.

## 👥 How to get a Facebook permanent access token

Following the instructions laid out in Facebook's [extending page tokens documentation][2] I was able to get a page access token that does not expire.

I suggest using the [Graph API Explorer][3] for all of these steps except where otherwise stated.

### 0. Create Facebook App

**If you already have an app**, skip to step 1.

1. Go to [My Apps][4].
2. Click "+ Add a New App".
3. Setup a website app.

You don't need to change its permissions or anything. You just need an app that wont go away before you're done with your access token.

### 1. Get User Short-Lived Access Token

1. Go to the [Graph API Explorer][3].
3. Select the application you want to get the access token for (in the "Facebook App" drop-down menu, not the "My Apps" menu).
4. In the "Add a Permission" drop-down, search and check "pages_manage_posts" and "pages_read_engagement".
5. Click "Generate Access Token".
6. Grant access from a Facebook account that has access to manage the target page. Note that if this user loses access the final, never-expiring access token will likely stop working.

The token that appears in the "Access Token" field is your short-lived access token.

### 2. Generate Long-Lived Access Token

Following [these instructions][5] from the Facebook docs, make a GET request to

> https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=**{app_id}**&client_secret=**{app_secret}**&fb_exchange_token=**{short_lived_token}**

entering in your app's ID and secret and the short-lived token generated in the previous step.

You **cannot use the Graph API Explorer**. For some reason it gets stuck on this request. I think it's because the response isn't JSON, but a query string. Since it's a GET request, you can just go to the URL in your browser.

The response should look like this:

> {"access_token":"**ABC123**","token_type":"bearer","expires_in":5183791}

"ABC123" will be your long-lived access token. You can put it into the [Access Token Debugger][7] to verify. Under "Expires" it should have something like "2 months".

### 3. Get User ID

Using the long-lived access token, make a GET request to 

> https://graph.facebook.com/me?access_token=**{long_lived_access_token}**

The `id` field is your account ID. You'll need it for the next step.

### 4. Get Permanent Page Access Token

Make a GET request to

> https://graph.facebook.com/**{account_id}**/accounts?access_token=**{long_lived_access_token}**

The JSON response should have a `data` field under which is an array of items the user has access to. Find the item for the page you want the permanent access token from. The `access_token` field should have your permanent access token. Copy it and test it in the [Access Token Debugger][7]. Under "Expires" it should say "Never".

[2]:https://developers.facebook.com/docs/facebook-login/access-tokens#extendingpagetokens
[3]:https://developers.facebook.com/tools/explorer
[4]:https://developers.facebook.com/apps/
[5]:https://developers.facebook.com/docs/facebook-login/access-tokens#extending
[6]:https://luckymarmot.com/paw
[7]:https://developers.facebook.com/tools/debug/accesstoken

## 👥 How to get a Facebook page ID

To find your Page ID:

1. From News Feed, click Pages in the left side menu.
2. Click your Page name to go to your Page.
3. Click About in the left column. If you don't see About in the left column, click See More.
4. Scroll down to find your Page ID below More Info.

## 🕵🏾 Hacking suggestions

- You can test the script locally with Docker Compose:

  * Install [Docker Community Edition](https://docs.docker.com/install/#supported-platforms) according with your operating system
  * Install [Docker Compose](https://docs.docker.com/compose/install/) according with your operating system.

      - [Linux](https://docs.docker.com/compose/install/#install-compose-on-linux-systems)
      - [Mac](https://docs.docker.com/compose/install/#install-compose-on-macos)
      - [Windows](https://docs.docker.com/compose/install/#install-compose-on-windows-desktop-systems)

  * Install a git client.
  * Fork this repo.
  * Clone your fork of the repository into your local computer.
  * Open a terminal and navigate to the newly created folder.
  * Change to the `develop` branch.

          git checkout develop

  * Create a `.env` file with the content of the environment secrets as variables, like this (with real values):

          FACEBOOK_ACCESS_TOKEN=xxxx
          FACEBOOK_PAGE_ID=xxxx
          FEED_URL=xxxx

  * Execute the following command to create the docker image (first time only):

          make image

  * You can execute the tweet script with this command:

          make publish

  * Or, alternatively, open a console where you can manually execute the script and debug any errors:

          make console
          python3 entrypoint.py

  * You can stop the docker container with:
  
          make stop

  * Or, destroy it completely:
  
          make destroy
  

## Made with :heart: and :hamburger:

![Banner](https://github.com/LuisAlejandro/fb-random-post-from-feed/blob/develop/branding/author-banner.svg)

> Web [luisalejandro.org](http://luisalejandro.org/) · GitHub [@LuisAlejandro](https://github.com/LuisAlejandro) · Twitter [@LuisAlejandro](https://twitter.com/LuisAlejandro)