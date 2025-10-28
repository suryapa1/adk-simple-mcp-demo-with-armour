"""
Model Armor Plugin for ADK Multi-Agent System

This plugin integrates Google Cloud Model Armor to provide runtime security
for AI agents, protecting against prompt injection, jailbreaks, PII leaks,
and harmful content.

Usage:
    from plugins.model_armor_plugin import ModelArmorPlugin
    
    plugin = ModelArmorPlugin(
        project_id="your-project-id",
        block_threshold=0.7,
    )
    
    agent = LlmAgent(
        name="my_agent",
        model="gemini-2.0-flash-exp",
        before_model_callback=plugin.before_model_callback,
        after_model_callback=plugin.after_model_callback,
    )
"""

from google.adk.plugins import Plugin
from google.adk.core import CallbackContext
from typing import Optional, Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelArmorPlugin(Plugin):
    """
    Plugin that uses Google Cloud Model Armor to screen
    user inputs and agent outputs for security threats.
    """
    
    def __init__(
        self,
        project_id: str,
        location: str = "global",
        block_threshold: float = 0.7,
        check_input: bool = True,
        check_output: bool = True,
        check_tool_calls: bool = False,
        dry_run: bool = False,
    ):
        """
        Initialize Model Armor Plugin
        
        Args:
            project_id: GCP project ID
            location: Model Armor location (default: "global")
            block_threshold: Confidence threshold to block (0.0-1.0)
            check_input: Screen user inputs
            check_output: Screen agent outputs
            check_tool_calls: Screen tool inputs/outputs
            dry_run: If True, log violations but don't block
        """
        super().__init__()
        self.project_id = project_id
        self.location = location
        self.block_threshold = block_threshold
        self.check_input = check_input
        self.check_output = check_output
        self.check_tool_calls = check_tool_calls
        self.dry_run = dry_run
        
        # Initialize Model Armor client (lazy loading)
        self._client = None
        self.parent = f"projects/{project_id}/locations/{location}"
        
        logger.info(
            f"Model Armor Plugin initialized: "
            f"project={project_id}, threshold={block_threshold}, "
            f"check_input={check_input}, check_output={check_output}, "
            f"dry_run={dry_run}"
        )
    
    @property
    def client(self):
        """Lazy load Model Armor client"""
        if self._client is None:
            try:
                from google.cloud import modelarmor_v1
                self._client = modelarmor_v1.ModelArmorServiceClient()
                logger.info("Model Armor client initialized successfully")
            except ImportError:
                logger.error(
                    "google-cloud-modelarmor not installed. "
                    "Install with: pip install google-cloud-modelarmor"
                )
                raise
            except Exception as e:
                logger.error(f"Failed to initialize Model Armor client: {e}")
                raise
        return self._client
    
    def _screen_content(
        self,
        content: str,
        context: str = "input"
    ) -> Dict[str, Any]:
        """
        Screen content using Model Armor API
        
        Args:
            content: Text content to screen
            context: Context label for logging (input/output/tool)
        
        Returns:
            dict with 'safe' (bool), 'violations' (list), and metadata
        """
        try:
            from google.cloud import modelarmor_v1
            
            # Create screening request
            request = modelarmor_v1.ScreenContentRequest(
                parent=self.parent,
                content=content,
                # Enable all threat categories
                threat_categories=[
                    "PROMPT_INJECTION",
                    "JAILBREAK",
                    "SENSITIVE_DATA_LEAK",
                    "HARMFUL_CONTENT",
                    "MALWARE",
                ],
            )
            
            # Call Model Armor API
            response = self.client.screen_content(request=request)
            
            # Check if any violations exceed threshold
            violations = []
            max_confidence = 0.0
            
            for detection in response.detections:
                if detection.confidence >= self.block_threshold:
                    violations.append({
                        "category": detection.category,
                        "confidence": detection.confidence,
                        "description": detection.description,
                    })
                    max_confidence = max(max_confidence, detection.confidence)
            
            is_safe = len(violations) == 0
            
            # Log results
            if not is_safe:
                logger.warning(
                    f"🛡️ Model Armor detected threats in {context}: "
                    f"{[v['category'] for v in violations]} "
                    f"(max confidence: {max_confidence:.2f})"
                )
            else:
                logger.debug(f"✅ Model Armor: {context} is safe")
            
            return {
                "safe": is_safe,
                "violations": violations,
                "max_confidence": max_confidence,
                "context": context,
            }
            
        except Exception as e:
            # Log error but don't block on API failures (fail open)
            logger.error(f"Model Armor API error: {e}")
            return {
                "safe": True,
                "violations": [],
                "error": str(e),
                "context": context,
            }
    
    async def before_model_callback(
        self,
        callback_context: CallbackContext,
        messages: List[Dict[str, Any]],
    ) -> Optional[str]:
        """
        Screen user input before sending to model
        
        Args:
            callback_context: ADK callback context
            messages: List of conversation messages
        
        Returns:
            String to block request, or None to allow
        """
        if not self.check_input:
            return None
        
        # Get the last user message
        if not messages:
            return None
        
        user_message = messages[-1].get("content", "")
        if not user_message:
            return None
        
        # Screen with Model Armor
        result = self._screen_content(user_message, context="user_input")
        
        if not result["safe"]:
            violations_str = ", ".join([v["category"] for v in result["violations"]])
            
            if self.dry_run:
                logger.warning(
                    f"[DRY RUN] Would block input: {violations_str}"
                )
                return None  # Don't actually block in dry run mode
            
            logger.warning(f"🛡️ Blocking input: {violations_str}")
            
            # Return safe response to user
            return (
                "I apologize, but I cannot process that request as it may "
                "contain unsafe content. Please rephrase your question or "
                "contact our support team for assistance."
            )
        
        return None  # Allow the request to proceed
    
    async def after_model_callback(
        self,
        callback_context: CallbackContext,
        response: str,
    ) -> Optional[str]:
        """
        Screen agent output before returning to user
        
        Args:
            callback_context: ADK callback context
            response: Agent's response text
        
        Returns:
            String to replace response, or None to allow
        """
        if not self.check_output:
            return None
        
        if not response:
            return None
        
        # Screen with Model Armor
        result = self._screen_content(response, context="agent_output")
        
        if not result["safe"]:
            violations_str = ", ".join([v["category"] for v in result["violations"]])
            
            if self.dry_run:
                logger.warning(
                    f"[DRY RUN] Would block output: {violations_str}"
                )
                return None  # Don't actually block in dry run mode
            
            logger.warning(f"🛡️ Blocking output: {violations_str}")
            
            # Return safe alternative response
            return (
                "I apologize, but I cannot provide that information at this time. "
                "Please contact our support team for further assistance."
            )
        
        return None  # Allow the response to proceed
    
    async def before_tool_callback(
        self,
        callback_context: CallbackContext,
        tool: Any,
        args: Dict[str, Any],
        tool_context: Any,
    ) -> Optional[Dict]:
        """
        Screen tool inputs before execution (optional)
        
        Args:
            callback_context: ADK callback context
            tool: Tool being called
            args: Tool arguments
            tool_context: Tool context
        
        Returns:
            Dict to block tool call, or None to allow
        """
        if not self.check_tool_calls:
            return None
        
        # Screen tool arguments
        args_str = str(args)
        result = self._screen_content(args_str, context="tool_input")
        
        if not result["safe"]:
            violations_str = ", ".join([v["category"] for v in result["violations"]])
            
            if self.dry_run:
                logger.warning(
                    f"[DRY RUN] Would block tool call to {tool.name}: {violations_str}"
                )
                return None  # Don't actually block in dry run mode
            
            logger.warning(f"🛡️ Blocking tool call to {tool.name}: {violations_str}")
            
            return {
                "error": "Tool call blocked by security policy",
                "details": violations_str,
            }
        
        return None  # Allow tool execution

