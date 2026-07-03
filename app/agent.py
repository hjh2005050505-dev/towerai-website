from __future__ import annotations

from dataclasses import dataclass
from .knowledge_base import search_knowledge

SCENE_HINTS = {
    "工业安全智能体": ["工业", "工厂", "制造", "车间", "施工", "工地", "安全", "巡检", "安全帽", "背心"],
    "运营复盘智能体": ["运营", "复盘", "事件", "汇报", "沉淀", "知识"],
    "岗位任务智能体": ["销售", "采购", "财务", "人事", "生产", "客服", "质量", "岗位", "任务"],
    "文档生成与信息处理智能体": ["文档", "资料", "报告", "生成", "整理", "信息"],
}

@dataclass
class AgentReply:
    reply: str
    intent: str
    recommended: list[str]

class TowerAgent:
    def reply(self, message: str) -> AgentReply:
        normalized = message.strip()
        if not normalized:
            return AgentReply("你好，我是塔外智能方案顾问。你可以告诉我所在行业、关注岗位或业务痛点，我会推荐适合的企业智能体方案。", "greeting", [])
        if any(word in normalized for word in ["预约", "联系", "电话", "微信", "演示", "沟通"]):
            return AgentReply("可以。建议先确认三个信息：公司行业、优先落地的岗位或场景、希望验证的业务指标。你可以在右侧留下联系方式，我会把需求整理成一份适合初步沟通的方案摘要。", "lead", ["预约演示", "需求收集"])
        matches = search_knowledge(normalized, limit=2)
        if not matches:
            scene = self._guess_scene(normalized)
            return AgentReply(f"我先把你的需求归入「{scene}」方向。塔外智能适合从真实岗位任务切入，把资料处理、流程推进、结果复核和经验沉淀做成稳定的数字工作单元。你可以继续补充行业、岗位和当前痛点，我会给出更具体的落地建议。", "clarify", [scene])
        primary = matches[0]
        features = "、".join(primary.get("features", [])[:5])
        flow = primary.get("flow") or ["需求梳理", "任务拆解", "能力配置", "执行试点", "复核沉淀"]
        flow_text = " -> ".join(flow)
        secondary = f"\n\n可联动方向：{matches[1]['title']}。" if len(matches) > 1 else ""
        reply = f"推荐方案：{primary['title']}。\n\n业务痛点：{primary['summary']}\n\n核心能力：{features}。\n\n落地路径：{flow_text}。\n\n预期价值：{primary.get('value', '让业务过程从人工经验变成可追踪、可复核、可复用的组织资产。')}{secondary}\n\n如果继续推进，下一步可以整理一版试点方案：明确试点岗位、数据来源、复核节点和验收指标。"
        return AgentReply(reply, "recommendation", [item["title"] for item in matches])

    def _guess_scene(self, message: str) -> str:
        for scene, keywords in SCENE_HINTS.items():
            if any(keyword in message for keyword in keywords):
                return scene
        return "企业岗位任务智能体"

tower_agent = TowerAgent()
