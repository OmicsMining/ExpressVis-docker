FROM bioconductor/bioconductor_docker:latest

# Installing plumber requires sodium
RUN apt-get update -y \
    && apt-get install -y libsodium-dev \
    && apt-get install -y dos2unix

COPY ./code ./code
COPY ./annoPackagesInfo ./annoPackagesInfo

RUN dos2unix ./code/installAllRequiredPackages.sh

RUN sh ./code/installAllRequiredPackages.sh

