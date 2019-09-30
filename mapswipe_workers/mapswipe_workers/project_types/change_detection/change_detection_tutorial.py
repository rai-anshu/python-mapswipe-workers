import csv
import json

from mapswipe_workers.definitions import logger
from mapswipe_workers import auth
from mapswipe_workers.project_types.change_detection import tile_functions as t


def create_tutorial(tutorial):
    tutorial, groups_dict, tasks_dict = generate_tutorial_data(tutorial)
    upload_tutorial_to_firebase(tutorial, groups_dict, tasks_dict)


def generate_tutorial_data(tutorial):
    tutorial_id = tutorial['projectId']
    logger.info(f'create tutorial for tutorial id: {tutorial_id}')

    groups_dict = {}
    tasks_dict = {}

    with open(tutorial['examplesFile']) as json_file:
        tutorial_tasks = json.load(json_file)
        print(len(tutorial_tasks))
        print(tutorial_tasks)

        for feature in tutorial_tasks['features']:

            print(feature)

            category = feature['properties']['category']
            group_id = 100 + feature['properties']['id']

            if not group_id in groups_dict.keys():
                groups_dict[group_id] = {
                    "xMax": "104",
                    "xMin": "100",
                    "yMax": "200",
                    "yMin": "200",
                    "requiredCount": 5,
                    "finishedCount": 0,
                    "groupId": group_id,
                    "projectId": tutorial_id,
                    "numberOfTasks": 4,
                    "progress": 0
                }

            reference = feature['properties']['reference']
            zoom = feature['properties']['TileZ']
            task_x = feature['properties']['TileX']
            task_y = feature['properties']['TileY']
            task_id_real = '{}-{}-{}'.format(zoom, task_x, task_y)

            urlA = t.tile_coords_zoom_and_tileserver_to_URL(
                task_x,
                task_y,
                zoom,
                tutorial['tileServerA']['name'],
                tutorial['tileServerA']['apiKey'],
                tutorial['tileServerA']['url'],
                None,
            )
            urlB = t.tile_coords_zoom_and_tileserver_to_URL(
                task_x,
                task_y,
                zoom,
                tutorial['tileServerB']['name'],
                tutorial['tileServerB']['apiKey'],
                tutorial['tileServerB']['url'],
                None,
            )

            if not group_id in tasks_dict.keys():
                tasks_dict[group_id] = {}
                task_id = '{}-{}-{}'.format(16, 100, 200)
            else:
                task_id = '{}-{}-{}'.format(16, 100 + len(tasks_dict[group_id].keys()), 200)

            task = {
                'taskId_real': task_id_real,
                'taskId': task_id,
                'taskX': 100 + len(tasks_dict[group_id].keys()),
                'taskY': 200,
                'groupId': group_id,
                'projectId': tutorial_id,
                'referenceAnswer': reference,
                'category': category,
                'urlA': urlA,
                'urlB': urlB,
            }

            tasks_dict[group_id][len(tasks_dict[group_id].keys())] = task

    return tutorial, groups_dict, tasks_dict


def upload_tutorial_to_firebase(tutorial, groups_dict, tasks_dict):
    # upload groups and tasks to firebase
    tutorial_id = tutorial['projectId']

    fb_db = auth.firebaseDB()
    ref = fb_db.reference('')
    ref.update({
        'v2/projects/{}'.format(tutorial_id): tutorial,
        'v2/groups/{}'.format(tutorial_id): groups_dict,
        'v2/tasks/{}'.format(tutorial_id): tasks_dict,
    })
    logger.info(f'uploaded tutorial data to firebase for {tutorial_id}')