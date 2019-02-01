# UAVCAN website

Sources of the [uavcan.org](https://uavcan.org) website.

## Running locally

A GNU/Linux-based OS is required.

```sh
pip3 install -r requirements.txt
./debug.py
```

## Push-to-deploy

A sample git post-receive hook is shown below.

```sh
#!/bin/sh

WORKTREE=/var/www/uavcan.org        # Web server root
GITDIR=/var/repo/uavcan.org.git     # Repository root

git --work-tree=$WORKTREE --git-dir=$GITDIR checkout -f
cd $WORKTREE && git --work-tree=$WORKTREE --git-dir=$GITDIR submodule update --init --recursive

chmod 777 -R $WORKTREE

sudo systemctl reload apache2
```

In order to use push-to-deploy, add a new remote to your copy of the git repository
(adjust the URL as necessary):

```bash
git remote add production ssh://ubuntu@ec2-18-196-176-112.eu-central-1.compute.amazonaws.com/var/repo/uavcan.org.git
```

Then just say `git push production` whenever you want things released.
