#!/usr/bin/env bash
set -e
exec 3<>/dev/tcp/127.0.0.1/8080
printf 'GET /auth/realms/master/.well-known/openid-configuration HTTP/1.0\r\nHost: localhost\r\n\r\n' >&3
grep -q 'HTTP/1.[01] 200' <&3
