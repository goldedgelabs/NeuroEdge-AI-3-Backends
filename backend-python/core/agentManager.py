# backend-python/core/agentManager.py

from .dbManager import db
from .eventBus import eventBus
from .logger import logger

# --- import all 71 agents ---
from ..agents.ARVAgent import ARVAgent
from ..agents.AnalyticsAgent import AnalyticsAgent
from ..agents.AntiTheftAgent import AntiTheftAgent
from ..agents.AutoUpdateAgent import AutoUpdateAgent
from ..agents.BackupAgent import BackupAgent
from ..agents.BillingAgent import BillingAgent
from ..agents.CollaborationAgent import CollaborationAgent
from ..agents.ComplianceAgent import ComplianceAgent
from ..agents.ContentModerationAgent import ContentModerationAgent
from ..agents.ConversationAgent import ConversationAgent
from ..agents.CorrectionAgent import CorrectionAgent
from ..agents.CreativityAgent import CreativityAgent
from ..agents.CriticAgent import CriticAgent
from ..agents.DataIngestAgent import DataIngestAgent
from ..agents.DataProcessingAgent import DataProcessingAgent
from ..agents.DecisionAgent import DecisionAgent
from ..agents.DeploymentAgent import DeploymentAgent
from ..agents.DeviceProtectionAgent import DeviceProtectionAgent
from ..agents.DiscoveryAgent import DiscoveryAgent
from ..agents.DistributedTaskAgent import DistributedTaskAgent
from ..agents.DoctrineAgent import DoctrineAgent
from ..agents.EncryptionAgent import EncryptionAgent
from ..agents.EvolutionAgent import EvolutionAgent
from ..agents.FeedbackAgent import FeedbackAgent
from ..agents.FounderAgent import FounderAgent
from ..agents.GPIAgent import GPIAgent
from ..agents.GlobalMedAgent import GlobalMedAgent
from ..agents.GoldEdgeIntegrationAgent import GoldEdgeIntegrationAgent
from ..agents.HealthMonitoringAgent import HealthMonitoringAgent
from ..agents.HotReloadAgent import HotReloadAgent
from ..agents.IdentityAgent import IdentityAgent
from ..agents.InspectionAgent import InspectionAgent
from ..agents.LearningAgent import LearningAgent
from ..agents.LoadBalancingAgent import LoadBalancingAgent
from ..agents.LocalStorageAgent import LocalStorageAgent
from ..agents.MarketAssessmentAgent import MarketAssessmentAgent
from ..agents.MetricsAgent import MetricsAgent
from ..agents.MonitoringAgent import MonitoringAgent
from ..agents.NotificationAgent import NotificationAgent
from ..agents.OfflineAgent import OfflineAgent
from ..agents.OrchestrationAgent import OrchestrationAgent
from ..agents.PersonalAgent import PersonalAgent
from ..agents.PhoneSecurityAgent import PhoneSecurityAgent
from ..agents.PlannerAgent import PlannerAgent
from ..agents.PlannerHelperAgent import PlannerHelperAgent
from ..agents.PluginManagerAgent import PluginManagerAgent
from ..agents.PredictionAgent import PredictionAgent
from ..agents.PredictiveAgent import PredictiveAgent
from ..agents.RecommendationAgent import RecommendationAgent
from ..agents.RecoveryAgent import RecoveryAgent
from ..agents.ResearchAgent import ResearchAgent
from ..agents.ResearchAnalyticsAgent import ResearchAnalyticsAgent
from ..agents.RoutingAgent import RoutingAgent
from ..agents.SchedulingAgent import SchedulingAgent
from ..agents.SearchAgent import SearchAgent
from ..agents.SecurityAgent import SecurityAgent
from ..agents.SecurityAuditAgent import SecurityAuditAgent
from ..agents.SelfHealingAgent import SelfHealingAgent
from ..agents.SelfImprovementAgent import SelfImprovementAgent
from ..agents.SelfProtectionAgent import SelfProtectionAgent
from ..agents.SimulationAgent import SimulationAgent
from ..agents.SummarizationAgent import SummarizationAgent
from ..agents.SupervisorAgent import SupervisorAgent
from ..agents.SyncAgent import SyncAgent
from ..agents.TelemetryAgent import TelemetryAgent
from ..agents.TestingAgent import TestingAgent
from ..agents.TranslationAgent import TranslationAgent
from ..agents.UIAgent import UIAgent
from ..agents.ValidationAgent import ValidationAgent
from ..agents.VerifierAgent import VerifierAgent
from ..agents.WorkerAgent import WorkerAgent

agentManager = {}

def register_agent(name: str, instance):
    agentManager[name] = instance
    eventBus.subscribe("db:update", getattr(instance, "handle_db_update", lambda x: None))
    eventBus.subscribe("db:delete", getattr(instance, "handle_db_delete", lambda x: None))

# Register all agents
for AgentClass in [
    ARVAgent, AnalyticsAgent, AntiTheftAgent, AutoUpdateAgent, BackupAgent, BillingAgent,
    CollaborationAgent, ComplianceAgent, ContentModerationAgent, ConversationAgent, CorrectionAgent,
    CreativityAgent, CriticAgent, DataIngestAgent, DataProcessingAgent, DecisionAgent, DeploymentAgent,
    DeviceProtectionAgent, DiscoveryAgent, DistributedTaskAgent, DoctrineAgent, EncryptionAgent,
    EvolutionAgent, FeedbackAgent, FounderAgent, GPIAgent, GlobalMedAgent, GoldEdgeIntegrationAgent,
    HealthMonitoringAgent, HotReloadAgent, IdentityAgent, InspectionAgent, LearningAgent,
    LoadBalancingAgent, LocalStorageAgent, MarketAssessmentAgent, MetricsAgent, MonitoringAgent,
    NotificationAgent, OfflineAgent, OrchestrationAgent, PersonalAgent, PhoneSecurityAgent,
    PlannerAgent, PlannerHelperAgent, PluginManagerAgent, PredictionAgent, PredictiveAgent,
    RecommendationAgent, RecoveryAgent, ResearchAgent, ResearchAnalyticsAgent, RoutingAgent,
    SchedulingAgent, SearchAgent, SecurityAgent, SecurityAuditAgent, SelfHealingAgent,
    SelfImprovementAgent, SelfProtectionAgent, SimulationAgent, SummarizationAgent,
    SupervisorAgent, SyncAgent, TelemetryAgent, TestingAgent, TranslationAgent, UIAgent,
    ValidationAgent, VerifierAgent, WorkerAgent
]:
    register_agent(AgentClass.__name__, AgentClass())
