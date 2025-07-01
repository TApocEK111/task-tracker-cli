# To-do list

## CRUD JSON File Repository

### ~Models:~
#### ~Task:~
- ~id~
- ~description~
- ~status (todo, in-progress, done)~
- ~createdAt~
- ~updatedAt~

### Methods:
#### ~Create:~
- ~Create a task~

#### Update:
- ~Update task's status (mark)~
- ~Update task's description (update)~
- ~When using any of the update methods, update task's updatedAt property~

#### Read:
- ~Get a task by id~
- ~Get a task by status~
- ~Get all tasks~


## Comands

#### probably there will be parser
input: list of strings
output: comand object (probably will be changed later)

##### Models:
###### Command:
- method
- kwargs

### Input validation
- command
- id
- status
- description
    - length

### `add [<description>]`
- Output example: `Task added successfully (ID: 1)` 
    - File was not found
    - Write unsuccessful
    - Maybe something else

### `update [<id>][<description>]`
- Ouput example: `Task updated successfully (ID: 1)` **// This output is not in the original idea**
    - Handle possible exceptions
    - Inform a user about exceptions

### `delete [<id>]`
- Ouput example: `Task deleted successfully (ID: 1)` **// This output is not in the original idea**
    - Handle possible exceptions
    - Inform a user about exceptions

### `mark [--done | --in-progress][<id>]` **// This command structure was not in the original idea, but I think it is much better** 
- Ouput example: `Task status is done (ID: 1)` **// This output is not in the original idea**
    - Handle possible exceptions
    - Inform a user about exceptions

### `list [done | todo | in-progress][--id][--color]` **// This commands structure has also been changed in order for user to be able to browse task ids. Color indication of statuses is also my idea, just thought it would be cool.**
- Ouput example: `in-progress: "Description 1" (ID: 1)\n done: "Description 2" (ID: 2)\n todo: "Description 3" (ID: 3)` **// This output is not in the original idea**
    - If no color, add status as text
    - Make color distinction
    - Handle possible exceptions
    - Inform a user about exceptions

## Documentation ideas

### Troubleshooting advice

- What to do in case of damaged id_pool.json or my_tasks.json files

## Optimization and refactoring ideas

- Change generating and releasing id
    - Most probably inserting an id at index of its value is gonna result in quicker sort of the pool.
- Refactor id generator test
- Making id pool into hashset probably would be fastre (though not sure it worths the work in this case)