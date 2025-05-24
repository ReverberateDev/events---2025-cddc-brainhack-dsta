FROM ubuntu:22.04 AS base

FROM disconnect3d/nsjail

COPY --from=base / /jail/

COPY account /jail/
COPY flag /jail/
COPY banner /jail/

COPY start.sh /
RUN chmod +x /start.sh

CMD [ "/start.sh" ]