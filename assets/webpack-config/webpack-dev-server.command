#!/usr/bin/env bash
{ set +x; } 2>/dev/null

{ set -x; cd "${BASH_SOURCE[0]%/*/*/*}"; { set +x; } 2>/dev/null; }

( set -x; webpack-dev-server --config "${BASH_SOURCE[0]%/*}"/dev.js --mode=none )
