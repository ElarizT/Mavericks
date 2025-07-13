from typing import List, Optional, Union

from pydantic import BaseModel, Field
from src.schemas.api.agent.dto import MLAgentSchema
from src.schemas.api.flow.schemas import FlowSchema


class AgentAndFlowsDTO(BaseModel):
    agents: Optional[List[Union[MLAgentSchema, FlowSchema]]] = Field(default=[])
