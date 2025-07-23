#!/usr/bin/env bash

set -euo pipefail

if [ -z "${LAKE:-}" ]; then
    LAKE="$HOME/lake"
    mkdir -p "$LAKE"
fi

duckdb -cmd "$(cat <<EOF
install ducklake;
install sqlite;

create secret (
    type ducklake,
    metadata_path 'sqlite:$LAKE/metadata.sqlite',
    data_path '$LAKE/data'
);

attach 'sqlite:$LAKE/metadata.sqlite' as metadata;
attach 'ducklake:' as data;

use data;

EOF
)"
