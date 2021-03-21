ARG VERSION=0.0.1

FROM registry.access.redhat.com/ubi8/python-38 as BUILD

LABEL summary="Linker server used to simplify link sharing." \
      description="Linker server used to simplify link sharing." \
      io.k8s.description="Linker server used to simplify link sharing." \
      io.k8s.display-name="Linker server container" \
      io.openshift.expose-services="5000:http" \
      io.openshift.tags="peznauts,linker" \
      name="linker" \
      version="${VERSION}" \
      maintainer="peznauts.com <kevin@cloudnull.com>"

USER root

WORKDIR /build
RUN python3.8 -m venv /build/builder
RUN /build/builder/bin/pip install --force --upgrade pip setuptools bindep wheel
ADD . /build/
RUN dnf install -y $(/build/builder/bin/bindep -b -f /build/bindep.txt test)

WORKDIR /linker
RUN /bin/python3.8 -m venv /linker
RUN /linker/bin/pip install --force --upgrade pip setuptools
RUN /linker/bin/pip install --force --upgrade uwsgi

WORKDIR /build
RUN /linker/bin/pip install . --force --upgrade

FROM registry.access.redhat.com/ubi8/ubi-minimal
EXPOSE 5000
RUN microdnf install -y openssh-clients python3.8 && rm -rf /var/cache/{dnf,yum}
RUN /bin/python3.8 -m venv --upgrade /linker
COPY --from=BUILD /linker /linker
ADD assets/entrypoint /bin/entrypoint
RUN chmod +x /bin/entrypoint
USER 1001
ENTRYPOINT ["entrypoint"]
