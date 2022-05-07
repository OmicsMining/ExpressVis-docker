# ExpressVis-docker

#### Description
The project contains all necessary files for deploying ExpressVis (https://omicsmining.ncpsb.org.cn/ExpressVis/home) with Docker. Users can easily deploy ExpressVis locally or in their own server.

#### Prerequisite

1. Install [Docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/)
   
2. Download ExpressVis.database.zip from ftp(ftp://omicsmining.ncpsb.org.cn/pub). Unzip the data and place them in a directory. You can download ftp data using [filezilla](https://filezilla-project.org/).

3. Change R mirror. By default, installing R packages will use CRAN mirror "https://mirrors.tuna.tsinghua.edu.cn/CRAN" and bioconductor mirror "https://mirrors.tuna.tsinghua.edu.cn/bioconductor". Installing R packages will take a long time. You would better change them according to your location in the R code files that starts with install.


#### Deploy ExpressVis
1. Clone this project
   
   `
   git clone https://github.com/OmicsMining/ExpressVis-docker.git
   `

2.  Change to ExpressVis-Docker directory

    `
      cd ExpressVis-docker
    `

3.  Change database path in docker-compose.yml file.

    > change '/user/annotationDatabasePath' to your database directory(from prerequisite 2) in setion djangoserver/volumes and section nginx/volumns/

4. Build intermediate image rserverbase. This image will be used in all R-based servers.
   ```
   cd ./rServerBase
   docker build -t rserverbase .
   ```

5. Build docker image rdiffbase. Rdifbase image will be used in rdiffServer image. Docker installs all necessary Microaray annotation packages and so building rdiffbase will take a long time. We recommend users only install Microarray packages they requires. By default, the Microarray packages in this project are just a few packages for test. Users can change the packages to be installed in ./rdiffbase/annoPackagesInfo/**.txt files. MicroarrayPackages.zip file that contains all Microarray packages infos can be downloaded from ftp(ftp://omicsmining.ncpsb.org.cn/pub). 
   
    ```
    cd .. # Go back the root directory
    cd ./rdiffbase       
    docker build -t rdiffbase .
    ```

6. Build images and run containsers using docker-compose

   ```
   cd .. # Go back to the root directory of ExpressVis-docker from ./diffBase
   docker-compose up -d
   ```

7. Open ExpessVis in a browser with the url [localhost:80/ExpressVis/home](localhost:80/ExpressVis/home).







