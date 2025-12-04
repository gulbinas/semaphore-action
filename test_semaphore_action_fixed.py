#!/usr/bin/env python3
"""
Comprehensive Unit Tests for Semaphore GitHub Action
Tests all functionality using real API response data
"""

import asyncio
import json
import os
import pytest
import tempfile
from unittest.mock import Mock, patch, AsyncMock, MagicMock, mock_open
import re

# Test environment setup
TEST_ENV = {
    'INPUT_API_KEY': 'test_api_key_12345',
    'INPUT_API_URL': 'http://test-api.example.com:3000/api',
    'INPUT_WS_API_URL': 'ws://test-api.example.com:3000/api',
    'INPUT_PROJECT_ID': '1',
    'INPUT_MYINPUT': '44',
    'GITHUB_OUTPUT': '/tmp/test_github_output'
}

@pytest.fixture
def mock_env():
    """Fixture to provide test environment"""
    with patch.dict(os.environ, TEST_ENV):
        yield

@pytest.fixture
def temp_output_file():
    """Fixture to provide temporary GITHUB_OUTPUT file"""
    temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
    temp_file.close()
    with patch.dict(os.environ, {'GITHUB_OUTPUT': temp_file.name}):
        yield temp_file.name
    try:
        os.unlink(temp_file.name)
    except FileNotFoundError:
        pass

