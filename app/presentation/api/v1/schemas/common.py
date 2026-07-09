from pydantic import BaseModel, Field, ConfigDict


class FilterParams(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    offset: int = Field(gt=0)
    limit: int = Field(lt=200, gt=0)