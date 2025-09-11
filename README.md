# Polarco Cálculos Judiciais

## Requirements

- Docker
- docker-compose

## Installation

1. **Clone the project:**

   ```bash
   git clone
   ```

3. **Build and start the containers:**

   ```bash
   docker-compose up --build
   ```

4. **Access the application:**

   Open your web browser and go to [http://localhost](http://localhost)

## Run Backend Tests

1. **Access the container:**

   ```bash
   docker exec -it <container_id> bash
   ```

2. **Run the tests:**

   ```bash
   pytest
   ```

## Run Frontend Tests

1. **Access the container:**

   ```bash
   docker exec -it <container_id> sh
   ```

2. **Run the tests:**

   ```bash
   npm run test
   ```
