import os
import pickle
from typing import Any, ClassVar, Tuple, Type
from zenml.enums import ArtifactType
from zenml.environment import Environment
from zenml.io import fileio
from zenml.logger import get_logger
from zenml.materializers.base_materializer import BaseMaterializer
from zenml.utils.io_utils import (
    read_file_contents_as_string,
    write_file_contents_as_string,
)

logger = get_logger(__name__)

DEFAULT_FILENAME = "agent_executor.pkl"
DEFAULT_PYTHON_VERSION_FILENAME = "python_version.txt"

class AgentExecutorMaterializer(BaseMaterializer):
    """AWS-compatible Agent Executor Materializer.

    This materializer saves and loads agent executors (e.g., LangGraph or LangChain)
    using pickle serialization. It works across both local and AWS S3 artifact stores
    managed by ZenML.
    """

    ASSOCIATED_TYPES: ClassVar[Tuple[Type[Any], ...]] = (object,)
    ASSOCIATED_ARTIFACT_TYPE: ClassVar[ArtifactType] = ArtifactType.DATA
    SKIP_REGISTRATION: ClassVar[bool] = True

    def load(self, data_type: Type[Any]) -> Any:
        """Load serialized agent executor from pickle file."""
        source_python_version = self._load_python_version()
        current_python_version = Environment().python_version()

        if source_python_version != current_python_version:
            logger.warning(
                f"⚠️ Python version mismatch: stored='{source_python_version}', current='{current_python_version}'."
                " Deserialization may cause unexpected behavior."
            )

        filepath = os.path.join(self.uri, DEFAULT_FILENAME)
        with fileio.open(filepath, "rb") as fid:
            data = pickle.load(fid)
        logger.info("✅ Agent executor successfully loaded from storage.")
        return data

    def save(self, data: Any) -> None:
        """Save agent executor to pickle file."""
        self._save_python_version()
        filepath = os.path.join(self.uri, DEFAULT_FILENAME)
        with fileio.open(filepath, "wb") as fid:
            pickle.dump(data, fid)
        logger.info("✅ Agent executor successfully saved to storage.")

    def _save_python_version(self) -> None:
        filepath = os.path.join(self.uri, DEFAULT_PYTHON_VERSION_FILENAME)
        write_file_contents_as_string(filepath, Environment().python_version())

    def _load_python_version(self) -> str:
        filepath = os.path.join(self.uri, DEFAULT_PYTHON_VERSION_FILENAME)
        if os.path.exists(filepath):
            return read_file_contents_as_string(filepath)
        return "unknown"
