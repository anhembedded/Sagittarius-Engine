> Applies to Sagittarius Engine v1.x

# Project Templates

The Sagittarius SDK provides project templates to generate a structured application skeleton.

---

## Available Templates

| Template | Best For | Structure |
|---|---|---|
| `minimal` | Quick scripts, prototyping | Single-file entry point |
| `clean` | General applications | Layered architecture (domain / app / infra) |
| `ddd` | Domain-heavy systems | DDD-oriented folder layout |
| `mvc` | UI or web-style projects | Model / View / Controller separation |

---

## Generate a Project

```bash
sagittarius new <template> <project_name>
```

Examples:

```bash
sagittarius new minimal my_bot
sagittarius new clean my_service
sagittarius new mvc my_app
```

Each generated project is immediately runnable:

```bash
cd my_bot
python main.py
```

---

## Template Comparison

### `minimal`

Suitable for: quick experiments, simple automation scripts.

```
my_bot/
├── main.py
└── requirements.txt
```

### `clean`

Suitable for: production services, worker applications.

```
my_service/
├── main.py
├── domain/
├── application/
└── infrastructure/
```

### `ddd`

Suitable for: complex business domains, event-sourced applications.

```
my_service/
├── main.py
├── domain/
│   ├── entities/
│   ├── events/
│   └── services/
├── application/
└── infrastructure/
```

### `mvc`

Suitable for: desktop applications, REST API services.

```
my_app/
├── main.py
├── models/
├── views/
└── controllers/
```

---

## Best Practices

**Start with `minimal`** when exploring a new integration or prototyping a solution.

**Switch to `clean` or `ddd`** as your application grows in complexity.

**Templates are starting points, not constraints.** You can freely rename directories, add layers, or reorganize as your application's architecture evolves. The engine does not enforce any specific folder structure.

---

> [Found an issue? Edit this page on GitHub.](https://github.com/your-repo/edit/main/docs/getting-started/project_templates.md)
