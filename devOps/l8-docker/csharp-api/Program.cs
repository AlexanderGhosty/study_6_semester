using Microsoft.EntityFrameworkCore;
using CsharpApi.Models;
using System.ComponentModel.DataAnnotations;

var builder = WebApplication.CreateBuilder(args);

// Подключение к PostgreSQL через connection string из переменной окружения
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection")
    ?? Environment.GetEnvironmentVariable("CONNECTION_STRING")
    ?? "Host=dbhost;Port=5432;Database=labdb;Username=postgres;Password=postgres";

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString));

var app = builder.Build();

// Автоматическое применение миграций при старте
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.EnsureCreated();
}

// POST /api/items приём и валидация данных
app.MapPost("/api/items", async (ItemDto dto, AppDbContext db, IConfiguration config) =>
{
    // Валидация
    if (string.IsNullOrWhiteSpace(dto.Name))
        return Results.BadRequest(new { error = "Поле 'name' обязательно для заполнения." });

    if (dto.Name.Length < 2 || dto.Name.Length > 100)
        return Results.BadRequest(new { error = "Поле 'name' должно содержать от 2 до 100 символов." });

    var item = new Item
    {
        Name = dto.Name,
        Description = dto.Description
    };

    db.Items.Add(item);
    await db.SaveChangesAsync();

    // Отправка данных в Микросервис 2 (Python)
    var pythonUrl = Environment.GetEnvironmentVariable("PYTHON_SERVICE_URL")
                    ?? "http://python-api:8000";
    try
    {
        using var httpClient = new HttpClient();
        var processedData = new
        {
            original_name = item.Name,
            processed_name = item.Name.ToUpper(),
            description = item.Description ?? "",
            source_id = item.Id,
            processed_at = DateTime.UtcNow.ToString("o")
        };

        await httpClient.PostAsJsonAsync($"{pythonUrl}/api/processed", processedData);
    }
    catch (Exception ex)
    {
        // Логируем ошибку, но не прерываем основной запрос
        Console.WriteLine($"Ошибка при отправке в Python-сервис: {ex.Message}");
    }

    return Results.Created($"/api/items/{item.Id}", item);
});

// GET /api/items — получение всех элементов
app.MapGet("/api/items", async (AppDbContext db) =>
    await db.Items.OrderByDescending(i => i.CreatedAt).ToListAsync());

// GET /health — проверка здоровья сервиса
app.MapGet("/health", () => Results.Ok(new { status = "healthy" }));

app.Run();

// DTO для входных данных
public record ItemDto(string Name, string? Description);

// DbContext
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
    public DbSet<Item> Items => Set<Item>();
}