# ROLE

You are a principal software architect implementing Phase 5 of the Sagittarius Engine.

The kernel architecture is considered stable.

Do NOT redesign the kernel.

Do NOT modify EngineContext.

Do NOT modify the Extension System.

Do NOT modify Dispatcher.

Do NOT modify Middleware.

Do NOT modify Event Bus.

This phase focuses entirely on Developer Experience.

--------------------------------------------------

# OBJECTIVE

Separate the Sagittarius Engine from the application layout.

The engine should no longer assume any project structure.

Instead, provide a Project SDK capable of generating application skeletons.

The engine becomes reusable.

Project layouts become templates.

--------------------------------------------------

# DESIGN PRINCIPLE

The engine owns runtime behavior.

Templates own project architecture.

Never mix the two.

--------------------------------------------------

# CREATE PROJECT SDK

Introduce a new package

sagittarius_engine.sdk

Suggested structure

sdk/

    templates/

        minimal/

        clean/

        ddd/

        mvc/

    project_generator.py

    template_loader.py

    template_renderer.py

--------------------------------------------------

# PROJECT GENERATOR

Create a ProjectGenerator service.

Responsibilities

- create a new project

- copy template files

- render placeholders

- initialize configuration

- prepare engine bootstrap

The engine itself must never depend on templates.

--------------------------------------------------

# TEMPLATE SYSTEM

Templates should describe project layouts only.

Examples

minimal

clean architecture

ddd

mvc

hexagonal

Future templates should be added without modifying the engine.

--------------------------------------------------

# TEMPLATE PLACEHOLDERS

Support placeholders such as

{{project_name}}

{{package_name}}

{{author}}

{{python_version}}

Do not hardcode values.

--------------------------------------------------

# BOOTSTRAP

Every generated project should expose

main.py

which creates

App()

loads extensions

boots the engine

The generated project should be runnable immediately.

--------------------------------------------------

# EXTENSIBILITY

Third-party template packages should be supported.

The SDK should load templates dynamically.

Avoid hardcoded template lists.

--------------------------------------------------

# DOCUMENTATION

Document the separation clearly.

Engine

↓

SDK

↓

Templates

↓

Application

--------------------------------------------------

# TESTS

Add tests covering

project generation

placeholder rendering

template loading

template discovery

--------------------------------------------------

# ACCEPTANCE CRITERIA

✓ Engine no longer assumes project layout

✓ Project generation is template-driven

✓ SDK is independent from kernel

✓ Templates are pluggable

✓ Existing engine tests continue passing

--------------------------------------------------

# OUTPUT

Provide

1. SDK architecture

2. Template architecture

3. Generated project example

4. Dependency diagram

5. Compatibility report

Do not implement a CLI.

Only build the SDK foundation.
Đây là lý do mình chọn hướng này

Nếu tiếp tục refactor kernel, lợi ích sẽ giảm dần. Trong khi đó, developer experience sẽ quyết định người khác có dùng Sagittarius hay không.

Một người dùng mới sẽ đánh giá framework theo những câu hỏi như:

Mình tạo project mới trong bao lâu?
Có template phù hợp không?
Có ví dụ chạy được ngay không?
Có thể chọn DDD, MVC hay tối giản không?

Khi kernel đã ổn định, việc đầu tư vào SDK, template và tooling sẽ mang lại giá trị lớn hơn rất nhiều so với tiếp tục thay đổi kiến trúc lõi. Đây cũng là cách các framework trưởng thành như ASP.NET Core, Spring hay NestJS phát triển sau khi kernel của họ ổn định.