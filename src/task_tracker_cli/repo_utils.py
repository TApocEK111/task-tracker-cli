import os
import json
from .models import Task

_SAVE_FILE_PATH = os.path.join(os.getcwd(), 'data', 'my_tasks.json')
_ID_POOL_PATH = os.path.join(os.getcwd(), 'data', 'id_pool.json')

def load_tasks() -> dict[int, Task]:
    if os.path.exists(_SAVE_FILE_PATH) and not os.path.getsize(_SAVE_FILE_PATH) == 0:
        with open(_SAVE_FILE_PATH, 'r') as file:
            try:
                data = json.load(file)
                result = {}
                for item in data:
                    task = Task.fromdict(item)
                    result[task.id] = task
                return result
            except json.JSONDecodeError as ex:
                print('Json save file is damaged!')
                raise ex
    else:
        with open(_SAVE_FILE_PATH, 'w'):
            return dict()
        
def save_tasks(tasks: list[Task]):
    with open(_SAVE_FILE_PATH, 'w') as file:
        json.dump([task.todict() for task in tasks], file)

def _load_id_pool() -> dict[str, list[int]]:
    if os.path.exists(_ID_POOL_PATH) and not os.path.getsize(_ID_POOL_PATH) == 0:
        with open(_ID_POOL_PATH, 'r') as pool:
            try:
                data = json.load(pool)
                return data
            except json.JSONDecodeError as ex:
                print('Json id pool was damaged!')
                raise ex
    else:
        with open(_ID_POOL_PATH, 'w'):
            return {'taken': [], 'reuse': []}
        
def _dump_id_pool(new_pool: dict[str, list[int]]):
    with open(_ID_POOL_PATH, 'w') as pool:
        json.dump(new_pool, pool)

def generate_id() -> int:
    pool = _load_id_pool()
    if pool['reuse']:
        res = pool['reuse'][0]
        pool['reuse'].pop(0)
        pool['taken'].append(res)
        pool['taken'].sort()
    elif pool['taken']:
        res = pool['taken'][-1] + 1
        pool['taken'].append(res)
    else:
        res = 1
        pool['taken'].append(res)

    _dump_id_pool(pool)
    return res

def release_id(free_id: int):
    pool = _load_id_pool()
    pool['taken'].remove(free_id)
    pool['reuse'].append(free_id)
    pool['reuse'].sort()
    _dump_id_pool(pool)