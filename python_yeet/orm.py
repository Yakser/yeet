import pymysql
from pymysql import connect


class BaseManager:
    connection: None | pymysql.Connection = None

    def __init__(self, model_class):
        self.model_class = model_class

    def select(self, *field_names, chunk_size=2000):
        formatted_fields = ', '.join(field_names)

        if not field_names:
            raise ValueError("Specify the fields to be returned.")

        query = f"SELECT {formatted_fields} FROM {self.model_class.table_name}"

        cursor = self._get_cursor()
        cursor.execute(query)

        # Fetch data obtained with the previous query execution
        # and transform it into `model_class` objects.
        # The fetching is done by batches of `chunk_size` to
        # avoid to run out of memory.
        model_objects = []
        is_fetching_completed = False

        while not is_fetching_completed:
            result = cursor.fetchmany(size=chunk_size)
            for row_values in result:
                keys = field_names
                values = row_values
                row_data = dict(zip(keys, values))
                model_objects.append(self.model_class(**row_data))

            is_fetching_completed = len(result) < chunk_size
        return model_objects

    def get(self, id, *field_names):
        """
        Returns a model object with the given id

        Args:
            id:
            *field_names: a list of fields to be returned
        """
        id = int(id)
        if "id" not in field_names:
            model_objects = self.select(*field_names, "id")
        else:
            model_objects = self.select(*field_names)

        for obj in model_objects:
            if obj.id == id:
                return obj

    def bulk_insert(self, rows: list):
        field_names = rows[0].keys()

        assert all(row.keys() == field_names for row in rows), "Field names must be the same in every row."

        formatted_fields = ', '.join(field_names)
        # looks like "(%s, %s), (%s, %s), ..."
        values_placeholder_format = ", ".join([f'({", ".join(["%s"] * len(field_names))})'] * len(
            rows))

        query = f"INSERT INTO {self.model_class.table_name} ({formatted_fields})" \
                f" VALUES {values_placeholder_format}"

        params = []
        for row in rows:
            row_values = [row[field_name] for field_name in field_names]
            params.extend(row_values)

        self._execute(query, params)

    def update(self, new_data: dict):
        field_names = new_data.keys()

        # looks like "field_name=%s, another_field_name=%s, ..."
        placeholder_format = ', '.join([f"{field_name} = %s" for field_name in field_names])

        query = f"UPDATE {self.model_class.table_name} SET {placeholder_format}"
        params = list(new_data.values())

        self._execute(query, params)

    def delete(self, where):
        raise NotImplementedError

    def delete_all(self):
        query = f"DELETE FROM {self.model_class.table_name}"

        self._execute(query)

    @classmethod
    def set_connection(cls, db_settings):
        connection = connect(**db_settings, autocommit=True)
        cls.connection = connection

    @classmethod
    def _execute(cls, query, params=None):
        cursor = cls._get_cursor()
        cursor.execute(query=query, args=params)

    @classmethod
    def _get_cursor(cls):
        return cls.connection.cursor()


class MetaModel(type):
    manager_class = BaseManager

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()


class BaseModel(metaclass=MetaModel):
    table_name = ""

    def __init__(self, **row_data):
        for field_name, value in row_data.items():
            setattr(self, field_name, value)

    def __repr__(self):
        formatted_attrs = ", ".join([f"{field}={value}" for field, value in self.__dict__.items()])
        return f"<{self.__class__.__name__}: ({formatted_attrs})>"
