import pytest

from database.database import (
    get_connection,
    create_message,
    delete_message,
    get_messages,
    update_message,
)


def test_get_connection():
    """Verify that the application can connect to PostgreSQL."""

    connection = get_connection()
    try:
        assert connection is not None
        assert not connection.closed
    finally:
        connection.close()
    assert connection.closed


def test_create_message():
    """Verify that a message can be created."""

    message = "Test create message"
    message_id = create_message(message)
    assert message_id is not None
    assert isinstance(message_id, int)

    # Cleanup
    delete_message(message_id)


def test_get_messages():
    """Verify that messages can be retrieved."""

    message = "Test get message"
    message_id = create_message(message)
    try:
        messages = get_messages()
        assert isinstance(messages, list)
        assert any(
            row_id == message_id and row_message == message
            for row_id, row_message in messages
        )
    finally:
        delete_message(message_id)


def test_create_and_get_message():
    """Verify the complete CREATE -> READ flow."""

    message = "Hello from automated test"
    message_id = create_message(message)
    try:
        messages = get_messages()
        matching_messages = [row for row in messages if row[0] == message_id]
        assert len(matching_messages) == 1
        returned_id, returned_message = matching_messages[0]
        assert returned_id == message_id
        assert returned_message == message

    finally:
        delete_message(message_id)


def test_create_multiple_messages():
    """Verify that multiple messages can be stored."""

    messages_to_create = ["Test message 1", "Test message 2", "Test message 3"]
    message_ids = []
    try:
        for message in messages_to_create:
            message_id = create_message(message)
            message_ids.append(message_id)
        messages = get_messages()
        returned_messages = {message_id: message for message_id, message in messages}
        for message_id, expected_message in zip(message_ids, messages_to_create):
            assert returned_messages[message_id] == expected_message
    finally:
        for message_id in message_ids:
            delete_message(message_id)


def test_update_message():
    """Verify that an existing message can be updated."""

    original_message = "Original message"
    updated_message = "Updated message"
    message_id = create_message(original_message)
    try:
        result = update_message(message_id, updated_message)
        assert result is True
        messages = get_messages()
        matching_messages = [row for row in messages if row[0] == message_id]
        assert len(matching_messages) == 1
        returned_id, returned_message = matching_messages[0]
        assert returned_id == message_id
        assert returned_message == updated_message
    finally:
        delete_message(message_id)


def test_update_nonexistent_message():
    """Verify that updating a non-existent message returns False."""

    result = update_message(999999999, "This should not exist")
    assert result is False


def test_delete_message():
    """Verify that an existing message can be deleted."""

    message_id = create_message("Message to delete")
    result = delete_message(message_id)
    assert result is True
    messages = get_messages()
    assert not any(row_id == message_id for row_id, _ in messages)


def test_delete_nonexistent_message():
    """Verify that deleting a non-existent message returns False."""

    result = delete_message(999999999)
    assert result is False
