FROM mcr.microsoft.com/playwright:v1.40.0-jammy

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npx playwright install --with-deps chromium
RUN chmod +x scripts/docker-entrypoint.sh

ENV CI=true
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

ENTRYPOINT ["/app/scripts/docker-entrypoint.sh"]
