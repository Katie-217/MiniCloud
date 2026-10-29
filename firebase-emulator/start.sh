#!/bin/sh
set -eu
mkdir -p /data
set -- emulators:start --project demo-minicloud --only auth,firestore,storage --export-on-exit /data/export
if [ -f /data/export/firebase-export-metadata.json ]; then
    set -- "$@" --import /data/export
fi
exec firebase "$@"
