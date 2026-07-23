from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


db_url = 'sqlite:///diary.db'

engine = create_engine(db_url, echo=True)


class Base(DeclarativeBase):
    pass


class EntryORM(Base):
    __tablename__ = 'entry_orm'
    id: Mapped[int] = mapped_column(primary_key=True)
    theme: Mapped[str]
    date: Mapped[date]
    text: Mapped[str]


session = sessionmaker(engine)

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


class Database:
    def __init__(self, engine, model):
        self.engine = engine
        self.session = sessionmaker(self.engine)
        self.model = model

    def add_entry(self, theme: str, text: str):
        new_entry = self.model(
            theme=theme,
            date=date.today(),
            text=text
        )
        try:
            with self.session() as sess:
                sess.add(new_entry)
                sess.commit()
            print('Запись успешно добавлена')
            return True
        except Exception as e:
            print(f'Ошибка: {e}')
            return False

    def update_entry(
            self,
            id: int,
            new_theme: str | None,
            new_text: str | None
            ):
        try:
            with self.session() as sess:
                entry = sess.get(EntryORM, id)
                if new_theme:
                    entry.theme = new_theme
                if new_text:
                    entry.text = new_text
                sess.commit()
                print(f'Запись #{id} успешно обновлена')
            return True
        except Exception as e:
            print(f'Ошибка: {e}')
            return False

    def get_all_entrys(self):
        try:
            with self.session() as sess:
                query = sess.query(
                    self.model
                    ).all()
                return query
        except Exception as e:
            print(f'Ошибка: {e}')
            return False

    def delete_entry(self, id: int):
        try:
            with self.session() as sess:
                entry = sess.get(self.model, id)
                sess.delete(entry)
                sess.commit()
            print(f'Запись #{id} успешно удалена')
            return True
        except Exception as e:
            print(f'Ошибка: {e}')
            return False
