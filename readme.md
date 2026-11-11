# Karaoke!
## A simple tool for lyrics managing

This is a simple script intended to run on top of any music player or server that uses metadata for lyrics.

Karaoke! searches for lyrics on lrclib, and adds them to their respective ID3 tag or vorbisComment.
It can search both synced and plain lyrics, if availible.

It is, for now, a WIP, and will open every single file in its starting directory (recursively).

### Roadmap

 - [ ] Dockerize
 - [x] Add a mode to scan for a single file
 - [x] Modify starting directory
 - [ ] Modify to env variable its lrc preference (or both)
 - [ ] Add a SQLite DB to keep track of scanned files
