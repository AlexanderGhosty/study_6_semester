# Этап 1: Сборка
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build

WORKDIR /src

COPY HelloDocker/ .

RUN dotnet publish -c Release -o /app/publish

# Этап 2: Runtime
FROM mcr.microsoft.com/dotnet/runtime:10.0 AS runtime

WORKDIR /app

COPY --from=build /app/publish .

CMD ["dotnet", "HelloDocker.dll"]