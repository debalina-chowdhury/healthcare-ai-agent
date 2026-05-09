def test_tools_defined():
    """Test that all required tools are defined"""
    from app import tools
    tool_names = [t["name"] for t in tools]
    assert "search_patient_records" in tool_names
    assert "check_insurance" in tool_names
    assert "schedule_appointment" in tool_names

def test_execute_tool_records():
    """Test tool execution returns expected format"""
    from app import execute_tool
    result = execute_tool("search_patient_records", {"patient_id": "P001"})
    assert "P001" in result
    assert "appointment" in result.lower()

def test_execute_tool_insurance():
    """Test insurance tool returns active status"""
    from app import execute_tool
    result = execute_tool("check_insurance", {"patient_id": "P001"})
    assert "P001" in result
    assert "active" in result.lower()