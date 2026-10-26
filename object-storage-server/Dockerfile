# Official historical sources are used because the registry images/downloads
# referenced by the assignment are no longer available. Keep source + license.
FROM golang:1.24-alpine AS builder
WORKDIR /src
ADD --checksum=sha256:1a63209927b9d1fb239b2a776b7b01d1902eff19379a108f4bc7005edcc0968c https://codeload.github.com/minio/minio/tar.gz/refs/tags/RELEASE.2025-04-22T22-12-26Z /tmp/minio.tar.gz
RUN tar -xzf /tmp/minio.tar.gz --strip-components=1 && rm /tmp/minio.tar.gz
ENV CGO_ENABLED=0 GOMAXPROCS=4
RUN --mount=type=cache,target=/go/pkg/mod --mount=type=cache,target=/root/.cache/go-build \
    go build -p 4 -trimpath -ldflags="-s -w" -o /out/minio .

FROM alpine:3.21
RUN apk add --no-cache ca-certificates && adduser -D -u 1000 minio
COPY --from=builder /out/minio /usr/local/bin/minio
COPY --from=builder /src/LICENSE /licenses/LICENSE-minio
LABEL org.opencontainers.image.source="https://github.com/minio/minio" \
      org.opencontainers.image.version="source-RELEASE.2025-04-22T22-12-26Z" \
      org.opencontainers.image.licenses="AGPL-3.0-only"
RUN mkdir /data && chown minio:minio /data
USER minio
EXPOSE 9000 9001
ENTRYPOINT ["minio"]
CMD ["server", "/data", "--console-address", ":9001"]
