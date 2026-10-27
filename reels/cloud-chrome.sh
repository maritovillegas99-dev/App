#!/usr/bin/env bash
# Solo nube: Remotion lanza Chrome con --no-proxy-server; aquí se quita y se usa el proxy del contenedor.
args=()
for a in "$@"; do
  case "$a" in --no-proxy-server|--proxy-server=*|--proxy-bypass-list=*) ;; *) args+=("$a") ;; esac
done
[ -n "${HTTPS_PROXY:-}" ] && args+=("--proxy-server=$HTTPS_PROXY" "--proxy-bypass-list=localhost;127.0.0.1;<local>")
exec /opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell "${args[@]}"
