#Base Python image 
FROM python:3.11

#Installing pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Setting up the working directory in our container
WORKDIR /progetto
COPY . /progetto

#Exposing port where our container will run
EXPOSE 8000

CMD [ "python", "/progetto/off_chain/main.py" ]

#POSSIBILE MODIFICA PER ESTRAZIONE AUTOMATICA

# # Copy the extract.sh script into the container and make it executable
# COPY extract.sh /usr/local/bin/
# RUN chmod +x /usr/local/bin/extract.sh

# # Exposing port where our container will run
# EXPOSE 8000

# # Modify the CMD to run extract.sh before starting the main application
# CMD ["/bin/bash", "-c", "/usr/local/bin/extract.sh && python /progetto/off_chain/main.py"]

