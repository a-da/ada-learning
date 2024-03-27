# see https://makefiletutorial.com/
SHELL := /bin/bash -eu -o pipefail

DOCKER_PYTHON_VERSION ?= 3.11
DOCKER_EXT_TAG ?= 0.1
DOCKER_IMAGE_NAME ?= selenium_python_google-chrome

debian-requirements:
	apt update -y
	apt install -y unzip wget build-essential

google-chrome: debian-requirements

	# Adding trusting keys to apt for repositories
	wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
	# Adding Google Chrome to the repositories
	sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
	# Updating apt to see and install Google Chrome
	apt -y update

	apt install -y google-chrome-stable

chrome-driver:
	# google-chrome --version
	# Google Chrome 72.0.3626.109

	# Download the Chrome Driver
	_CHROME_VERSION=$(shell google-chrome --version | grep -Po '[\.\d]+') && \
		wget -O /tmp/chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$${_CHROME_VERSION}/linux64/chromedriver-linux64.zip"

	# Unzip the Chrome Driver into /usr/local/bin directory
	unzip /tmp/chromedriver.zip
	cp chromedriver-linux64/chromedriver /usr/local/bin/
	rm -r chromedriver-linux64/chromedriver

docker-build:
	docker build . \
		--platform linux/amd64 \
		-t ${DOCKER_IMAGE_NAME}:${DOCKER_PYTHON_VERSION}.${DOCKER_EXT_TAG} \
			--build-arg="PYTHON_VERSION=${DOCKER_PYTHON_VERSION}"

docker-bash:
	docker run \
		--platform linux/amd64 \
		--name os2 \
		--env="DISPLAY" \
		--net=host \
		-it ${DOCKER_IMAGE_NAME}:${DOCKER_PYTHON_VERSION}.${DOCKER_EXT_TAG} \
		bash
