# Product Requirements Document (PRD): TimeGlass

This document outlines the refined requirements and high-level vision for **TimeGlass**, a developer tool for profiling FastAPI applications.

## 1. Introduction

* **Product Name:** TimeGlass
* **Problem Statement:** The FastAPI ecosystem lacks a dedicated, easy-to-use, and low-overhead profiling tool for local development. Developers rely on a mix of production APM tools (overkill) or manual benchmarking methods that are slow and provide limited insight.
* **Goal:** To provide a seamless, integrated developer experience for benchmarking FastAPI REST endpoints, allowing engineers to quickly identify and address performance bottlenecks related to request/response times and database queries. The tool will be lightweight, accurate, and provide an intuitive visual interface.

## 2. Core Features & Functionality

### A. Profiling Engine (Rust) 🦀

The core will be a **Rust-based engine** to ensure minimal overhead during profiling. It will collect the following metrics:

* **Total Request Duration:** The total time from request start to response end.
* **Database Query Metrics:** Time for each database query, including the raw SQL statement. This will include a wrapper for popular libraries like `asyncpg` and `SQLAlchemy`.
* **Function Call Timing:** A high-level breakdown of time spent in the endpoint's core functions.
* **Resource Metrics:** CPU and Memory usage per request, captured at the process level.

### B. FastAPI Middleware (Python) 🐍

* A single `TimeGlassMiddleware` class will be added to the `FastAPI` application.
* It will automatically intercept every incoming request, initiate the Rust profiler, and attach a profiling object to the request context.
* The middleware will finalize profiling on response completion, collect the data, and send it to the local storage service.

### C. CLI (`timeglass`) 🛠️

The CLI will provide a simple, predictable interface for developers to interact with the tool.

* `timeglass ui`: This command will start the web dashboard, which will be served as a separate process.
* `timeglass --help`: Built-in help and auto-completion for all commands.
* `timeglass --version`: Displays the current version of the tool.

### D. Web Dashboard 📈

A self-hosted web application served by the `timeglass ui` command, acting as the user's primary interface.

* **Requests List:** A clean, filterable table showing all recent requests. Columns will include:
    * **Timestamp**
    * **Endpoint Path**
    * **HTTP Method**
    * **Status Code**
    * **Total Duration**
* **Detailed Request View:** Clicking a row will open a new page with an in-depth analysis.
    * **Summary Card:** A concise overview of key metrics (duration, status, CPU, memory).
    * **Timeline View:** A visual breakdown of time spent in different stages (middleware, database, processing).
    * **Database Queries Panel:** A list of all SQL queries executed during the request, with individual execution times.
    * **Flame Graph/Call Tree:** A visual representation that helps pinpoint exact bottlenecks within the code.
    * **Context Panel:** Shows request headers, body, and response headers.

## 3. User Experience (UX)

TimeGlass will adhere to a human-centered design philosophy to provide a world-class experience.

* **Clarity:** Descriptive command names and clear dashboard labels.
* **Predictability:** The tool will work out-of-the-box with sensible defaults, requiring minimal configuration.
* **Informative Feedback:** Error messages will be human-readable and actionable. The dashboard will use color to highlight performance issues and potential bottlenecks.
* **Non-Intrusive:** The profiling engine will have a negligible performance impact on the application being tested, ensuring accurate results.
* **Built-in Help:** A comprehensive `--help` option and clear documentation will be available.

## 4. Technical & Business Requirements

* **Technology Stack:** Python (3.10+), FastAPI, Rust, PyO3, Uvicorn, SQLite.
* **Installation:** A single `pip install timeglass` command.
* **Configuration:** A single line of code to add the middleware to the FastAPI app.
* **Open Source:** The project will be open source under a permissive license (e.g., MIT).
* **Monorepo:** The Python and Rust codebases will reside in a single repository for easy management and development.

## 5. Out of Scope

* **Production Monitoring:** This tool is strictly for local development and will not offer features for production environments (e.g., long-term data storage, distributed tracing, alerting, or integration with external APM services).
* **Load Testing:** TimeGlass is a profiler, not a load generator. It will not include features to simulate high traffic or concurrency.
* **Front-end Frameworks:** The web dashboard will be kept simple, avoiding complex front-end frameworks to minimize dependencies and maintain a lightweight footprint.
* **Cloud Integrations:** No direct integrations with cloud providers.

## 6. Benchmarks

TimeGlass will test and score the following benchmarks:

### Performance Benchmarks ⚡️

These metrics measure how fast and efficient your application is under load.

* **Latency (Response Time):**
  * Average Latency: The mean time for a request to be completed.
  * p90 Latency: The latency value at which 90% of requests are faster. This is a crucial indicator of a good user experience.
  * p99 Latency: The latency value at which 99% of requests are faster. This reveals the performance of your application under heavy load and helps catch outliers.

* **Throughput:** The number of Requests Per Second (RPS) your application can handle. You should test this at different load levels to find the maximum sustainable throughput.

* **Resource Utilization:**
  * CPU Usage: The percentage of CPU cores used by your application. An optimized app maintains a stable, low CPU footprint under load.
  * Memory (RAM) Usage: The amount of memory consumed by the application.
  * Database Query Time: The execution time of individual database queries. This is a critical metric for a data-driven application.

### Resilience Benchmarks 🛡️

These metrics measure your application's ability to handle failures and errors gracefully.

* **Error Rate:** The percentage of requests that result in a server-side error (5xx status code). A world-class application should aim for an error rate of 0% in normal operation.
* **Response to Bad Input:** The application's ability to return clear, correct 4xx errors (e.g., 400 Bad Request, 404 Not Found) instead of generic server errors when faced with invalid input.

### Additional Benchmarks

* **Test Coverage:** The percentage of code covered by automated tests.
