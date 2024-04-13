#Base Python image from Alpine
FROM python:3.11-alpine

#Packages for alpine dependecies
RUN apk add --no-cache gcc musl-dev libffi-dev

#Installing pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Setting up the working directory in our container
WORKDIR /blockchain
COPY . /blockchain

#Exposing port 8000 where our container will run
EXPOSE 8000

CMD [ "python", "/blockchain/off_chain/main.py" ]


