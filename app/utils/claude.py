import anthropic
import dotenv
import json
dotenv.load_dotenv()


class RoadmapClaude:
    def __init__(self):
        self.client = anthropic.Anthropic()

    def get_message(self, project, skillslevels):
        skills = ""
        for skill,level in skillslevels:
            skills += f"{skill}-{level}\n"
        prompt = f"Project:\n\n{project}\n\nSkill Levels:\n{skills}"
        
        message = self.client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=3000,
        temperature=0.1,
        system="You are a very experienced and skilled project guide. You can guide students to learn technologies through hands on development along with learning to complete projects. You will be given a description about a project and scores of skill levels out of 5 for each related skill of the student. With the skill levels in consideration give a complete road map for the project. The road map must be implementation oriented learning. The road map must be project focused not skill focused\n\nStep 1: Identify the intermediate implementation goals of the project\n\nStep 2: Split each implementation goal to small milestones.\n\nStep 3: Identify tasks and what must be learned to implement each small milestones.\n\nStep 4: Give the final roadmap as a JSON such as\n{\n\"intermediate goals\": [{\n\n\"title\": goal title,\n\n\"milestones\":[{\n\n\"title\": milestone title,\n\n\"tasks\":[{\n\n\"task\": task name,\n\n\"description\": detailed description of task\n\n}]\n\n}]\n\n}]\n}",
        messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": "{\"intermediate goals\":"
                        }
                    ]
                }
            ]
        )

        if message.type == "message":
            with open('usage.txt','a') as f:
                f.write(str(message.usage.input_tokens) +" "+ str(message.usage.output_tokens)+"\n") 

            content = "{\"intermediate goals\":" + message.content[0].text
            try:
                return json.loads(content)
            except:
                with open('logs.txt','a') as f:
                    f.write("--------\n"+content +"\n")
        
        print(message)
        raise Exception("JSON ERROR")
    
    def __call__(self, project, skillslevels):
        content = self.get_message(project, skillslevels)
        return content