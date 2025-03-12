from dataclasses import dataclass
from typing import Dict, Optional, Any, List
from uuid import uuid4
import os, json, logging

logger = logging.getLogger(__name__)

@dataclass
class PPT:
    title: str
    description: str
    intent: str
    id: Optional[str] = None
    file: Optional[str] = None
    content: Optional[List[Dict[str, Any]]] = None

    def __init__(self, title: str, description: str, intent: str, id: Optional[str] = None, file:Optional[str]=None, content: Optional[List[Dict[str, Any]]] = []):
        self.id = id or str(uuid4())
        self.title = title
        self.description = description
        self.intent = intent
        self.file = file
        self.content = content
        self._set_mapping()

    @classmethod
    def load(cls, dict: Dict[str, str]) -> 'PPT':
        logger.info(f"Loading PPT from dictionary...")
        return cls(
            id=dict.get('id', None),
            title=dict.get('title', ''),
            description=dict.get('description', ''),
            file=dict.get('file', ''),
            intent=dict.get('intent', ''),
            content=dict.get('content', [])
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'intent': self.intent,
            'file': self.file,
            'content': self.content
        }

    def extract_content_from_file(self, file=None):
        if not file: file = self.file
        if not file: raise ValueError("No file provided to extract content from.")
        # To be implemented later
        return []

    def ppt_and_slide_prompt(self):
        return self.ppt_prompt() + "\n------\n" + self.slide_prompt()

    def ppt_prompt(self):
        return f"""
Here are the details about the Powerpoint Presentation:
Presentation Title: {self.title}
Presentation Description: {self.description}
Presentation Intent: {self.intent}
----------
"""
        
    def slide_prompt(self):
        slides = []
        for i, content in enumerate(self.content):
            slide_content = f"""
                Slide {i+1}
                Slide Text: {content.get('text', 'No Text')}
                Slide Notes: {content.get('notes', 'No Notes')}
            """
            slides.append(slide_content.strip())
        return "Presentation content:\n---" + '\n---\n'.join(slides)

    def set_title(self, title: str): self.title = title
    def set_description(self, description: str): self.description = description
    def set_intent(self, intent: str): self.intent = intent
    def set_content(self, content: List[Dict[str, Any]]): self.content = content
    def has_content(self): return len(self.content) > 0
    def _set_mapping(self):
        self.mapping = {
            f'ppt_title': self.title,
            f'ppt_description': self.description,
            f'ppt_intent': self.intent,
            f'ppt_content': self.content,
            f'ppt_details': self.ppt_prompt()
        }

    def update_mapping(self) -> Dict[str, str]:
        self._set_mapping()
        return self.mapping

    def to_html(self) -> str:
        html = f"""
        <div class="ppt-details">
            <details>
                <summary>PPT Details</summary>
                <p><strong>ID:</strong> {self.id}</p>
                <p><strong>Title:</strong> {self.title}</p>
                <p><strong>Description:</strong> {self.description}</p>
                <p><strong>Intent:</strong> {self.intent}</p>
                <details>
                    <summary>PPT Content</summary>
                    <div class="ppt-content scrollable-content">
                        {''.join([f'''
                            <div class="slide">
                                <h4>Slide {i+1}</h4>
                                <p><strong>Text:</strong> {content.get('text', 'No Text')}</p>
                                <p><strong>Notes:</strong> {content.get('notes', 'No Notes')}</p>
                                {f'<hr style="width:30%; margin: 10px auto;">' if i < len(self.content or []) - 1 else ''}
                            </div>
                        ''' for i, content in enumerate(self.content or [])])}
                    </div>
                </details>
            </details>
        </div>
        """
        return html
