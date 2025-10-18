# OOP ES - OOP Event sourcing

### WARNING

Still in development

### Installation

```
pip install oop-es
```

### Postgres adapter

Use `pip install oop-es[pg]` instead. Use [this script](./oop_es_pg/tests/integration/init.sql) to init the tables.
You can rename the `events` or use a custom schema, just pass the table name during the `PostgresEventStore` 
initialization.

### Usage

Check `example` folder