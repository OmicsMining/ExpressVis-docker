FROM rserverbase:latest

# Installing plumber requires sodium
RUN apt-get update -y \
    && apt-get install -y libsodium-dev

COPY ./code ./code


RUN dos2unix ./code/installRequiredPackages.R
RUN Rscript ./code/installRequiredPackages.R