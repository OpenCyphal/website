# Cyphal website

Sources of the [opencyphal.org](https://opencyphal.org) website (formerly uavcan.org).

## Running locally

A GNU/Linux-based OS is required.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./debug.py
```

## Push-to-deploy

Changes pushed to `master` are automatically deployed to production at [opencyphal.org](https://opencyphal.org).
Changes pushed to `uat` are automatically deployed to [uat.opencyphal.org](https://uat.opencyphal.org);
use it to test changes before they go to production.

The deployment job runs on a self-hosted runner that lives on the web server itself;
see `.github/workflows/deployment.yml` for details.
