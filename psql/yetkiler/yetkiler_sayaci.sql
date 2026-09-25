SELECT setval(
    pg_get_serial_sequence('yetkiler', 'id'),
    (SELECT MAX(id) FROM yetkiler)
);