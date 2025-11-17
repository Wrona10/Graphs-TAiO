# Use the official .NET 8.0 SDK image for building
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy the solution file
COPY ["Grafy TAiO.sln", "./"]
COPY ["Grafy TAiO/Grafy TAiO.csproj", "Grafy TAiO/"]

# Restore dependencies
RUN dotnet restore "Grafy TAiO.sln"

# Copy the rest of the source code
COPY . .

# Build the application
WORKDIR "/src/Grafy TAiO"
RUN dotnet build "Grafy TAiO.csproj" -c Release -o /app/build

# Publish the application
FROM build AS publish
RUN dotnet publish "Grafy TAiO.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Use the runtime image for the final stage
FROM mcr.microsoft.com/dotnet/runtime:8.0 AS final
WORKDIR /app
COPY --from=publish /app/publish .

# Set the entry point
ENTRYPOINT ["dotnet", "Grafy TAiO.dll"]
