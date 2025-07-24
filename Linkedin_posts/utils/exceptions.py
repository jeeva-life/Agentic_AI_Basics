class WorkflowException(Exception):
    """Base exception for workflow-related errors"""
    pass

class TranscriptExtractionError(WorkflowException):
    """Exception raised when transcript extraction fails"""
    pass

class TitleGenerationError(WorkflowException):
    """Exception raised when title generation fails"""
    pass

class ContentGenerationError(WorkflowException):
    """Exception raised when content generation fails"""
    pass

class ValidationError(WorkflowException):
    """Exception raised when input validation fails"""
    pass

class ConfigurationError(WorkflowException):
    """Exception raised when configuration is invalid"""
    pass 