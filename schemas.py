from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class CandidateProfile(BaseModel):
    full_name: Optional[str] = Field(None, description="The full name of the candidate")
    email: Optional[EmailStr] = Field(None, description="A valid email address for contact")
    phone: Optional[str] = Field(None, description="Phone number. Formats can vary.")
    years_experience: Optional[int] = Field(None, description="Total years of professional experience")
    desired_roles: Optional[List[str]] = Field(default_factory=list, description="Target positions or titles")
    location: Optional[str] = Field(None, description="Current city or equivalent location string")
    tech_stack: Optional[List[str]] = Field(default_factory=list, description="Array of technical skills, languages, or tools")

    def is_complete(self) -> bool:
        """Helper to quickly evaluate if all required fields are present."""
        return all([
            self.full_name, 
            self.email, 
            self.phone, 
            self.years_experience is not None, 
            bool(self.desired_roles), 
            self.location, 
            bool(self.tech_stack)
        ])
