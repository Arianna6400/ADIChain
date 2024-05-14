# An Healtcare DAPP: ADIChain

![](https://github.com/Arianna6400/ADIChain/blob/master/docs/logo_adichain.png)

## Table of Contents

- [Introduction](#introduction)
    - [Overview](#overview)
    - [Key Features](#key-features)
    - [Technologies Used to Develop](#technologies-used-to-develop)
- [Installation](#installation)
    - [Requirements](#requirements)
    - [Setup in UNIX-like OS's](#setup-in-unix-like-oss)
    - [Setup in Windows](#setup-in-windows)
- [How to use it](#how-to-use-it)
    - [First look](#first-look)
    - [Bonus track: Scripts](#bonus-track-scripts)
- [Contributors](#contributors)

## Introduction

Welcome to **ADIChain**, a decentralized DApp platform built on blockchain, designed to give a new prospective to the management of health information. ADIChain utilizes blockchain technology to ensure security, privacy, and accessibility of medical information, offering an innovative solution for doctors, patients and caregivers.

### Overview

ADIChain is a medical platform that facilitates effective and secure management of health data. Using Ethereum as the backbone for data security and immutability, and Python for offchain operations, ADIChain aims to improve communication between doctors and patients. This application is designed to allow doctors to manage medical reports and treatment plans efficiently, while patients, both autonomous and non-autonomous (assisted by caregivers), can access and view their medical information securely and privately.

> **N.D.R.:** ADI stands for *Assistenza Domiciliare Integrata*, as for *Integrated Home Care*

### Key Features

Our mission is to simplify the way medical information is managed and shared, prioritizing the security and privacy of data.
ADIChain is designed to be used both by healthcare professionals and patients and/or their caregivers. Here are listed some of the main functions:

- **Medical Report Management**: Doctors can create, manage, and share medical reports and treatment plans digitally in real-time.
- **Customized Treatment Plans**: Development of specific treatment plans for each patient, accessible by both doctors and patients or their caregivers.
- **Secure and Decentralized Access**: Thanks to the use of the blockchain technology, all information is protected against unauthorized changes, ensuring a secure and transparent environment.
- **Intuitive User Interface**: Designed to be accessible and easy to use for all users, regardless of their technical expertise.

### Technologies Used to Develop

- [Python](https://www.python.org/) -> Main programming language
- [Sqlite3](https://www.sqlite.org/) -> Database used
- [Ganache](https://archive.trufflesuite.com/ganache/) -> Personal blockchain as Ethereum simulator
- [Web3](https://web3py.readthedocs.io/en/stable/) -> Python library for interacting with Ethereum
- [Docker](https://www.docker.com/) and [Docker-compose](https://docs.docker.com/compose/) -> Containerization
- [Solidity](https://soliditylang.org/) -> Smart contract development
- [Py-solc-x](https://solcx.readthedocs.io/en/latest/) -> Solidity compiler
- [Unittest](https://docs.python.org/3/library/unittest.html) -> Unit testing framework

## Installation

In order to run our application, you need to follow a few steps.

### Requirements

Before getting started, make sure you have installed Docker on your computer. Docker provides an isolated environment to run applications in containers, ensuring the portability and security of project components. You can run the Docker installation file from the following [link](https://www.docker.com/).

Also, make sure you have installed `git` on your computer. In **Windows** systems, you could download [here](https://git-scm.com/download/win) the latest version of **Git for Windows**. In **UNIX-like** operating systems, you could run the following command:

```bash
sudo apt install git
```

### Setup in UNIX-like OS's

First, you need to clone this repository. In order to do that, you can open your command shell and run this command:

```bash
git clone https://github.com/Arianna6400/ADIChain
```

Then, make sure you are placed in the right directory:

```bash
cd ADIChain
```

You can run the following command if you want to re-build Docker's image:

```bash
docker-compose build --no-cache
```

Now, you can initiate the process of creating and starting the Docker containers required to host the Ethereum blockchain by running the following simple command:

```bash
docker-compose up -d
```

You could also check if services were built properly by running `docker-compose logs`. Also, make sure your user has the proper privileges to run Docker commands. Otherwise, you can address this issue by prefixing each command with `sudo`.

> **NOTE:** The application has been tested on [Ubuntu](https://ubuntu.com/) and [Kali Linux](https://www.kali.org/).

### Setup in Windows

To setup the application on Windows, you can basically run the same commands previously listed in your **Windows PowerShell**. Make sure you open the Shell in the project's directory.

If the docker commands do not work due to the missing *engine*, you will probably need to start [Docker Desktop](https://www.docker.com/products/docker-desktop/) in the background, which is the fastest way to start docker on Windows systems.

> **NOTE:** The application has been tested both on Windows 10 and Windows 11. 

### Setup in macOS

The application on macOS systems works in the same way as previously described. You can test it on your terminal following the UNIX-like setup. 

If `docker-compose` does not run at first, you probably need to set up an environment variable to set the Docker platform. You should run the following command:

```bash
sudo DOCKER_DEFAULT_PLATFORM=linux/amd64 docker-compose run -it adichain
```

After this set-up, the application should run properly.

> **NOTE:** The application has been tested on macOS M1 Pro (ARM64 architecture).

## How to use it

Once the setup has been completed, you can proceed with running the main application interface with the following command:

```bash
docker-compose run -it adichain
```

Remember to include `-it`, because `-i` ensures that the container's *STDIN* is kept open and `-t` allocates a *pseudo-TTY*, which is essential for interacting with the application via terminal. Together, these flags allow you to interact with the `adichain` service through a command line interface.

At this point, the program is ready to be used. After executing the previous command and successfully deploying the entire infrastructure, you can interact with the application through the terminal that opens after deployment.

### First look

Upon the very first startup of the program, it will perform an application check mechanism from Docker to verify that Ganache is ready to listen. If there are no errors, ADIChain will start correctly and run the first homepage.

![](https://github.com/Arianna6400/ADIChain/blob/master/docs/first_look.png)

Now, you can *register* a new account as a Doctor, Patient or Caregiver, or *login* if you are already enrolled, and start exploring every feature of our application.
**Enjoy it!**

> **NOTE:** If you want to test the entire application, you **need** to have both *public key* and *private key* once the deployment has been completed during the registration phase. In order to access those elements, you could run the `extract.sh`script described below, or you could connect your local Ganache to find them. We would like to highlight the fact that the extraction script is for **educational purposes only**. In a real-world context, it is strongly discoureged to use this solution for security purposes. 

### Bonus track: Scripts

In order to make registration tests easy, we have included some interesting scripts:

1. `extract.sh` -> Allows you to extract the Ganache logs, through Docker-compose, to access both the *public key* and the *private key* associated with the contract being deployed.
2. `gen_email.sh` -> Generates a list of random emails, with the domain '**adichain.com**', associated with a username that is also randomic.
3. `gen_phone.sh` -> Generates a list of random phone numbers, both landline and mobile, with Italian prefixes.
4. `gen_password.sh` -> Generates a list of random passwords according to the **Regex** format required by the system.

To run the scripts, you need to go to the project's `/scripts` directory. After that, you need to run the following command to make the scripts executable:

```bash
chmod +x ./SCRIPT_NAME.sh
```

After that, you can run the following command:

```bash
./SCRIPT_NAME.sh
```

Changing the `SCRIPT_NAME` with the proper name of the script you want to execute. You can find your `FILE_NAME.txt`. files inside the directory and use one of the results to register your user in our application.

## Contributors
Meet the team that made ADIChain possible:

| Contributor Name      | GitHub                                  |
|:----------------------|:----------------------------------------|
| ⭐ **Agresta Arianna**    | [Click here](https://github.com/Arianna6400) |
| ⭐ **Biccheri Emanuele**  | [Click here](https://github.com/Emanuele1087650) |
| ⭐ **Giacconi Alessio**   | [Click here](https://github.com/AlessioGiacconi) |
| ⭐ **Giuliani Mauro**     | [Click here](https://github.com/Mau-Hub) |
| ⭐ **Visi Andrea**        | [Click here](https://github.com/Andreavisi1) |



