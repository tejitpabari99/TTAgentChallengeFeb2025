class PPT:
    def __init__(self, ppt_details, ppt_json):
        self.ppt_details = ppt_details
        self.ppt_json = ppt_json

    def ppt_details_prompt(self):
        return f"""
Presentation Name: {self.ppt_details.get('title', '')}
Presentation Description: {self.ppt_details.get('description', '')}
Presentation Intent: {self.ppt_details.get('intent', '')}
Presentation Audience: {self.ppt_details.get('audience', '')}
"""
    
    def slide_content_prompt(self):
        slides = []
        for i in range(1,len(self.ppt_json.keys())+1):
            slideNo = f"slide{i}"
            slide_content = f"""
                Slide {i}
                Slide Text: {self.ppt_json[slideNo].get('text', 'No Text')}
                Slide Notes: {self.ppt_json[slideNo].get('notes', 'No Notes')}
            """
            slides.append(slide_content.strip())
        return "Presentation content:\n\n"'\n\n--------\n'.join(slides)