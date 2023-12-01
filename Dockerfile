FROM ubuntu:22.04

SHELL ["/bin/bash", "-c"]

# Skip country selection
RUN apt-get update && \
    apt-get install -yq tzdata && \
    #localedef -i en_US -f UTF-8 en_US.UTF-8 && \
    echo "LANG=\"en_US.UTF-8\"" > /etc/locale.conf && \
    ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Packages
RUN apt-get update && apt-get -y --quiet --no-install-recommends install \
    # Ubuntu requirements
    sudo openssh-client locales build-essential \
    # Backend Python packages
    python3.11 python3-pip python3-pexpect \
    # Tools
    htop net-tools vim curl git bash-completion \
    sed desktop-file-utils libgl1-mesa-dev libglu1-mesa-dev

# # Install Node.js
# RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -
# RUN apt-get install -y nodejs

# Env variable to use terminal / editors
ENV TERM=xterm
# Set timezone format
ENV TZ=UTC

# Create user (Mandatory to mkdir)
ENV HOME="/home/user"
ENV USER="user"
RUN useradd -m ${USER} && echo "${USER}:${USER}" | chpasswd && adduser ${USER} sudo
# Dodge sudo password
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Swap to user ${USER} (Root things before this line)
USER ${USER}

# Create ssh folder and Load gitlab as known host
RUN mkdir -p ${HOME}/.ssh
RUN chmod +rw ${HOME}/.ssh
RUN ssh-keyscan github.com >> ${HOME}/.ssh/known_hosts

WORKDIR ${HOME}

# Update pip
RUN pip install --upgrade pip

# Backend Python Packages
COPY requirements.txt .
RUN pip install -r requirements.txt


# Set RUN using Bash instead of Sh (Mandatory for repo)

CMD [ "/bin/bash" ]