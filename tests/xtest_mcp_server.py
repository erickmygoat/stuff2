import json
import pytest
import pytest_asyncio
from unittest.mock import patch, MagicMock
from core_agent.files_dict import FilesDict
from mcp_servers.my_son_server.server import app
from arcade_mcp_server.server import MCPServer
from arcade_mcp_server.types import CallToolRequest

@pytest.fixture
def mcp_settings():
    from arcade_mcp_server.settings import MCPSettings
    settings = MCPSettings()
    settings.debug = True
    settings.middleware.enable_logging = False
    settings.middleware.mask_error_details = False
    return settings

@pytest_asyncio.fixture
async def mcp_server(mcp_settings):
    server = MCPServer(
        catalog=app._catalog,
        name="test_server",
        version="1.0.0",
        settings=mcp_settings,
    )
    await server.start()
    yield server
    await server.stop()

@pytest.mark.asyncio
async def test_get_status(mcp_server):
    """Tests the get_status tool."""
    message = CallToolRequest(
        jsonrpc="2.0",
        id=1,
        method="tools/call",
        params={"name": "MySonServer.GetStatus", "arguments": {}},
    )
    response = await mcp_server._handle_call_tool(message)
    assert "Online and operational" in response.result.structuredContent["result"]

@pytest.mark.asyncio
@patch('mcp_servers.my_son_server.server.SystemMonitor')
async def test_system_snapshot(mock_monitor, mcp_server):
    """Tests the system_snapshot tool."""
    mock_monitor.return_value.get_snapshot.return_value = {"cpu": 50}
    message = CallToolRequest(
        jsonrpc="2.0",
        id=1,
        method="tools/call",
        params={"name": "MySonServer.SystemSnapshot", "arguments": {}},
    )
    response = await mcp_server._handle_call_tool(message)
    assert response.result.structuredContent["result"] == '{"cpu": 50}'

@pytest.mark.asyncio
@patch('mcp_servers.my_son_server.server.GptEngineerPromptGenerator')
@patch('mcp_servers.my_son_server.server.BaseMemory')
@patch('mcp_servers.my_son_server.server.AI')
@patch('core_agent.engineering.gpt_engineer.gen_code')
async def test_generate_code(mock_gen_code, mock_ai, mock_memory, mock_prompt_generator, mcp_server):
    """Tests the generate_code tool."""
    mock_gen_code.return_value = FilesDict({"main.py": "print('Hello, World!')"})
    message = CallToolRequest(
        jsonrpc="2.0",
        id=1,
        method="tools/call",
        params={"name": "MySonServer.GenerateCode", "arguments": {"prompt": "Create a hello world program."}},
    )
    response = await mcp_server._handle_call_tool(message)
    result_dict = json.loads(response.result.structuredContent["result"])
    assert "main.py" in result_dict
    assert result_dict["main.py"] == "print('Hello, World!')"

@pytest.mark.asyncio
@patch('mcp_servers.my_son_server.server.GptEngineerPromptGenerator')
@patch('mcp_servers.my_son_server.server.BaseMemory')
@patch('mcp_servers.my_son_server.server.AI')
@patch('core_agent.engineering.gpt_engineer.improve_fn')
async def test_improve_code(mock_improve_fn, mock_ai, mock_memory, mock_prompt_generator, mcp_server):
    """Tests the improve_code tool."""
    mock_improve_fn.return_value = FilesDict({"main.py": "print('Hello, Jules!')"})
    message = CallToolRequest(
        jsonrpc="2.0",
        id=1,
        method="tools/call",
        params={"name": "MySonServer.ImproveCode", "arguments": {"prompt": "Change the name to Jules.", "files": '{"main.py": "print(\'Hello, World!\')"}'}},
    )
    response = await mcp_server._handle_call_tool(message)
    result_dict = json.loads(response.result.structuredContent["result"])
    assert "main.py" in result_dict
    assert result_dict["main.py"] == "print('Hello, Jules!')"
