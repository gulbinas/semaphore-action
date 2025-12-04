"""
Test data module containing real API responses from Semaphore
This data is extracted from live API calls to ensure tests use realistic data
"""

# Real templates response from curl call to /api/project/1/templates
REAL_TEMPLATES_RESPONSE = [
    {
        "id": 49,
        "project_id": 1,
        "inventory_id": 1,
        "repository_id": 1,
        "environment_id": 1,
        "name": "01 provision beta without git/db update for app",
        "playbook": "inrento-playbook.yml",
        "arguments": None,
        "allow_override_args_in_task": True,
        "description": None,
        "vault_key_id": 5,
        "type": "",
        "start_version": None,
        "build_template_id": None,
        "view_id": 1,
        "autorun": False,
        "survey_vars": None,
        "suppress_success_alerts": False
    },
    {
        "id": 44,
        "project_id": 1,
        "inventory_id": 1,
        "repository_id": 1,
        "environment_id": 1,
        "name": "03 update beta app from git",
        "playbook": "inrento-playbook.yml",
        "arguments": ["--tags=deploy_app"],
        "allow_override_args_in_task": True,
        "description": None,
        "vault_key_id": 5,
        "type": "",
        "start_version": None,
        "build_template_id": None,
        "view_id": 1,
        "last_task": {
            "id": 5199,
            "template_id": 44,
            "project_id": 1,
            "status": "success",
            "debug": False,
            "dry_run": False,
            "diff": False,
            "playbook": "",
            "environment": "{}",
            "limit": "",
            "user_id": 1,
            "created": "2025-12-04T07:55:22Z",
            "start": "2025-12-04T07:55:27Z",
            "end": "2025-12-04T07:59:45Z",
            "message": "",
            "commit_hash": None,
            "commit_message": "",
            "build_task_id": None,
            "version": None,
            "arguments": None,
            "tpl_playbook": "inrento-playbook.yml",
            "tpl_alias": "03 update beta app from git",
            "tpl_type": "",
            "user_name": "Justinas",
            "build_task": None
        },
        "autorun": False,
        "survey_vars": None,
        "suppress_success_alerts": False
    }
]

# Real task creation response from POST /api/project/1/tasks
REAL_TASK_CREATION_RESPONSE = {
    "id": 5205,
    "template_id": 44,
    "project_id": 1,
    "status": "waiting",
    "debug": False,
    "dry_run": False,
    "diff": False,
    "playbook": "",
    "environment": "{}",
    "limit": "",
    "user_id": 1,
    "created": "2025-12-04T11:38:43.290584995+02:00",
    "start": None,
    "end": None,
    "message": "",
    "commit_hash": None,
    "commit_message": "",
    "build_task_id": None,
    "version": None,
    "arguments": None
}

# Real task status response from GET /api/project/1/tasks/5205
REAL_TASK_STATUS_RUNNING = {
    "id": 5205,
    "template_id": 44,
    "project_id": 1,
    "status": "running",
    "debug": False,
    "dry_run": False,
    "diff": False,
    "playbook": "",
    "environment": "{}",
    "limit": "",
    "user_id": 1,
    "created": "2025-12-04T09:38:43Z",
    "start": "2025-12-04T09:38:47Z",
    "end": None,
    "message": "",
    "commit_hash": None,
    "commit_message": "",
    "build_task_id": None,
    "version": None,
    "arguments": None
}

REAL_TASK_STATUS_SUCCESS = {
    "id": 1011,
    "template_id": 44,
    "project_id": 1,
    "status": "success",
    "debug": False,
    "dry_run": False,
    "diff": False,
    "playbook": "",
    "environment": "{}",
    "limit": "",
    "user_id": 1,
    "created": "2024-03-25T13:13:12Z",
    "start": "2024-03-25T13:13:12Z",
    "end": "2024-03-25T13:16:18Z",
    "message": "",
    "commit_hash": None,
    "commit_message": "",
    "build_task_id": None,
    "version": None,
    "arguments": None
}

