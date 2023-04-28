# ПРОТОТИПНЫЙ КОД

from typing import Dict, List, Tuple, Optional

# тип для строки таблицы
Row = Dict[str, any]

class Table:
    def __init__(self):
        self.rows = {}
        self.next_row_id = 1
        self.sorted_by = []  # список полей, по которым производится сортировка
        self.sorted_rows = []  # отсортированные строки

    def add_row(self, row: Row) -> int:
        row_id = self.next_row_id
        self.rows[row_id] = row
        self.next_row_id += 1
        self._update_sorted_rows()
        return row_id

    def update_row(self, row_id: int, new_values: Row) -> bool:
        if row_id not in self.rows:
            return False
        self.rows[row_id].update(new_values)
        self._update_sorted_rows()
        return True

    def delete_row(self, row_id: int) -> bool:
        if row_id not in self.rows:
            return False
        del self.rows[row_id]
        self._update_sorted_rows()
        return True

    def get_rows(self, start: int, count: int, sort_by: Optional[List[str]] = None) -> List[Row]:
        # если не указаны поля для сортировки, используем текущие
        sort_by = sort_by or self.sorted_by
        # сортируем строки по указанным полям
        sorted_rows = sorted(self.rows.values(), key=lambda row: [row[field] for field in sort_by])
        # запоминаем отсортированные поля для будущих запросов
        self.sorted_by = sort_by
        self.sorted_rows = sorted_rows
        # возвращаем запрошенные строки
        return sorted_rows[start:start + count]

    def _update_sorted_rows(self):
        # обновляем список отсортированных строк
        self.sorted_rows = sorted(self.rows.values(), key=lambda row: [row[field] for field in self.sorted_by])


# пример использования
t = Table()

t.add_row({'name': 'Alice', 'age': 25})
t.add_row({'name': 'Bob', 'age': 30})
t.add_row({'name': 'Charlie', 'age': 20})

print(t.get_rows(0, 3))  # [{'name': 'Alice', 'age': 25}, {'name': 'Charlie', 'age': 20}, {'name': 'Bob', 'age': 30}]

t.delete_row(2)

print(t.get_rows(0, 3))  # [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]

t.update_row(1, {'age': 26})

print(t.get_rows(0, 3))  # [{'name': 'Charlie', 'age': 20}, {'name': 'Alice', 'age': 26}, {'name': 'Bob', 'age': 30}]
