FROM rserverbase:latest

# Installing plumber requires sodium
RUN apt-get update -y \
    && apt-get install -y libsodium-dev

COPY ./code ./code
COPY ./annoPackagesInfo ./annoPackagesInfo

RUN dos2unix ./code/installAllRequiredPackages.sh

RUN sh ./code/installAllRequiredPackages.sh

