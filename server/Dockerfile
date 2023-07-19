    FROM python:3.8.2

    ENV PYTHONBUFFERED 1
    ENV PYTHONWRITEBYTECODE 1

    RUN apt-get update \
        && apt-get install -y netcat

    ENV APP=/app

    # Change the workdir.
    WORKDIR $APP

    # Install the requirements
    COPY requirements.txt $APP

    RUN pip3 install -r requirements.txt

    # Copy the rest of the files
    COPY . $APP

    EXPOSE 8000

    RUN chmod +x /app/entrypoint.sh

    RUN export URL_NLU="https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/7c29c038-64fb-4ffc-90c5-26c180368811"

    RUN export URL_GET_DEALERS="https://us-south.functions.appdomain.cloud/api/v1/web/3359b9cf-db9c-4cef-8e9b-c4855d4a5213/dealership-package/get-dealership"

    RUN export URL_POST_REVIEW="https://us-south.functions.appdomain.cloud/api/v1/web/3359b9cf-db9c-4cef-8e9b-c4855d4a5213/dealership-package/post-review"

    RUN export URL_GET_REVIEWS="https://us-south.functions.appdomain.cloud/api/v1/web/3359b9cf-db9c-4cef-8e9b-c4855d4a5213/dealership-package/get-reviews"

    ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]

    CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]