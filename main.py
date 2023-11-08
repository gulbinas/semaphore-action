import time
import os
import asyncio
import websockets
import semaphore_client
import json
import re
from pprint import pprint
from semaphore_client.semaphore import authentication_api
from semaphore_client.semaphore import project_api
from semaphore_client.semaphore import default_api
from semaphore_client.model.project_project_id_tasks_get_request import ProjectProjectIdTasksGetRequest
from semaphore_client.model.task import Task
from semaphore_client.model.api_token import APIToken
from semaphore_client.model.login import Login

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from websockets import ConnectionClosed

API_KEY = 'f4ws0obik6ilc1bxmk6gxwj2kiz_xvoenhl0ysnpst0='
API_URL = "http://10.8.0.1:3000/api"
WS_API_URL = "ws://10.8.0.1:3000/api"

configuration = semaphore_client.Configuration(
    host=API_URL
)


# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: bearer
configuration.api_key['bearer'] = API_KEY

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
configuration.api_key_prefix['bearer'] = 'Bearer'


# Configure API key authorization: cookie
#configuration.api_key['cookie'] = 'semaphore=MTY5OTQyNTkxOHxORlZweXBLaWN4c1NFYW5rNDd2VXp6MmQzSmMwT082QlBNdE92cDJfamZKYnhEVE1lY3RFb3dnREp5dG5SaTBLOEJZcGxHQVNSRWtCZXRWdXpqUE9aaEE9fOSfyO-B-aeugZnoX75lpOj_FQ1XuDhBPJ7fURcVxduM'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
#configuration.api_key_prefix['cookie'] = 'Bearer'
def start_task(template_id, project_id=1):
    out = None
    with semaphore_client.ApiClient(configuration) as api_client:
        # pass
        # Create an instance of the API class

        # api_instance = authentication_api.AuthenticationApi(api_client)
        # out = api_instance.user_tokens_get()

        # print(out)

        api_instance = project_api.ProjectApi(api_client)
        task = ProjectProjectIdTasksGetRequest(
            template_id=template_id,
            debug=False,
            dry_run=False,
            environment="{}",
        )  # ProjectProjectIdTasksGetRequest |

        # example passing only required values which don't have defaults set
        try:
            # Starts a job
            api_response = api_instance.project_project_id_tasks_post(project_id, task)
            #pprint(api_response)
            out = api_response['id']
        except semaphore_client.ApiException as e:
            print("Exception when calling ProjectApi->project_project_id_tasks_post: %s\n" % e)

        # api_instance = default_api.DefaultApi(api_client)

        # example, this endpoint has no required or optional parameters
        # try:
        #     # Websocket handler
        #     thread = api_instance.ws_get(async_req=True, _preload_content=False, _return_http_data_only=False)
        #     result = thread.get()
        #     print(result)
        # except semaphore_client.ApiException as e:
        #     print("Exception when calling DefaultApi->ws_get: %s\n" % e)
        # login_body = Login(
        #     auth="admin",
        #     password="adminadmin",
        # ) # Login |
        #
        # try:
        #     # Performs Login
        #     out = api_instance.auth_login_post(login_body, async_req=False)
        #     print(out)
        # except semaphore_client.ApiException as e:
        #     print("Exception when calling AuthenticationApi->auth_login_post: %s\n" % e)
    return out


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


async def pool_task_updates(run_id=None, api_instance=None, project_id=None):
    def get_task_status(task_id=None, project_id=1):
        out = None
        try:
            # Get a single task
            api_response = api_instance.project_project_id_tasks_task_id_get(project_id, task_id)
            out = api_response
        except semaphore_client.ApiException as e:
            print("Exception when calling ProjectApi->project_project_id_tasks_task_id_get: %s\n" % e)

        return out

    uri = WS_API_URL + '/ws'

    async with websockets.connect(
            uri,
            extra_headers={"Authorization": f"Bearer {API_KEY}"}
    ) as websocket:
        while True:
            try:

                greeting = await websocket.recv()
                log_item = json.loads(greeting)
                log_item['output'] = ansi_escape.sub('', log_item.get('output', ''))
                status = ''
                if log_item.get('task_id', 0) == run_id:
                    print(f"{log_item}")
                    status = log_item.get('status', '')
                else:
                    task_object = get_task_status(run_id, project_id)
                    print(f"{task_object.to_dict()}")
                    status = task_object.to_dict().get('status', '')

                if status in ['success', 'error']:
                    break

            except ConnectionClosed as ex:
                break

def set_github_action_output(output_name, output_value):
    f = open(os.path.abspath(os.environ["GITHUB_OUTPUT"]), "a")
    f.write(f'{output_name}={output_value}')
    f.close()


def main():
    my_input = os.environ["INPUT_MYINPUT"]
    my_output = f'Hello {my_input}'
    set_github_action_output('myOutput', my_output)

    project_id = 1  # int | Project ID
    print_hi('PyCharm')
    task_id = start_task(29, project_id)
    with semaphore_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = project_api.ProjectApi(api_client)

        asyncio.run(pool_task_updates(task_id, api_instance, project_id))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