# Real WebSocket messages extracted from the asd file
REAL_WEBSOCKET_MESSAGES = [
    # Task starting
    {
        'end': None,
        'project_id': 1,
        'start': None,
        'status': 'starting',
        'task_id': 1011,
        'template_id': 44,
        'type': 'update',
        'version': None,
        'output': ''
    },

    # Initial log messages
    {
        'output': 'Started: 1011',
        'project_id': 1,
        'task_id': 1011,
        'time': '2024-03-25T13:13:12.518262242+02:00',
        'type': 'log'
    },
    {
        'output': 'Run TaskRunner with template: 03 update beta app from git\n',
        'project_id': 1,
        'task_id': 1011,
        'time': '2024-03-25T13:13:12.518466964+02:00',
        'type': 'log'
    },

    # Status update to running
    {
        'end': None,
        'project_id': 1,
        'start': '2024-03-25T13:13:12.519270403+02:00',
        'status': 'running',
        'task_id': 1011,
        'template_id': 44,
        'type': 'update',
        'version': None,
        'output': ''
    },

    # Task execution logs
    {
        'output': 'Preparing: 1011',
        'project_id': 1,
        'task_id': 1011,
        'time': '2024-03-25T13:13:12.524941948+02:00',
        'type': 'log'
    },
    {
        'output': 'Cloning Repository git@github.com:InRento/ansible.git',
        'project_id': 1,
        'task_id': 1011,
        'time': '2024-03-25T13:13:12.525293792+02:00',
        'type': 'log'
    },
    {
        'output': "Cloning into 'repository_1_44'...",
        'project_id': 1,
        'task_id': 1011,
        'time': '2024-03-25T13:13:12.530122447+02:00',
        'type': 'log'
    },
    {
        'output': "Warning: Permanently added 'github.com' (ED25519) to the list of known hosts.",
        'project_id': 1,
        'task_id': 1011,
        'time': '2024-03-25T13:13:12.80717744+02:00',
        'type': 'log'
    },

    # Ansible playbook execution
    {
        'output': 'PLAY [all] *********************************************************************',
        'project_id': 1,
        'task_id': 1011,
        'time': '2024-03-25T13:13:30.580162177+02:00',
        'type': 'log'
    },
    {
        'output': 'TASK [Gathering Facts] *********************************************************',
        'project_id': 1,
        'task_id': 1011,
        'time': '2024-03-25T13:13:30.611275651+02:00',
        'type': 'log'
    },
    {
        'output': 'ok: [beta_php_worker]',
        'project_id': 1,
        'task_id': 1011,
        'time': '2024-03-25T13:13:32.83856509+02:00',
        'type': 'log'
    },
    {
        'output': 'ok: [beta_host]',
        'project_id': 1,
        'task_id': 1011,
        'time': '2024-03-25T13:13:33.066688287+02:00',
        'type': 'log'
    },

    # Task completion logs
    {
        'output': 'PLAY RECAP *********************************************************************',
        'project_id': 1,
        'task_id': 1011,
        'time': '2024-03-25T13:16:18.444132596+02:00',
        'type': 'log'
    },
    {
        'output': 'beta_host                  : ok=31   changed=13   unreachable=0    failed=0    skipped=2    rescued=0    ignored=0   ',
        'project_id': 1,
        'task_id': 1011,
        'time': '2024-03-25T13:16:18.444184496+02:00',
        'type': 'log'
    },
    {
        'output': 'beta_php_worker            : ok=20   changed=7    unreachable=0    failed=0    skipped=9    rescued=0    ignored=0   ',
        'project_id': 1,
        'task_id': 1011,
        'time': '2024-03-25T13:16:18.444241207+02:00',
        'type': 'log'
    },

    # Final success update
    {
        'end': None,
        'project_id': 1,
        'start': '2024-03-25T13:13:12.519270403+02:00',
        'status': 'success',
        'task_id': 1011,
        'template_id': 44,
        'type': 'update',
        'version': None,
        'output': ''
    }
]

# WebSocket messages for error scenarios
WEBSOCKET_ERROR_MESSAGES = [
    # Task failing
    {
        'end': None,
        'project_id': 1,
        'start': '2024-03-25T13:13:12.519270403+02:00',
        'status': 'error',
        'task_id': 1011,
        'template_id': 44,
        'type': 'update',
        'version': None,
        'output': ''
    }
]

# Different task ID messages for testing filtering
WEBSOCKET_DIFFERENT_TASK_MESSAGES = [
    {
        'output': 'Different task log',
        'project_id': 1,
        'task_id': 9999,  # Different task ID
        'time': '2024-03-25T13:13:12.518262242+02:00',
        'type': 'log'
    }
]

# API Exception simulation data
API_EXCEPTION_RESPONSE = {
    "error": "Template not found",
    "status": 404,
    "message": "Template with ID 999 does not exist"
}

# Test environment configurations
TEST_ENV_CONFIGS = {
    'valid': {
        'INPUT_API_KEY': 'test_api_key_12345',
        'INPUT_API_URL': 'http://test-api.example.com:3000/api',
        'INPUT_WS_API_URL': 'ws://test-api.example.com:3000/api',
        'INPUT_PROJECT_ID': '1',
        'INPUT_MYINPUT': '44',
        'GITHUB_OUTPUT': '/tmp/test_github_output'
    },
    'world_input': {
        'INPUT_API_KEY': 'test_api_key_12345',
        'INPUT_API_URL': 'http://test-api.example.com:3000/api',
        'INPUT_WS_API_URL': 'ws://test-api.example.com:3000/api',
        'INPUT_PROJECT_ID': '1',
        'INPUT_MYINPUT': 'world',
        'GITHUB_OUTPUT': '/tmp/test_github_output'
    },
    'missing_api_key': {
        'INPUT_API_URL': 'http://test-api.example.com:3000/api',
        'INPUT_WS_API_URL': 'ws://test-api.example.com:3000/api',
        'INPUT_PROJECT_ID': '1',
        'INPUT_MYINPUT': '44',
        'GITHUB_OUTPUT': '/tmp/test_github_output'
    }
}

# Expected output patterns for testing
EXPECTED_OUTPUT_PATTERNS = {
    'world_greeting': 'Hello world',
    'template_greeting': 'Hello 44',
    'task_starting': 'starting',
    'task_running': 'running',
    'task_success': 'success',
    'task_error': 'error'
}
