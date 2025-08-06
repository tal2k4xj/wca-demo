def format_timestamp(timestamp: str) -> str:
    """Format a timestamp string to a more readable format."""
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except ValueError as e:
        return timestamp  # Return original if parsing fails
