import reflex as rx

config = rx.Config(
    app_name="finance_tracker",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)