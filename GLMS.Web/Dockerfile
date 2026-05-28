# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy project files
COPY GLMS.Web/GLMS.Web.csproj GLMS.Web/
RUN dotnet restore GLMS.Web/GLMS.Web.csproj

# Copy all source files
COPY GLMS.Web/ GLMS.Web/

# Build and publish
WORKDIR /src/GLMS.Web
RUN dotnet publish -c Release -o /app/publish

# Stage 2: Runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .
EXPOSE 5000
ENV ASPNETCORE_URLS=http://+:5000
ENTRYPOINT ["dotnet", "GLMS.Web.dll"]