def get_real_task_creation_response():
    """Returns real API response for task creation based on actual curl output"""
    return {
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

def get_real_websocket_messages():
    """Returns real WebSocket messages from the asd file"""
    return [
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
        {
            'output': 'Started: 1011',
            'project_id': 1,
            'task_id': 1011,
            'time': '2024-03-25T13:13:12.518262242+02:00',
            'type': 'log'
        },
        {
            'output': 'Preparing: 1011',
            'project_id': 1,
            'task_id': 1011,
            'time': '2024-03-25T13:13:12.524941948+02:00',
            'type': 'log'
        },
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

def test_github_action_output_writing(mock_env, temp_output_file):
    """Test GitHub Action output writing functionality"""
    # Import after environment is set
    import main
    
    # Test writing output
    main.set_github_action_output('testOutput', 'testValue')
    
    # Read and verify the output file
    with open(temp_output_file, 'r') as f:
        content = f.read()
    
    assert content == 'testOutput=testValue'

def test_ansi_escape_regex(mock_env):
    """Test ANSI escape sequence removal"""
    import main
    
    test_string = '\x1B[31mRed Text\x1B[0m Normal Text'
    cleaned = main.ansi_escape.sub('', test_string)
    assert cleaned == 'Red Text Normal Text'

def test_print_hi_function(mock_env):
    """Test the print_hi utility function"""
    import main
    
    with patch('builtins.print') as mock_print:
        main.print_hi('Test')
        mock_print.assert_called_with('Hi, Test')

@patch('semaphore_client.ApiClient')
@patch('main.project_api.ProjectApi')
def test_start_task_success(mock_project_api, mock_api_client, mock_env):
    """Test successful task creation"""
    import main
    from semaphore_client.model.project_project_id_tasks_get_request import ProjectProjectIdTasksGetRequest
    
    # Setup mocks
    mock_api_instance = Mock()
    mock_project_api.return_value = mock_api_instance
    mock_api_instance.project_project_id_tasks_post.return_value = get_real_task_creation_response()
    
    # Test task creation
    task_id = main.start_task(44, 1)
    
    # Verify the API was called correctly
    mock_api_instance.project_project_id_tasks_post.assert_called_once()
    call_args = mock_api_instance.project_project_id_tasks_post.call_args
    
    # Verify project_id
    assert call_args[0][0] == 1
    
    # Verify task request object
    task_request = call_args[0][1]
    assert isinstance(task_request, ProjectProjectIdTasksGetRequest)
    assert task_request.template_id == 44
    assert task_request.debug == False
    assert task_request.dry_run == False
    assert task_request.environment == "{}"
    
    # Verify returned task ID
    assert task_id == 5205

@patch('semaphore_client.ApiClient')
@patch('main.project_api.ProjectApi')  
def test_start_task_api_exception(mock_project_api, mock_api_client, mock_env):
    """Test task creation with API exception"""
    import main
    import semaphore_client
    
    # Setup mocks to raise exception
    mock_api_instance = Mock()
    mock_project_api.return_value = mock_api_instance
    mock_api_instance.project_project_id_tasks_post.side_effect = semaphore_client.ApiException("API Error")
    
    with patch('builtins.print') as mock_print:
        task_id = main.start_task(44, 1)
        
        # Verify error handling
        assert task_id is None
        # Check that print was called with error message containing expected strings
        assert mock_print.called
        error_msg = mock_print.call_args[0][0]
        assert "Exception when calling ProjectApi->project_project_id_tasks_post" in error_msg
        assert "API Error" in error_msg

@patch('websockets.connect')
@patch('main.set_github_action_output')
@pytest.mark.asyncio
async def test_websocket_polling_success(mock_set_output, mock_websocket_connect, mock_env):
    """Test WebSocket polling for task updates with successful completion"""
    import main
    
    # Setup WebSocket mock
    mock_websocket = AsyncMock()
    mock_websocket_connect.return_value.__aenter__.return_value = mock_websocket
    
    # Simulate receiving messages
    real_messages = get_real_websocket_messages()
    message_queue = [json.dumps(msg) for msg in real_messages]
    mock_websocket.recv.side_effect = message_queue
    
    # Setup API instance mock
    mock_api_instance = Mock()
    mock_task_response = Mock()
    mock_task_response.to_dict.return_value = {'status': 'success', 'task_id': 1011}
    mock_api_instance.project_project_id_tasks_task_id_get.return_value = mock_task_response
    
    # Run the test
    await main.poll_task_updates(1011, mock_api_instance, 1)
    
    # Verify WebSocket connection
    mock_websocket_connect.assert_called_once_with(
        'ws://test-api.example.com:3000/api/ws',
        extra_headers={"Authorization": "Bearer test_api_key_12345"}
    )
    
    # Verify output was set at least once
    assert mock_set_output.call_count >= 1

@patch('websockets.connect')
@pytest.mark.asyncio
async def test_websocket_connection_closed(mock_websocket_connect, mock_env):
    """Test WebSocket polling with connection closed"""
    import main
    from websockets import ConnectionClosed
    
    # Setup WebSocket mock to raise ConnectionClosed
    mock_websocket = AsyncMock()
    mock_websocket_connect.return_value.__aenter__.return_value = mock_websocket
    mock_websocket.recv.side_effect = ConnectionClosed(None, None)
    
    # Setup API instance mock
    mock_api_instance = Mock()
    
    # Run the test - should not raise exception
    await main.pool_task_updates(1011, mock_api_instance, 1)
    
    # Verify WebSocket connection was attempted
    mock_websocket_connect.assert_called_once()

@patch('main.start_task')
@patch('main.set_github_action_output')
def test_main_function_world_input(mock_set_output, mock_start_task, mock_env):
    """Test main function with 'world' input"""
    import main
    
    with patch.dict(os.environ, {'INPUT_MYINPUT': 'world'}):
        result = main.main()
        
        # Verify early return for 'world'
        assert result == 0
        mock_set_output.assert_called_with('myOutput', 'Hello world')
        mock_start_task.assert_not_called()

@patch('main.start_task')
@patch('main.set_github_action_output')
@patch('main.pool_task_updates')
@patch('semaphore_client.ApiClient')
@patch('main.project_api.ProjectApi')
def test_main_function_template_execution(mock_project_api, mock_api_client, mock_pool_updates, mock_set_output, mock_start_task, mock_env):
    """Test main function with template ID input"""
    import main
    
    with patch.dict(os.environ, {'INPUT_MYINPUT': '44', 'INPUT_PROJECT_ID': '1'}):
        # Setup mocks
        mock_start_task.return_value = 5205
        mock_api_instance = Mock()
        mock_project_api.return_value = mock_api_instance
        
        main.main()
        
        # Verify task creation
        mock_start_task.assert_called_with(44, 1)
        mock_set_output.assert_called_with('myOutput', 'Hello 44')
        
        # Verify WebSocket polling
        mock_pool_updates.assert_called_once_with(5205, mock_api_instance, 1)

def test_configuration_setup(mock_env):
    """Test Semaphore client configuration"""
    import main
    
    # Verify environment variables are read correctly
    assert main.API_KEY == 'test_api_key_12345'
    assert main.API_URL == 'http://test-api.example.com:3000/api'
    assert main.WS_API_URL == 'ws://test-api.example.com:3000/api'
    
    # Verify configuration object
    config = main.configuration
    assert config.host == 'http://test-api.example.com:3000/api'
    assert config.api_key['bearer'] == 'test_api_key_12345'
    assert config.api_key_prefix['bearer'] == 'Bearer'

def test_multiple_github_outputs(mock_env, temp_output_file):
    """Test multiple GitHub output writes accumulate properly"""
    import main
    
    # Test writing multiple outputs
    main.set_github_action_output('output1', 'value1')
    main.set_github_action_output('output2', 'value2')
    
    # Read and verify the output file
    with open(temp_output_file, 'r') as f:
        content = f.read()
    
    assert 'output1=value1' in content
    assert 'output2=value2' in content

def test_real_api_data_consistency():
    """Test that our test data is consistent with real API responses"""
    task_response = get_real_task_creation_response()
    websocket_messages = get_real_websocket_messages()
    
    # Verify task response structure
    assert 'id' in task_response
    assert 'template_id' in task_response
    assert 'status' in task_response
    assert task_response['template_id'] == 44
    
    # Verify websocket messages have correct structure
    for msg in websocket_messages:
        if msg.get('type') == 'log':
            assert 'output' in msg
            assert 'task_id' in msg
        elif msg.get('type') == 'update':
            assert 'status' in msg
            assert 'task_id' in msg

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
