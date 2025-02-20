# app/Dockerfile

# pull the official docker image
FROM python:3.11.2-slim

# set work directory
WORKDIR /django_ecommerce/e_commerce

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY=algumsegredo
ENV ALLOWED_HOSTS=localhost,127.0.0.1
ENV STRIPE_API_KEY=sk_test_51QuHhSD6xIbnoKxMa1kS3JGDJ538Tcx6jjyHSai9JQjlu1HpgFNLYH61kqQpraKdldSKtlRy91u71UgzV4hSvC9j00EgFFAtob
ENV STRIPE_PUB_KEY=pk_test_51QuHhSD6xIbnoKxMHOFfmofIRSlMzZRdR3J169OPx0B73oI92OdmY7z9otZewbt2q76tzZup8w0Kezglt1y6wBFp006FRR4XkI
ENV DEBUG=False
ENV DB_NAME=postgres
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_HOST=db
ENV DB_PORT=5432

# install dependencies
COPY .env /django_ecommerce/e_commerce/billing/.env
COPY requirements.txt .
RUN pip install -r requirements.txt



# copy project
COPY . .
