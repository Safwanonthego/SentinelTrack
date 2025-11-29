from pydantic import BaseModel, field_validator, model_validator, Field
from typing import Annotated, Optional, Any

# Pre-Defined Choices List
SEVERITY_CHOICES = {"Low", "Medium", "High","Critical"}
STATUS_CHOICES = {"Open", "Fixed", "Accepted","False Positive"}

# Vulnerability Class As Pydantic Model
class Vulnerability(BaseModel):
    id: Optional[int] = None
    title: Annotated[str, Field(strip_whitespace=True, min_length=1)] # Trim WhiteSpace & Min Length 1
    asset: Annotated[str, Field(strip_whitespace=True, min_length=1)]
    severity: str = "Low" # Default = Low
    status: str = "Open"  # Default = Open
    description: str = ""
    steps: str = ""
    mitigation: str = ""

#   Checks If The Given Severity & Status Val Is Valid Or Not
#   Mode = Before Gives The Raw Data To Validator 
#       If Good Then Gives To The Pydantic's Validation Chain 

    @model_validator(mode='before')
    @classmethod
    def normalize_raw_data(cls, data: Any) -> Any:

        if not isinstance(data, dict):
            return data

        def normalize_string(key: str, data: dict):
             if key in data and isinstance(data[key], str):
                 data[key] = data[key].title().strip()
        
        normalize_string("title", data)
        normalize_string("asset", data)
        normalize_string("description", data)
        normalize_string("steps", data)
        normalize_string("mitigation", data)
        normalize_string("severity", data)
        normalize_string("status", data)

        return data


    @field_validator("severity", mode='after')
    @classmethod
    def validate_severity(cls, val):
        
        if val not in SEVERITY_CHOICES:
            raise ValueError(f"Severity Must Be One Of {', '.join(SEVERITY_CHOICES)}")
        return val


    @field_validator("status", mode='after')
    @classmethod
    def validate_status(cls, val):
  
        if val not in STATUS_CHOICES:
            raise ValueError(f"Status Must Be One Of {STATUS_CHOICES}")
        return val








