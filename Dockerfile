FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    fontconfig \
    libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Download Inter font family from GitHub release
RUN mkdir -p bizcard/assets/fonts && \
    wget -q "https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip" -O /tmp/inter.zip && \
    unzip -q /tmp/inter.zip -d /tmp/inter && \
    cp /tmp/inter/Inter\ Desktop/Inter-Regular.ttf bizcard/assets/fonts/ && \
    cp /tmp/inter/Inter\ Desktop/Inter-Medium.ttf bizcard/assets/fonts/ && \
    cp /tmp/inter/Inter\ Desktop/Inter-Bold.ttf bizcard/assets/fonts/ && \
    cp /tmp/inter/Inter\ Desktop/Inter-Light.ttf bizcard/assets/fonts/ && \
    cp /tmp/inter/Inter\ Desktop/Inter-SemiBold.ttf bizcard/assets/fonts/ && \
    rm -rf /tmp/inter /tmp/inter.zip

COPY . .

RUN pip install --no-cache-dir -e .

RUN fc-cache -fv

VOLUME ["/data"]
WORKDIR /data

ENTRYPOINT ["python", "-m", "bizcard"]
CMD ["--help"]
