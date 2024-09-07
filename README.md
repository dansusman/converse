# Converse

Simple python script to convert Spotify playlists into YouTube Music playlists. 

## Usage

Get API keys from [Spotify Developer
Dashboard](https://developer.spotify.com/dashboard/applications) and set up a
Youtube Data API v3 application with OAuth 2.0 permissions. Download your
credentials.json from Google Cloud Console and put it in this directory.

Run `python3 converse "{Spotify Playlist Name}" "{Desired Playlist Name in Youtube Music}`.

## Caveats

It's not perfect and really just intended for personal, recreational use. I
wanted to migrate some of my own playlists to YT Music and didn't want to use
existing tools I'd have to audit for privacy. There are bugs that I don't care
enough to fix right now. Maybe I will in the future if I actually end up using
this tool for lots of playlists. It works decently well for my purposes.

