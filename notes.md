# OPUS NOTA

It's na app that aserves as task manager. It works like a kanban board but also features a continous feed with events related to tasks.
Individual tasks feature adding comments, notes and etc. Additional features are related to feed integration. You can ask for help,
add dependency add question and an answer.

Task board and detail interfaces are both inside left pane window. Content is dynamically rendered based on type of loaded object:
if project is loaded displays task board
if task is loaded displays task detail

## TASK BOARD INTERFACE
Show 4 columns of task cards: PLANNING, PENDING, IN PROGRESS, REVIEW, FINISHED
Clicking on task card opens CARD DETAIL INTERFACE.
There's a button to add new tasks.

?> TRACK feature. A horizontal divider spanning across all columns that groups tasks with common theme.


## TASK DETAIL INTERFACE
Shows details of specific tasks.

1) Overall
    1.1) Creation
    1.2) Assignned people
    1.3) Type

2) Notes / description
    Notes maybe just text containing description

3) Discussion
    List of text comments. Also features commands like questions and answers and help requests

## FEED
Contains list of chronological events that happen within application. Events featured in feed:
- task created
- task progress updated
- added comment
- description updated
- changed assignment
- question asked and answered
- help requested

## MODELS:

### PROJECT (refers to a single task board)
opus-nota.com/projects/<project_id>/
- created
- name
- assigned users / groups

### USER

### TASK 
opus-nota.com/projects/<project_id>/tasks/
opus-nota.com/projects/<project_id>/tasks/<task_id>/
- title
- description
- project_id (fk)
- track_id? (fk)
- stage
- created
- assigned people (many to many)

TRACK
opus-nota.com/projects/<project_id>/tracks/
opus-nota.com/projects/<project_id>/tracks/<track_id>/
- name
- created
- color
- project_id

COMMENT
- created
- author
- text
- task_id (fk)
- type (question, answer)

EVENT
- title
- created
- event type
- related object id (idealy hyperlinked field)
- text
