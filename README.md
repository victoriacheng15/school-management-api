# School Flask API


## What I learned:

Here is a section of what I learned from this project:

### Docker builds
During the development of this Flask API, I compared the build process between **single-stage** and **multi-stage** Dockerfiles. Here are some of the findings:
- Single-stage build: 
  - Time taken: Approximately 0.50s
  - Process:
    - All dependencies, including build tools and caches, are installed into the same image.
    - The final image size is larger due to the inclusion of build tools and extra files.
- Multi-Stage Build
  - Time Taken: Approximately 0.32s
  - Process:
    - Dependencies are installed in a separate builder stage, and only the necessary files (like the app and required libraries) are copied into the final image.
    - The final image is smaller and cleaner, containing only the essential runtime environment.
- Conclusion:
  - Multi-Stage Builds are faster and create smaller, cleaner images than single-stage builds.
  - For small apps like this one, the difference in build time might not be significant, but the resulting image size is smaller and more efficient.
  - Multi-stage builds are particularly useful when you want to separate build dependencies from production runtime, reducing security risks and keeping images optimized.