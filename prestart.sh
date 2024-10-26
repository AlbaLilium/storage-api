if [ ! $(find . -name 'init_database*')]; then
    alembic revision --autogenerate -m "init database"
fi
alembic upgrade head
