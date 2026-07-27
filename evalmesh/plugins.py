"""
EvalMesh Enterprise Plugin Marketplace Registry.
Enables 1-click third-party integrations (Salesforce, SAP, Jira, Slack, Notion, ServiceNow).
"""

from typing import Dict, Any, List

class PluginMarketplaceRegistry:
    """
    Manages third-party marketplace plugins and integrations.
    """

    def __init__(self):
        self.plugins = [
            {"id": "plug_salesforce", "name": "Salesforce CRM Connector", "category": "CRM", "status": "INSTALLED", "icon": "fa-brands fa-salesforce"},
            {"id": "plug_sap", "name": "SAP ERP Security Bridge", "category": "ERP", "status": "AVAILABLE", "icon": "fa-solid fa-building-columns"},
            {"id": "plug_jira", "name": "Jira Incident Ticketing", "category": "DevOps", "status": "INSTALLED", "icon": "fa-brands fa-jira"},
            {"id": "plug_slack", "name": "Slack Security Alert Bot", "category": "Communications", "status": "INSTALLED", "icon": "fa-brands fa-slack"},
            {"id": "plug_notion", "name": "Notion Knowledge Base RAG", "category": "Knowledge Base", "status": "AVAILABLE", "icon": "fa-solid fa-file-pen"},
            {"id": "plug_servicenow", "name": "ServiceNow ITSM Governance", "category": "ITSM", "status": "AVAILABLE", "icon": "fa-solid fa-headset"}
        ]

    def list_plugins(self) -> List[Dict[str, Any]]:
        return self.plugins

    def toggle_plugin_status(self, plugin_id: str, status: str) -> bool:
        for p in self.plugins:
            if p["id"] == plugin_id:
                p["status"] = status.upper()
                return True
        return False

plugin_marketplace = PluginMarketplaceRegistry()
