# Tracklift

### A command lint tool for exporting playlists from NTS or BBC Sounds to Spotify

![Alt Text](./.docs/demo.gif)

## Setup

The application requires environment variables that should be set in the .env file
in the root folder. 

The required environment variables are:
- [SPOTIFY_CLIENT_ID](https://spotipy.readthedocs.io/en/2.21.0/#quick-start)
- [SPOTIFY_CLIENT_SECRET](https://spotipy.readthedocs.io/en/2.21.0/#quick-start)
- [SPOTIFY_REDIRECT_URL](https://spotipy.readthedocs.io/en/2.21.0/#quick-start)

## Available scripts

All actions that are used in the repository are available in the Makefile.
All pre-commit hooks, GitHub workflows, and build tooling use this Makefile to perform these actions.
This allows for DRY, self-documentation, and easy manual running.

The following Makefile commands are available for this repository:

### `make install`
Installs the application.

### `make update`
Update all the dependencies to the latest available version.

### `make start`
Runs the command line tool. Please refer to the [setup guide](#Setup)
before running the command line tool. 

### `make test-all`
Runs all available tests - unit, integration, acceptance, load, performance

### `make test-unit`
Runs unit tests and build a coverage report

### `make test-integration`
Runs integration tests

### `make check-all`
Runs all code style and security checks

### `make check-format`
Checks formatting

### `make check-poetry`
Checks the lock file is up to date

### `make check-lint`
Checks for any linting errors

### `make check-mypy`
Checks static typing

### `make check-bandit`
Checks for security vulnerabilities in the file.

### `make check-private-keys`
Checks for the any hardcoded string that could be private keys.

### `make check-format`
Checks for any formatting errors

### `make format`
Re-formats all files
