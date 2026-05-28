# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy project files
COPY GLMS.Web/GLMS.Web.csproj GLMS.Web/
COPY GLMS.API/GLMS.API.csproj GLMS.API/
RUN dotnet restore GLMS.API/GLMS.API.csproj

# Copy source files
COPY GLMS.Web/ GLMS.Web/
COPY GLMS.API/ GLMS.API/

# Build and publish
WORKDIR /src/GLMS.API
RUN dotnet publish -c Release -o /app/publish

# Stage 2: Runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .
EXPOSE 5001
ENV ASPNETCORE_URLS=http://+:5001
ENTRYPOINT ["dotnet", "GLMS.API.dll"]
