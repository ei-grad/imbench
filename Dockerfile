FROM python:slim
ADD requirements.txt .
RUN apt update && apt install -y --no-install-recommends \
    libjpeg62-turbo \
    libturbojpeg0 \
    libglib2.0-0 \
    gcc \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir -r requirements.txt \
 && apt autoremove -y gcc
ADD imbench.py .
ENTRYPOINT ["pytest", "imbench.py"]
