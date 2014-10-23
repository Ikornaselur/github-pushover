# Github Bullet
A simple layer between the Github API and Pushover API to forward github push messages to a device running Pushover.

This script uses the [agithub library by Jonathan Paugh](https://github.com/jpaugh/agithub) for Github communication.

## Usage
This script needs two files by default, a `token` file and `pushover` file. They need to be formatted exactly like this:

### token
```
<Github username>,<Github password or token with notifications access (recommended)>
```

### Pushover
```
<Pushover user key>,<Pushover app key>
```

Then setup a cron job to run the script every minute.
