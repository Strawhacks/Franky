# franky

It's a Robot! For Discord!

## Getting started

This project manages dependencies with [pipenv](https://github.com/pypa/pipenv). One way to install it is with pip.

```Bash
python -m pip install pipenv
```

Once `pipenv` is installed, invoke it to grab our project dependencies.

```Bash
python -m pipenv install
```

### Running the bot

Set the appropriate environment variables, then run!

```Bash
$ export DISCORD_TOKEN="super-secret-token"
$ export DISCORD_GUILD_IDS="90210"
$ python -m pipenv run python bot.py
Ready!
```

Optionally activate pipenv's virtual environment.

```Bash
python -m pipenv shell
```

## Contributing

This project uses [black](https://github.com/psf/black) to enforce consistent syntax and style. Run it with `pipenv`.

```Bash
python -m pipenv run black .
```