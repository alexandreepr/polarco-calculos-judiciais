FROM node:24-alpine

WORKDIR /app

COPY . .

RUN corepack enable && corepack prepare pnpm@latest --activate
RUN pnpm install --frozen-lockfile

EXPOSE 3000

CMD ["pnpm", "dev", "--host"]